"""
代码坏味道检测器模块

实现15+种常见代码坏味道的检测规则
"""

import ast
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class SmellSeverity(Enum):
    """坏味道严重程度"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SmellType(Enum):
    """坏味道类型枚举"""
    LONG_FUNCTION = "long_function"
    HIGH_COMPLEXITY = "high_complexity"
    TOO_MANY_ARGUMENTS = "too_many_arguments"
    DUPLICATE_CODE = "duplicate_code"
    MAGIC_NUMBER = "magic_number"
    UNUSED_VARIABLE = "unused_variable"
    LONG_LINE = "long_line"
    NESTED_DEPTH = "nested_depth"
    GOD_CLASS = "god_class"
    FEATURE_ENVY = "feature_envy"
    TEMPORARY_FIELD = "temporary_field"
    MESSAGE_CHAIN = "message_chain"
    MIDDLE_MAN = "middle_man"
    PRIMITIVE_OBSESSION = "primitive_obsession"
    SWITCH_STATEMENTS = "switch_statements"


@dataclass
class CodeSmell:
    """代码坏味道数据类"""
    smell_type: SmellType
    severity: SmellSeverity
    message: str
    line: int
    column: int
    suggestion: str
    confidence: float  # 0.0 - 1.0


class SmellDetector:
    """
    代码坏味道检测器
    
    基于AST和文本分析检测代码中的坏味道
    """
    
    # 检测阈值配置
    DEFAULT_THRESHOLDS = {
        'max_function_lines': 50,
        'max_complexity': 10,
        'max_arguments': 5,
        'max_line_length': 100,
        'max_nesting_depth': 4,
        'max_class_methods': 20,
        'min_duplicate_lines': 6,
    }
    
    def __init__(self, thresholds: Optional[Dict[str, int]] = None):
        """
        初始化检测器
        
        Args:
            thresholds: 自定义阈值配置
        """
        self.thresholds = {**self.DEFAULT_THRESHOLDS, **(thresholds or {})}
        self.smells: List[CodeSmell] = []
        self.source_lines: List[str] = []
        self.tree: Optional[ast.AST] = None
    
    def detect(self, source: str, tree: ast.AST) -> List[CodeSmell]:
        """
        执行坏味道检测
        
        Args:
            source: 源代码字符串
            tree: AST语法树
        
        Returns:
            检测到的坏味道列表
        """
        self.smells = []
        self.source_lines = source.split('\n')
        self.tree = tree
        
        # 运行各种检测器
        self._detect_long_functions(tree)
        self._detect_high_complexity(tree)
        self._detect_too_many_arguments(tree)
        self._detect_magic_numbers(tree)
        self._detect_unused_variables(tree)
        self._detect_long_lines()
        self._detect_deep_nesting(tree)
        self._detect_god_classes(tree)
        self._detect_switch_statements(tree)
        self._detect_primitive_obsession(tree)
        
        # 按严重程度和行号排序
        severity_order = {
            SmellSeverity.CRITICAL: 0,
            SmellSeverity.HIGH: 1,
            SmellSeverity.MEDIUM: 2,
            SmellSeverity.LOW: 3
        }
        self.smells.sort(key=lambda s: (severity_order[s.severity], s.line))
        
        return self.smells
    
    def _detect_long_functions(self, tree: ast.AST) -> None:
        """检测过长函数"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lines = node.end_lineno - node.lineno + 1
                if lines > self.thresholds['max_function_lines']:
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.LONG_FUNCTION,
                        severity=SmellSeverity.HIGH if lines > 100 else SmellSeverity.MEDIUM,
                        message=f"函数 '{node.name}' 过长 ({lines} 行)，建议拆分为更小的函数",
                        line=node.lineno,
                        column=node.col_offset,
                        suggestion=f"将函数拆分为多个职责单一的子函数，每个函数不超过 {self.thresholds['max_function_lines']} 行",
                        confidence=0.9
                    ))
    
    def _detect_high_complexity(self, tree: ast.AST) -> None:
        """检测高复杂度函数"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                if complexity > self.thresholds['max_complexity']:
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.HIGH_COMPLEXITY,
                        severity=SmellSeverity.CRITICAL if complexity > 20 else SmellSeverity.HIGH,
                        message=f"函数 '{node.name}' 圈复杂度过高 ({complexity})，难以测试和维护",
                        line=node.lineno,
                        column=node.col_offset,
                        suggestion="简化条件逻辑，提取复杂条件为独立函数，使用策略模式替代多重条件",
                        confidence=0.95
                    ))
    
    def _detect_too_many_arguments(self, tree: ast.AST) -> None:
        """检测参数过多的函数"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args_count = len(node.args.args) + len(node.args.kwonlyargs)
                if node.args.vararg:
                    args_count += 1
                if node.args.kwarg:
                    args_count += 1
                
                if args_count > self.thresholds['max_arguments']:
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.TOO_MANY_ARGUMENTS,
                        severity=SmellSeverity.MEDIUM,
                        message=f"函数 '{node.name}' 参数过多 ({args_count} 个)，建议封装为对象",
                        line=node.lineno,
                        column=node.col_offset,
                        suggestion="将相关参数封装为数据类或配置对象，使用建造者模式",
                        confidence=0.85
                    ))
    
    def _detect_magic_numbers(self, tree: ast.AST) -> None:
        """检测魔法数字"""
        # 常见常量，不算魔法数字
        common_constants = {0, 1, -1, 2, 100, 1000}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    if node.value not in common_constants and abs(node.value) > 10:
                        # 检查是否在赋值语句的右侧
                        parent = self._get_parent(node, tree)
                        if not isinstance(parent, ast.Assign):
                            self.smells.append(CodeSmell(
                                smell_type=SmellType.MAGIC_NUMBER,
                                severity=SmellSeverity.LOW,
                                message=f"发现魔法数字: {node.value}，应定义为命名常量",
                                line=node.lineno,
                                column=node.col_offset,
                                suggestion=f"将 {node.value} 定义为有意义的常量，如 MAX_RETRY_COUNT = {node.value}",
                                confidence=0.7
                            ))
    
    def _detect_unused_variables(self, tree: ast.AST) -> None:
        """检测未使用的变量"""
        # 收集所有赋值和引用
        assigned = {}  # name -> (node, is_used)
        referenced = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    assigned[node.id] = (node, False)
                elif isinstance(node.ctx, ast.Load):
                    referenced.add(node.id)
        
        # 检查未使用的变量
        for name, (node, _) in assigned.items():
            if name not in referenced and not name.startswith('_'):
                # 排除特殊变量
                if name not in ['self', 'cls']:
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.UNUSED_VARIABLE,
                        severity=SmellSeverity.LOW,
                        message=f"变量 '{name}' 被赋值但从未使用",
                        line=node.lineno,
                        column=node.col_offset,
                        suggestion=f"删除未使用的变量 '{name}'，或在其名称前加下划线表示有意忽略",
                        confidence=0.8
                    ))
    
    def _detect_long_lines(self) -> None:
        """检测过长的代码行"""
        for i, line in enumerate(self.source_lines, 1):
            if len(line) > self.thresholds['max_line_length']:
                self.smells.append(CodeSmell(
                    smell_type=SmellType.LONG_LINE,
                    severity=SmellSeverity.LOW,
                    message=f"第 {i} 行过长 ({len(line)} 字符)，影响可读性",
                    line=i,
                    column=0,
                    suggestion="拆分长行，使用括号进行隐式续行，或将复杂表达式提取为变量",
                    confidence=0.9
                ))
    
    def _detect_deep_nesting(self, tree: ast.AST) -> None:
        """检测过深的嵌套"""
        def get_nesting_depth(node: ast.AST, current_depth: int = 0) -> int:
            if isinstance(node, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                current_depth += 1
            
            max_depth = current_depth
            for child in ast.iter_child_nodes(node):
                child_depth = get_nesting_depth(child, current_depth)
                max_depth = max(max_depth, child_depth)
            
            return max_depth
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                depth = get_nesting_depth(node)
                if depth > self.thresholds['max_nesting_depth']:
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.NESTED_DEPTH,
                        severity=SmellSeverity.MEDIUM,
                        message=f"函数 '{node.name}' 嵌套深度过大 ({depth} 层)，代码难以跟踪",
                        line=node.lineno,
                        column=node.col_offset,
                        suggestion="使用卫语句提前返回，提取嵌套逻辑为独立函数，或使用多态替代条件",
                        confidence=0.75
                    ))
    
    def _detect_god_classes(self, tree: ast.AST) -> None:
        """检测上帝类（过大的类）"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                
                if method_count > self.thresholds['max_class_methods']:
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.GOD_CLASS,
                        severity=SmellSeverity.HIGH,
                        message=f"类 '{node.name}' 方法过多 ({method_count} 个)，可能违反单一职责原则",
                        line=node.lineno,
                        column=node.col_offset,
                        suggestion="将类拆分为多个职责单一的类，使用组合替代继承",
                        confidence=0.8
                    ))
    
    def _detect_switch_statements(self, tree: ast.AST) -> None:
        """检测过多的条件分支（模拟switch语句）"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if_count = len([n for n in ast.walk(node) if isinstance(n, ast.If)])
                
                if if_count > 10:
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.SWITCH_STATEMENTS,
                        severity=SmellSeverity.MEDIUM,
                        message=f"函数 '{node.name}' 包含过多条件分支 ({if_count} 个 if 语句)",
                        line=node.lineno,
                        column=node.col_offset,
                        suggestion="使用策略模式、状态模式或多态替代多重条件分支",
                        confidence=0.75
                    ))
    
    def _detect_primitive_obsession(self, tree: ast.AST) -> None:
        """检测基本类型偏执"""
        # 检测使用多个基本类型参数表示概念的情况
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 检查是否有多个相关的基本类型参数（如x, y坐标）
                arg_names = [arg.arg for arg in node.args.args]
                
                # 检测常见的坐标对
                coordinate_pairs = [
                    ('x', 'y'), ('lat', 'lng'), ('latitude', 'longitude'),
                    ('width', 'height'), ('start', 'end')
                ]
                
                for pair in coordinate_pairs:
                    if pair[0] in arg_names and pair[1] in arg_names:
                        self.smells.append(CodeSmell(
                            smell_type=SmellType.PRIMITIVE_OBSESSION,
                            severity=SmellSeverity.LOW,
                            message=f"函数 '{node.name}' 使用基本类型 '{pair[0]}' 和 '{pair[1]}' 表示概念",
                            line=node.lineno,
                            column=node.col_offset,
                            suggestion=f"将 '{pair[0]}' 和 '{pair[1]}' 封装为数据类，如 Point、Coordinate 等",
                            confidence=0.6
                        ))
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """计算圈复杂度"""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
        
        return complexity
    
    def _get_parent(self, target: ast.AST, tree: ast.AST) -> Optional[ast.AST]:
        """获取节点的父节点"""
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                if child is target:
                    return node
        return None
    
    def get_smells_by_type(self, smell_type: SmellType) -> List[CodeSmell]:
        """按类型获取坏味道"""
        return [s for s in self.smells if s.smell_type == smell_type]
    
    def get_smells_by_severity(self, severity: SmellSeverity) -> List[CodeSmell]:
        """按严重程度获取坏味道"""
        return [s for s in self.smells if s.severity == severity]
    
    def get_summary(self) -> Dict[str, Any]:
        """获取检测摘要"""
        type_counts = {}
        severity_counts = {}
        
        for smell in self.smells:
            type_counts[smell.smell_type.value] = type_counts.get(smell.smell_type.value, 0) + 1
            severity_counts[smell.severity.value] = severity_counts.get(smell.severity.value, 0) + 1
        
        return {
            'total_smells': len(self.smells),
            'by_type': type_counts,
            'by_severity': severity_counts
        }
