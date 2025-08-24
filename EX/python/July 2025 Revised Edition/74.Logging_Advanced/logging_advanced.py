"""Advanced logging configuration examples."""

from __future__ import annotations

import logging
import logging.config


def setup_manual_handlers() -> logging.Logger:
    logger = logging.getLogger("manual")
    logger.setLevel(logging.DEBUG)
    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    # file handler
    fh = logging.FileHandler("manual.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s"))
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def setup_dictconfig() -> None:
    config = {
        'version': 1,
        'formatters': {
            'detailed': {'format': '%(asctime)s %(name)s [%(levelname)s] %(message)s'},
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'detailed',
                'level': 'WARNING',
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'detailed',
                'level': 'DEBUG',
                'filename': 'dictconfig.log',
                'encoding': 'utf-8',
            },
        },
        'loggers': {
            'dictcfg': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
            },
        },
    }
    logging.config.dictConfig(config)
    logger = logging.getLogger('dictcfg')
    logger.debug("This debug message only goes to the file")
    logger.warning("This warning goes to both file and console")


if __name__ == "__main__":
    logger = setup_manual_handlers()
    logger.info("Manual handler: info message")
    logger.debug("Manual handler: debug message")
    setup_dictconfig()