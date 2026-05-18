"""
代码分析器测试
"""

import ast
import unittest
from refactorpilot.analyzer import CodeAnalyzer, FunctionInfo, ClassInfo, ModuleInfo


class TestCodeAnalyzer(unittest.TestCase):
    """测试代码分析器"""
    
    def setUp(self):
        """设置测试数据"""
        self.test_code = '''
"""Test module docstring"""

import os
import sys
from typing import List

def simple_function():
    """Simple function docstring"""
    return 42

def complex_function(x, y, z=None, *args, **kwargs):
    """Complex function with many args"""
    if x > 0:
        if y > 0:
            return x + y
    return 0

class TestClass:
    """Test class docstring"""
    
    def __init__(self):
        self.value = 0
    
    def method(self, arg):
        """Method docstring"""
        return self.value + arg
'''
    
    def test_parse_success(self):
        """测试解析成功"""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.test_code)
            temp_path = f.name
        
        try:
            analyzer = CodeAnalyzer(temp_path)
            self.assertTrue(analyzer.parse())
            self.assertIsNotNone(analyzer.tree)
            self.assertIsNone(analyzer.get_parse_error())
        finally:
            os.unlink(temp_path)
    
    def test_analyze_module(self):
        """测试模块分析"""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.test_code)
            temp_path = f.name
        
        try:
            analyzer = CodeAnalyzer(temp_path)
            info = analyzer.analyze()
            
            self.assertIsNotNone(info)
            self.assertEqual(info.filepath, temp_path)
            self.assertEqual(info.language, 'python')
            self.assertEqual(info.function_count, 3)  # simple, complex, method
            self.assertEqual(info.class_count, 1)
            self.assertEqual(info.import_count, 4)
        finally:
            os.unlink(temp_path)
    
    def test_function_info(self):
        """测试函数信息提取"""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.test_code)
            temp_path = f.name
        
        try:
            analyzer = CodeAnalyzer(temp_path)
            info = analyzer.analyze()
            
            # 查找复杂函数
            complex_func = None
            for func in info.functions:
                if func.name == 'complex_function':
                    complex_func = func
                    break
            
            self.assertIsNotNone(complex_func)
            self.assertTrue(complex_func.args_count >= 4)
            self.assertTrue(complex_func.complexity > 1)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
