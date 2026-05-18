"""
工具函数模块
"""

import os
import re
from typing import List, Tuple, Optional


def get_file_extension(filepath: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(filepath)[1].lower()


def is_supported_file(filepath: str) -> bool:
    """检查文件是否为支持的代码文件"""
    supported_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx'}
    return get_file_extension(filepath) in supported_extensions


def get_language(filepath: str) -> str:
    """根据文件路径获取编程语言"""
    ext_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
    }
    return ext_map.get(get_file_extension(filepath), 'unknown')


def read_file(filepath: str) -> str:
    """读取文件内容"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def write_file(filepath: str, content: str) -> None:
    """写入文件内容"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def find_files(directory: str, extensions: Optional[List[str]] = None) -> List[str]:
    """
    递归查找目录下的所有代码文件
    
    Args:
        directory: 目标目录
        extensions: 文件扩展名列表，默认为支持的代码文件
    
    Returns:
        文件路径列表
    """
    if extensions is None:
        extensions = ['.py', '.js', '.ts', '.jsx', '.tsx']
    
    files = []
    for root, _, filenames in os.walk(directory):
        # 跳过隐藏目录和常见非项目目录
        if any(part.startswith('.') for part in root.split(os.sep)):
            continue
        if any(skip in root for skip in ['node_modules', '__pycache__', 'venv', '.git']):
            continue
            
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))
    
    return files


def calculate_line_count(filepath: str) -> int:
    """计算文件行数"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return len(f.readlines())
    except:
        return 0


def truncate_string(s: str, max_length: int, suffix: str = "...") -> str:
    """截断字符串到指定长度"""
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


def format_number(num: int) -> str:
    """格式化数字显示"""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}K"
    return str(num)


def camel_to_snake(name: str) -> str:
    """驼峰命名转蛇形命名"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name: str) -> str:
    """蛇形命名转驼峰命名"""
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def get_common_prefix(strings: List[str]) -> str:
    """获取字符串列表的公共前缀"""
    if not strings:
        return ""
    
    prefix = strings[0]
    for s in strings[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def highlight_code_line(code: str, line_number: int, context: int = 2) -> str:
    """
    高亮显示指定行及其上下文
    
    Args:
        code: 代码内容
        line_number: 目标行号（1-based）
        context: 上下文行数
    
    Returns:
        格式化后的代码片段
    """
    lines = code.split('\n')
    start = max(0, line_number - context - 1)
    end = min(len(lines), line_number + context)
    
    result = []
    for i in range(start, end):
        line_num = i + 1
        prefix = ">>> " if line_num == line_number else "    "
        result.append(f"{prefix}{line_num:4d} | {lines[i]}")
    
    return '\n'.join(result)


def generate_diff(original: str, modified: str, filename: str = "file") -> str:
    """
    生成代码差异对比
    
    Args:
        original: 原始代码
        modified: 修改后代码
        filename: 文件名
    
    Returns:
        diff格式的字符串
    """
    import difflib
    
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f"{filename}.original",
        tofile=f"{filename}.refactored",
        lineterm=''
    )
    
    return ''.join(diff)


class Colors:
    """终端颜色代码"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'


def supports_color() -> bool:
    """检查终端是否支持颜色"""
    return hasattr(os, 'isatty') and os.isatty(1)


def colorize(text: str, color: str) -> str:
    """为文本添加颜色"""
    if not supports_color():
        return text
    return f"{color}{text}{Colors.RESET}"


def print_colored(text: str, color: str, end: str = '\n') -> None:
    """打印带颜色的文本"""
    print(colorize(text, color), end=end)


def get_terminal_width() -> int:
    """获取终端宽度"""
    try:
        import shutil
        return shutil.get_terminal_size().columns
    except:
        return 80


def center_text(text: str, width: Optional[int] = None, fillchar: str = ' ') -> str:
    """居中文本"""
    if width is None:
        width = get_terminal_width()
    return text.center(width, fillchar)


def create_box(text: str, width: Optional[int] = None, title: str = "") -> str:
    """
    创建带边框的文本框
    
    Args:
        text: 文本内容
        width: 宽度
        title: 标题
    
    Returns:
        带边框的文本
    """
    if width is None:
        width = min(get_terminal_width() - 4, 80)
    
    lines = text.split('\n')
    result = []
    
    # 顶部边框
    if title:
        title_str = f"[ {title} ]"
        padding = (width - len(title_str)) // 2
        result.append('┌' + '─' * padding + title_str + '─' * (width - padding - len(title_str)) + '┐')
    else:
        result.append('┌' + '─' * width + '┐')
    
    # 内容
    for line in lines:
        if len(line) > width:
            line = line[:width-3] + '...'
        result.append('│ ' + line.ljust(width - 2) + ' │')
    
    # 底部边框
    result.append('└' + '─' * width + '┘')
    
    return '\n'.join(result)
