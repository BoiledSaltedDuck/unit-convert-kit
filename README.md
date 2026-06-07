# unit-convert-kit 单位换算工具

[![PyPI version](https://img.shields.io/pypi/v/unit-convert-kit)](https://pypi.org/project/unit-convert-kit/)
[![Downloads](https://img.shields.io/pypi/dm/unit-convert-kit)](https://pypi.org/project/unit-convert-kit/)
[![License](https://img.shields.io/pypi/l/unit-convert-kit)](https://github.com/BoiledSaltedDuck/unit-convert-kit/blob/main/LICENSE)

> **Office Tools Kit 系列** — 用AI写代码，用工具提效。一行命令搞定日常办公与开发杂务。

## 安装

```bash
pip install unit-convert-kit
```

## 用法

```bash
# 长度换算
unit-convert 100 cm m

# 温度换算
unit-convert 32 f c

# 重量换算
unit-convert 1.5 kg lb

# 数据大小换算
unit-convert 1024 mb gb

# 列出所有支持的单位
unit-convert list

# 批量替换文件中的单位
unit-convert batch data.txt inch cm
```

## 支持的类别

| 类别 | 示例单位 |
|------|----------|
| 长度 | mm, cm, m, km, inch, ft, yard, mile, 里, 丈, 尺, 寸 |
| 重量 | mg, g, kg, t, oz, lb, 斤, 两, carat |
| 温度 | c (摄氏度), f (华氏度), k (开尔文) |
| 面积 | m², km², ha, acre, 亩, sqft |
| 体积 | ml, l, m³, gal, qt, pt, cup |
| 数据大小 | b, kb, mb, gb, tb, kib, mib, gib |

## 特点

- 支持6大类100+种单位
- 支持中文单位（里、丈、尺、寸、斤、两）
- 温度自动转换公式
- 批量文件替换功能
- 纯 Python，零依赖

## 🧰 Office Tools Kit 系列工具

本工具属于 **Office Tools Kit 系列**，同类工具推荐：

| 工具 | 功能 | 安装 |
|------|------|------|
| [office-tools-kit](https://pypi.org/project/office-tools-kit/) | Excel合并拆分、PDF合并 | `pip install office-tools-kit` |
| [file-org-kit](https://pypi.org/project/file-org-kit/) | 文件智能分类整理 | `pip install file-org-kit` |
| [img-convert-kit](https://pypi.org/project/img-convert-kit/) | 图片格式批量转换 | `pip install img-convert-kit` |
| [img-resize-kit](https://pypi.org/project/img-resize-kit/) | 图片批量缩放与压缩 | `pip install img-resize-kit` |
| [json-tool-kit](https://pypi.org/project/json-tool-kit/) | JSON 文件处理 | `pip install json-tool-kit` |
| [markdown-kit](https://pypi.org/project/markdown-kit/) | Markdown 文档辅助 | `pip install markdown-kit` |
| [qr-code-kit](https://pypi.org/project/qr-code-kit/) | 二维码生成与解析 | `pip install qr-code-kit` |
| [text-clean-kit](https://pypi.org/project/text-clean-kit/) | 文本文件清洗处理 | `pip install text-clean-kit` |
| [unit-convert-kit](https://pypi.org/project/unit-convert-kit/) | 单位换算 | `pip install unit-convert-kit` |

> 📚 更多工具请访问 [BoiledSaltedDuck 工具主页](https://boiledsaltedduck.github.io/)

## 支持

如果 unit-convert-kit 帮到了您，欢迎打赏支持：

```
USDT (TRC20): TMPQygMkv42QPeyYnkxMkPwsqs7udbD2Aa
```

您的支持是开源项目持续发展的动力 ❤️
