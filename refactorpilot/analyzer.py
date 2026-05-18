"""
代码分析器模块

基于AST进行代码结构分析，提取代码指标和结构信息
"""

import ast
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from .utils import read_file, get_language


@dataclass
class FunctionInfo:
    """函数信息数据类"""
    name: str
    line_start: int
    line_end: int
    args_count: int
    complexity: int
    returns_count: int
    docstring: Optional[str]
    is_method: bool
    class_name: Optional[str]


@dataclass
class ClassInfo:
    """类信息数据类"""
    name: str
    line_start: int
    line_end: int
    method_count: int
    attribute_count: int
    docstring: Optional[str]
    base_classes: List[str]


@dataclass
class ModuleInfo:
    """模块信息数据类"""
    filepath: str
    language: str
    line_count: int
    function_count: int
    class_count: int
    import_count: int
    docstring: Optional[str]
    functions: List[FunctionInfo]
    classes: List[ClassInfo]


class CodeAnalyzer:
    """
    代码分析器
    
    基于AST分析代码结构，提取函数、类、复杂度等信息
    """
    
    def __init__(self, filepath: str):
        """
        初始化分析器
        
        Args:
            filepath: 代码文件路径
        """
        self.filepath = filepath
        self.language = get_language(filepath)
        self.source = read_file(filepath)
        self.tree = None
        self._parse_error = None
        
    def parse(self) -> bool:
        """
        解析代码文件
        
        Returns:
            解析是否成功
        """
        if self.language != 'python':
            self._parse_error = f"Unsupported language: {self.language}"
            return False
            
        try:
            self.tree = ast.parse(self.source)
            return True
        except SyntaxError as e:
            self._parse_error = f"Syntax error at line {e.lineno}: {e.msg}"
            return False
        except Exception as e:
            self._parse_error = str(e)
            return False
    
    def get_parse_error(self) -> Optional[str]:
        """获取解析错误信息"""
        return self._parse_error
    
    def analyze(self) -> Optional[ModuleInfo]:
        """
        执行完整分析
        
        Returns:
            模块信息对象，解析失败返回None
        """
        if not self.parse():
            return None
        
        lines = self.source.split('\n')
        
        # 提取模块级文档字符串
        docstring = ast.get_docstring(self.tree)
        
        # 分析导入语句
        import_count = len([
            node for node in ast.walk(self.tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ])
        
        # 收集函数和类
        functions = []
        classes = []
        
        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(self._analyze_function(node))
            elif isinstance(node, ast.ClassDef):
                class_info = self._analyze_class(node)
                classes.append(class_info)
                # 收集类方法
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        functions.append(self._analyze_function(item, class_name=node.name))
        
        return ModuleInfo(
            filepath=self.filepath,
            language=self.language,
            line_count=len(lines),
            function_count=len([n for n in ast.walk(self.tree) if isinstance(n, ast.FunctionDef)]),
            class_count=len([n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)]),
            import_count=import_count,
            docstring=docstring,
            functions=functions,
            classes=classes
        )
    
    def _analyze_function(self, node: ast.FunctionDef, class_name: Optional[str] = None) -> FunctionInfo:
        """
        分析函数节点
        
        Args:
            node: AST函数节点
            class_name: 所属类名（如果是方法）
        
        Returns:
            函数信息对象
        """
        # 计算圈复杂度
        complexity = self._calculate_complexity(node)
        
        # 统计return语句
        returns_count = len([
            n for n in ast.walk(node)
            if isinstance(n, ast.Return) and n.value is not None
        ])
        
        # 获取文档字符串
        docstring = ast.get_docstring(node)
        
        # 统计参数数量
        args_count = len(node.args.args) + len(node.args.kwonlyargs)
        if node.args.vararg:
            args_count += 1
        if node.args.kwarg:
            args_count += 1
        
        return FunctionInfo(
            name=node.name,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            args_count=args_count,
            complexity=complexity,
            returns_count=returns_count,
            docstring=docstring,
            is_method=class_name is not None,
            class_name=class_name
        )
    
    def _analyze_class(self, node: ast.ClassDef) -> ClassInfo:
        """
        分析类节点
        
        Args:
            node: AST类节点
        
        Returns:
            类信息对象
        """
        # 统计方法数量
        method_count = len([
            n for n in node.body if isinstance(n, ast.FunctionDef)
        ])
        
        # 统计属性数量（类级别赋值）
        attribute_count = len([
            n for n in node.body if isinstance(n, ast.Assign)
        ])
        
        # 获取文档字符串
        docstring = ast.get_docstring(node)
        
        # 获取基类
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(base.attr)
        
        return ClassInfo(
            name=node.name,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            method_count=method_count,
            attribute_count=attribute_count,
            docstring=docstring,
            base_classes=base_classes
        )
    
    def _calculate_complexity(self, node: ast.AST) -> int:
        """
        计算圈复杂度
        
        Args:
            node: AST节点
        
        Returns:
            圈复杂度数值
        """
        complexity = 1  # 基础复杂度
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
        
        return complexity
    
    def get_function_by_name(self, name: str) -> Optional[ast.FunctionDef]:
        """
        根据名称查找函数定义
        
        Args:
            name: 函数名
        
        Returns:
            函数AST节点，未找到返回None
        """
        if not self.tree:
            return None
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and node.name == name:
                return node
        return None
    
    def get_class_by_name(self, name: str) -> Optional[ast.ClassDef]:
        """
        根据名称查找类定义
        
        Args:
            name: 类名
        
        Returns:
            类AST节点，未找到返回None
        """
        if not self.tree:
            return None
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef) and node.name == name:
                return node
        return None
    
    def get_source_segment(self, node: ast.AST) -> Optional[str]:
        """
        获取AST节点对应的源代码片段
        
        Args:
            node: AST节点
        
        Returns:
            源代码片段
        """
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            lines = self.source.split('\n')
            start = node.lineno - 1
            end = node.end_lineno or node.lineno
            return '\n'.join(lines[start:end])
        return None
    
    def to_json(self) -> str:
        """
        将分析结果导出为JSON
        
        Returns:
            JSON字符串
        """
        info = self.analyze()
        if not info:
            return "{}"
        
        data = asdict(info)
        return json.dumps(data, indent=2, ensure_ascii=False)


