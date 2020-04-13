import os
import logging
from google_drive_downloader import GoogleDriveDownloader as gdd


def config_logger(level=logging.INFO):
    LOG_FORMAT = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=level, format=LOG_FORMAT)


class ConfigurationError(Exception):
    pass


def load_config_var(key, default=None):
    return os.getenv(key, default)


def build_config():
    modes = ['dev', 'prod']

    config = {
        key: load_config_var(key)
        for key in ('MODE', 'TOKEN', 'API_ID', 'API_HASH')
    }

    if not all(config.values()):
        missing = [k for k, v in config.items() if v is None]
        raise ConfigurationError(
            f'Missing one of required config params: {missing}')

    if config['MODE'] not in modes:
        raise ConfigurationError(
            f'Unsopported mode: {config["MODE"]}. Expected: {modes}')

    if config['MODE'] == 'dev':
        config_logger(logging.DEBUG)
    else:
        config_logger(logging.INFO)

    config.update(build_proxy_config())

    return config


def build_proxy_config():
    supported_types = ['MTProto', 'SOCKS5']

    config = {
        key: load_config_var(key)
        for key in ('PROXY_TYPE', 'PROXY_HOST', 'PROXY_PORT')
    }

    if config['PROXY_TYPE']:
        config['USE_PROXY'] = True
        if config['PROXY_TYPE'] not in supported_types:
            raise ConfigurationError(
                'Unsupported proxy type: {}. Expected: {}'.format(
                    config['PROXY_TYPE'], supported_types))

        config['PROXY_PORT'] = int(config['PROXY_PORT'])

        if config['PROXY_TYPE'] == 'MTProto':
            config['PROXY_SECRET'] = load_config_var('PROXY_SECRET')

        if not all(config.values()):
            missing = [k for k, v in config.items() if v is None]
            raise ConfigurationError(
                f'Missing one of required proxy params: {missing}')
        return config

    return {'USE_PROXY': False}


def download_model():
    import logging
    logger = logging.getLogger(__name__)

    ID_GOOGLE_FILE = "1FR72Ib40V0nXxfH__x91NWGsy13hzcs5"

    logger.info("Downloading model...")
    gdd.download_file_from_google_drive(
        ID_GOOGLE_FILE, './data/model_checkpoint.zip')
    logger.info("Download completed!")
    files = os.listdir()
    logger.info(f"Dir: {files}")
