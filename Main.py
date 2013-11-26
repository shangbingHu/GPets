__author__ = 'Ice'
# -*- coding: utf-8 -*-

import re
import time

import Constants
import Utils

def getUserInfo(ID):
    return "merrymax", "861560"

class Game(object):
    def __init__(self):
        self.username, self.password = getUserInfo(0)
        self.serverurl = Constants.SERVERURL
        #here it will be a str
        self.cookie = ""
        self.loginhash = ""
        self.lastsaltkey = ""
        self.lastsid = ""
        self.pkcode = "6731"
        self.skillcount = 0
        self.SHI = 0
        self.ZHUAN = 0
        self.LEVEL = 0
        self.CANZHUAN = 0
        self.point = 0
        self.formhash = 0

    def writetolog(self, content):
        fp = None
        fp = open("log", "w")
        fp.write(content)
        fp.close()

    def __get_full_url__(self, url_prefix="", url=""):
        if url_prefix:
            return url_prefix + "/" + url
        return self.serverurl + "/" + url

    def login(self):
        print "start to login"
        url = "member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
        real_url = self.__get_full_url__(self.serverurl, url)
        login_data = {
                'fastloginfield':   'username',
                'username':     self.username,
                'password':     self.password,
                'quickforward':    "yes",
                'handlekey':       "ls"
        }
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.INITCOOKIE
        rsp, cnt = Utils.Web.do_post(real_url, headers, login_data)
        self.cookie = Utils.Web.get_cookie(rsp)

    def gotomainmenu(self):
        print "start to go to main menu"
        url = 'forum.php'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = self.cookie
        rsp, cnt = Utils.Web.do_get(real_url, headers)

    # Main page of game
    def gotopetmenu(self):
        print "start to go to pet menu"
        url = 'wxpet-pet.html'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = self.cookie
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        self.updatecookie(rsp)
        print self.cookie

    def gotomainmap(self):
        print "start to go to mainmap"
        url = 'plugin.php?id=wxpet:pet&index=map'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        #print cnt  that's ok

    def gotomap(self, mapid):
        print "start to go to map: ", mapid
        url = 'plugin.php?id=wxpet:pet&index=fight&mapid=%s' % mapid
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        rsp, cnt = Utils.Web.do_get(real_url, headers)

    def getlastsaltkey(self, cookies):
        return Utils.StrUtils.search(cookies, "8VcR_2132_saltkey=(\w+)")

    def getlastsid(self, cookies):
        return Utils.StrUtils.search(cookies, "8VcR_2132_sid=(\w+)")

    def skill(self):
        print self.skillcount
        if self.skillcount != 0:
            return None
        print "start to use skill"
        url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=fight_callmagic&\
action=callmsleep&timestamp=1385401239678'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        self.cookie = Constants.MAINCOOKIE
        rsp, cnt = Utils.Web.do_get(real_url, headers)

    def findmonster(self):
        print "start to find monster"
        url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=fight_findnpc&timestamp=1385402992136'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        self.cookie = Constants.MAINCOOKIE
        rsp, cnt = Utils.Web.do_get(real_url, headers)

    def kill(self):
        print "start to kill monster"
        url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=fight&\
skillname=mlightbomb&pkcode=%s&autosell=0&timestamp=1385401456697' % self.pkcode
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.KILLCOOKIE
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        self.pkcode = Utils.StrUtils.search(cnt, "<pkcode>(\d+)</pkcode>")
        self.skillcount = int(Utils.StrUtils.search(cnt, "<font color=red>(\d+)\s+</font></td>"))
        self.LEVEL = Utils.StrUtils.search(cnt, "\[(\d+)\]\]></petlevel>")
        self.CANZHUAN = Utils.StrUtils.search(cnt, "\[(\d+)\]\]></joblevel>")
        print "level ==> %s | canzhuan = %s" % (self.LEVEL, self.CANZHUAN)

    def zhuanshen(self):
        print "start to zhuanshen"
        url = 'plugin.php?id=wxpet:pet&index=petjob'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.KILLCOOKIE
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        formhash = Utils.StrUtils.search(cnt, "formhash=(\w+)")
        url = "plugin.php?id=wxpet:pet&index=petjob&do=buy"
        real_url = self.__get_full_url__(self.serverurl, url)
        login_data = {
                'formhash':     formhash,
                'career':        3,
                'sn':        "",
                'petid':        21,
                'do':        "buy",
                'submit':        ""
        }
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        rsp, cnt = Utils.Web.do_post(real_url, headers, login_data)

    def jiadian(self):
        self.gotopetattributemenu()
        print "start to jiadian"
        url = "plugin.php?id=wxpet:pet&index=mypet&action=addpoints"
        real_url = self.__get_full_url__(self.serverurl, url)
        login_data = {
                'formhash':     self.formhash,
                'upstr':        0,
                'upvit':        0,
                'upagi':        0,
                'upint':        self.point,
                'updex':        0
        }
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        rsp, cnt = Utils.Web.do_post(real_url, headers, login_data)

    def zhuangbei(self):
        print "start to zhuangbei"
        url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=storage&action=\
