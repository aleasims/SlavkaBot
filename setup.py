"""
SlavkaBot

    Dev instalation (with updates):
pip install -e .
    Prod installation:
pip install .
"""

from setuptools import setup


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
