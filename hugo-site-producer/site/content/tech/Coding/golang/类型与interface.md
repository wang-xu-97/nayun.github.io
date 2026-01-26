---
title: "类型与interface"
date: 2026-01-26T11:05:26+08:00
draft: false
tags: ['code', 'golang', 'learning']
toc: true
showTableOfContents: true
---

类型拥有方法，接口声明方法(签名)

## interface
### 1. 接口%v格式化输出
1. 非空接口：输出的是动态值的 %v 格式化结果
1. 空接口：同样输出动态值的 %v 格式化结果
1. 如果类型实现了 String() 方法：%v 会调用该方法
1. %#v 输出更详细信息：包括类型信息

### 2. 组合、嵌套
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

### 2. 函数类型
```go
// 函数类型实现接口
type Handler func(http.ResponseWriter, *http.Request)

func (h Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    h(w, r)
}

// 使用
func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello!")
}

func main() {
    http.Handle("/hello", Handler(helloHandler))
}
```
### 3. 基本类型（int, string 等）
```go
// 为基本类型定义新类型
type Celsius float64
type Fahrenheit float64

// 为 Celsius 定义方法
func (c Celsius) String() string {
    return fmt.Sprintf("%.1f°C", c)
}

// 为 Fahrenheit 定义方法
func (f Fahrenheit) ToCelsius() Celsius {
    return Celsius((f - 32) * 5 / 9)
}

// 使用
var temp Celsius = 37.5
fmt.Println(temp.String())  // 37.5°C
```

### 4. 切片类型
```go
// 为切片定义类型
type IntSlice []int

// 为切片类型定义方法
func (s IntSlice) Sum() int {
    total := 0
    for _, v := range s {
        total += v
    }
    return total
}

// 使用
nums := IntSlice{1, 2, 3, 4}
fmt.Println(nums.Sum())  // 10
```
### 5. 映射类型(map)
```go
// 为映射定义类型
type StringMap map[string]string

// 为映射类型定义方法
func (m StringMap) Keys() []string {
    keys := make([]string, 0, len(m))
    for k := range m {
        keys.append(k)
    }
    return keys
}

// 使用
m := StringMap{"a": "apple", "b": "banana"}
fmt.Println(m.Keys())  // [a b]
```
### 6. 通道类型
```go
// 为通道定义类型
type ResultChan chan Result

// 为通道类型定义方法
func (ch ResultChan) SafeClose() {
    defer func() {
        if recover() != nil {
            fmt.Println("Channel already closed")
        }
    }()
    close(ch)
}
```
### 7. 数组类型
```go
// 为数组定义类型
type Matrix3x3 [3][3]float64

// 为数组类型定义方法
func (m Matrix3x3) Determinant() float64 {
    // 计算 3x3 矩阵的行列式
    return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) -
           m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) +
           m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
}
```
### 8. 接口类型 (不常见，但可以)
```go
// 为接口类型本身定义方法（罕见用法）
type Shape interface {
    Area() float64
}

// 为 Shape 接口类型定义方法
func (s Shape) Describe() string {
    return "This is a shape"
}
// 注意：这很少见，因为接口通常是其他类型实现的
```
### 9. 指针类型 (特例)
```go
// 为指针类型本身定义方法（不是常见的指针接收者）
type IntPointer *int

// 这是允许的，但不常用
func (ip IntPointer) Address() uintptr {
    return uintptr(unsafe.Pointer(ip))
}
```
### 10. 自定义类型别名 (任意类型的别名)
```go
// 任意类型的别名都可以定义方法
type UserID string
type Money decimal.Decimal
type Timestamp time.Time

// 为这些别名定义方法
func (uid UserID) IsValid() bool {
    return len(uid) > 0 && uid[0] != '#'
}

func (m Money) Format() string {
    return fmt.Sprintf("$%.2f", m)
}

func (t Timestamp) ISOString() string {
    return time.Time(t).Format(time.RFC3339)
}
```
