from resources.lib.di.requiredfeature import RequiredFeature


class Update:
    def __init__(self, current_version=None, update_version=None, asset_url=None, asset_name=None, changelog=None,
                 file_path=None):
        self.current_version = current_version,
        self.update_version = update_version,
        self.asset_url = asset_url,
        self.asset_name = asset_name,
        self.changelog = changelog
        self.file_path = file_path

    def do_update(self):
        updater = RequiredFeature('update-service').request()
        updater.do_update(self)
