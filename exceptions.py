class RedditException(Exception):
    pass


class DownloadException(Exception):
    pass


class NotADownloadableLinkError(DownloadException):
    pass


class BaseDownloaderException(DownloadException):
    pass


class ResourceNotFound(DownloadException):
    pass


class SiteDownloaderError(DownloadException):
    pass
