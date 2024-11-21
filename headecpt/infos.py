from enum import IntEnum
from typing import Union, Optional
import hashlib

from headecpt.encrypt_funcs import EncryptType


MD5_MAX_SIZE = 8


def md5(data: bytes) -> bytes:
    return hashlib.md5(data).digest()[:MD5_MAX_SIZE]


class VersionType(IntEnum):
    V1 = 0

    def to_bytes(self):  # noqa
        return super().to_bytes(2, "big", signed=False)

    @classmethod
    def from_bytes(cls, _bytes, byteorder = "big", *, signed = False):
        if len(_bytes) != 2 or byteorder !="big" or signed != False:
            raise ValueError
        return super().from_bytes(_bytes, "big", signed=signed)


class SizeInfo(int):

    def to_bytes(self):  # noqa
        return super().to_bytes(4, "big", signed=False)

    @classmethod
    def from_bytes(cls, _bytes, byteorder = "big", *, signed = False):
        if len(_bytes) != 4 or byteorder !="big" or signed != False:
            raise ValueError
        return super().from_bytes(_bytes, "big", signed=signed)


class HeadInfo(object):

    __magic__code__ = b'\x54\x63\x0e\x1a'
    HEAD_INFO_SIZE = 28

    @classmethod
    def from_bytes(cls, data: bytes):
        magic_code = data[:4]
        if magic_code != cls.__magic__code__:
            raise ValueError('this file is not a encrypt file.')

        version = VersionType.from_bytes(data[4:6])
        encrypt_type = EncryptType.from_bytes(data[6:8])
        key_size = SizeInfo.from_bytes(data[8:12])
        head_size = SizeInfo.from_bytes(data[12:16])
        encrypt_size = SizeInfo.from_bytes(data[16:20])
        encrypt_md5 = data[20:20 + MD5_MAX_SIZE]
        return cls(version, encrypt_type, key_size, head_size, encrypt_size, encrypt_md5)

    def __init__(self, version: VersionType, encrypt_type: EncryptType,
                 key_size: Union[SizeInfo, int],
                 head_size: Union[SizeInfo, int], encrypt_size: SizeInfo = None,
                 encrypt_md5: Optional[bytes] = None):
        self.version: VersionType = version
        self.encrypt_type: EncryptType = encrypt_type

        self.key_size: SizeInfo = SizeInfo(key_size)
        self.head_size: SizeInfo = SizeInfo(head_size)

        self.encrypt_size: Optional[encrypt_size] = encrypt_size
        self.encrypt_md5: Optional[bytes] = encrypt_md5

        if head_size < len(self):
            raise ValueError(f'head_size must > {len(self)}.')

    def to_bytes_without_encrypt_size(self):
        return (self.__magic__code__ + self.version.to_bytes() + self.encrypt_type.to_bytes() +
                self.key_size.to_bytes() + self.head_size.to_bytes())

    def to_bytes_with_data(self, head: bytes, encrypt_data: bytes):
        encrypt_size = SizeInfo(len(encrypt_data))
        encrypt_md5 = md5(head)
        return self.to_bytes_without_encrypt_size() + encrypt_size.to_bytes() + encrypt_md5

    def __len__(self):
        return len(self.to_bytes_without_encrypt_size()) + 4 + MD5_MAX_SIZE

    @property
    def encrypt_func(self):
        from headecpt.encrypt_funcs import encrypt_func_map
        return encrypt_func_map[self.encrypt_type]

    @property
    def decrypt_func(self):
        from headecpt.encrypt_funcs import decrypt_func_map
        return decrypt_func_map[self.encrypt_type]


