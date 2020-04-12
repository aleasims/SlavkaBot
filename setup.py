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
    'torch==1.4.0+cpu',
    'youtokentome',
    'regex',
    'transformers'
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
    install_requires=requierments,
    entry_points=entry_points
)
