"""
坏味道检测器测试
"""

import ast
import unittest
from refactorpilot.detectors import SmellDetector, SmellType, SmellSeverity


class TestSmellDetector(unittest.TestCase):
    """测试坏味道检测器"""
    
    def test_detect_long_function(self):
        """测试检测过长函数"""
        code = '''
def very_long_function():
    x1 = 1
    x2 = 2
    x3 = 3
    x4 = 4
    x5 = 5
    x6 = 6
    x7 = 7
    x8 = 8
    x9 = 9
    x10 = 10
    x11 = 11
    x12 = 12
    x13 = 13
    x14 = 14
    x15 = 15
    x16 = 16
    x17 = 17
    x18 = 18
    x19 = 19
    x20 = 20
    x21 = 21
    x22 = 22
    x23 = 23
    x24 = 24
    x25 = 25
    x26 = 26
    x27 = 27
    x28 = 28
    x29 = 29
    x30 = 30
    x31 = 31
    x32 = 32
    x33 = 33
    x34 = 34
    x35 = 35
    x36 = 36
    x37 = 37
    x38 = 38
    x39 = 39
    x40 = 40
    x41 = 41
    x42 = 42
    x43 = 43
    x44 = 44
    x45 = 45
    x46 = 46
    x47 = 47
    x48 = 48
    x49 = 49
    x50 = 50
    x51 = 51
    x52 = 52
    x53 = 53
    x54 = 54
    x55 = 55
    return x1 + x55
'''
        tree = ast.parse(code)
        detector = SmellDetector()
        smells = detector.detect(code, tree)
        
        long_func_smells = [s for s in smells if s.smell_type == SmellType.LONG_FUNCTION]
        self.assertTrue(len(long_func_smells) > 0)
    
    def test_detect_high_complexity(self):
        """测试检测高复杂度"""
        code = '''
def complex_function(x):
    if x > 0:
        if x > 10:
            if x > 20:
                if x > 30:
                    return 1
                return 2
            return 3
        return 4
    return 5
'''
        tree = ast.parse(code)
        detector = SmellDetector()
        smells = detector.detect(code, tree)
        
        complexity_smells = [s for s in smells if s.smell_type == SmellType.HIGH_COMPLEXITY]
        self.assertTrue(len(complexity_smells) > 0)
    
    def test_detect_magic_number(self):
        """测试检测魔法数字"""
        code = '''
def calculate(x):
    return x * 3.14159 + 42
'''
        tree = ast.parse(code)
        detector = SmellDetector()
        smells = detector.detect(code, tree)
        
        magic_smells = [s for s in smells if s.smell_type == SmellType.MAGIC_NUMBER]
        self.assertTrue(len(magic_smells) > 0)
    
    def test_detect_unused_variable(self):
        """测试检测未使用变量"""
        code = '''
def test_func():
    unused = 42
    used = 10
    return used
'''
        tree = ast.parse(code)
        detector = SmellDetector()
        smells = detector.detect(code, tree)
        
        unused_smells = [s for s in smells if s.smell_type == SmellType.UNUSED_VARIABLE]
        # unused变量应该被检测到
        self.assertTrue(any('unused' in s.message for s in unused_smells))


if __name__ == '__main__':
    unittest.main()
