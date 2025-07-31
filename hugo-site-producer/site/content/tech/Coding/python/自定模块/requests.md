---
title: "Requests"
date: 2025-07-31T15:29:43+08:00
draft: false
tags: ["技","code","python", 'http']
toc: true
showTableOfContents: true
---

## requests.request方法
基础用法：
```python
requests.request(method, url, headers, json)
requests.request(method, url, headers, data)
```
参数json和data的区别：
json为字典对象
data为字典字符串，需要使用`json.dumps(payload)`转换为字符串