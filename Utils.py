__author__ = 'Ice'

import re
import urllib
import httplib2
import random
import cStringIO
from gzip import GzipFile


class Web(object):
    @staticmethod
    def do_get(url, headers=None):
        http = httplib2.Http()
        response, content = http.request(url, 'GET', headers=headers)
        return response,content

    @staticmethod
    def do_post(url, headers=None, data={}):
        http = httplib2.Http()
        response, content = http.request(url, 'POST', headers=headers, body=urllib.urlencode(data))
        return response, content

    @staticmethod
    def get_cookie(response, ismultiple=False):
        cookie_temp = response["set-cookie"]
        # if there are more than one "set-cookie" segment
        # all of them will be joined by ,
        # A known issue is that the expire attribute with ","
        if ismultiple:
            cookie = cookie_temp.replace(",", ";")
        else:
            print "try to get cookie"
            cookie_temp = cookie_temp.replace(" path=/;", "")
            cookie_temp = cookie_temp.replace(" path=/", "")
            cookie_temp = cookie_temp.replace(" httponly", "")
            cookie_temp = re.sub(r"expires=\w+,\s\w+-\w+-\w+\s\d+:\d+:\d+\sGMT;", "", cookie_temp)
            cookie_temp = re.sub(r"\s*,\s*", "", cookie_temp)
            cookie = cookie_temp
        return cookie


class StrUtils(object):
    @staticmethod
    def search(given_str, pattern, index=1):
        match = re.search(pattern, given_str)
        if match:
            return match.group(index)
        return None

    @staticmethod
    def strtoint(str):
        return int(str)

    @staticmethod
    def getrandomstr():
        return str(random.uniform(0.00000000000000001, 0.99999999999999999))


class CodingUtils(object):
    @staticmethod
    def decodegzip(gzipcontent):
        try:
            gf = GzipFile(fileobj=cStringIO.StringIO(gzipcontent), mode="rb")
            html_data = gf.read()
        except:
            print "gzip error"
            html_data = gf.extrabuf
        return html_data


class Utils(object):
    @staticmethod
    def between(num, start, end):
        if num > start and num < end:
            return True
        return False