#coding=utf-8
'''
name:chemipro
time:2018-07
'''

from socket import *
import sys
import re
from threading import Thread
from setting import *
import time

class HTTPServer(object):
    def __init__(self,addr = ('0.0.0.0',80)):#http 默认监听80端口
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
        self.bind()

    def bind(self):
        self.ip = self.addr[0]
        self.port = self.addr[1]
        self.sockfd.bind(self.addr)

    def serve_forever(self):
        self.sockfd.listen(10)
        print('listen the port %d..'%self.port)
        while True:
            connfd,add = self.sockfd.accept()
            print('connect from',add)
            handle_client = Thread(target = self.handle_request,args = (connfd,))
            handle_client.setDaemon(True)
            handle_client.start()

    def handle_request(self,connfd):
        #接收浏览器请求
        request = connfd.recv(4096)
        request_lines = request.splitlines()
        #获取请求行
        request_line = request_lines[0].decode()
        # 正则提取请求方法和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern,request_line).groupdict()
        except:
            response_headlers = 'HTTP/1.1 500 Server Error\r\n'
            response_headlers += '\r\n'
            response_body = 'Server Error'
            response = response_headlers + response_body
            connfd.send(response.encode())
            return
        print(env)
        #将浏览器请求发给frame得到返回数据结果(响应码和响应内容)
        status,response_body = self.send_request(env['METHOD'],env['PATH'])

        # 根据frame发送过来的响应码status组织回发给浏览器的响应头内容
        response_headlers = self.get_headlers(status)

        # 将结果组织为http　response发送给客户端
        response = response_headlers + response_body
        connfd.send(response.encode())
        connfd.close()

    # 和框架frame交互　，发送request获取response,返回响应码和响应内容
    def send_request(self,method,path):
        s = socket()
        s.connect(frame_addr)

        # 向webframe发送method和path
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        # 接收到webframe的status和response_body
        status = s.recv(128).decode()
        response_body = s.recv(4096 * 10).decode()
        return status,response_body

    def get_headlers(self,status):
        if status == '200':
            response_headlers = 'HTTP/1.1 200 OK\r\n'
            response_headlers += '\r\n'
        elif status == '404':
            response_headlers = 'HTTP/1.1 400 NOT FOUND\r\n'
            response_headlers += '\r\n'
        return response_headlers


if __name__ == '__main__':
    httpserver =HTTPServer(ADDR)
    httpserver.serve_forever()








































