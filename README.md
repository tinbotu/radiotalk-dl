# radiotalk-dl

## Overview

this is a downloader like youtube-dl for https://radiotalk.jp/ 

You can download the Radio as `m4a` file without re-encoding.


## Requirements

- Python3
    - venv
	- requests

## how to setup

1. clone this repo to some directory

   ```sh
   $ mkdir -p ~/workspace
   $ git clone git@github.com:tinbotu/radiotalk-dl.git ~/workspace/radiotalk-dl
   $ cd ~/workspace/radiotalk-dl
   ```

1. setup venv and install requirements

   ```sh
   $ make setup
   ```
   if you don't want to use `venv`, you can just rewrite shebang without setting up `venv`, though you have to satisty requirements.txt


## run
```
usage: radiotalk-dl.py [OPTIONS] url [url2] [url3]...
  [OPTIONS]
    -o --outdir=./path/to/output/directory
    -v --verbose
    -m --download-meta
```
## sample


```sh
$ cd ~/workspace/radiotalk-dl
$ ./radiotalk-dl.py https://radiotalk.jp/talk/2797 https://radiotalk.jp/talk/248986
運コミュ！（Radiotalk運営の公式番組） - 2797 第0回 運コミュって何だ？（雑談） (2017-10-13)
波よ聞いてくれ～Wave, Listen to me!～ - 248986 [4-2] ミナレの1つ1つのセリフが長い...！アニメ『波よ聞いてくれ』の制作エピソード (2020-03-28)
$ 
```


result

```sh
$ ls -l data/
-rw-r--r-- 1 user user 6050853 10月 13  2017 '運コミュ！（Radiotalk運営の公式番組） - 2797 第0回 運コミュって何だ？（雑談） (2017-10-13).m4a'
-rw-r--r-- 1 user user 2671878  3月 28 10:16 '波よ聞いてくれ～Wave, Listen to me!～ - 248986 [4-2] ミナレの1つ1つのセリフが長い...！ アニメ『波よ聞いてくれ』の制作エピソード (2020-03-28).m4a'
```


## uninstall

1. delete working directory that git clone


## License

MIT
