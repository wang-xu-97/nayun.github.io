---
title: "LinuxHttp工具"
date: 2025-08-05T14:28:04+08:00
draft: false
tags: ["技", "linux", "工具", "http"]
toc: true
showTableOfContents: true
---

## wget
wget获取指定ip路由下的全部文件
`-r`：递归
`--no-parent`：无父目录
`--accept`：接收文件，支持通配符
`--reject`：拒绝文件，支持通配符
`-P`：指定下载路径
```shell
wget -r --no-parent --accept "*.zip*" --reject "*.html" ip:port -P ./download/
```


## Http文件服务器
1. python3 http server模块快速启动
`python3 -m http.server 8000 --directory /path/`
```console
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```
优点：快速
缺点：不能直观看到本地ip

2. python3 代码
```python
import socket
import sys
import http.server  
import socketserver 
import traceback

class Handler(http.server.SimpleHTTPRequestHandler): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=target, **kwargs)
    
    def end_headers(self):
        self.send_header('Connection', 'close')
        super().end_headers()

def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  
        local_ip = s.getsockname()[0] 
        s.close() 
        return local_ip
    except Exception as e:
        raise Exception(f"无法获取IP: {str(e)}\n请检查网络环境")

if __name__ == '__main__':
    local_ip = get_local_ip()
    target = ''
    try:
        target = sys.argv[1]
    except:
        target = "."
    
    with socketserver.ThreadingTCPServer(("", 0), Handler) as httpd:
        port = httpd.server_address[1] 
        print(f"Serving HTTP on http://{local_ip}:{port}/")
        try:
            httpd.serve_forever()
        except:
            print(traceback.format_exc())
        finally:
            httpd.server_close()
    print('exit.')
```
```shell
python3 autofileserver.py /path/
```
优点：快速、直观看到ip:port