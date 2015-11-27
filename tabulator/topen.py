import os
from six.moves.urllib.parse import urlparse
from .table import Table
from . import loaders, parsers


LOADERS = {
    'file': loaders.File,
    'text': loaders.Text,
    'ftp': loaders.Web,
    'ftps': loaders.Web,
    'http': loaders.Web,
    'https': loaders.Web,
}

PARSERS = {
    'csv': parsers.CSV,
    'xls': parsers.Excel,
    'xlsx': parsers.Excel,
    'json': parsers.JSON,
}


def topen(source, encoding=None, format=None):
    """Open table from source with encoding and format.

    Args:

        source (str): table source
            - file (default)
            - text
            - http
            - https
            - ftp
            - ftps

        encoding (str): encoding of source
            - None (infer)
            - utf-8
            - <any>

        format (str): format of source
            - None (infer)
            - csv
            - json
            - xls
            - xlsx

    """
    # TODO: refactor code
    # TODO: implement error handling
    scheme = urlparse(source).scheme or 'file'
    format = format or os.path.splitext(source)[1].replace('.', '')
    loader = LOADERS[scheme](source, encoding)
    parser = PARSERS[format]()
    table = Table(loader=loader, parser=parser)
    table.open()
    return table
