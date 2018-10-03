from socket import *
import time
from setting import *#配置文件　设置一些客户可变更的变量等
from views import *#将具体数据的处理函数放在一个文件里
from urls import *#将能处理的数据事件放到一个文件里
import sys

class Application(object):
    def __init__(self,addr):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
        self.ip,self.port = self.addr
        self.bind()

    def bind(self):
        self.sockfd.bind(self.addr)

    def start(self):
        self.sockfd.listen(3)
        print('listen to %d'%self.port)
        while True:
            try:
                connfd,add = self.sockfd.accept()
                print('connet from',add)
            except KeyboardInterrupt:
                sys.exit('服务器退出')
            except Exception as e:
                print(e)
                continue
            # 接受httpserver的请求类型和请求内容
            method = connfd.recv(128).decode()
            path = connfd.recv(128).decode()
            print(path)

            # 根据请求类型分类处理不同的请求
            if method == 'GET':
                # 根据请求网页和请求数据分类处理
                if path == '/' or path[-5:] == '.html':
                    status,response_body = self.get_html(path)
                else:
                    status,response_body = self.get_data(path)
            elif method == 'POST':
                pass
            connfd.send(status.encode())
            time.sleep(0.1)
            connfd.send(response_body.encode())
            connfd.close()

    # 处理网页请求
    def get_html(self,path):
        if path == '/':
            filename = STATIC_DIR + '/msg.html'
        else:
            filename = STATIC_DIR + path

        try:
            f = open(filename)
        except:
            return '404','----sorry, not found-----'
        else:
            response_body = f.read()
            f.close()
            return '200',response_body

    # 处理数据请求
    def get_data(self,path):
        for url,func in urls:
            if path == url:
                response_body = func()
                return '200',response_body
        return '404','----sorry, not found-----'

if __name__ == '__main__':
    app = Application(frame_addr)
    app.start()
