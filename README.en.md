<div align="center">

# 🔧 RefactorPilot

**Lightweight Terminal Code Intelligent Refactoring Assistant**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-yellow.svg)]()

[简体中文](./README.md) | [繁體中文](./README.zh-TW.md)

</div>

---

## 🎉 Introduction

RefactorPilot is a **zero-dependency** lightweight terminal code intelligent refactoring assistant, designed for developers who pursue code quality. Based on AST (Abstract Syntax Tree) analysis technology, it can intelligently identify "code smells" in your code, provide professional refactoring suggestions, and even automatically generate applicable refactoring patches.

### 💡 Inspiration

In daily development, we often encounter these problems:
- Functions get longer and longer, becoming difficult to maintain
- Code complexity keeps increasing, making testing difficult
- Magic numbers everywhere, reducing readability
- Want to refactor but don't know where to start

RefactorPilot was born to solve these problems. It acts like an experienced code reviewer, always by your side, helping you discover issues in your code and providing improvement solutions.

### ✨ Key Differentiators

1. **🚀 Zero Dependencies** - Pure Python standard library implementation, no third-party dependencies required
2. **🎯 Intelligent Smell Detection** - AST-based analysis identifies 10+ common code smells
3. **💡 Refactoring Suggestions** - Automatically generates refactoring solutions and code patches
4. **🖥️ TUI Interface** - Built-in terminal user interface with interactive refactoring support
5. **🔍 Multi-dimensional Analysis** - Comprehensive analysis including cyclomatic complexity, line count, function parameters, etc.

---

## ✨ Core Features

### 🔍 Code Smell Detection
- **Long Functions** - Detect functions exceeding thresholds and suggest splitting
- **High Complexity** - Identify hard-to-test code based on cyclomatic complexity
- **Too Many Arguments** - Find functions with excessive parameters, suggest encapsulation
- **Magic Numbers** - Identify unnamed constants, suggest extraction as named constants
- **Unused Variables** - Discover useless variable assignments
- **Long Lines** - Detect code lines exceeding recommended length
- **Deep Nesting** - Identify deeply nested code blocks
- **God Classes** - Discover large classes with too many responsibilities
- **Primitive Obsession** - Detect primitive type combinations that should be encapsulated

### 🔧 Intelligent Refactoring Suggestions
- Generate specific refactoring solutions based on detected smells
- Provide before/after code comparisons
- Evaluate refactoring effort and risk levels
- Identify quick wins (low effort, low risk)

### 🖥️ Terminal Interactive Interface
- Beautiful TUI interface with interactive operations
- Colored output with clear information hierarchy
- Support for file and project-level batch analysis
- Real-time refactoring preview

### 📊 Project-level Analysis
- Scan entire project code quality
- Generate project health reports
- Identify high-risk files and functions
- Support for multiple code file formats

---

## 🚀 Quick Start

### Requirements
- **Python**: 3.8 or higher
- **OS**: Linux / macOS / Windows

### Installation

#### Option 1: Direct Installation
```bash
# Clone repository
git clone https://github.com/gitstq/refactorpilot.git
cd refactorpilot

# Install
pip install -e .
```

#### Option 2: Direct Usage
```bash
# No installation needed, run directly
python -m refactorpilot --help
```

### Quick Usage

#### Analyze Single File
```bash
refactorpilot analyze your_code.py
```

#### Analyze Entire Project
```bash
refactorpilot analyze -p ./your_project
```

#### Launch Interactive Interface
```bash
refactorpilot tui
```

#### Generate Refactoring Suggestions
```bash
refactorpilot suggest your_code.py
```

---

## 📖 Detailed Usage Guide

### CLI Commands

#### `analyze` - Analyze Code
```bash
# Analyze single file
refactorpilot analyze file.py

# Analyze project
refactorpilot analyze -p ./project

# Output JSON format
refactorpilot analyze file.py -f json

# Show only high severity issues
refactorpilot analyze file.py --severity high
```

