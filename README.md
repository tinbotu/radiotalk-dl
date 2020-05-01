# radiotalk-dl

## Overview

this is a downloader like youtube-dl for https://radiotalk.jp/ 


## Requirements

- Python3
    - venv

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
   or satisty requirements.txt, edit shebang


1. mkdir output directory

   ```sh
   $ mkdir -p data
   ```
   or edit `RadiotalkDl.outdir`

## run

usage: radiotalk-dl.py url [url2] [url3]...


## sample


```sh
$ cd ~/workspace/radiotalk-dl
$ ./radiotalk-dl.py 
$ ./radiotalk-dl.py https://radiotalk.jp/talk/248986 https://radiotalk.jp/talk/2797
波よ聞いてくれ～Wave, Listen to me!～ - 248986 [4-2] ミナレの1つ1つのセリフが長い...！アニメ『波よ聞いてくれ』の制作エピソード (2020-03-28)
運コミュ！（Radiotalk運営の公式番組） - 2797 第0回 運コミュって何だ？（雑談） (2017-10-13)
$ 
```

```sh
$ ls -l data/
-rw-r--r-- 1 user user 6050853 10月 13  2017 '運コミュ！（Radiotalk運営の公式番組） - 2797 第0回 運コミュって何だ？（雑談） (2017-10-13).m4a'
-rw-r--r-- 1 user user 2671878  3月 28 10:16 '波よ聞いてくれ～Wave, Listen to me!～ - 248986 [4-2] ミナレの1つ1つのセリフが長い...！ アニメ『波よ聞いてくれ』の制作エピソード (2020-03-28).m4a'
```


## uninstall

1. remote working directory that git clone


## License

MIT


