---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
tags: ["生活"]
categories: ["{{ .Section }}"]
toc: true
showTableOfContents: true
---

{{ .Section }}