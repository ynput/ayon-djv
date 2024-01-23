# DJV addon for AYON
This addon adds action plugins to other AYON addons to launch DJV. The addon does not contain DJV executables, only allows you to set them up in the addon settings.

## Create package
To create addon package run `create_package.py` script in the root of repository.

```shell
python create_package.py
```

That will create `./package/djv-<version>.zip` file which can be uploaded to AYON server.
