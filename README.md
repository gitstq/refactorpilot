<div align="center">

# 🔧 RefactorPilot

**轻量级终端代码智能重构助手**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-yellow.svg)]()

[English](./README.en.md) | [繁體中文](./README.zh-TW.md)

</div>

---

## 🎉 项目介绍

RefactorPilot 是一款**零依赖**的轻量级终端代码智能重构助手，专为追求代码质量的开发者打造。它基于AST（抽象语法树）分析技术，能够智能识别代码中的"坏味道"，提供专业的重构建议，甚至自动生成可应用的重构补丁。

### 💡 灵感来源

在日常开发中，我们常常会遇到这样的问题：
- 函数越写越长，难以维护
- 代码复杂度越来越高，测试困难
- 魔法数字满天飞，可读性差
- 想重构但不知道从何下手

RefactorPilot 就是为了解决这些问题而生。它像一位经验丰富的代码审查员，时刻陪伴在你身边，帮你发现代码中的问题并提供改进方案。

### ✨ 核心差异化亮点

1. **🚀 零依赖设计** - 纯Python标准库实现，无需安装任何第三方依赖
2. **🎯 智能坏味道检测** - 基于AST分析识别10+种常见代码坏味道
3. **💡 重构建议生成** - 自动生成重构方案与代码补丁
4. **🖥️ TUI交互界面** - 内置终端用户界面，支持交互式重构
5. **🔍 多维度分析** - 圈复杂度、代码行数、函数参数等全方位分析

---

## ✨ 核心特性

### 🔍 代码坏味道检测
- **过长函数** - 检测超过阈值的函数，建议拆分
- **高复杂度** - 基于圈复杂度识别难以测试的代码
- **参数过多** - 发现参数过多的函数，建议封装为对象
- **魔法数字** - 识别未命名的常量，建议提取为命名常量
- **未使用变量** - 发现无用的变量赋值
- **代码行过长** - 检测超出推荐长度的代码行
- **嵌套过深** - 识别深层嵌套的代码块
- **上帝类** - 发现职责过多的大型类
- **基本类型偏执** - 检测应封装为对象的原始类型组合

### 🔧 智能重构建议
- 基于检测到的坏味道生成具体的重构方案
- 提供重构前后的代码对比
- 评估重构的工作量和风险等级
- 识别快速改进项（低工作量、低风险）

### 🖥️ 终端交互界面
- 美观的TUI界面，支持交互式操作
- 彩色输出，信息层次清晰
- 支持文件和项目级别的批量分析
- 实时预览重构效果

### 📊 项目级分析
- 扫描整个项目的代码质量
- 生成项目健康度报告
- 识别高风险文件和函数
- 支持多种代码文件格式

---

## 🚀 快速开始

### 环境要求
- **Python**: 3.8 或更高版本
- **操作系统**: Linux / macOS / Windows

### 安装方式

#### 方式一：直接安装
```bash
# 克隆仓库
git clone https://github.com/gitstq/refactorpilot.git
cd refactorpilot

# 安装
pip install -e .
```

#### 方式二：直接使用
```bash
# 无需安装，直接运行
python -m refactorpilot --help
```

### 快速使用

#### 分析单个文件
```bash
refactorpilot analyze your_code.py
```

#### 分析整个项目
```bash
refactorpilot analyze -p ./your_project
```

#### 启动交互式界面
```bash
refactorpilot tui
```

#### 生成重构建议
```bash
refactorpilot suggest your_code.py
```

---

## 📖 详细使用指南

### 命令行接口

#### `analyze` - 分析代码
```bash
# 分析单个文件
refactorpilot analyze file.py

# 分析项目
refactorpilot analyze -p ./project

# 输出JSON格式
refactorpilot analyze file.py -f json

# 只显示高严重级别问题
refactorpilot analyze file.py --severity high
```

