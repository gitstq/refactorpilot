"""
工具函数测试
"""

import unittest
from refactorpilot.utils import (
    camel_to_snake, snake_to_camel, truncate_string,
    get_file_extension, is_supported_file, format_number
)


class TestUtils(unittest.TestCase):
    """测试工具函数"""
    
    def test_camel_to_snake(self):
        """测试驼峰转蛇形"""
        self.assertEqual(camel_to_snake('CamelCase'), 'camel_case')
        self.assertEqual(camel_to_snake('simple'), 'simple')
        self.assertEqual(camel_to_snake('HTTPSConnection'), 'https_connection')
    
    def test_snake_to_camel(self):
        """测试蛇形转驼峰"""
        self.assertEqual(snake_to_camel('snake_case'), 'snakeCase')
        self.assertEqual(snake_to_camel('simple'), 'simple')
    
    def test_truncate_string(self):
        """测试字符串截断"""
        self.assertEqual(truncate_string('hello world', 20), 'hello world')
        self.assertEqual(truncate_string('hello world', 8), 'hello...')
    
    def test_get_file_extension(self):
        """测试获取文件扩展名"""
        self.assertEqual(get_file_extension('test.py'), '.py')
        self.assertEqual(get_file_extension('test.JS'), '.js')
        self.assertEqual(get_file_extension('no_extension'), '')
    
    def test_is_supported_file(self):
        """测试支持的文件类型检查"""
        self.assertTrue(is_supported_file('test.py'))
        self.assertTrue(is_supported_file('test.js'))
        self.assertFalse(is_supported_file('test.txt'))
    
    def test_format_number(self):
        """测试数字格式化"""
        self.assertEqual(format_number(42), '42')
        self.assertEqual(format_number(1500), '1.5K')
        self.assertEqual(format_number(2500000), '2.5M')


if __name__ == '__main__':
    unittest.main()
