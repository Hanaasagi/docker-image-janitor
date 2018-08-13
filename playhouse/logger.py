import logging

logger = logging.getLogger(__name__)

fmt = "[%(levelname)s %(asctime)-15s] %(message)s"
timefmt = "%d %b %Y %H:%M:%S"
sh = logging.StreamHandler()
formatter = logging.Formatter(fmt, timefmt)
sh.setFormatter(formatter)
logger.addHandler(sh)


__all__ = [
    'logger',
]
