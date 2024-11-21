from enum import IntEnum
from typing import Callable, Dict


class EncryptType(IntEnum):
    NO_ENCRYPT = 0
    RC4 = 1

    def to_bytes(self):  # noqa
        return super().to_bytes(2, "big", signed=False)

    @classmethod
    def from_bytes(cls, _bytes, byteorder = "big", *, signed = False):
        if len(_bytes) != 2 or byteorder !="big" or signed != False:
            raise ValueError
        return super().from_bytes(_bytes, "big", signed=signed)


def no_encrypt_func(key: str, x: bytes) -> bytes:
    return x

def no_decrypt_func(key: str, x: bytes) -> bytes:
    return x


def rc4_encrypt_func(key: str, x: bytes) -> bytes:
    from Crypto.Cipher import ARC4
    cipher = ARC4.new(key.encode('utf8'))
    return cipher.encrypt(x)

def rc4_decrypt_func(key: str, x: bytes) -> bytes:
    from Crypto.Cipher import ARC4
    cipher = ARC4.new(key.encode('utf8'))
    return cipher.decrypt(x)


encrypt_func_map: Dict[EncryptType, Callable[[str, bytes], bytes]] = {
    EncryptType.NO_ENCRYPT: no_encrypt_func,
    EncryptType.RC4: rc4_encrypt_func,
}

decrypt_func_map: Dict[EncryptType, Callable[[str, bytes], bytes]] = {
    EncryptType.NO_ENCRYPT: no_decrypt_func,
    EncryptType.RC4: rc4_decrypt_func,
}
