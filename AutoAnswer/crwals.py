import requests
from random import randint
import time,re



# 获取页面js中的变量
def get_jqnonce(url, proxy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.6 Safari/537.36',
    }
    proxies = {
        "http": f"http://{proxy}",
    }

    res = requests.get(url, headers=headers, proxies=proxies)
    rn = re.search(r'rndnum="(.*?)";', res.text, re.M).group(1)
    jqnonce = re.search(r'jqnonce="(.*?)";', res.text, re.M).group(1)
    # print(rn)
    # print(jqnonce)
    return {"rn":rn,"jqnonce":jqnonce}

# 获取curid


# js 加密函数
# 根据 jqnonce, ktimes 获取jqsign
# 还可以使用execjs来解决
def dataenc(jqnonce, ktimes):
    b = 1 if ktimes % 10 == 0 else (ktimes % 10)
    c = []
    for char in jqnonce:
        temp = ord(char) ^ b
        c.append(chr(temp))
    return "".join(c)


def getTime(flag=1):
    if flag == 1:
        # 返回时间戳
        return str(time.time()).replace('.', '')[:-4]

    temp = str(time.time()).split(".")[0]
    now = int(temp)-randint(200,600)
    res = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(now))
    return res



def get_proxies():
    res = requests.get("http://127.0.0.1:5010/get_all")
    return res.json()

def get_proxy():
    res = requests.get("http://127.0.0.1:5010/get")
    return res.text
def delete_proxies(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def sendRequests(url, proxy, **kwargs):
    ktimes = randint(200,500)
    t = getTime(1)
    starttime = getTime(2)

    jqsign = dataenc(kwargs.get("jqnonce"), ktimes)
    headers = {
        'Host': 'www.wjx.cn',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wjx.cn',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.6 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    proxies = {
        "http": f"http://{proxy}",
    }
    url = f'https://www.wjx.cn/joinnew/processjq.ashx?curid={curid}&starttime={starttime}&source=directphone&submittype=1&ktimes={ktimes}&hlv=1&rn={kwargs.get("rn")}&t={t}&jqnonce={kwargs.get("jqnonce")}&jqsign={jqsign}'
    submitdata = '1$1}2$1}3$5000}4$打工}5$2}6$阿萨德}7$阿萨德}8$3|4}9$2}10$2}11$2}12$2}13$3}14$4|5}15$1}16$水电费}17$大师傅}18$大师傅}19$水电费}20$1'
    data = {
        "submitdata": submitdata,
    }
    leftry = 5
    while leftry > 0:
        try:
            res = requests.post(url, headers=headers, data=data, proxies=proxies)

            print(res.headers,"\t",res.text,"\t")
            time.sleep(0.5)
            return

        except(Exception):

            leftry -= 1
        finally:
            res.close()
    # 该代理不可用
    delete_proxies(proxy)


def main(url):
    proxy = get_proxy()
    msg = get_jqnonce(url, proxy)

    while True:
        proxies = get_proxies()
        for proxy in proxies:
            sendRequests(url, proxy, **msg)


if __name__ == "__main__":
    url = "https://www.wjx.cn/m/42808662.aspx"
    curid = 42808662


    main(url)


