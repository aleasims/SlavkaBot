"""
SlavkaBot

    Dev instalation (with updates):
pip install -e .
    Prod installation:
pip install .
"""

import logging
import os

from google_drive_downloader import GoogleDriveDownloader as gdd
from setuptools import setup

logger = logging.getLogger(__name__)

requierments = [
    'Telethon',
    'gunicorn',
    'flask',
    'youtokentome',
    'regex',
    'transformers',
    'torch @ https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp36-cp36m-linux_x86_64.whl',
    'googledrivedownloader',
]

ID_GOOGLE_FILE = "1FR72Ib40V0nXxfH__x91NWGsy13hzcs5"
ZIP_NAME = "model_checkpoint.zip"

logger.info("Downloading model...")
gdd.download_file_from_google_drive(file_id=ID_GOOGLE_FILE,
                                    dest_path=f'./{ZIP_NAME}')
logger.info("Download completed!")
files = os.listdir()
logger.info(f"Dir: {files}")


entry_points = {
    'console_scripts': [
        'run_bot=slavkabot:main'
    ]
}

setup(
    name='slavkabot',
    version='0.1.0',
    description='Your best friend Slavka',
    url='https://github.com/aleasims/SlavkaBot',
    packages=['slavkabot', 'web'],
    package_dir={'slavkabot': 'slavkabot', 'web': 'web'},
    python_requires='>=3.5',
    dependency_links=[
        "https://download.pytorch.org/whl/cpu/",
        "https://download.pytorch.org/whl/torch_stable/cpu/",
        "https://download.pytorch.org/whl/torch_stable.html",
        "https://download.pytorch.org/whl/torch_stable/",
    ],
    install_requires=requierments,
    entry_points=entry_points
)
