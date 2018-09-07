import logging


fmt = "[%(levelname)s %(asctime)-15s] %(message)s"
timefmt = "%d %b %H:%M:%S"
logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
formatter = logging.Formatter(fmt, timefmt)
sh.setFormatter(formatter)
logger.addHandler(sh)


__all__ = [
    'logger'
]
