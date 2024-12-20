# head-encrypt

## 简介

[pypi](https://pypi.org/project/headecpt/)

`head-encrypt` 是一款创新的文件加密工具，专门设计用于快速且高效地保护文件的首部信息。
在许多情况下，完全加密大型文件既不实际又耗时，尤其是当您只想防止未经授权的访问者识别文件类型或内容时。
`head-encrypt`提供了一种解决方案，通过仅加密文件的头部部分，既减少了加密过程所需的时间，又显著降低了磁盘空间的占用。

### 使用场景
- 当您需要分享文件但又不想暴露文件类型时.
- 当您想要保护文件内容不被轻易识别时。
- 当您需要一种快速而有效的方式来“损害”文件，使其难以被未经授权的用户使用时。

### 特点
- **快速加密**：只加密文件头部，大幅减少加密所需时间。
- **轻量化**：由于仅加密文件的一部分，对系统资源的需求极小。
- **不安全性：该加密仅加密文件头部，不要把它当成一个非常安全的加密手段**

## 安装指南

- 通过pip进行安装

```bash
pip install headecpt
```


- 或采用离线方式，进行源码安装
```bash
git clone https://github.com/lichunown/head-encrypt.git
cd head-encrypt
python setup.py install
```

## 使用方法

在命令行中
```bash
> headecpt --help

Usage: headecpt [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  de   Decrypt the files
  en   Encrypt the files
  tde  Traverse dirs and Decrypt the matching files
  ten  Traverse dirs and encrypt the matching files
```

- 加密指定文件

```bash
> headecpt en --help

Usage: headecpt en [OPTIONS] [PATH]...

  Encrypt the files

Options:
  -t, --type [rc4|no]      加密方式：no为无密钥加密，rc4为有密钥加密
  -h, --head_size INTEGER  待加密文件头大小
  -p, --password TEXT      加密密钥，若不指定则默认no加密方法，指定则默认为rc4方法
  --remain_name            是否对文件名进行加密，默认加密，若不加密则指定--without-name
  --help                   Show this message and exit.

```

例如：
```bash
headecpt en [filename]  # 单个文件
headecpt en [filename] -p "password"  # 有密码的加密
headecpt en *.mp4       # 基于通配符的多个文件
```


- 解密指定文件

```bash
> headecpt de --help

Usage: headecpt de [OPTIONS] [PATH]...

  Decrypt the files

Options:
  -p, --password TEXT  解密密钥
  --help               Show this message and exit.
```

例如：
```bash
headecpt de [filename]  # 单个文件解密
headecpt de [filename] -p "password"  # 有密码的解密
headecpt de *.mp4       # 基于通配符的多个文件
```
