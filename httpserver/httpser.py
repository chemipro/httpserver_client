from socket import *
import sys
import time
from setting import *#配置文件　设置一些客户可变更的变量等
from threading import Thread
import re

class HttpServer(object):
    def __init__(self,addr):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
        self.bind()

    def bind(self):
        self.ip = self.addr[0]
        self.port = self.addr[1]
        self.sockfd.bind(self.addr)

    def forver_serve(self):
        self.sockfd.listen(3)
        print('listening to %d...'%self.port)
        while True:
            try:
                c,addr = self.sockfd.accept()
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('服务器退出')
            except Exception as err:
                print('服务器异常',err)
                continue

            print('connect to',addr)

            th = Thread(target = self.request_handler,args =(c,))
            th.setDaemon(True)
            th.start()

    def request_handler(self,c):
        request = c.recv(4096)
        # 获取请求行
        requestlines = request.splitlines()
        request_line = requestlines[0].decode()
        # 正则表达式匹配请求类型和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern,request_line).groupdict()
        except:
            response_head = 'HTTP/1.1 404 NOT FOUND\r\n'
            response_head += '\r\n'
            response_body = '==========sorry, not found=============='
            response = response_head + response_body
            c.send(response.encode())
            c.close()

        print(env)
        # 将请求类型和请求内容发给webframe，返回响应码和响应内容
        status,response_body = self.send_request(env['METHOD'],env['PATH'])

        # 根据响应码处理响应头
        response_head = self.get_response_head(status)
        response = response_head + response_body
        c.send(response.encode())
        c.close()

    def send_request(self,method,path):
        # 连接webframe服务器
        s = socket()
        s.connect(frame_addr)

        # 发送请求类型和请求内容
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        # 接收响应码和响应内容
        status = s.recv(128).decode()
        response_body = s.recv(4096).decode()
        return status,response_body

    def get_response_head(self,status):
        # 根据响应码类型组织不同的响应头
        if status == '200':
            response_head = 'HTTP/1.1 200 OK\r\n'
            response_head += '\r\n'
        elif status == '404':
            response_head = 'HTTP/1.1 404 not found\r\n'
            response_head += '\r\n' 
        return response_head        

if __name__ == '__main__':
    http_server = HttpServer(ADDR)
    http_server.forver_serve()






































