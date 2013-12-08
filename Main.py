__author__ = 'Ice'
# -*- coding: utf-8 -*-

import re
import threading

import Constants
import Utils

lock = threading.RLock()
zhuansheng_lock = True
jiadian_lock = True

def getUserInfo(ID):
    return "merrymin", "861560"

class Game(object):
    def __init__(self, username, password):
        if not username and not password:
            self.username, self.password = getUserInfo(0)
        else:
            self.username = username
            self.password = password
        self.serverurl = Constants.SERVERURL
        #here it will be a str
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
        self.mapid = 1      # which map for killing
        self.isspecialtime = False

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
        print "start to login for %s" % self.username
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
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["INITCOOKIE"]
        rsp, cnt = Utils.Web.do_post(real_url, headers, login_data)


    def gotomainmenu(self):
        print "start to go to main menu"
        url = 'forum.php'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)

    # Main page of game
    def gotopetmenu(self):
        print "start to go to pet menu"
        url = 'wxpet-pet.html'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)

    def gotomainmap(self):
        print "start to go to mainmap"
        url = 'plugin.php?id=wxpet:pet&index=map'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)

    def gotomap(self, mapid=24):
        self.gotopetattributemenu()
        if not mapid:
            mapid = self.selectmapforzhuan(self.ZHUAN)
        self.mapid = mapid
        print "start to go to map: ", mapid
        url = 'plugin.php?id=wxpet:pet&index=fight&mapid=%s' % self.mapid
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        self.jiabei(cnt)
        return cnt

    def selectmapforzhuan(self, zhuan):
        print "Zhuan: %s" % zhuan
        value = "0"
        last_chaju = 100
        for key in Constants.ZHUAN_LEVEL_MAP.keys():
            if int(zhuan) < 22:
                chaju = int(zhuan) - int(key)
            else:
                chaju = int(zhuan) - int(key) + 2
            if chaju == 0:
                value = key
                break
            if chaju > 0:
                print key, last_chaju, chaju
                if last_chaju > chaju:
                    value = key
                    last_chaju = chaju
        return Constants.ZHUAN_LEVEL_MAP[value]

    def gotospecialmap(self, mapid):
        if self.isspecialtime:
            if self.mapid != mapid:
                self.gotomap(mapid)
                self.refreshzhandoustatus()

    def jiabei(self, mapcnt):
        print "start to jiabei"
        def getkaid(mapcnt):
            kaid = Utils.StrUtils.search(mapcnt, "经验卡&nbsp;&nbsp;&nbsp;&nbsp;<br>数量：\
<font color=darkgreen><span id='item(\d+)")
            if not kaid:
                kaid = Utils.StrUtils.search(mapcnt, "经验卡&#8226签&nbsp;&nbsp;&nbsp;&nbsp;<br>数量：\
<font color=darkgreen><span id='item(\d+)")
            return kaid
        kaid = getkaid(mapcnt)
        if not kaid:
            return
        url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=fight_itemuse&\
storageid=%s&nums=1&timestamp=1385546091727' % kaid
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        print cnt

    def getlastsaltkey(self, cookies):
        return Utils.StrUtils.search(cookies, "8VcR_2132_saltkey=(\w+)")

    def getlastsid(self, cookies):
        return Utils.StrUtils.search(cookies, "8VcR_2132_sid=(\w+)")

    def skill(self):
        print "skillcount: ", self.skillcount
        if int(self.skillcount) != 0:
            return None
        print "start to use skill"
        url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=fight_callmagic&\
action=callmsleep&timestamp=1385401239678'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        self.cookie = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)

    def findmonster(self):
        print "start to find monster"
        url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=fight_findnpc&timestamp=1386359230497'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        self.cookie = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        print cnt

    def kill(self, interval=120):
        """
        interval:   the time interval to search level and the level to zhuanshen;
            since before, each time of killing will search, it will cost time
        """
        print "start to kill monster"
        skill = "noskill"
        if int(self.ZHUAN) > 0:
            skill = "mlightbomb"
        url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=fight&\
