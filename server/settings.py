from ayon_server.settings import (
    BaseSettingsModel,
    SettingsField,
    MultiplatformPathListModel,
)


class DJVSettings(BaseSettingsModel):
    """DJV addon settings."""

    enabled: bool = SettingsField(True)
    djv_path: MultiplatformPathListModel = SettingsField(
        title="DJV paths",
        default_factory=MultiplatformPathListModel,
        scope=["studio"],
    )


DEFAULT_VALUES = {
    "enabled": True,
    "djv_path": {
        "windows": [
            "C:\\Program Files\\DJV2\\bin\\djv.exe",
        ],
        "linux": [],
        "darwin": [
            "/Applications/DJV2.app/Contents/MacOS/DJV2",
        ]
    }
}
