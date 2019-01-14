# sponsorship_remover

# Requirements:
- Docker (optional)
- Python 3.6

### Installation Instructions:

Assuming you have already installed Docker for either [OSX](https://docs.docker.com/v17.09/docker-for-mac/install/), [Windows](https://docs.docker.com/v17.09/docker-for-windows/install/), or [Linux](https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/)...

1. `$ git clone https://github.com/98mprice/sponsorship_remover.git`

1. `$ cd /path/to/sponsorship_remover`

1. `$ docker build . -t py-sponsorship-remover`

1. `$ docker run py-sponsorship-remover python /scripts/predict.py --id <<ID of youtube video>>`

Example:
```bash
$ docker build . -t py-sponsorship-remover
$ docker run py-sponsorship-remover python /scripts/predict.py --id IorDYGI1uqc
$ 2019-01-14 13:14:00.439558: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
  predicting IorDYGI1uqc...
  9
  [{'start': '0:00:00', 'end': '0:00:11'}, {'start': '0:02:37', 'end': '0:02:51'}, {'start': '0:06:01', 'end': '0:06:15'}, {'start': '0:08:34', 'end': '0:08:46'}, {'start': '0:09:05', 'end': '0:09:19'}, {'start': '0:09:12', 'end': '0:09:24'}, {'start': '0:09:18', 'end': '0:09:31'}]
```

---


At the moment this is super bare bones, basically though you can run `python predict.py` to do any predictions.

Either pass the id of an individual video with flag `--id <id>` or of a channel with `--channel <channel_id>`

If you want to help with development please join the discord https://discord.gg/54R7Rr6

Thanks all! 😊

---

##### Using docker for further development
Use the `-v` flag to place a directory on your host OS into docker's "guest OS," then start an interactive shell session inside the container to run any latest changes

1. `$ docker build . -t py-sponsorship-remover`
1. `$ docker run -it --rm -v $PWD:/scripts py-sponsorship-remover bash`
1. Make any changes using your favorite editor on your OS; any changes in your host OS are automagically synced into the container
1. From inside the container... `$ python predict.py --id <<ID of youtube video>>`

##### Python Only Installation

1. `$ git clone https://github.com/98mprice/sponsorship_remover.git`

1. `$ cd /path/to/sponsorship_remover`

1. `$ virtualenv -p python3 <desired-path>`

1. `$ pip3 install -r requirements.txt`

1. `$ python predict.py --id <<ID of youtube video>>`

1. `$ source <desired-path>/bin/activate`

1. `$ deactivate`
