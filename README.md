# docker-image-janitor

Clean unneeded image layer.

### Install

```Bash
pip install git+https://github.com/Hanaasagi/docker-image-janitor
```

*Notice: It will add entrypoint file `rmi` in you `/usr/local/bin/`, make sure there is no bad influence in you system.*

### Usage

```
usage: rmi [-h] [-c /you/path/maintenance.yaml]

==============================
##### clean docker image #####
==============================

optional arguments:
  -h, --help            show this help message and exit
  -c /you/path/maintenance.yaml, --config /you/path/maintenance.yaml
                        config path
```

List all images that you don't want to clean in a yaml file, then run `rmi -c yaml-file-path` to clean the other.


### Why not `docker rmi`

Actually, `docker rmi` support remove a multi images. But if these images has dependencies, it will only clean child images, and you need to `docker rmi [parents images]` again.

For example:

`3436b23f8703` is the parent image of `597c05fbac24`. And you run `docker rmi 3436b23f8703 597c05fbac24`, docker will complain

```
Deleted: sha256:597c05fbac24b41dc4cf4b90b6e66adc741e1fc348bc6eb898ffd6842cb7cef9
Deleted: sha256:b5602fd6cc2c021701fdfdd19356eba2b6f31ac46819b74fc46b24f8e59f7c85
Error response from daemon: conflict: unable to delete 3436b23f8703 (cannot be forced) - image has dependent child images
```

The correct remove command is `docker rmi 597c05fbac24 3436b23f8703`. So I create this script to sort out the dependencies through `docker history` command, try to remove child images first, then their parents.
