#! bin/python
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 sts=4 ff=unix ft=python expandtab

import sys
import os
import json
import re
import requests
import time


class RadiotalkDl(object):
    outdir = './data'
    url = None
    api_url = None
    program_id = None
    _api_url = r'https://radiotalk.jp/api/talks/%d'
    _id_re = None


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


    def write_as_file(self, filename: str, content: str, timestamp: float):
        with open(filename, "wb") as fp:
            fp.write(content)
        os.utime(filename, (timestamp, timestamp))


    def download(self, url: str, program_name: str, timestamp: float):
        filename = self.outdir + "/%s.m4a" % (program_name)
        r = requests.get(url)
        self.write_as_file(filename, r.content, timestamp)


    def get_audio(self, url: str) -> str:
        program_id = self.get_program_id(url)
        program = self.get_program(program_id)

        tm = time.strptime(program['createdAt'], '%Y-%m-%d %H:%M:%S')
        program_timestamp = time.mktime(tm)
        program_timestamp_str = "%04d-%02d-%02d" % (tm.tm_year, tm.tm_mon, tm.tm_mday)
        program_name = self.get_program_name(program, program_timestamp_str)

        self.download(self.get_audio_url(program), program_name, program_timestamp)

        return program_name



if __name__ == '__main__':
    dl = RadiotalkDl()
    for url in sys.argv:
        if('http' in url):
            try:
                print(dl.get_audio(url))
            except ValueError as e:
                print("%s: %s" % (e, url))
