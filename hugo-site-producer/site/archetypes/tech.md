---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
tags: ["技"]
toc: true
showTableOfContents: true
---

{{ .Section }}