skillname=%s&pkcode=%s&autosell=0&timestamp=1385401456697' % (skill, self.pkcode)
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["KILLCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        print cnt
        regex = '(\w+)npc\(.*剩余\s+(\d+)\s+回合.*\[(\d+)\]\]></petlevel>.*<pkcode>(\d+)</pkcode>'
        try:
            action, self.skillcount, self.LEVEL, self.pkcode = Utils.StrUtils.getstrgroup(cnt, regex)
            #self.isspecialtime = self.checkwhetherinspecialtime(self.getservertime(rsp))
            print "action ===> %s | shi ==> %s | zhuan ==> %s | level ==> %s | to_be_level = %s" % \
                  (action, self.SHI, self.ZHUAN, self.LEVEL, self.CANZHUAN)
            if action == Constants.ACTION["runnpc"]:
                self.skill()
                self.kill(interval)
        except Exception, e:
            #print cnt
            self.skillcount = 0
            print "Error -- %s" % str(e)
        finally:

            pass

    def getservertime(self, rsp):
        #Date: Wed, 27 Nov 2013 04:12:50 GMT
        print rsp
        #servertime = Utils.StrUtils.search(rsp, "Date:(.*)")
        servertime = rsp["date"]
        print servertime
        return servertime

    def checkwhetherinspecialtime(self, atime):
        week, hour = Utils.TimeUtils.getweekandhourfromtime(atime)
        if (week in [1, 3, 5, 7] and hour == 21) or (week in [2, 4, 6, 7] and hour == 13):
            self.isspecialtime = True

    def zhuanshen(self):
        print "start to zhuanshen"
        url = 'plugin.php?id=wxpet:pet&index=petjob'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        url = "plugin.php?id=wxpet:pet&index=petjob&do=buy"
        real_url = self.__get_full_url__(self.serverurl, url)
        login_data = {
                'petid':        21,
                'do':        "buy",
                'submit':        ""
        }
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_post(real_url, headers, login_data)
        self.ZHUAN = int(self.ZHUAN) + 1

    def zhuanshiaffair(self):
        print "start to go to office"
        url = 'plugin.php?id=wxpet:pet&index=office'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)

        canzhuanshi = 31 + int(self.SHI) * 5
        formhash = Utils.StrUtils.search(cnt, "formhash=(\w+)")
        print "<== zhuan of %s can zhuanshi ==>" % canzhuanshi
        if canzhuanshi <= int(self.ZHUAN):
            self.zhuanshi(formhash)

    def zhuanshi(self, formhash):
        print "start to zhuanshi"
        url = "plugin.php?id=wxpet:pet&index=office&action=world"
        real_url = self.__get_full_url__(self.serverurl, url)
        zhuanshi_data = {
                'petworld':     1
        }
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_post(real_url, headers, zhuanshi_data)

    def jiadian(self):
        self.gotopetattributemenu()
        print "start to jiadian"
        url = "plugin.php?id=wxpet:pet&index=mypet&action=addpoints"
        real_url = self.__get_full_url__(self.serverurl, url)
        jiadian_data = {
                'formhash':     self.formhash,
                'upstr':        0,
                'upvit':        0,
                'upagi':        0,
                'upint':        self.point,
                'updex':        0
        }
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_post(real_url, headers, jiadian_data)

    def zhuangbei(self):
        print "start to zhuangbei"

        def mainzhuangbei():
            def getzhuangbeifromzhuan(zhuan):
                return zhuan

            def getallzhuangbei():
                url = 'plugin.php?id=wxpet:pet&index=suit'
                real_url = self.__get_full_url__(self.serverurl, url)
                headers = Constants.WEBHEADERS
                headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
                rsp, cnt = Utils.Web.do_get(real_url, headers)
                #print cnt
                formhash = Utils.StrUtils.search(cnt, "formhash=(\w+)")
                cnt_list = cnt.splitlines()
                index = 0
                dest_index = 0
                for line in cnt_list:
                    if line == '<td align="center" width="10%">神器＆江河万古流<br>':
                        dest_index = index + 4
                        break
                    index += 1
                if not dest_index:
                    index = 0
                    for line in cnt_list:
                        if line == '<td align="center" width="10%">神器＆江河万古流<br>':
                            dest_index = index + 4
                            break
                        index += 1
                print "zhuangbei: %s" % cnt_list[dest_index]
                suitid = Utils.StrUtils.search(cnt_list[dest_index], "nums(\d+)")
                return formhash, suitid
            formhash, suitid = getallzhuangbei()
            url = 'plugin.php?id=wxpet:pet&index=suit&action=wears'
            real_url = self.__get_full_url__(self.serverurl, url)
            wear_data = {
                    'formhash':     formhash,
                    'suitid':    suitid
            }
            headers = Constants.WEBHEADERS
            headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
            rsp, cnt = Utils.Web.do_post(real_url, headers, wear_data)

        def jiezhizhuangbei():
            url = 'plugin.php?id=wxpet:pet&index=storage&itemtype=6'
            real_url = self.__get_full_url__(self.serverurl, url)
            headers = Constants.WEBHEADERS
            headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
            rsp, cnt = Utils.Web.do_get(real_url, headers)
            jiezhiid = Utils.StrUtils.search(cnt, 'id="cname(\d+)" value="经验之戒"')
            url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=storage&storageid=%s&\
