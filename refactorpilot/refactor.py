"""
重构引擎模块

执行代码重构操作，生成和应用重构补丁
"""

import ast
import re
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from .detectors import CodeSmell, SmellType
from .utils import generate_diff, read_file, write_file


@dataclass
class RefactoringPatch:
    """重构补丁数据类"""
    smell: CodeSmell
    original_code: str
    refactored_code: str
    diff: str
    line_start: int
    line_end: int


class RefactoringEngine:
    """
    重构引擎
    
    执行自动化的代码重构操作
    """
    
    def __init__(self, filepath: str):
        """
        初始化重构引擎
        
        Args:
            filepath: 目标文件路径
        """
        self.filepath = filepath
        self.source = read_file(filepath)
        self.lines = self.source.split('\n')
        self.patches: List[RefactoringPatch] = []
    
    def generate_patch(self, smell: CodeSmell) -> Optional[RefactoringPatch]:
        """
        为坏味道生成重构补丁
        
        Args:
            smell: 代码坏味道
        
        Returns:
            重构补丁，如果不适用返回None
        """
        generators = {
            SmellType.UNUSED_VARIABLE: self._patch_unused_variable,
            SmellType.MAGIC_NUMBER: self._patch_magic_number,
            SmellType.LONG_LINE: self._patch_long_line,
        }
        
        generator = generators.get(smell.smell_type)
        if generator:
            return generator(smell)
        
        return None
    
    def _patch_unused_variable(self, smell: CodeSmell) -> Optional[RefactoringPatch]:
        """生成删除未使用变量的补丁"""
        line_idx = smell.line - 1
        if line_idx < 0 or line_idx >= len(self.lines):
            return None
        
        original_line = self.lines[line_idx]
        
        # 尝试匹配赋值语句
        match = re.match(r'^(\s*)(\w+)\s*=\s*(.+)$', original_line)
        if match:
            indent = match.group(1)
            var_name = match.group(2)
            value = match.group(3)
            
            # 如果右侧有函数调用，保留调用但删除赋值
            if '(' in value and ')' in value:
                refactored_line = indent + value
            else:
                # 整行删除，返回空字符串
                refactored_line = ""
            
            diff = generate_diff(original_line, refactored_line or "# Removed unused variable", "line")
            
            return RefactoringPatch(
                smell=smell,
                original_code=original_line,
                refactored_code=refactored_line,
                diff=diff,
                line_start=smell.line,
                line_end=smell.line
            )
        
        return None
    
    def _patch_magic_number(self, smell: CodeSmell) -> Optional[RefactoringPatch]:
        """生成提取常量的补丁（示例实现）"""
        # 这是一个简化的实现，实际应用中需要更复杂的逻辑
        line_idx = smell.line - 1
        if line_idx < 0 or line_idx >= len(self.lines):
            return None
        
        original_line = self.lines[line_idx]
        
        # 提取魔法数字
        match = re.search(r'[=\+\-\*/<>!]+\s*(\d+\.?\d*)', original_line)
        if match:
            number = match.group(1)
            constant_name = f"CONSTANT_{number.replace('.', '_')}"
            
            # 生成重构后的代码
            refactored_line = original_line.replace(number, constant_name, 1)
            
            diff = generate_diff(original_line, refactored_line, "line")
            
            return RefactoringPatch(
                smell=smell,
                original_code=original_line,
                refactored_code=refactored_line,
                diff=diff,
                line_start=smell.line,
                line_end=smell.line
            )
        
        return None
    
    def _patch_long_line(self, smell: CodeSmell) -> Optional[RefactoringPatch]:
        """生成分拆长行的补丁"""
        line_idx = smell.line - 1
        if line_idx < 0 or line_idx >= len(self.lines):
            return None
        
        original_line = self.lines[line_idx]
        
        # 简单的行分割策略
        if len(original_line) <= 100:
            return None
        
        # 尝试在参数列表处分割
        if '(' in original_line and ')' in original_line:
            refactored = self._split_function_call(original_line)
            if refactored:
                diff = generate_diff(original_line, refactored, "line")
                
                return RefactoringPatch(
                    smell=smell,
                    original_code=original_line,
                    refactored_code=refactored,
                    diff=diff,
                    line_start=smell.line,
                    line_end=smell.line
                )
        
        return None
    
    def _split_function_call(self, line: str) -> Optional[str]:
        """分割函数调用"""
        # 匹配函数调用模式
        match = re.match(r'^(\s*)(\w+)\((.+)\)(.*)$', line)
        if not match:
            return None
        
        indent = match.group(1)
        func_name = match.group(2)
        args = match.group(3)
        suffix = match.group(4)
        
        # 简单地在逗号处分割
        arg_list = [a.strip() for a in args.split(',')]
        
        if len(arg_list) <= 1:
            return None
        
        # 生成多行格式
        lines = [f"{indent}{func_name}("]
        for i, arg in enumerate(arg_list):
            comma = ',' if i < len(arg_list) - 1 else ''
            lines.append(f"{indent}    {arg}{comma}")
        lines.append(f"{indent}){suffix}")
        
        return '\n'.join(lines)
    
    def apply_patch(self, patch: RefactoringPatch, dry_run: bool = False) -> bool:
        """
        应用重构补丁
        
        Args:
            patch: 重构补丁
            dry_run: 是否仅模拟，不实际修改
        
        Returns:
            是否成功应用
        """
        try:
            start_idx = patch.line_start - 1
            end_idx = patch.line_end
            
            # 检查行号有效性
            if start_idx < 0 or end_idx > len(self.lines):
                return False
            
            if not dry_run:
                # 应用修改
                new_lines = patch.refactored_code.split('\n')
                self.lines[start_idx:end_idx] = new_lines
                
                # 更新源代码
                self.source = '\n'.join(self.lines)
            
            return True
        except Exception as e:
            print(f"Error applying patch: {e}")
            return False
    
    def save(self) -> bool:
        """
        保存修改后的代码
        
        Returns:
            是否成功保存
        """
        try:
            write_file(self.filepath, self.source)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def get_modified_source(self) -> str:
        """获取修改后的源代码"""
        return '\n'.join(self.lines)
    
    def preview_all_patches(self, smells: List[CodeSmell]) -> List[RefactoringPatch]:
        """
        预览所有可能的重构补丁
        
        Args:
            smells: 坏味道列表
        
        Returns:
            可应用的补丁列表
        """
        patches = []
        
        for smell in smells:
            patch = self.generate_patch(smell)
            if patch:
                patches.append(patch)
        
        return patches


