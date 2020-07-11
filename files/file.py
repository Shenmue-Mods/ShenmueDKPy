from abc import ABC, abstractmethod
import typing
import io
from os import path

class File(ABC):
    """
        The File object is the base of all files

        Attributes:
            base_offset (int): The base offset at which the read function was called.
            file_path (str): The path of the file
    """
    def __init__(self):
        super().__init__()
        self.base_offset = 0
        self.file_path = ''

    def read(self, file_path: str) -> bool:

        if not path.exists(file_path):
            print('Given path does not exists: ', file_path)
            return False

        if not path.isfile(file_path):
            print('Given path is not a file: ', file_path)
            return False

        self.file_path = file_path
        with open(self.file_path, 'rb') as binary_file:
            if not self.read_stream(binary_file):
                print('Reading of file failed. ', self.file_path)
                return False

        return True

    def read_stream(self, binary_stream: typing.BinaryIO) -> bool:
        self.base_offset = binary_stream.tell()
        if not self._read(binary_stream):
            print('Reading from file stream failed at position ', self.base_offset)
            return False
        return True

    def write(self, file_path: str) -> bool:

        if not path.exists(file_path):
            print('Given path does not exists: ', file_path)
            return False

        if not path.isfile(file_path):
            print('Given path is not a file: ', file_path)
            return False

        self.file_path = file_path
        with open(self.file_path, 'rb') as binary_file:
            if not self.write_stream(binary_file):
                print('Reading of file failed. ', self.file_path)
                return False

        return True

    def write_stream(self, binary_stream: typing.BinaryIO) -> bool:
        self.base_offset = binary_stream.tell()
        self._write(binary_stream)
        if not self._write(binary_stream):
            print('Writing to file stream failed at position ', self.base_offset)
            return False
        return True

    def clean(self) -> bool:
        if not self._clean():
            print('Cleaning file stream resources failed')
            return False
        return True

    @abstractmethod
    def _read(self, binary_stream: typing.BinaryIO) -> bool:
        return False

    @abstractmethod
    def _write(self, binary_stream: typing.BinaryIO) -> bool:
        return False

    @abstractmethod
    def _clean(self) -> bool:
        return False