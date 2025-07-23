---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
tags: ["艺"]
categories: ["{{ .Section }}"]
toc: true
showTableOfContents: true
---

{{ .Section }}