#### `refactor` - Refactor Code
```bash
# Preview refactoring (no actual changes)
refactorpilot refactor file.py -d

# Apply refactoring
refactorpilot refactor file.py --apply

# Batch refactor project
refactorpilot refactor -p ./project --apply
```

#### `suggest` - Generate Suggestions
```bash
refactorpilot suggest file.py
```

#### `tui` - Interactive Interface
```bash
refactorpilot tui
```

### Configuration Options

Customize detection thresholds via environment variables or configuration:

```python
# Custom thresholds
detector = SmellDetector(thresholds={
    'max_function_lines': 30,      # Max function lines
    'max_complexity': 8,           # Max cyclomatic complexity
    'max_arguments': 4,            # Max argument count
    'max_line_length': 80,         # Max line length
    'max_nesting_depth': 3,        # Max nesting depth
    'max_class_methods': 15,       # Max class methods
})
```

---

## 💡 Design Philosophy & Roadmap

### Design Principles
RefactorPilot follows these principles:

1. **Simplicity First** - Zero dependencies, works out of the box
2. **Practicality** - Focus on most common code quality issues
3. **Incremental Refactoring** - Support gradual improvements
4. **Developer Friendly** - Clear output, actionable feedback

### Technology Choices
- **AST Analysis** - Python standard library `ast` module for accurate code parsing
- **Zero Dependencies** - Only Python standard library for compatibility and lightness
- **TUI Interface** - `curses` for cross-platform terminal interface
- **Modular Design** - Separate analyzer, detector, suggestor for easy extension

### Roadmap

#### v1.1.0 (Planned)
- [ ] JavaScript/TypeScript code analysis support
- [ ] More refactoring patterns (extract variable, inline variable, etc.)
- [ ] Configuration file support (YAML/JSON format)
- [ ] Ignore rules configuration (comment markers to skip detection)

#### v1.2.0 (Planned)
- [ ] Refactoring history and rollback functionality
- [ ] Git integration with pre-commit checks
- [ ] HTML report generation
- [ ] CI/CD plugins (GitHub Actions, etc.)

#### v2.0.0 (Planned)
- [ ] AI-based intelligent refactoring suggestions
- [ ] Code similarity detection (duplicate code identification)
- [ ] Architecture-level smell detection
- [ ] Team collaboration features (rule sharing)

### Contributing
We welcome contributions in:
- 🐛 Bug fixes
- ✨ New smell detection rules
- 🌍 Multi-language support
- 📚 Documentation improvements
- 🎨 UI/UX enhancements

---

## 📦 Packaging & Deployment Guide

### Local Development
```bash
# Clone repository
git clone https://github.com/gitstq/refactorpilot.git
cd refactorpilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# Or: venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e .

# Run tests
python -m unittest discover tests/
```

### Build Release Package
```bash
# Install build tools
pip install build twine

# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### Cross-platform Compatibility
- ✅ Linux - Fully supported
- ✅ macOS - Fully supported
- ✅ Windows - Fully supported (TUI requires Windows 10+)

---

## 🤝 Contributing Guide

### Submitting PRs
1. Fork this repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

### Commit Convention
We use [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `style:` Code style change
- `refactor:` Code refactoring
- `test:` Test related
- `chore:` Build/tool related

### Reporting Issues
Please use [GitHub Issues](https://github.com/gitstq/refactorpilot/issues) and include:
- Issue description
- Reproduction steps
- Expected behavior
- Actual behavior
- Environment info (Python version, OS)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

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

## 🙏 Acknowledgments

Thanks to these open source projects and resources:
- [Python AST](https://docs.python.org/3/library/ast.html) - Code analysis foundation
- [Refactoring Guru](https://refactoring.guru/) - Refactoring pattern reference
- [Code Smells](https://sourcemaking.com/refactoring/smells) - Code smell definitions

---

<div align="center">

**Made with ❤️ by RefactorPilot Team**

If this project helps you, please give us a ⭐ Star!

</div>
