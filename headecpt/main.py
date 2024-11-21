import sys
import glob
from pygments.lexer import default

sys.path.append('../')
sys.path.append('../../')
import logging
import click

from headecpt.crypts import encrypt, decrypt
from headecpt.infos import EncryptType


encrypt_str_map = {
    None: EncryptType.NO_ENCRYPT,
    '': EncryptType.NO_ENCRYPT,
    'no': EncryptType.NO_ENCRYPT,
    'RC4': EncryptType.RC4,
    'rc4': EncryptType.RC4,
}


@click.group()
def main():
    pass


@main.command(help="Encrypt the files")
@click.argument('path', type=click.Path(exists=True), nargs=-1)
@click.option('-t', '--type', default=None, type=click.Choice(['rc4', 'no']),
              help="加密方式：no为无密钥加密，rc4为有密钥加密")
@click.option('-h', '--head_size', default=1024, type=int, help="待加密文件头大小")
@click.option('-p', '--password', hide_input=True, confirmation_prompt=True, default='',
              help="加密密钥，若不指定则默认no加密方法，指定则默认为rc4方法")
@click.option('-o', '--output-suffix',  default=None,
              help="输出文件后缀")
def en(path, head_size, type = None, password = '', output_suffix=None):
    encrypt_type = encrypt_str_map[type]
    for p in path:
        try:
            encrypt(p, head_size, encrypt_type, password)
        except Exception as e:
            logging.error(f'{e}')


@main.command(help="Decrypt the files")
@click.argument('path', type=click.Path(exists=True), nargs=-1)
@click.option('-p', '--password', hide_input=True, confirmation_prompt=True, default='',
              help="解密密钥")
def de(path, password = ''):
    for p in path:
        try:
            decrypt(p, password)
        except Exception as e:
            logging.error(f'{e}')


if __name__ == '__main__':
    main()
