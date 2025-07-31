---
title: "元类MetaClass"
date: 2025-07-25T16:08:19+08:00
draft: false
tags: ["技", 'code', 'python', "概念"]
toc: true
showTableOfContents: true
---


元类作用时机
当使用此元类定义新类时（如 class MyClass(metaclass=StaticMethodMeta)），元类的 ```__new__``` 方法会在类创建时被调用。

利用元类改变类特性 -> 创建一个成员函数自动转换为静态成员函数的类
```python
class StaticMethodMeta(type):
    def __new__(cls, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                namespace[attr_name] = staticmethod(attr_value)
        return super().__new__(cls, name, bases, namespace)

class tool(metaclass=StaticMethodMeta):
    # 静态成员没有self参数
    def tool1(p1, p2):
        pass
```
