import xlrd
from .api import API


class Excel(API):
    """Parser to parse Excel data format.
    """

    # Public

    def __init__(self, sheet_index=0):
        self.__sheet_index = sheet_index
        self.__bytes = None
        self.__items = None

    def open(self, loader):
        self.close()
        self.__loader = loader
        self.__bytes, self.__encoding = loader.load(mode='b')
        self.reset()

    def close(self):
        if not self.closed:
            self.__bytes.close()

    @property
    def closed(self):
        return self.__bytes is None or self.__bytes.closed

    @property
    def items(self):
        return self.__items

    def reset(self):
        self.__bytes.seek(0)
        self.__workbook = xlrd.open_workbook(
                file_contents=self.__bytes.read(),
                encoding_override=self.__encoding)
        self.__sheet = self.__workbook.sheet_by_index(self.__sheet_index)
        self.__items = (
            (None, tuple(self.__sheet.row_values(rownum)))
            for rownum in range(self.__sheet.nrows))
