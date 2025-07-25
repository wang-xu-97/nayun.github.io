---
title: "Hugo理解"
date: 2025-07-09T14:07:34+08:00
draft: false
tags: ["技", 'hugo']
categories: ["tech"]
toc: true
showTableOfContents: true
showAuthor: false
showReadingTime: false
showCategoryOnly: true
---

## hugo工作流程
1. 导入主题后，完成[自定义配置和资源](#自定义配置和资源)
```markdown
- config yaml/toml/json
- assets
    - css
    - js
    - images
- layouts
  - 404.html : 404错误页面模板
  - _default/ : 默认模板
    - baseof.html : 基础模板框架
    - list.html : 列表页模板（如分类、标签页）
    - single.html : 单内容页模板（如文章页）
    - terms.html : 分类列表模板（如所有标签的列表）
  - partials/ : 可重用部分模板
    - header.html : 页头部分
    - footer.html : 页脚部分
    - head.html : <head>部分
    - ... : 其他部分模板
  - shortcodes/ : 短代码模板
    - figure.html : 图片短代码
    - ... : 其他短代码
  - index.html : 首页模板
  - section/ : 分区模板（如博客、文档等）
    - blog.html : 博客分区模板
    - ... : 其他分区模板
  - taxonomy/ : 分类法模板
    - category.html : 分类页面模板
    - tag.html : 标签页面模板
  - ... : 其他自定义模板
```
所有layouts模板均可
1. 通过 {{ define "blockname" }} 和 {{ block }} 继承主题逻辑
限制：需要原模板使用{{ block "blockname" . }}定义了对应block，才能继承这个block，并添加自定义逻辑
```html
{{ define "blockname" }}

    <!-- 你的自定义内容 -->
    <div>...</div>
{{ end }}
```
2. 直接复制主题的模板文件到自定义html中更改






## 自定义配置和资源
### config/_default 中的 yaml/toml/json格式基础全局配置
1. 所有配置文件可以随意增加用户自定义参数，但不同的文件中可能有不同的预定义参数
1. 一般分为
- config.yaml
config配置一般是hugo原生预定义参数
```yaml
# 部署网页url，如部署在Github pages上，需要改为github page的url，本地开发时无影响
baseURL: "http://example.org"
# 网站title
title: "nayun blog"
# 网站默认语言，影响本地化设置
languageCode: "zh-cn"
# 文档（内容文件）默认语言
defaultContentLanguage: "zh-cn"
# 主题
theme: "blowfish"
# markup也即markdown 相关设置
# 参考https://hugo.opendocs.io/getting-started/%E9%85%8D%E7%BD%AE%E6%A0%87%E8%AE%B0%E8%AF%AD%E8%A8%80/
markup: 
  goldmark:
    renderer:
      hardWraps: True       # markup.goldmark.renderer.hardWraps 硬换行，md文档中强制单个回车换行（默认回车不会换行，而是双空格换行）

```
- menu.yaml
导航栏目录，原生预定义参数，但不同主题可能有不同的主题预定义参数，以实现不同的效果，比如icon
```yaml
main:
  - identifier: "tech"
    name: "技"
    url: "/tech/"
    weight: 2
```
- params.yaml
完全由主题预定义参数构成

## Blowfish调用链
{{< mermaid title="系统架构" >}}
graph LR
A[baseof.html] --> B[head.html]
A --> C[header.html]
A --> D[main content]
A --> E[footer.html]

B --> F[CSS 资源]
B --> G[预加载资源]
C --> H[导航栏部分]
E --> I[JS 资源]

F --> F1[main.min.css]
F --> F2[syntax.min.css]
F --> F3[第三方字体]

G --> G1[preload 字体]
G --> G2[preload 图标]

I --> I1[theme.min.js]
I --> I2[第三方 JS]
I1 --> I1a[暗黑模式切换]
I1 --> I1b[移动端菜单]
I2 --> I2a[Alpine.js]
I2 --> I2b[HTMX]
{{< /mermaid >}}