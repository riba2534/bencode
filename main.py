#!/usr/bin/python3
# -*- coding: UTF-8 -*-

__author__ = 'riba2534'
"""
    Date        : '2021/3/25'
    Description :  用 Bencode 编码解析torrent文件
"""

import sys
from datetime import datetime
import json


class BDecode(object):
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.i = 0

    def parse(self):
        return self.dic()

    def peek(self):
        next = None
        if self.i < self.n:
            next = self.arr[self.i]
        return chr(next)

    def next(self):
        next = None
        if self.i < self.n:
            next = self.arr[self.i]
            self.i += 1
        return chr(next)

    def num(self):
        num_str = ""
        peek = self.peek()

        if peek is None:
            raise Exception("malformed num.")

        if peek == '-' and self.peek(1) in '123456789':
            self.next()  # ignore '-'
            while self.peek() in "0123456789":
                num_str += self.next()
            if num_str[0] in '0' and len(num_str) > 1:
                raise Exception("error : 0 starts with num")
            return -int(num_str)
        elif peek in '0123456789':
            while self.peek() in "0123456789":
                num_str += self.next()
            if num_str[0] in '0' and len(num_str) > 1:
                raise Exception("error : 0 starts with num")
            return int(num_str)
        else:
            raise Exception("malformed num.")

    def string(self, pieces=False):
        length = self.num()
        if self.next() != ':':
            raise Exception("String must contain colon")
        s = self.arr[self.i:(self.i + length)]
        self.i += length

        if not pieces:
            return s.decode("utf8")
        else:
            # pieces maps to a string whose length is a multiple of 20.
            # It is to be subdivided into strings of length 20,
            # each of which is the SHA1 hash of the piece at the corresponding index.
            result = []
            for j in range(0, length, 20):
                hash = s[j:j + 20]
                result.append(hash.hex().lower())
            return result

    def integer(self, timestamp=False):
        if self.next() != "i":
            raise Exception("Integer must begin with i")
        val = self.num()

        if timestamp:
            val = datetime.fromtimestamp(val).__str__()

        if self.next() != "e":
            raise Exception("Integer must end with e")
        return val

    def element(self, pieces=False, timestamp=False):
        peek = self.peek()
        if peek == 'i':
            return self.integer(timestamp)
        elif peek == "l":
            return self.list()
        elif peek == 'd':
            return self.dic()
        elif peek in "0123456789":
            return self.string(pieces)
        else:
            raise Exception("not recognize.")

    def list(self):
        if self.next() != "l":
            raise Exception("list must begin with l")
        result = []
        while self.peek() != 'e':
            result.append(self.element())
        self.next()
        return result

    def dic(self):
        if self.next() != 'd':
            raise Exception("dic must begin with d")
        result = dict()

        while self.peek() != "e":
            key = self.string()
            val = None
            if key == "pieces":
                val = self.element(pieces=True)
            elif key == 'creation date':
                val = self.element(timestamp=True)
            else:
                info_start = None
                info_end = None
                if key == 'info':
                    info_start = self.i
                val = self.element()
                if key == 'info':
                    info_end = self.i
                    result['info_hash'] = self.sha1(
                        self.arr[info_start:info_end])
            result[key] = val

        self.next()
        return result

    def sha1(self, info):
        import hashlib
        p = hashlib.sha1()
        p.update(info)
        return p.hexdigest()


def get_content():
    args = sys.argv
    if len(args) == 1:
        print('参数列表为空，请检查')
        exit(0)
    path = args[1]
    with open(path, "rb") as f:
        return f.read()


def main():
    content = get_content()
    result = BDecode(content).parse()
    result_json = json.dumps(result)
    print(result_json)


def test_string():
    s = "4:abcd".encode("utf8")
    result = BDecode(s).string()
    print(result)


def test_integer():
    s = "i123e".encode("utf8")
    print(BDecode(s).integer())


if __name__ == '__main__':
    main()