class ProjectAnalyzer:
    """
    项目级分析器
    
    分析整个项目的代码结构和指标
    """
    
    def __init__(self, directory: str):
        """
        初始化项目分析器
        
        Args:
            directory: 项目目录路径
        """
        self.directory = directory
        self.files: List[str] = []
        self.results: List[ModuleInfo] = []
        self.errors: List[Tuple[str, str]] = []
    
    def analyze(self) -> Dict[str, Any]:
        """
        分析整个项目
        
        Returns:
            项目分析结果字典
        """
        from .utils import find_files
        
        self.files = find_files(self.directory)
        self.results = []
        self.errors = []
        
        for filepath in self.files:
            analyzer = CodeAnalyzer(filepath)
            info = analyzer.analyze()
            
            if info:
                self.results.append(info)
            else:
                self.errors.append((filepath, analyzer.get_parse_error() or "Unknown error"))
        
        return self._generate_summary()
    
    def _generate_summary(self) -> Dict[str, Any]:
        """
        生成项目汇总信息
        
        Returns:
            汇总信息字典
        """
        total_lines = sum(r.line_count for r in self.results)
        total_functions = sum(r.function_count for r in self.results)
        total_classes = sum(r.class_count for r in self.results)
        total_imports = sum(r.import_count for r in self.results)
        
        # 计算平均复杂度
        all_complexities = [
            f.complexity for r in self.results for f in r.functions
        ]
        avg_complexity = sum(all_complexities) / len(all_complexities) if all_complexities else 0
        max_complexity = max(all_complexities) if all_complexities else 0
        
        # 按语言统计
        language_stats: Dict[str, int] = {}
        for r in self.results:
            lang = r.language
            language_stats[lang] = language_stats.get(lang, 0) + 1
        
        return {
            'directory': self.directory,
            'total_files': len(self.files),
            'analyzed_files': len(self.results),
            'error_files': len(self.errors),
            'total_lines': total_lines,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'total_imports': total_imports,
            'avg_complexity': round(avg_complexity, 2),
            'max_complexity': max_complexity,
            'language_stats': language_stats,
            'files': [asdict(r) for r in self.results],
            'errors': [{'file': f, 'error': e} for f, e in self.errors]
        }
    
    def get_complex_functions(self, threshold: int = 10) -> List[Tuple[str, FunctionInfo]]:
        """
        获取高复杂度函数列表
        
        Args:
            threshold: 复杂度阈值
        
        Returns:
            (文件路径, 函数信息) 列表
        """
        result = []
        for module in self.results:
            for func in module.functions:
                if func.complexity >= threshold:
                    result.append((module.filepath, func))
        
        # 按复杂度排序
        result.sort(key=lambda x: x[1].complexity, reverse=True)
        return result
    
    def get_large_functions(self, threshold: int = 50) -> List[Tuple[str, FunctionInfo]]:
        """
        获取大型函数列表（按行数）
        
        Args:
            threshold: 行数阈值
        
        Returns:
            (文件路径, 函数信息) 列表
        """
        result = []
        for module in self.results:
            for func in module.functions:
                lines = func.line_end - func.line_start + 1
                if lines >= threshold:
                    result.append((module.filepath, func))
        
        # 按行数排序
        result.sort(key=lambda x: x[1].line_end - x[1].line_start, reverse=True)
        return result