class BatchRefactorer:
    """
    批量重构器
    
    对多个文件执行批量重构操作
    """
    
    def __init__(self, directory: str):
        """
        初始化批量重构器
        
        Args:
            directory: 目标目录
        """
        self.directory = directory
        self.results: List[Dict[str, Any]] = []
    
    def refactor_all(self, smell_types: Optional[List[SmellType]] = None, dry_run: bool = True) -> Dict[str, Any]:
        """
        重构目录下的所有文件
        
        Args:
            smell_types: 要重构的坏味道类型，None表示全部
            dry_run: 是否仅模拟
        
        Returns:
            重构结果摘要
        """
        from .utils import find_files
        from .analyzer import CodeAnalyzer
        from .detectors import SmellDetector
        
        files = find_files(self.directory)
        self.results = []
        
        total_patches = 0
        applied_patches = 0
        
        for filepath in files:
            analyzer = CodeAnalyzer(filepath)
            info = analyzer.analyze()
            
            if not info:
                continue
            
            detector = SmellDetector()
            tree = ast.parse(analyzer.source)
            smells = detector.detect(analyzer.source, tree)
            
            # 筛选指定类型的坏味道
            if smell_types:
                smells = [s for s in smells if s.smell_type in smell_types]
            
            if not smells:
                continue
            
            engine = RefactoringEngine(filepath)
            patches = engine.preview_all_patches(smells)
            
            file_applied = 0
            for patch in patches:
                if engine.apply_patch(patch, dry_run=dry_run):
                    file_applied += 1
            
            if not dry_run and file_applied > 0:
                engine.save()
            
            total_patches += len(patches)
            applied_patches += file_applied
            
            self.results.append({
                'filepath': filepath,
                'smells_found': len(smells),
                'patches_generated': len(patches),
                'patches_applied': file_applied
            })
        
        return {
            'directory': self.directory,
            'files_processed': len(files),
            'files_modified': len([r for r in self.results if r['patches_applied'] > 0]),
            'total_patches': total_patches,
            'applied_patches': applied_patches,
            'dry_run': dry_run,
            'details': self.results
        }
