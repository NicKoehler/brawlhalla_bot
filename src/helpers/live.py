import httpx
import datetime

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
                "start": datetime.datetime.fromisoformat(event["start_dt"]),
                "end": datetime.datetime.fromisoformat(event["end_dt"]),
            }
            for event in r.json()["events"]
        ]

        if not data:
            return []

        # filter out already played lives
        return [event for event in data if is_event_valid(event)]
