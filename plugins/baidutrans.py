#coding=utf-8

import httplib
import md5
import urllib
import random

class BaiduFanyi(object):

    appid = '20151113000005349'
    secretKey = 'osubCEzlGjzvw8qdQc41'

    def __init__(self):
        pass
    def query_word(self, q, fromLang="cn", toLang="en"):

        httpClient = None
        myurl = '/api/trans/vip/translate'
        salt = random.randint(32768, 65536)

        sign = self.appid+q+str(salt)+self.secretKey
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = myurl+'?appid='+self.appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

        try:
            httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            #response是HTTPResponse对象
            response = httpClient.getresponse()
            return response.read()
        except Exception, e:
            print e
        finally:
            if httpClient:
                httpClient.close()

if __name__ == "__main__":
    bot = BaiduFanyi()
    print bot.query_word("天气")
    print bot.query_word("天极")
    print bot.query_word("今天天气不错阿", "cn", "jp")
