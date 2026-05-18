"""
RefactorPilot - 轻量级终端代码智能重构助手

一款零依赖的终端代码重构工具，基于AST分析识别代码坏味道，
提供智能重构建议与补丁生成功能。

Author: RefactorPilot Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "RefactorPilot Team"
__license__ = "MIT"

from .analyzer import CodeAnalyzer
from .detectors import SmellDetector
from .suggesters import RefactoringSuggester
from .refactor import RefactoringEngine

__all__ = [
    "CodeAnalyzer",
    "SmellDetector", 
    "RefactoringSuggester",
    "RefactoringEngine",
]
