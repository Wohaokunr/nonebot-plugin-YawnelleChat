<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

## ✨ nonebot-plugin-YawnelleChat ✨

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Wohaokunr/nonebot-plugin-YawnelleChat.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-YawnelleChat">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-YawnelleChat.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="ruff">
</a>
<a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
</a>
</div>

> [!IMPORTANT]
> **收藏项目** ～⭐️

<img width="100%" src="https://starify.komoridevs.icu/api/starify?owner=Wohaokunr&repo=nonebot-plugin-YawnelleChat" alt="starify" />


## 📖 介绍

<img src="https://raw.githubusercontent.com/Wohaokunr/nonebot-plugin-YawnelleChat/refs/heads/master/file_000000003a7061f7baf3123399fefa73.png" />

NoneBot2 插件 YawnelleChat 是一个基于 OpenAI API 的智能群聊助手插件。它能够：

- 🤖 提供智能群聊对话功能
- 💬 自动维护对话历史记录
- 🎯 支持自定义系统提示词
- ⚡ 支持自定义 API 接口
- 💾 历史记录持久化保存
- 🔧 支持群级别模型和提示词配置
- ⏰ 定时向群聊推送提醒

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-YawnelleChat --upgrade
使用 **pypi** 源安装

    nb plugin install nonebot-plugin-YawnelleChat --upgrade -i "https://pypi.org/simple"
使用**清华源**安装

    nb plugin install nonebot-plugin-YawnelleChat --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple"


</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details open>
<summary>uv</summary>

    uv add nonebot-plugin-YawnelleChat
安装仓库 master 分支

    uv add git+https://github.com/Wohaokunr/nonebot-plugin-YawnelleChat@master
</details>

<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-YawnelleChat
安装仓库 master 分支

    pdm add git+https://github.com/Wohaokunr/nonebot-plugin-YawnelleChat@master
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-YawnelleChat
安装仓库 master 分支

    poetry add git+https://github.com/Wohaokunr/nonebot-plugin-YawnelleChat@master
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_YawnelleChat"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
| :-----: | :---: | :----: | :------: |
| openai_api_key | 是 | none | OpenAI API密钥 |
| openai_api_base | 否 | https://dashscope.aliyuncs.com/compatible-mode/v1 | OpenAI API基础URL |
| openai_model | 否 | qwen2.5-vl-32b-instruct | OpenAI模型名称 |
| system_prompt | 否 | 预设的系统提示词 | AI系统提示词 |
| max_history_length | 否 | 3 | 群聊历史消息最大保存数量 |
| history_file | 否 | chat_history.json | 历史记录文件路径 |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
| :---: | :---: | :---: | :---: | :------: |
| /chat [消息] | 群员 | 否 | 群聊 | 与AI助手对话 |
| @机器人 [消息] | 群员 | 是 | 群聊 | 与AI助手对话 |
| /chat_config <model|prompt> <值> | 群管理员 | 否 | 群聊 | 设置群模型或提示词 |

### 🎨 效果图
如果有效果图的话
