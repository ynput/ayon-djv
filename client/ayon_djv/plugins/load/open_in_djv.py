import os
import time
import subprocess

import clique

from openpype.lib.transcoding import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS
from openpype.pipeline import load

from ayon_djv.utils import DJVExecutableCache


class OpenInDJV(load.LoaderPlugin):
    """Open Image Sequence with system default"""

    _executable_cache = DJVExecutableCache()
    families = ["*"]
    representations = ["*"]
    extensions = {
        ext.lstrip(".")
        for ext in set(IMAGE_EXTENSIONS) | set(VIDEO_EXTENSIONS)
    }

    label = "Open in DJV"
    order = -10
    icon = "play-circle"
    color = "orange"

    @classmethod
    def get_djv_path(cls):
        return cls._executable_cache.get_path()

    @classmethod
    def is_compatible_loader(cls, context):
        if not cls.get_djv_path():
            return False
        return super().is_compatible_loader(context)

    def load(self, context, name, namespace, data):

        path = self.filepath_from_context(context)
        directory = os.path.dirname(path)

        pattern = clique.PATTERNS["frames"]
        files = os.listdir(directory)
        collections, remainder = clique.assemble(
            files,
            patterns=[pattern],
            minimum_items=1
        )

        if not remainder:
            sequence = collections[0]
            first_image = list(sequence)[0]
        else:
            first_image = path
        filepath = os.path.normpath(os.path.join(directory, first_image))

        self.log.info("Opening : {}".format(filepath))

        executable = self.get_djv_path()
        cmd = [
            # DJV path
            str(executable),
            # PATH TO COMPONENT
            filepath
        ]

        try:
            # Run DJV with these commands
            _process = subprocess.Popen(cmd)
            # Keep process in memory for some time
            time.sleep(0.1)

        except FileNotFoundError:
            self.log.error(
                f"File \"{os.path.basename(filepath)}\" was not found."
            )
