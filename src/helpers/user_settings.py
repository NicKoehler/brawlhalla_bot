class UserSettings:
    def __init__(self):
        self._users_settings = {}

    def get_user(self, user_id: int, attribute: str, default=None):
        if user_id not in self._users_settings:
            self._users_settings[user_id] = {attribute: default}
        if attribute not in self._users_settings[user_id]:
            self._users_settings[user_id][attribute] = default
        return self._users_settings[user_id][attribute]

    def set_user(self, user_id: int, attribute: str, value):
        if user_id not in self._users_settings:
            self._users_settings[user_id] = {attribute: value}
        if attribute not in self._users_settings[user_id]:
            self._users_settings[user_id][attribute] = value
        self._users_settings[user_id][attribute] = value

    def del_user(self, user_id: int, attribute: str):
        if user_id not in self._users_settings:
            return
        if attribute not in self._users_settings[user_id]:
            return
        del self._users_settings[user_id][attribute]
