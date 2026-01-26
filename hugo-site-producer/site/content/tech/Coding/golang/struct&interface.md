---
title: "struct&interface"
date: 2026-01-26T11:05:26+08:00
draft: false
tags: ["技"]
toc: true
showTableOfContents: true
---

## struct
1. 嵌入特性（Embedding）
```go
type Animal struct {
    Name string
}
type Dog struct {
    Animal // 嵌入结构体（组合而非继承）
}
func main() {
    // 创建 Dog 实例
    dog := Dog{
        Animal: Animal{Name: "Buddy"},
    }
    
    // 访问方式1：通过嵌入类型访问
    fmt.Println(dog.Animal.Name)  // "Buddy"
    
    // 访问方式2：直接访问（提升字段）
    fmt.Println(dog.Name)         // "Buddy"
    
    // 也可以直接设置
    dog.Name = "Max"
    fmt.Println(dog.Name)         // "Max"
}
```


## interface
### 1. 接口%v格式化输出
1. 非空接口：输出的是动态值的 %v 格式化结果
1. 空接口：同样输出动态值的 %v 格式化结果
1. 如果类型实现了 String() 方法：%v 会调用该方法
1. %#v 输出更详细信息：包括类型信息


## 相关技巧
1. 创建存储不同值类型的map
```go
// 1. 用空接口
var data1 map[string]any
var data2 map[string]interface{}

// 2. 已知接口，使用结构体
type Config struct {
    Name string   `json:"name"`
    Age  int      `json:"age"`
    Tags []string `json:"tags"`
}

```