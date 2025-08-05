---
title: "LearnHugo250804"
date: 2025-08-04T17:11:01+08:00
draft: false
tags: ["技", 'hugo', '前端']
toc: true
showTableOfContents: true
---

## 设置code-header.language-label点击折叠
1. 设置悬停spacing扩展效果
```css
.language-brackets {
    /* 全属性切换过渡动画效果 */
    transition: all 0.3s ease; 
}
/* 悬停间距扩展，颜色高亮 */
.language-label:hover .language-brackets {
    letter-spacing: 3px;
    color: var(--code-header-hover-color);
}
.language-label:hover .language-name {
    color: var(--code-header-hover-color);
}
```
2. js设置点击label切换chroma.collapsed
```javascript
    document.querySelectorAll('.language-label').forEach(button => {
      button.addEventListener('click', () => {
        const codeBlock = button.closest('.code-block-wrapper');
        const chroma = codeBlock?.querySelector('pre.chroma');
        if (chroma) {
          chroma.classList.toggle('collapsed');
        }
        else console.error('chroma折叠失败');
      });
    });
```
3. 设置pre.chroma.collapsed折叠样式
```css
pre.chroma.collapsed{
  /* 折叠方法：设置高度为0 */
  max-height: 0 !important;
  /* 去除溢出拖动条 */
  overflow: hidden !important;
  /* 去除顽固padding */
  padding: 0 !important;
}
```
