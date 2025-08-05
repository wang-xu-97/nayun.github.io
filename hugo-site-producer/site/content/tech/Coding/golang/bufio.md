---
title: "Bufio"
date: 2025-07-29T17:43:19+08:00
draft: false
tags: ["技", 'code', 'golang', 'learning']
toc: true
showTableOfContents: true
---

# bufio 包详解

`bufio` 是 Go 标准库中的一个包，提供了带缓冲的 I/O 操作功能。它可以包装现有的 `io.Reader` 和 `io.Writer` 对象，创建具有缓冲功能的对象，从而提高 I/O 操作的效率。

## 核心概念

### 缓冲 I/O 的优势

1. **减少系统调用**：通过缓冲数据，减少实际的 I/O 操作次数
2. **提高性能**：特别是对于小数据量的频繁读写操作
3. **提供更方便的接口**：如按行读取等功能

## 主要类型和方法

### 1. Reader

`bufio.Reader` 为读取操作提供缓冲。

```go
func NewReader(rd io.Reader) *Reader
func NewReaderSize(rd io.Reader, size int) *Reader
```

常用方法：

- `Read(p []byte) (n int, err error)` - 读取数据到 p
- `ReadByte() (byte, error)` - 读取一个字节
- `ReadBytes(delim byte) ([]byte, error)` - 读取直到遇到 delim
- `ReadLine() (line []byte, isPrefix bool, err error)` - 读取一行
- `ReadString(delim byte) (string, error)` - 读取字符串直到 delim
- `Peek(n int) ([]byte, error)` - 预览前 n 个字节但不移动读取位置
- `Reset(r io.Reader)` - 重置 Reader 以读取新的输入源

### 2. Writer

`bufio.Writer` 为写入操作提供缓冲。

```go
func NewWriter(w io.Writer) *Writer
func NewWriterSize(w io.Writer, size int) *Writer
```

常用方法：

- `Write(p []byte) (nn int, err error)` - 写入 p
- `WriteByte(c byte) error` - 写入一个字节
- `WriteRune(r rune) (size int, err error)` - 写入一个 rune
- `WriteString(s string) (int, error)` - 写入字符串
- `Flush() error` - 刷新缓冲区，确保所有数据已写入底层 Writer
- `Available() int` - 返回缓冲区中未使用的字节数
- `Buffered() int` - 返回已缓冲但未写入的字节数
- `Reset(w io.Writer)` - 重置 Writer 以写入新的目标

### 3. Scanner

`bufio.Scanner` 提供了更方便的逐行或按分隔符读取的接口。

```go
func NewScanner(r io.Reader) *Scanner
```

常用方法：

- `Scan() bool` - 扫描下一个 token
- `Text() string` - 返回扫描到的文本
- `Bytes() []byte` - 返回扫描到的字节
- `Split(split SplitFunc)` - 设置分割函数

预定义的分割函数：

- `ScanLines` - 按行分割（默认）
- `ScanWords` - 按单词分割
- `ScanRunes` - 按 rune 分割
- `ScanBytes` - 按字节分割

## 使用示例

### Reader 示例

```go
package main

import (
	"bufio"
	"fmt"
	"strings"
)

func main() {
	s := strings.NewReader("Hello\nWorld\nGoodbye")
	reader := bufio.NewReader(s)
	
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			break
		}
		fmt.Print(line)
	}
}
```

### Writer 示例

```go
package main

import (
	"bufio"
	"os"
)

func main() {
	file, _ := os.Create("output.txt")
	defer file.Close()
	
	writer := bufio.NewWriter(file)
	writer.WriteString("Hello, ")
	writer.WriteString("World!\n")
	writer.Flush() // 必须调用 Flush 确保数据写入文件
}
```

### Scanner 示例

```go
package main

import (
	"bufio"
	"fmt"
	"strings"
)

func main() {
	s := strings.NewReader("Hello World\nGoodbye Moon")
	scanner := bufio.NewScanner(s)
	
	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
	
	if err := scanner.Err(); err != nil {
		fmt.Println("Error:", err)
	}
}
```

## 性能考虑

1. **缓冲区大小**：默认缓冲区大小是 4096 字节，对于特定场景可以调整
2. **及时 Flush**：写入操作后记得调用 Flush，或使用 `defer writer.Flush()`
3. **错误处理**：注意检查 Peek 和 Read 等操作的错误
4. **重用对象**：可以使用 Reset 方法重用 Reader/Writer 以减少分配

## 常见使用场景

1. 逐行读取文件
2. 高效写入大量小数据
3. 网络通信中的缓冲读写
4. 解析文本数据
5. 实现自定义的协议解析

`bufio` 包是 Go 中处理 I/O 操作的重要工具，合理使用可以显著提高程序性能。