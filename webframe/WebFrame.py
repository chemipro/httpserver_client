#coding=utf-8

from socket import *
from setting import *
import time
from urls import *
from views import *


class Application(object):
    def __init__(self,frame_addr):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(frame_addr)
    def start(self):
        self.sockfd.listen(5)
        while True:
            connfd,addr = self.sockfd.accept()
            # 接受请求方法
            method = connfd.recv(128).decode()
            # 接受请求内容
            path = connfd.recv(128).decode()
            print(path)
            if method == 'GET':
                if path == '/' or path[-5:] == '.html':
                    status,response_body = self.get_html(path)
                else:
                    status,response_body = self.get_data(path)

                # 将结果给httpserver
                connfd.send(status.encode())
                time.sleep(0.1)
                connfd.send(response_body.encode())

                connfd.close()

            elif method == 'POST':
                pass

    def get_html(self,path):
        if path == '/':
            get_file = STATIC_DIR + '/msg.html'
        else:
            get_file = STATIC_DIR + path
        try:
            f = open(get_file)
        except IOError:
            response = ('404','====Sorry not found the page====')
        else:
            response = ('200',f.read())
        finally:
            return response

    def get_data(self,path):
        for url,handler in urls:
            if path == url:
                response_body = handler()
                return '200',response_body
        return '404','====Sorry not found the data===='

if __name__ == '__main__':
    app = Application(frame_addr)# 从setting获取地址
    app.start()#启动框架等待request