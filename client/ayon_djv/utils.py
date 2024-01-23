import os
import time
import platform

import ayon_api

from .version import __version__
from .constants import ADDON_NAME


def get_djv_paths_from_settings(addon_settings=None):
    """

    Args:
        addon_settings (Optional[dict[str, Any]): Addon settings.

    Returns:
        list[str]: List to DJV executable paths. Paths are not validated.
    """

    if addon_settings is None:
        addon_settings = ayon_api.get_addon_settings(ADDON_NAME, __version__)

    platform_name = platform.system().lower()
    return addon_settings.get("djv_path", {}).get(platform_name, [])


def get_djv_executable_path(paths=None, addon_settings=None):
    """

    Args:
        paths (Optional[list[str]]): List of paths to DJV executable.
        addon_settings (Optional[dict[str, Any]): Addon settings.

    Returns:
        list[str]: List of available paths to DJV executable.
    """

    if paths is None:
        paths = get_djv_paths_from_settings(addon_settings)

    for path in paths:
        if path and os.path.exists(path):
            return path
    return None


class DJVExecutableCache:
    lifetime = 10

    def __init__(self):
        self._cached_time = None
        self._djv_paths = None
        self._djv_path = None

    def is_cache_valid(self):
        """Cache is valid.

        Returns:
            bool: True if cache is valid, False otherwise.
        """

        if self._cached_time is None:
            return False

        start = time.time()
        return (start - self._cached_time) <= self.lifetime

    def get_paths(self):
        """Get all paths to DJV executable from settings.

        Returns:
            list[str]: Path to DJV executables.
        """

        if not self.is_cache_valid():
            self._djv_paths = get_djv_paths_from_settings()
            self._cached_time = time.time()
        return self._djv_paths

    def get_path(self):
        """Get path to DJV executable.

        Returns:
            Union[str, None]: Path to DJV executable or None.
        """

        if not self.is_cache_valid():
            self._djv_path = get_djv_executable_path(self.get_paths())
        return self._djv_path
