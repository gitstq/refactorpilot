<div align="center">

# 🔧 RefactorPilot

**輕量級終端代碼智能重構助手**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP8-yellow.svg)]()

[简体中文](./README.md) | [English](./README.en.md)

</div>

---

## 🎉 專案介紹

RefactorPilot 是一款**零依賴**的輕量級終端代碼智能重構助手，專為追求代碼品質的開發者打造。它基於AST（抽象語法樹）分析技術，能夠智能識別代碼中的「壞味道」，提供專業的重構建議，甚至自動生成可應用的重構補丁。

### 💡 靈感來源

在日常開發中，我們常常會遇到這樣的問題：
- 函數越寫越長，難以維護
- 代碼複雜度越來越高，測試困難
- 魔法數字滿天飛，可讀性差
- 想重構但不知道從何下手

RefactorPilot 就是為了解決這些問題而生。它像一位經驗豐富的代碼審查員，時刻陪伴在你身邊，幫你發現代碼中的問題並提供改進方案。

### ✨ 核心差異化亮點

1. **🚀 零依賴設計** - 純Python標準庫實現，無需安裝任何第三方依賴
2. **🎯 智能壞味道檢測** - 基於AST分析識別10+種常見代碼壞味道
3. **💡 重構建議生成** - 自動生成重構方案與代碼補丁
4. **🖥️ TUI交互介面** - 內置終端使用者介面，支援交互式重構
5. **🔍 多維度分析** - 圈複雜度、代碼行數、函數參數等全方位分析

---

## ✨ 核心特性

### 🔍 代碼壞味道檢測
- **過長函數** - 檢測超過閾值的函數，建議拆分
- **高複雜度** - 基於圈複雜度識別難以測試的代碼
- **參數過多** - 發現參數過多的函數，建議封裝為物件
- **魔法數字** - 識別未命名的常量，建議提取為命名常量
- **未使用變量** - 發現無用的變量賦值
- **代碼行過長** - 檢測超出推薦長度的代碼行
- **嵌套過深** - 識別深層嵌套的代碼塊
- **上帝類** - 發現職責過多的大型類
- **基本類型偏執** - 檢測應封裝為物件的原始類型組合

### 🔧 智能重構建議
- 基於檢測到的壞味道生成具體的重構方案
- 提供重構前後的代碼對比
- 評估重構的工作量和風險等級
- 識別快速改進項（低工作量、低風險）

### 🖥️ 終端交互介面
- 美觀的TUI介面，支援交互式操作
- 彩色輸出，資訊層次清晰
- 支援檔案和專案級別的批次分析
- 即時預覽重構效果

### 📊 專案級分析
- 掃描整個專案的代碼品質
- 生成專案健康度報告
- 識別高風險檔案和函數
- 支援多種代碼檔案格式

---

## 🚀 快速開始

### 環境要求
- **Python**: 3.8 或更高版本
- **作業系統**: Linux / macOS / Windows

### 安裝方式

#### 方式一：直接安裝
```bash
# 克隆倉庫
git clone https://github.com/gitstq/refactorpilot.git
cd refactorpilot

# 安裝
pip install -e .
```

#### 方式二：直接使用
```bash
# 無需安裝，直接運行
python -m refactorpilot --help
```

### 快速使用

#### 分析單個檔案
```bash
refactorpilot analyze your_code.py
```

#### 分析整個專案
```bash
refactorpilot analyze -p ./your_project
```

#### 啟動交互式介面
```bash
refactorpilot tui
```

#### 生成重構建議
```bash
refactorpilot suggest your_code.py
```

---

## 📖 詳細使用指南

### 命令列介面

#### `analyze` - 分析代碼
```bash
# 分析單個檔案
refactorpilot analyze file.py

# 分析專案
refactorpilot analyze -p ./project

# 輸出JSON格式
refactorpilot analyze file.py -f json

# 只顯示高嚴重級別問題
refactorpilot analyze file.py --severity high
```

#### `refactor` - 重構代碼
```bash
# 預覽重構（不實際修改）
refactorpilot refactor file.py -d

# 應用重構
refactorpilot refactor file.py --apply

# 批次重構專案
refactorpilot refactor -p ./project --apply
```

#### `suggest` - 生成建議
```bash
refactorpilot suggest file.py
```