action=wear&nums=1&timestamp=1385542559337' % (jiezhiid)
            real_url = self.__get_full_url__(self.serverurl, url)
            headers = Constants.WEBHEADERS
            headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
            Utils.Web.do_get(real_url, headers)

        def chibangzhuangbei():
            url = 'plugin.php?id=wxpet:pet&index=storage&itemtype=7'
            real_url = self.__get_full_url__(self.serverurl, url)
            headers = Constants.WEBHEADERS
            headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
            rsp, cnt = Utils.Web.do_get(real_url, headers)
            jiezhiid = Utils.StrUtils.search(cnt, 'id="cname(\d+)" value="天使之翼"')
            url = 'plugin.php?id=wxpet:pet&type=ajax&ajaxindex=storage&storageid=%s&\
action=wear&nums=1&timestamp=1385542559337' % (jiezhiid)
            real_url = self.__get_full_url__(self.serverurl, url)
            headers = Constants.WEBHEADERS
            headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
            Utils.Web.do_get(real_url, headers)

        jiezhizhuangbei()
        chibangzhuangbei()
        mainzhuangbei()

    def learnskill(self):
        print "start to learnskill"
        url = "plugin.php?id=wxpet:pet&index=magic&action=mlightbomb"
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)

        url = "plugin.php?id=wxpet:pet&index=magic&action=msleep"
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)

    def gotopetattributemenu(self):
        print "start to check attribute of pet"
        url = 'plugin.php?id=wxpet:pet&index=mypet'
        real_url = self.__get_full_url__(self.serverurl, url)
        headers = Constants.WEBHEADERS
        headers["Cookie"] = Constants.COOKIE_MAP[self.username]["MAINCOOKIE"]
        rsp, cnt = Utils.Web.do_get(real_url, headers)
        zhuan_info = Utils.StrUtils.getstrgroup(cnt, "(\d+)世(\d+)转(\d+)级")
        self.SHI = zhuan_info[0]
        self.ZHUAN = zhuan_info[1]
        self.LEVEL = zhuan_info[2]
        self.CANZHUAN = Utils.StrUtils.search(cnt, ">(\d+)级转生")
        self.point = Utils.StrUtils.search(cnt, "<b>(\d+)</b></font>")
        self.formhash = Utils.StrUtils.search(cnt, "formhash=(\w+)")
        print self.SHI, self.ZHUAN, self.CANZHUAN, self.LEVEL, self.point, self.formhash

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
        global zhuansheng_lock
        print "%s ===> %s" % (self.LEVEL, self.CANZHUAN)
        if int(self.LEVEL) < int(self.CANZHUAN):
            return
        zhuansheng_lock = False
        lock.acquire()
        if zhuansheng_lock:
            lock.release()
            return
        self.zhuanshen()
        self.zhuanshiaffair()
        self.jiadian()
        self.zhuangbei()
        self.forlevellimit()
        self.learnskill()
        self.gotomainmenu()
        self.gotomap()
        self.refreshzhandoustatus(refreshlevel=True)
        zhuansheng_lock = True
        lock.release()

    # skill can be learned at a higher level
    def forlevellimit(self):
        pass
        return
        # No limitation now
        self.gotomap(6)
        count = 5
        while(count):
            self.findmonster()
            self.kill()
            count -= 1

    def jiadianintime(self, interval=120):
        global jiadian_lock
        if interval <= 0:
            jiadian_lock = False
            lock.acquire()
            if jiadian_lock:
                lock.release()
                return
            self.jiadian()
            self.gotomainmap()
            self.gotomap()
            self.refreshzhandoustatus()
            jiadian_lock = True
            lock.release()

    def refreshzhandoustatus(self, refreshlevel=False):
        self.skillcount = 0
        if refreshlevel:
            self.LEVEL = 0

def test(a, b):
    tt = Game(a, b)
    tt.gotomainmenu()
    mapinfo = tt.gotomap()
    tt.jiabei(mapinfo)
    interval = Constants.INTERVAL
    while True:
        print "interval: ", interval
        tt.skill()
        tt.findmonster()
        tt.kill(interval)
        tt.jiadianintime(interval)
        tt.update()
        interval -= 1
        if interval < 0:
            interval = Constants.INTERVAL

class MyMultiThread(threading.Thread):
    def __init__(self, a, b):
        threading.Thread.__init__(self)
        self.a = a
        self.b = b

    def run(self):
        test(self.a, self.b)

if __name__ == '__main__':
    #test("merrymax", "861560")
    for i in range(0, 1):
        thread = MyMultiThread("%C9%F1%C5%A3", "861560")
        thread.start()
        #thread = MyMultiThread("merrymax", "861560")
        #thread.start()




