---
name: datetime
description: 当用户询问当前日期或时间时使用此技能。重要：回答前必须先调用 read_file 读取本技能的 SKILL.md 文件，然后按照其中的指示执行。
allowed-tools: execute read_file
---

# datetime

## 说明
当用户询问当前日期或时间时，使用 execute 工具运行技能目录下的脚本：
将输出结果用中文报告给用户。

## 脚本
`scripts/` 目录包含辅助脚本：
- `scripts/get_datetime.py` - 得到当前时间