#### `tui` - 交互式介面
```bash
refactorpilot tui
```

### 配置選項

可以通過環境變數或配置檔案自定義檢測閾值：

```python
# 自定義閾值
detector = SmellDetector(thresholds={
    'max_function_lines': 30,      # 函數最大行數
    'max_complexity': 8,           # 最大圈複雜度
    'max_arguments': 4,            # 最大參數數量
    'max_line_length': 80,         # 最大行長度
    'max_nesting_depth': 3,        # 最大嵌套深度
    'max_class_methods': 15,       # 類最大方法數
})
```

---

## 💡 設計思路與迭代規劃

### 設計理念
RefactorPilot 遵循以下設計原則：

1. **簡單至上** - 零依賴，開箱即用
2. **實用為先** - 專注於最常見的代碼品質問題
3. **漸進式重構** - 支援從小處著手，逐步改進
4. **開發者友好** - 清晰的輸出，可操作的反饋

### 技術選型
- **AST分析** - 使用Python標準庫`ast`模組，準確解析代碼結構
- **零依賴** - 僅使用Python標準庫，確保相容性和輕量性
- **TUI介面** - 使用`curses`實現跨平台的終端介面
- **模組化設計** - 分析器、檢測器、建議器分離，易於擴展

### 後續功能迭代計劃

#### v1.1.0 (計劃中)
- [ ] 支援JavaScript/TypeScript代碼分析
- [ ] 添加更多重構模式（如提取變量、內聯變量等）
- [ ] 配置檔案支援（YAML/JSON格式）
- [ ] 忽略規則配置（註釋標記跳過檢測）

#### v1.2.0 (計劃中)
- [ ] 重構歷史記錄與回滾功能
- [ ] 與Git整合，支援提交前檢查
- [ ] HTML報告生成
- [ ] 持續整合外掛程式（GitHub Actions等）

#### v2.0.0 (規劃中)
- [ ] 基於AI的智能重構建議
- [ ] 代碼相似度檢測（重複代碼識別）
- [ ] 架構層面的壞味道檢測
- [ ] 團隊協作功能（規則共享）

### 社區貢獻方向
我們歡迎以下方面的貢獻：
- 🐛 Bug修復
- ✨ 新的壞味道檢測規則
- 🌍 多語言支援
- 📚 文件改進
- 🎨 UI/UX優化

---

## 📦 打包與部署指南

### 本地開發
```bash
# 克隆倉庫
git clone https://github.com/gitstq/refactorpilot.git
cd refactorpilot

# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或: venv\Scripts\activate  # Windows

# 安裝開發依賴
pip install -e .

# 運行測試
python -m unittest discover tests/
```

### 構建發布包
```bash
# 安裝構建工具
pip install build twine

# 構建
python -m build

# 上傳到PyPI
python -m twine upload dist/*
```

### 跨平台相容性
- ✅ Linux - 完全支援
- ✅ macOS - 完全支援
- ✅ Windows - 完全支援（TUI功能需Windows 10+）

---

## 🤝 貢獻指南

### 提交PR
1. Fork 本倉庫
2. 創建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 創建 Pull Request

### 提交規範
我們使用 [Conventional Commits](https://www.conventionalcommits.org/) 規範：
- `feat:` 新功能
- `fix:` Bug修復
- `docs:` 文件更新
- `style:` 代碼格式調整
- `refactor:` 代碼重構
- `test:` 測試相關
- `chore:` 構建/工具相關

### 報告問題
請使用 [GitHub Issues](https://github.com/gitstq/refactorpilot/issues) 報告問題，並包含：
- 問題描述
- 復現步驟
- 期望行為
- 實際行為
- 環境資訊（Python版本、作業系統）

---

## 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

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

## 🙏 致謝

感謝以下開源專案和資源：
- [Python AST](https://docs.python.org/3/library/ast.html) - 代碼分析基礎
- [Refactoring Guru](https://refactoring.guru/) - 重構模式參考
- [Code Smells](https://sourcemaking.com/refactoring/smells) - 代碼壞味道定義

---

<div align="center">

**Made with ❤️ by RefactorPilot Team**

如果這個專案對你有幫助，請給我們一個 ⭐ Star！

</div>
