import logging
import yaml


MODES = ['dev', 'prod']
TELE_REQUIRED = ['token', 'api_id', 'api_hash']
PROXIES = ['MTProto', 'SOCKS5']
PROXY_REQUIRED = {
    'SOCKS5': ['host', 'port'],
    'MTProto': ['host', 'port', 'secret']
}


class ConfigurationError(Exception):
    pass


def build_config(config_path):
    try:
        f = open(config_path, 'r')
        config = yaml.load(f, Loader=yaml.CLoader)
        # TODO: Change this dict to case insensetive recursivly
    except OSError as e:
        raise ConfigurationError(f"Cannot read config file: {e}")

    if config.get('mode') not in MODES:
        raise ConfigurationError(f"Unsopported mode: {config.get('mode')}. Expected: {MODES}")

    missing = [key for key in TELE_REQUIRED if key not in config['telegram']]
    if missing:
        raise ConfigurationError(f"Missing one of required telegram params: {missing}")

    if config['mode'] == 'dev':
        config_logger(logging.DEBUG)
    else:
        config_logger(logging.INFO)

    if config.get('proxy') and config.get('use_proxy', True):
        if not config['proxy'].get('type'):
            config['proxy']['type'] = 'SOCKS5'
        if config['proxy']['type'] not in PROXIES:
            raise ConfigurationError(f"Unsupported proxy type: {config['proxy'].get('type')}. Expected: {PROXIES}")

        missing = [key for key in PROXY_REQUIRED[config['proxy']['type']]
                   if key not in config['proxy']]
        if missing:
            raise ConfigurationError(f"Missing one of required proxy params: {missing}")
        config['use_proxy'] = True

    return config


def config_logger(level):
    LOG_FORMAT = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=level, format=LOG_FORMAT)
    logger = logging.getLogger(__name__)
    levelname = logging._levelToName[logger.getEffectiveLevel()]
    logger.info(f'Logger configured for {levelname}')
