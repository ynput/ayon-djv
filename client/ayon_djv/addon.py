import os
from ayon_core.addon import AYONAddon, IPluginPaths

from .version import __version__
from .constants import ADDON_NAME, DJV_ROOT


class DJVAddon(AYONAddon, IPluginPaths):
    """Addon adds djv functionality via plugins."""

    name = ADDON_NAME
    version = __version__

    def get_plugin_paths(self):
        return {
            "load": self.get_load_plugin_paths()
        }

    def get_load_plugin_paths(self, host_name=None):
        return [
            os.path.join(DJV_ROOT, "plugins", "load"),
        ]

    def get_ftrack_event_handler_paths(self):
        return {
            "user": [
                os.path.join(DJV_ROOT, "plugins", "ftrack"),
            ]
        }
