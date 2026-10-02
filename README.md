# 歌词/字符图片生成器

从文本文件提取字符或歌词行，生成高清 PNG 图片的工具。支持按行或按字符提取，支持日文/中文/英文，可自定义字体、颜色、大小，最高支持 4x 超清导出。

## 功能特点

- **按行或按字符提取**：支持整行歌词或逐字提取
- **多语言支持**：日文、中文、英文，支持混合提取
- **自定义样式**：字体文件、字号、颜色、内边距
- **高清导出**：支持 1x ~ 4x 倍率导出，最高 4x 超清
- **批量处理**：全选/全不选，批量生成 PNG 图片
- **暗色主题**：护眼暗色界面
- **拖拽支持**：拖拽文本文件到窗口自动识别

## 系统要求

- Windows 10/11（64位）
- 无需安装 Python（使用便携版时）

## 安装

### 方式一：便携版（推荐）

下载 `CharExtractor_Portable.zip`，解压后双击 `CharExtractor.exe` 即可运行。

### 方式二：源码运行

```bash
git clone https://github.com/clehj/CharExtractor.git
cd CharExtractor
pip install -r requirements.txt
python main.py
````

## 依赖字体

本项目需要 **Meiryo** 字体。由于版权原因，字体文件未包含在仓库中，请自行准备。

**Windows 用户：**

1. 打开 `C:\Windows\Fonts\`
2. 复制 `meiryo.ttc` 和 `meiryob.ttc`
3. 粘贴到项目的 `font/` 目录

**其他系统：** 需自行获取该字体文件。

放置完成后，目录结构应为：

```text
CharExtractor/
└── font/
    ├── meiryo.ttc
    └── meiryob.ttc
```

> 缺少字体文件时，程序将无法正常生成图片。

## 使用说明

1. 选择或拖拽文本文件（`.txt`、`.lrc`、`.md` 等）
2. 选择提取模式：按行（歌词）或按字符
3. 选择语言：日文/中文/英文
4. 可选：混合提取、去重
5. 设置字体、颜色、导出倍率
6. 勾选要导出的项目
7. 点击「生成图片」

## 构建

### 打包为独立 EXE

```bash
pip install pyinstaller
pyinstaller --name "CharExtractor" --windowed --icon=icon.ico --add-data "style_config.json;." --hidden-import "PyQt5.sip" main.py
```

## 项目结构

```text
CharExtractor/
├── main.py                # 程序入口
├── build.py               # 打包脚本
├── requirements.txt       # 依赖列表
├── .gitignore
├── README.md
├── core/                  # 核心模块
│   ├── __init__.py
│   ├── extractor.py       # 文本提取器
│   ├── generator.py       # 图片生成器
│   └── constants.py       # 常量定义
├── gui/                   # GUI 模块
│   ├── __init__.py
│   ├── main_window.py     # 主窗口
│   ├── ui_main_window.py  # UI 构建
│   ├── about_dialog.py    # 关于对话框
│   ├── drop_area.py       # 拖拽区域
│   ├── workers.py         # 后台线程
│   └── style.py           # 样式常量
├── utils/
│   └── string_utils.py    # 字符串工具
└── font/                  # 字体目录（需自行放入，见上）
```

## 技术栈

| 模块 | 说明 |
| --- | --- |
| PyQt5 5.15 | GUI 框架 |
| Pillow | 图片生成 |
| PyInstaller 6.x | 打包为独立 EXE |

## License

MIT License © 2024 clehj

