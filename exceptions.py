class NotADownloadableLinkError(Exception):
    pass


class BaseDownloaderException(Exception):
    pass


class ResourceNotFound(Exception):
    pass


class SiteDownloaderError(Exception):
    pass
