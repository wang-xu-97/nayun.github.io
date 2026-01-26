---
title: "类型与interface"
date: 2026-01-26T11:05:26+08:00
draft: false
tags: ["技"]
toc: true
showTableOfContents: true
---


## interface
### 1. 接口%v格式化输出
1. 非空接口：输出的是动态值的 %v 格式化结果
1. 空接口：同样输出动态值的 %v 格式化结果
1. 如果类型实现了 String() 方法：%v 会调用该方法
1. %#v 输出更详细信息：包括类型信息

## 类型
    类型实现接口方法，编译时类型值验证接口定义
### 1. 结构体类型struct
    嵌入特性（Embedding）
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

1. 自定义类型别名
1. 函数类型
1. 基本类型（int, string 等）
1. 接口类型（虽然接口类型本身通常不定义方法）



## 组合、嵌套
```go
// 基础接口
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

// 接口组合
type ReadWriter interface {
    Reader
    Writer
}

type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}

// 组合+额外方法
type BufferedReadWriter interface {
    Reader
    Writer
    Buffered() int
    Peek(n int) ([]byte, error)
}

// 实现组合接口
type BufferedIO struct {
    buffer bytes.Buffer
}

func (bio *BufferedIO) Read(p []byte) (int, error) {
    return bio.buffer.Read(p)
}

func (bio *BufferedIO) Write(p []byte) (int, error) {
    return bio.buffer.Write(p)
}

func (bio *BufferedIO) Buffered() int {
    return bio.buffer.Len()
}

func (bio *BufferedIO) Peek(n int) ([]byte, error) {
    if n > bio.buffer.Len() {
        return nil, io.EOF
    }
    data := bio.buffer.Bytes()
    return data[:n], nil
}
```
## 技巧
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