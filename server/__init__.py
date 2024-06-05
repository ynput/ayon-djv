from typing import Type

from ayon_server.addons import BaseServerAddon, AddonLibrary

from .settings import DJVSettings, DEFAULT_VALUES


class DJVAddon(BaseServerAddon):
    settings_model: Type[DJVSettings] = DJVSettings

    async def get_default_settings(self):
        settings_model_cls = self.get_settings_model()
        return settings_model_cls(**DEFAULT_VALUES)
