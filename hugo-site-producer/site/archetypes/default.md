---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
tags: ["{{ .Section }}"]
categories: ["{{ .Section }}"]
toc: true
showTableOfContents: true
---

