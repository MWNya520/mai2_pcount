# mai2_pcount

## 介绍

wmc的机厅在线人数信息查询、修改插件~

## 功能

使用 mai2_pcount_help 来查看帮助信息喔~

- pcount on: 在本群开启这个插件~不开启的话，下面的指令（除了关闭）都用不了唔~

- pcount off: 在本群关闭这个插件~

- 添加机厅: 使用 `添加机厅 机厅名 机厅代号` 来添加哦~

- 删除机厅: 使用 `删除机厅 机厅代号` 来删除哦~

- [机厅代号]+ - =[数字]: 使用类似于 `mw=6` 的指令来修改机厅人数哦~

- [机厅代号]几: 使用类似于 `mw几` 的指令来查询机厅人数哦~

- 修改地区名 [地区名]: 使用类似于 `修改地区名 wmc聚集地` 的指令来修改地区名哦~

注意注意~！各个群聊的数据都是不一样的，需要自行配置机厅哦~

有问题可以致电Miaowing，我会竭尽全力帮助您解决问题哒！

## 安装

### 使用 NB-CLI 安装

在 Nonebot 根目录执行

```bash
nb plugin install mai2_pcount
```

### 手动安装

1. 将 `mai2_pcount` 文件夹放入你的 Nonebot 插件目录中

2. 在 `bot.py`中写入以下代码：

   ```python
   nonebot.load_plugin("FOLDER-TO-PLUGIN.mai2_pcount")

## 许可

MIT License
