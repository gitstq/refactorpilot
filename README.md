# RefactorPilot - 轻量级终端代码智能重构助手

## 项目定位
RefactorPilot 是一款零依赖的轻量级终端代码智能重构助手，专注于帮助开发者快速识别代码中的坏味道、自动建议重构方案、并生成可应用的重构补丁。

## 核心差异化亮点
1. **零依赖设计** - 纯Python标准库实现，无需安装额外依赖
2. **智能坏味道检测** - 基于AST分析识别15+种常见代码坏味道
3. **重构建议生成** - 自动生成重构方案与代码补丁
4. **TUI交互界面** - 内置终端用户界面，支持交互式重构
5. **多语言支持** - 支持Python、JavaScript、TypeScript代码分析

## 核心功能清单
- [ ] AST-based代码结构分析
- [ ] 15+代码坏味道检测规则
- [ ] 智能重构建议生成
- [ ] 重构补丁生成与应用
- [ ] TUI交互式重构界面
- [ ] 重构历史记录
- [ ] 批量重构支持
- [ ] 重构影响分析

## 技术架构
- 纯Python 3.8+标准库
- AST模块进行代码解析
- curses/textwrap实现TUI
- difflib生成代码补丁

## 项目结构
```
refactorpilot/
├── refactorpilot/
│   ├── __init__.py
│   ├── __main__.py
│   ├── analyzer.py      # AST分析器
│   ├── detectors.py     # 坏味道检测器
│   ├── suggesters.py    # 重构建议生成器
│   ├── refactor.py      # 重构引擎
│   ├── tui.py           # TUI界面
│   ├── cli.py           # CLI入口
│   └── utils.py         # 工具函数
├── tests/
├── docs/
├── README.md
├── README.zh-TW.md
├── README.en.md
└── LICENSE
```
