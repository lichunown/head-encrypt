import os
import subprocess

from setuptools import setup, find_packages


try:
    with open(os.path.join(os.path.split(__file__)[0], "readme.md"), "r", encoding='utf8') as fh:
        long_description = fh.read()
except Exception:
    long_description = subprocess.run(["curl", 'https://raw.githubusercontent.com/lichunown/head-encrypt/master/readme.md'],
                                      capture_output=True, text=True, encoding='utf8').stdout


setup(
    name='headecpt',
    version="1.0.0",
    author="lcy",
    author_email="lichunyang_1@outlook.com",
    description="encrypt/decrypt file header for simple and quick encrypt/decrypt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lichunown/head-encrypt.git",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ],

    packages=find_packages(),
    data_files=[],
    install_requires=[
        'click',
    ],
    extras_require={
        'crypto': ['pycryptodome'],
    },

    entry_points={'console_scripts': [
       'headecpt = headecpt.main:main',
    ]},

    zip_safe=False
)