import os

from operator import itemgetter

from ayon_ftrack.common import LocalAction

from ayon_djv.utils import DJVExecutableCache, get_djv_icon_url

from ayon_core.lib import run_detached_process
from ayon_core.lib.transcoding import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS


class DJVViewAction(LocalAction):
    """Launch DJVView action."""
    identifier = "djvview-launch-action"
    label = "DJV View"
    description = "DJV View Launcher"
    icon = get_djv_icon_url()

    type = "Application"

    allowed_types = {
        ext.lstrip(".")
        for ext in set(IMAGE_EXTENSIONS) | set(VIDEO_EXTENSIONS)
    }
    _executable_cache = DJVExecutableCache()

    def discover(self, session, entities, event):
        """Return available actions based on *event*. """
        selection = event["data"].get("selection", [])
        if len(selection) != 1:
            return False

        entityType = selection[0].get("entityType", None)
        if entityType not in ["assetversion", "task"]:
            return False

        return self._executable_cache.get_path() is not None

    def interface(self, session, entities, event):
        if event["data"].get("values", {}):
            return

        entity = entities[0]
        versions = []

        entity_type = entity.entity_type.lower()
        if entity_type == "assetversion":
            if (
                entity[
                    "components"
                ][0]["file_type"][1:] in self.allowed_types
            ):
                versions.append(entity)
        else:
            master_entity = entity
            if entity_type == "task":
                master_entity = entity["parent"]

            for asset in master_entity["assets"]:
                for version in asset["versions"]:
                    # Get only AssetVersion of selected task
                    if (
                        entity_type == "task" and
                        version["task"]["id"] != entity["id"]
                    ):
                        continue
                    # Get only components with allowed type
                    filetype = version["components"][0]["file_type"]
                    if filetype[1:] in self.allowed_types:
                        versions.append(version)

        if len(versions) < 1:
            return {
                "success": False,
                "message": "There are no Asset Versions to open."
            }

        path = self._executable_cache.get_path()
        if not path:
            return {
                "success": False,
                "message": "Couldn't find DJV executable."
            }

        version_items = []
        base_label = "v{0} - {1} - {2}"
        default_component = None
        last_available = None
        select_value = None
        for version in versions:
            for component in version["components"]:
                label = base_label.format(
                    str(version["version"]).zfill(3),
                    version["asset"]["type"]["name"],
                    component["name"]
                )

                try:
                    location = component[
                        "component_locations"
                    ][0]["location"]
                    file_path = location.get_filesystem_path(component)
                except Exception:
                    file_path = component[
                        "component_locations"
                    ][0]["resource_identifier"]

                if os.path.isdir(os.path.dirname(file_path)):
                    last_available = file_path
                    if component["name"] == default_component:
                        select_value = file_path
                    version_items.append(
                        {"label": label, "value": file_path}
                    )

        if len(version_items) == 0:
            return {
                "success": False,
                "message": (
                    "There are no Asset Versions with accessible path."
                )
            }

        item = {
            "label": "Items to view",
            "type": "enumerator",
            "name": "path",
            "data": sorted(
                version_items,
                key=itemgetter("label"),
                reverse=True
            )
        }
        if select_value is not None:
            item["value"] = select_value
        else:
            item["value"] = last_available

        return {"items": [item]}

    def launch(self, session, entities, event):
        """Callback method for DJVView action."""

        # Launching application
        event_values = event["data"].get("value")
        if not event_values:
            return

        executable = self._executable_cache.get_path()
        if not executable:
            return {
                "success": False,
                "message": "Couldn't find DJV executable."
            }

        filpath = os.path.normpath(event_values["path"])

        cmd = [
            # DJV path
            str(executable),
            # PATH TO COMPONENT
            filpath
        ]

        try:
            # Run DJV with these commands
            run_detached_process(cmd)

        except FileNotFoundError:
            return {
                "success": False,
                "message": "File \"{}\" was not found.".format(
                    os.path.basename(filpath)
                )
            }

        return True


def register(session):
    """Register hooks."""

    DJVViewAction(session).register()
