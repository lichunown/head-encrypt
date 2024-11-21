import os
from enum import IntEnum
from typing import Callable

from headecpt.encrypt_funcs import EncryptType
from headecpt.infos import HeadInfo, VersionType, md5


def encrypt(filename: str, head_size=1024*1024, encrypt_type: EncryptType = None, key=''):
    if encrypt_type is None:
        if key is None or len(key) <= 0:
            encrypt_type = EncryptType.NO_ENCRYPT
        else:
            encrypt_type = EncryptType.RC4

    file_size = os.path.getsize(filename)
    head_size = min(head_size, file_size)
    head_info = HeadInfo(VersionType.V1, encrypt_type, len(key), head_size, None)
    with open(filename, 'r+b') as f:
        f.seek(0)
        head = f.read(head_size)
        encrypt_data = head_info.encrypt_func(key, head)
        f.seek(0)
        f.write(head_info.to_bytes_with_data(head, encrypt_data))
        f.write(b'\x00' * (head_size - len(head_info)))

        f.seek(0, 2)
        f.write(head_info.encrypt_func(key, head))


def decrypt(filename: str, key: str = ''):
    with open(filename, 'r+b') as f:
        f.seek(0)
        head_info = HeadInfo.from_bytes(f.read(HeadInfo.HEAD_INFO_SIZE))
        if len(key) != head_info.key_size:
            raise ValueError('(1) password is not correct.')

        f.seek(-1 * head_info.encrypt_size, 2)
        encrypt_data = f.read(head_info.encrypt_size)
        decrypt_data = head_info.decrypt_func(key, encrypt_data)
        assert len(decrypt_data) == head_info.head_size
        assert md5(decrypt_data) == head_info.encrypt_md5, (f'(2) password is not correct. \n'
                                                            f'    md5(decrypt_data): {md5(decrypt_data)}\n'
                                                            f'head_info.encrypt_md5: {head_info.encrypt_md5}')

        f.seek(-1 * head_info.encrypt_size, 2)
        f.truncate()
        f.seek(0)
        f.write(decrypt_data)