#### `refactor` - 重构代码
```bash
# 预览重构（不实际修改）
refactorpilot refactor file.py -d

# 应用重构
refactorpilot refactor file.py --apply

# 批量重构项目
refactorpilot refactor -p ./project --apply
```

#### `suggest` - 生成建议
```bash
refactorpilot suggest file.py
```

#### `tui` - 交互式界面
```bash
refactorpilot tui
```

### 配置选项

可以通过环境变量或配置文件自定义检测阈值：

```python
# 自定义阈值
detector = SmellDetector(thresholds={
    'max_function_lines': 30,      # 函数最大行数
    'max_complexity': 8,           # 最大圈复杂度
    'max_arguments': 4,            # 最大参数数量
    'max_line_length': 80,         # 最大行长度
    'max_nesting_depth': 3,        # 最大嵌套深度
    'max_class_methods': 15,       # 类最大方法数
})
```

---

## 💡 设计思路与迭代规划

### 设计理念
RefactorPilot 遵循以下设计原则：

1. **简单至上** - 零依赖，开箱即用
2. **实用为先** - 专注于最常见的代码质量问题
3. **渐进式重构** - 支持从小处着手，逐步改进
4. **开发者友好** - 清晰的输出，可操作的反馈

### 技术选型
- **AST分析** - 使用Python标准库`ast`模块，准确解析代码结构
- **零依赖** - 仅使用Python标准库，确保兼容性和轻量性
- **TUI界面** - 使用`curses`实现跨平台的终端界面
- **模块化设计** - 分析器、检测器、建议器分离，易于扩展

### 后续功能迭代计划

#### v1.1.0 (计划中)
- [ ] 支持JavaScript/TypeScript代码分析
- [ ] 添加更多重构模式（如提取变量、内联变量等）
- [ ] 配置文件支持（YAML/JSON格式）
- [ ] 忽略规则配置（注释标记跳过检测）

#### v1.2.0 (计划中)
- [ ] 重构历史记录与回滚功能
- [ ] 与Git集成，支持提交前检查
- [ ] HTML报告生成
- [ ] 持续集成插件（GitHub Actions等）

#### v2.0.0 (规划中)
- [ ] 基于AI的智能重构建议
- [ ] 代码相似度检测（重复代码识别）
- [ ] 架构层面的坏味道检测
- [ ] 团队协作功能（规则共享）

### 社区贡献方向
我们欢迎以下方面的贡献：
- 🐛 Bug修复
- ✨ 新的坏味道检测规则
- 🌍 多语言支持
- 📚 文档改进
- 🎨 UI/UX优化

---

## 📦 打包与部署指南

### 本地开发
```bash
# 克隆仓库
git clone https://github.com/gitstq/refactorpilot.git
cd refactorpilot

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或: venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e .

# 运行测试
python -m unittest discover tests/
```

### 构建发布包
```bash
# 安装构建工具
pip install build twine

# 构建
python -m build

# 上传到PyPI
python -m twine upload dist/*
```

### 跨平台兼容性
- ✅ Linux - 完全支持
- ✅ macOS - 完全支持
- ✅ Windows - 完全支持（TUI功能需Windows 10+）

---

## 🤝 贡献指南

### 提交PR
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 提交规范
我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：
- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### 报告问题
请使用 [GitHub Issues](https://github.com/gitstq/refactorpilot/issues) 报告问题，并包含：
- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息（Python版本、操作系统）

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

```
MIT License

Copyright (c) 2025 RefactorPilot Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 致谢

感谢以下开源项目和资源：
- [Python AST](https://docs.python.org/3/library/ast.html) - 代码分析基础
- [Refactoring Guru](https://refactoring.guru/) - 重构模式参考
- [Code Smells](https://sourcemaking.com/refactoring/smells) - 代码坏味道定义

---

<div align="center">

**Made with ❤️ by RefactorPilot Team**

如果这个项目对你有帮助，请给我们一个 ⭐ Star！

</div>
