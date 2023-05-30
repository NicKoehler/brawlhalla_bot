import httpx
import datetime

from asyncio import sleep
from prisma import Prisma
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import UserBlocked
from scheduler.asyncio import Scheduler

from keyboards import Keyboard
from localization import Localization, Translator
from helpers.utils import get_translated_times_from_seconds

DATE_FORMAT = "%Y-%m-%d"


def is_event_valid(event: dict):
    date_now = datetime.datetime.now(event["start"].tzinfo)
    event["starts_in"] = (event["start"] - date_now).total_seconds()
    event["duration"] = (event["end"] - event["start"]).total_seconds()
    return event["start"] > date_now


async def get_lives():
    date_now = datetime.datetime.now() - datetime.timedelta(days=1)
    date_one_month = date_now + datetime.timedelta(days=30)

    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://teamup.com/ks53joip3zzxcsza3d/events",
            params={
                "startDate": date_now.strftime(DATE_FORMAT),
                "endDate": date_one_month.strftime(DATE_FORMAT),
            },
        )
        data = [
            {
                "title": event["title"],
                "date_tag": event["start_dt"] + " - " + str(event["update_dt"]),
                "start": datetime.datetime.fromisoformat(event["start_dt"]),
                "end": datetime.datetime.fromisoformat(event["end_dt"]),
            }
            for event in r.json()["events"]
        ]

        if not data:
            return []

        # filter out already played lives
        events = [event for event in data if is_event_valid(event)]

        return events


async def schedule_lives(
    bot: Client, db: Prisma, schedule: Scheduler, localization: Localization
):
    lives = await get_lives()
    jobs = schedule.get_jobs({"live"})
    job_aliases = {job.alias for job in jobs}
    event_aliases = set()

    for event in lives:
        date_string = event["date_tag"]
        event_aliases.add(date_string)

        if date_string in job_aliases:
            continue

        time_schedule = event["starts_in"] - (10 * 60)

        if time_schedule < 0:
            continue

        schedule.once(
            datetime.timedelta(seconds=time_schedule),
            notify_lives,
            args=(
                bot,
                db,
                event["title"],
                localization,
            ),
            tags={"live"},
            alias=date_string,
        )

    # clean up deleted jobs if they were previously scheduled and then removed
    for job in jobs:
        if job.alias not in event_aliases:
            schedule.delete_job(job)


async def send_event(
    message: Message,
    event: dict,
    translate: Translator,
    bot: Client,
):
    translated_start_times = get_translated_times_from_seconds(
        event["starts_in"],
        translate,
    )
    translate_duration_times = get_translated_times_from_seconds(
        event["duration"],
        translate,
    )
    start_string = ", ".join(translated_start_times)
    duration_string = ", ".join(translate_duration_times) or "🤷‍♂️"
    await message.reply(
        translate.results_live(
            title=event["title"],
            start=start_string,
            end=duration_string,
        ),
        reply_markup=await Keyboard.live(bot, translate),
    )


async def notify_lives(
    bot: Client, db: Prisma, event_title: str, localization: Localization
):
    users = await db.user.find_many(where={"notify_live": True})
    for user in users:
        try:
            translator = localization.get_translator(user.language)
            await bot.send_message(
                user.id,
                translator.result_live_notification(event_title),
                reply_markup=await Keyboard.live(bot, translator),
            )
        except UserBlocked:
            await db.user.update(where={"id": user.id}, data={"notify_live": False})
        finally:
            await sleep(0.5)
