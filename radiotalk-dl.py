#! bin/python
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 sts=4 ff=unix ft=python expandtab

import sys
import os
import json
import re
import requests
import getopt
import time


class RadiotalkDl(object):
    outdir = './'
    url = None
    api_url = None
    program_id = None
    _api_url = r'https://radiotalk.jp/api/talks/%d'
    _id_re = None
    download_meta = False
    verbose = 1


    def __init__(self) -> None:
        self._id_re = re.compile(r'\/talk\/([0-9]+)')


    def get_program_id(self, original_url: str) -> int:
        m = self._id_re.search(original_url)
        if m and m.group():
            self.program_id = int(m.group(1))
            return int(m.group(1))
        else:
            raise ValueError("Can't extract programid")


    def get_program(self, program_id: int) -> dict:
        url = (self._api_url % (program_id))
        r = requests.get(url)
        return json.loads(r.text)


    def get_program_name(self, p, timestamp: str) -> str:
        return p['programTitle'] + ' - ' + str(p['id']) + ' ' + p['title'] + ' (' + timestamp + ')'


    def get_audio_url(self, p: str) -> str:
        return p['audioFileUrl']


    def get_image_url(self, p: str) -> str:
        return p['imageUrl']


    def write_as_file(self, filename: str, content, timestamp: float) -> None:
        if type(content) is str:
            mode = "w"
        else:
            mode = "wb"

        self.message("write %s %s" % (mode, filename))

        with open(filename, mode) as fp:
            fp.write(content)
        os.utime(filename, (timestamp, timestamp))

        # creation timestamp modification on Microsoft Windows
        if os.name == 'nt':
            try:
                import win32_setctime
                win32_setctime.setctime(filename, timestamp)
            except ModuleNotFoundError:
                print("- - - -\nPlease consider to install win32_setctime\ne.g.\nPS> pip install win32_setctime\n")


    def download(self, url: str, filename: str, timestamp: float) -> None:
        self.message("Downloading: %s" % url)
        r = requests.get(url)
        self.write_as_file(filename, r.content, timestamp)


    def get_audio(self, url: str) -> str:
        program_id = self.get_program_id(url)
        program = self.get_program(program_id)

        tm = time.strptime(program['createdAt'], '%Y-%m-%d %H:%M:%S')
        program_timestamp = time.mktime(tm)
        program_timestamp_str = "%04d-%02d-%02d" % (tm.tm_year, tm.tm_mon, tm.tm_mday)
        program_name = self.get_program_name(program, program_timestamp_str)

        audio_filename = self.outdir + "/%s.m4a" % (program_name)
        self.download(self.get_audio_url(program), audio_filename, program_timestamp)

        if self.download_meta:
            meta_filename = self.outdir + "/%s.json" % (program_name)
            self.write_as_file(meta_filename, json.dumps(program, indent=2, ensure_ascii=False), program_timestamp)

            image_filename = self.outdir + "/%s.jpg" % program_name
            self.download(self.get_image_url(program), image_filename, program_timestamp)

        return program_name


    def usage(self, me: str) -> str:
        return ("usage: %s [OPTIONS] target URL [target URL] [target URL] ...\n"
                "  [OPTIONS]\n"
                "  -o --outdir=./path/to/output\n"
                "  -v --verbose\n"
                "  -m --download-meta\n"
                "e.g. %s -m https://radiotalk.jp/talk/248986 https://radiotalk.jp/talk/2797"
                % (me, me))


    def message(self, message: str) -> None:
        if self.verbose > 1:
            print(message, file=sys.stderr)


if __name__ == '__main__':
    dl = RadiotalkDl()

    try:
        (opts, args) = getopt.gnu_getopt(sys.argv[1:], "vhmo:", ["verbose", "help", "download-meta", "outdir=", ])
    except getopt.GetoptError:
        print(dl.usage(sys.argv[0]))
        sys.exit(1)

    for o, a in opts:
        if o == "-v":
            dl.verbose += 1
        elif o in ("-h", "--help"):
            print(dl.usage(sys.argv[0]))
            sys.exit(0)
        elif o in ("-m", "--download-meta"):
            dl.download_meta = True
        elif o in ("-o", "--outdir"):
            dl.outdir = a
        else:
            print(dl.usage(sys.argv[0]))
            assert False, "unknown option"


    succeed = 0
    for url in args:
        if('http' in url):
            try:
                message = dl.get_audio(url)
                if type(message) is str:
                    succeed += 1
                print(message)
            except ValueError as e:
                print("%s: %s" % (e, url))

    if not succeed > 0:
        print(dl.usage(sys.argv[0]))
        sys.exit(1)
