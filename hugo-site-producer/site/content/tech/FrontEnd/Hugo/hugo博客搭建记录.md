---
title: "Hugo博客搭建记录"
date: 2025-07-08T10:18:41+08:00
draft: false
tags: ["技", 'hugo', '前端', 'learning']
showTableOfContents: true
toc: true
# showWordCount: false
---

## 环境准备
1. 设备：ubuntu
2. github地址：[https://github.com/gohugoio/hugo](https://github.com/gohugoio/hugo)
3. 安装：
```shell linenums="1"
wget https://github.com/gohugoio/hugo/releases/download/v0.147.9/hugo_extended_0.147.9_Linux-64bit.tar.gz
tar -xvzf hugo_extended_0.147.9_Linux-64bit.tar.gz
sudo su
mv hugo /usr/bin
```
## Start!
### 1. 基础
#### 1. 创建新博客
```shell
hugo new site siteproducer
```
#### 2. 重要配置&配置逻辑链

### 2. 使用stack主题
```shell
git submodule add https://github.com/CaiJimmy/hugo-theme-stack themes/hugo-theme-stack
```


## Hugo Tricks
### 1. 自定义样式
#### 1. 样式覆盖规则：后引入覆盖前引入
1. params.yaml配置中指定自定义custom_css
```yaml
custom_css: ["scss/custom.scss"]
```
2. assets/custom.scss中
```scss
// 引入主题样式
@import "general";
// 引入你的自定义覆盖
@import "custom-markdown"; // 无下划线、无扩展名
```
#### 2. 自定义鸿蒙字体
1. 下载[鸿蒙字体](https://github.com/Irithys/cdn/tree/master/src/fonts?ref=irithys.com)
2. 解压到siteproducer/assets/fonts目录
3. 在assets/scss/中创建_fonts.scss，并在scss/custom.scss中引用

font.scss
```scss
@font-face {
    font-family: 'HarmonyOS_Sans_SC_Medium';
    font-style: normal;
    font-display: swap;
    src: url('{{ (resources.Get "fonts/HarmonyOS_Sans_SC_Medium.woff2").RelPermalink }}') format('woff2');
}
@font-face {
  font-family: 'JetBrainsMono Regular';
  font-style: normal;
  font-display: swap;
  src: url('{{ (resources.Get "fonts/JetBrainsMono-Regular.woff2").RelPermalink }}') format('woff2');
}

:root {
  --font-sans: 'HarmonyOS_Sans_SC_Medium', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrainsMono Regular', monospace;
}
body {
  font-family: var(--font-sans);
  line-height: 1.6;
  color: #333;
}

code, pre {
  font-family: var(--font-mono);
}

```
custom.scss
```scss
@import "fonts";
```
#### 3. blowfish theme 打开默认文档大纲
1. md Front Matter中设置对应toc变量，不同主题可能使用不同Front Matter变量
```yaml
# bluefish 使用showTableOfContents
showTableOfContents: true
# 默认使用toc
toc: true
```
2. params.yaml中设置
```yaml
smartTOC: true
```
### 2. 分级目录
1. 主题默认支持分级目录，但子目录不一定有独立样式，需要每一层子目录中创建
_index.md
```markdown
---
title: "title"
description: "desc"
---
```
2. 使用deepseek自定义list.html覆盖主题提供的样式

## todo
1. ~~分级目录、tag云图~~
1. ~~markdown代码块左上角显示代码语言，右上角复制按钮~~
1. ~~文档大纲-done~~
1. 文档字数正确记数
1. ~~markdown 代码块渲染~~
1. 文章标签
1. markdown代码块功能优化
    1. 取消单独折叠按钮
    1. </> 区 
        - 增加折叠功能
        - 增加悬浮伸缩动画效果
    1. 代码语言（hint）中文独立样式，支持markdown渲染
    1. 自动换行按钮
1. tag筛选搜索器