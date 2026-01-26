---
title: "fmt格式化动词表"
date: 2026-01-26T09:56:42+08:00
draft: false
tags: ['code', 'golang', 'AIGC', 'learning']
toc: true
showTableOfContents: true
---

### 通用格式化：

| 动词 | 描述 | 示例 |
|------|------|------|
| `%v` | 值的默认格式 | `fmt.Printf("%v", 42)` → `42` |
| `%#v` | Go语法表示 | `fmt.Printf("%#v", "hello")` → `"hello"` |
| `%T` | 值的类型 | `fmt.Printf("%T", 3.14)` → `float64` |
| `%%` | 字面百分号 | `fmt.Printf("%%")` → `%` |

### 布尔类型：
| 动词 | 描述 | 示例 |
|------|------|------|
| `%t` | true 或 false | `fmt.Printf("%t", true)` → `true` |

### 整数类型：
| 动词 | 描述 | 示例 |
|------|------|------|
| `%b` | 二进制 | `fmt.Printf("%b", 5)` → `101` |
| `%c` | Unicode字符 | `fmt.Printf("%c", 65)` → `A` |
| `%d` | 十进制 | `fmt.Printf("%d", 42)` → `42` |
| `%o` | 八进制 | `fmt.Printf("%o", 8)` → `10` |
| `%O` | 带0o前缀的八进制 | `fmt.Printf("%O", 8)` → `0o10` |
| `%x` | 十六进制（小写） | `fmt.Printf("%x", 255)` → `ff` |
| `%X` | 十六进制（大写） | `fmt.Printf("%X", 255)` → `FF` |
| `%U` | Unicode格式 | `fmt.Printf("%U", 'A')` → `U+0041` |
| `%q` | 单引号字符 | `fmt.Printf("%q", 65)` → `'A'` |

### 浮点数：
| 动词 | 描述 | 示例 |
|------|------|------|
| `%f` | 十进制浮点数 | `fmt.Printf("%f", 3.1415)` → `3.141500` |
| `%e` | 科学计数法（e） | `fmt.Printf("%e", 1000.0)` → `1.000000e+03` |
| `%E` | 科学计数法（E） | `fmt.Printf("%E", 1000.0)` → `1.000000E+03` |
| `%g` | 自动选择 %e 或 %f | `fmt.Printf("%g", 3.1415)` → `3.1415` |
| `%G` | 自动选择 %E 或 %f | `fmt.Printf("%G", 3.1415)` → `3.1415` |

### 字符串和字节切片：
| 动词 | 描述 | 示例 |
|------|------|------|
| `%s` | 普通字符串 | `fmt.Printf("%s", "hello")` → `hello` |
| `%q` | 双引号字符串 | `fmt.Printf("%q", "hello")` → `"hello"` |
| `%x` | 十六进制（小写） | `fmt.Printf("%x", "Go")` → `476f` |
| `%X` | 十六进制（大写） | `fmt.Printf("%X", "Go")` → `476F` |

### 指针：
| 动词 | 描述 | 示例 |
|------|------|------|
| `%p` | 十六进制指针地址 | `fmt.Printf("%p", &x)` → `0xc0000120a0` |

### 宽度和精度控制：

```go
// 宽度：最小字段宽度
fmt.Printf("|%6d|%6d|\n", 123, 45)      // |   123|    45|

// 精度：小数点后位数（浮点数）
fmt.Printf("|%6.2f|%6.2f|\n", 1.2, 3.456) // |  1.20|  3.46|

// 宽度和精度结合
fmt.Printf("|%8s|%8s|\n", "foo", "barbaz") // |     foo|  barbaz|

// 左对齐
fmt.Printf("|%-6d|%-6d|\n", 123, 45)    // |123   |45    |

// 始终显示符号
fmt.Printf("|%+6d|%+6d|\n", 123, -45)   // |  +123|   -45|

// 填充0而不是空格
fmt.Printf("|%06d|%06d|\n", 123, 45)    // |000123|000045|

// 空格占位符
fmt.Printf("|% d|% d|\n", 123, -45)     // | 123|-45|
```

### 复杂示例：

```go
package main

import "fmt"

type Person struct {
    Name string
    Age  int
}

func main() {
    // 结构体格式化
    p := Person{"Alice", 30}
    fmt.Printf("%v\n", p)   // {Alice 30}
    fmt.Printf("%+v\n", p)  // {Name:Alice Age:30}
    fmt.Printf("%#v\n", p)  // main.Person{Name:"Alice", Age:30}
    
    // 切片和数组
    arr := [3]int{1, 2, 3}
    slice := []int{1, 2, 3}
    fmt.Printf("%v\n", arr)    // [1 2 3]
    fmt.Printf("%#v\n", arr)   // [3]int{1, 2, 3}
    fmt.Printf("%#v\n", slice) // []int{1, 2, 3}
    
    // 指针
    x := 42
    ptr := &x
    fmt.Printf("%p\n", ptr)    // 0xc0000120a0
    fmt.Printf("%v\n", ptr)    // 0xc0000120a0
    fmt.Printf("%T\n", ptr)    // *int
    
    // 多种类型混合
    fmt.Printf("Name: %s, Age: %d, Score: %.2f\n", "Bob", 25, 95.5)
    // Name: Bob, Age: 25, Score: 95.50
    
    // 十六进制查看内存
    data := []byte{0x48, 0x65, 0x6c, 0x6c, 0x6f}
    fmt.Printf("% x\n", data)  // 48 65 6c 6c 6f
    fmt.Printf("%X\n", data)   // 48656C6C6F
}
```

### 特殊技巧：

```go
// 1. 索引引用参数（重复使用）
fmt.Printf("%[2]d %[1]d %[2]d\n", 1, 2)  // 2 1 2

// 2. 切片格式化
s := []int{1, 2, 3, 4, 5}
fmt.Printf("%v\n", s)       // [1 2 3 4 5]
fmt.Printf("%#v\n", s)      // []int{1, 2, 3, 4, 5}

// 3. 映射格式化
m := map[string]int{"a": 1, "b": 2}
fmt.Printf("%v\n", m)       // map[a:1 b:2]
fmt.Printf("%#v\n", m)      // map[string]int{"a":1, "b":2}

// 4. 自定义类型的 String() 方法
type MyType int
func (m MyType) String() string {
    return fmt.Sprintf("MyType(%d)", m)
}
var mt MyType = 42
fmt.Printf("%v\n", mt)      // MyType(42)
```

### 常用组合：

```go
// 调试信息常用
fmt.Printf("变量: %#v, 类型: %T, 地址: %p\n", var, var, &var)

// 表格输出
fmt.Printf("|%-10s|%10d|%10.2f|\n", "Alice", 30, 95.5)
fmt.Printf("|%-10s|%10d|%10.2f|\n", "Bob", 25, 88.75)

// 进度条样式
fmt.Printf("\r进度: [%-50s] %d%%", strings.Repeat("=", 25), 50)
```
