---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
tags: ["技"]
categories: ["{{ .Section }}"]
toc: true
---

{{ .Section }}