import subprocess
from colorama import Fore, Style
from .logger import logger
from typing import List


"""
docker image operation
"""


def list_images() -> List[str]:
    """list all images by 'docker images -qa' command"""
    proc = subprocess.Popen(
        'docker images -qa',
        shell=True, encoding='utf-8',  # encoding add in 3.6
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    return stdout.split()


def del_images(img_list: List[str]) -> None:
    """remove images by 'docker rmi' command"""
    proc = subprocess.Popen(
        'docker rmi {}'.format(' '.join(img_list)),
        shell=True, encoding='utf-8',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    if stderr:
        logger.error('\n' + stderr)
        print(f'{Fore.RED}Some images could not be deleted, '
              f'try to find out reason and delete manually!{Style.RESET_ALL}')


def get_layers(img_name: str) -> List[str]:
    """get image layers by 'docker history' command"""
    proc = subprocess.Popen(
        'docker history {} -q'.format(img_name),
        shell=True, encoding='utf-8',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    return [
        layer for layer in stdout.split() if layer != '<missing>'
    ]
