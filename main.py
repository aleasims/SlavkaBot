import sys
from argparse import ArgumentParser

from slavkabot.bot import Bot
from slavkabot.config import ConfigurationError, build_config


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-c', '--conf', default='config.yml',
                        help='Path to configuration.yaml file')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    try:
        config = build_config(args.conf)
    except ConfigurationError as e:
        sys.stderr.write(f'Configuration error: {e}')
        sys.exit(1)

    bot = Bot(config)
    bot.start()
