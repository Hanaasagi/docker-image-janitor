import os
import sys
import yaml
import argparse
import textwrap
from colorama import Fore, Style
from .image import get_layers, list_images, del_images
from .nodes import Node, merge_to_tree, flatten_tree


def parse_args():
    parser = argparse.ArgumentParser(
        prog='rmi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            ==============================
            ##### clean docker image #####
            ==============================
        ''')
    )
    parser.add_argument(
        '-c', '--config',
        metavar='/you/path/maintenance.yaml',
        default=None,
        help='config path'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.config is None:
        print(f"{Fore.RED}config not specified, "
              f"use '-h' to show help.{Style.RESET_ALL}")
        sys.exit(1)

    if not os.path.exists(args.config):
        print(f"{Fore.RED}config file does not exist.{Style.RESET_ALL}")
        sys.exit(1)

    maintenance_list = yaml.load(open(args.config, 'r'))

    layers = []
    for img_name in maintenance_list:
        layers.extend(get_layers(img_name))

    all_imgs = list_images()
    img_need_deleted = set(all_imgs) - set(layers)

    root = Node(None)
    tree = root
    for img_name in img_need_deleted:
        lyers = list(reversed(get_layers(img_name)))
        lst = [l for l in lyers if l in img_need_deleted]
        tree = merge_to_tree(tree, lst)
    # first element is root node(None)
    rm_list = flatten_tree(tree)[1:]
    print(f'{Fore.RED}Following image layers will be delete:{Style.RESET_ALL}')
    print(f'{Fore.WHITE}{chr(10).join(rm_list)}{Style.RESET_ALL}')
    answer = input(
        f'{Fore.BLUE}Enter y to continue [y/n]: {Style.RESET_ALL}'
    )
    if answer not in ('\n', 'Y', 'y'):
        sys.exit(0)
    if len(rm_list):
        del_images(list(reversed(rm_list)))
