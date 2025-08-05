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