
import requests
import base64
import json
import logging

def get_cookie_from_login_sina_com_cn(account, password):
    """ 获取一个账号的Cookie """
    loginURL = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
    username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode("gbk")
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print("Get Cookie Success!( Account:%s )" % account)
        cookie = session.cookies.get_dict()
        return cookie
    else:
        print("Failed!( Reason:%s )" % info["reason"])
        return ""
co = get_cookie_from_login_sina_com_cn("dragon0486@163.com","long0486.")
print(co)
def stringToDict(cookie):
    itemDict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict
cookie = "_s_tentry=gl.ali213.net; UOR=gl.ali213.net,widget.weibo.com,www.howtoing.com; login_sid_t=99adeb40c85314559f6ee27d85c6f289; cross_origin_proto=SSL; Apache=425584148259.2815.1577595064696; SINAGLOBAL=425584148259.2815.1577595064696; ULV=1577595064704:1:1:1:425584148259.2815.1577595064696:; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhYmq3C-xkW9MRrIH1nbCWm5JpX5K2hUgL.FozRSh57eo.0eKz2dJLoIpjLxK-L1KeL1h2LxK-LBonL12eLxKBLBonLBoqt; ALF=1609133169; SSOLoginState=1577597170; SCF=AguUrz2aOzj6aiKJhuVtR80rMWc5WaBk4DEu4fA0ueqokqMGKo5dXiMSSi_X2yY_tK-2Tqj6JRtgS9bif_JK-K4.; SUB=_2A25zDEilDeRhGeRG71IR8ifPyj6IHXVQeD1trDV8PUNbmtAfLWH2kW9NUgurf05WxcolUaME9v2DGd3xO5Sl9KVZ; SUHB=09P85gu_L9wMmP; un=dragon0486@163.com; wvr=6; WBStorage=42212210b087ca50|undefined"
print(stringToDict(cookie))
a = {"login": "d8da5b8932bcaeff71bb253de5c5fc5b", "tgc": "TGT-Mjg0MDAyOTMxMg==-1577603861-gz-F669F2517CC93028CE3D64B526B1089F-1", "sso_info": "v02m6alo5qztYScpoWzm7a4pp2WpaSPk4i4jYOAsIyjpLOMk4jA", "LT": "1577603862", "SCF": "Ailux0GxBrDXU8rawmddxFOIDsbe-1-mazrBFZNDJePFBhiUr0bN8BzRDLIFQ3S1quYDruGpMsyhOKqTIbmub-g.", "ALF": "1609139862", "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WhYmq3C-xkW9MRrIH1nbCWm5NHD95QE1hB7ehz4e02EWs4Dqcjdi--fiK.0iKnpi--fi-zRiKyhi--Xi-zRi-zc", "ALC": "ac%3D2%26bt%3D1577603862%26cv%3D5.0%26et%3D1609139862%26ic%3D1901628250%26login_time%3D1577603860%26scf%3D%26uid%3D2840029312%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D0a3f8a6f6cece99b9f0260c637acab99", "SUB": "_2A25zDCNeDeRhGeRG71IR8ifPyj6IHXVQeBOWrDV_PUNbm9AfLRWtkW9NUgurf5dH9TY-k97Uf00zHV54gU5pRJW3"}
print(a)
re = requests.get("https://s.weibo.com/weibo?q=%E6%8A%A2%E4%BF%AE%20%E6%B4%AA%E6%B6%9D&nodup=1&page=2",cookies=co)
print(re.text)