wearsuit&storageid=75887&suitid=4&timestamp=1385481542711'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        Utils.Web.do_get(real_url, headers)

    def learnskill(self):
        print "start to learnskill"
        url = "plugin.php?id=wxpet:pet&index=magic"
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        formhash = Utils.StrUtils.search(cnt, "formhash=(\w+)")
        url = 'plugin.php?id=wxpet:pet&index=magic&action=learn'
        real_url = self.__get_full_url__(self.serverurl, url)
        skill_data = {
                'formhash':     formhash,
                'magicname':    "msleep"
        }
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        rsp, cnt = Utils.Web.do_post(real_url, headers, skill_data)
        skill_data = {
                'formhash':     formhash,
                'magicname':    "mlightbomb"
        }
        rsp, cnt = Utils.Web.do_post(real_url, headers, skill_data)

    def gotopetattributemenu(self):
        print "start to check attribute of pet"
        url = 'plugin.php?id=wxpet:pet&index=mypet'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.MAINCOOKIE
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        self.SHI = Utils.StrUtils.search(cnt, "轮回(\d+)世(\d+)转(\d+)级", 1)
        self.ZHUAN = Utils.StrUtils.search(cnt, "轮回(\d+)世(\d+)转(\d+)级", 2)
        self.LEVEL = Utils.StrUtils.search(cnt, "轮回(\d+)世(\d+)转(\d+)级", 3)
        self.CANZHUAN = Utils.StrUtils.search(cnt, ">(\d+)级转生")
        self.point = Utils.StrUtils.search(cnt, "<b>(\d+)</b></font>")
        self.formhash = Utils.StrUtils.search(cnt, "formhash=(\w+)")
        print self.point, self.formhash

    def refreshlastactid(self, cookie, lastsaltkey, lastsid):
        temp = cookie
        if lastsaltkey:
            temp = re.sub("8VcR_2132_saltkey=\w+", "8VcR_2132_saltkey=%s" % lastsaltkey, cookie)
        if lastsid:
            temp = re.sub("8VcR_2132_sid=\w+", "8VcR_2132_sid=%s" % lastsid, temp)
        return temp

    def updatecookie(self, rsp):
        self.lastsaltkey = self.getlastsaltkey(Utils.Web.get_cookie(rsp))
        self.lastsid = self.getlastsid(Utils.Web.get_cookie(rsp))
        self.cookie = self.refreshlastactid(self.cookie, self.lastsaltkey, self.lastsid)

    # 包括转生，加点，学习技能，套装
    def update(self):
        print self.LEVEL, self.CANZHUAN
        if int(self.LEVEL) < int(self.CANZHUAN):
            return
        self.zhuanshen()
        self.jiadian()
        self.zhuangbei()
        self.learnskill()
        self.gotomainmenu()
        self.gotopetmenu()
        self.gotomainmap()
        self.gotomap(20)
        self.refreshzhandoustatus(refreshlevel=True)

    def jiadianintime(self):
        level = int(self.LEVEL)
        if Utils.Utils.between(level, 300, 350) or \
            Utils.Utils.between(level, 600, 620) or \
            Utils.Utils.between(level, 1000, 1020):
            self.jiadian()
            self.gotomainmap()
            self.gotomap(20)
            self.refreshzhandoustatus()

    def refreshzhandoustatus(self, refreshlevel=False):
        self.skillcount = 0
        if refreshlevel:
            self.LEVEL = 0

def test():
    tt = Game()
    tt.login()
    tt.gotomainmenu()
    tt.gotopetmenu()
    tt.gotomainmap()
    tt.gotomap(20)
    while True:
        tt.skill()
        tt.findmonster()
        tt.kill()
        tt.jiadianintime()
        tt.update()

if __name__ == '__main__':
    test()


