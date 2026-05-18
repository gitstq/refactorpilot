"""
CLI命令行接口模块

提供命令行入口和参数解析
"""

import sys
import os
import argparse
import ast
from typing import Optional, List

from . import __version__
from .analyzer import CodeAnalyzer, ProjectAnalyzer
from .detectors import SmellDetector, SmellSeverity
from .suggesters import RefactoringSuggester
from .refactor import RefactoringEngine, BatchRefactorer
from .tui import create_tui
from .utils import (
    Colors, colorize, print_colored, is_supported_file,
    get_terminal_width, create_box, truncate_string
)


def create_parser() -> argparse.ArgumentParser:
    """创建参数解析器"""
    parser = argparse.ArgumentParser(
        prog='refactorpilot',
        description='RefactorPilot - 轻量级终端代码智能重构助手',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s analyze file.py              分析单个文件
  %(prog)s analyze -p ./project         分析整个项目
  %(prog)s refactor file.py             重构单个文件
  %(prog)s refactor -p ./project        批量重构项目
  %(prog)s tui                          启动交互式界面

更多信息: https://github.com/gitstq/refactorpilot
        """
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # analyze 命令
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='分析代码文件或项目',
        description='分析代码中的坏味道和质量问题'
    )
    analyze_parser.add_argument(
        'path',
        nargs='?',
        help='文件或目录路径'
    )
    analyze_parser.add_argument(
        '-p', '--project',
        action='store_true',
        help='分析整个项目'
    )
    analyze_parser.add_argument(
        '-f', '--format',
        choices=['text', 'json'],
        default='text',
        help='输出格式 (默认: text)'
    )
    analyze_parser.add_argument(
        '--severity',
        choices=['low', 'medium', 'high', 'critical'],
        help='只显示指定严重程度及以上的问题'
    )
    
    # refactor 命令
    refactor_parser = subparsers.add_parser(
        'refactor',
        help='重构代码文件或项目',
        description='自动重构代码并生成补丁'
    )
    refactor_parser.add_argument(
        'path',
        nargs='?',
        help='文件或目录路径'
    )
    refactor_parser.add_argument(
        '-p', '--project',
        action='store_true',
        help='批量重构整个项目'
    )
    refactor_parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='模拟运行，不实际修改文件'
    )
    refactor_parser.add_argument(
        '--apply',
        action='store_true',
        help='直接应用重构（不询问）'
    )
    
    # suggest 命令
    suggest_parser = subparsers.add_parser(
        'suggest',
        help='生成重构建议',
        description='基于代码坏味道生成重构建议'
    )
    suggest_parser.add_argument(
        'path',
        help='文件路径'
    )
    
    # tui 命令
    tui_parser = subparsers.add_parser(
        'tui',
        help='启动交互式TUI界面',
        description='启动终端用户交互界面'
    )
    
    return parser


def print_banner() -> None:
    """打印程序横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗ ███████╗███████╗ █████╗  ██████╗████████╗      ║
║   ██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝╚══██╔══╝      ║
║   ██████╔╝█████╗  █████╗  ███████║██║        ██║         ║
║   ██╔══██╗██╔══╝  ██╔══╝  ██╔══██║██║        ██║         ║
║   ██║  ██║██║     ██║     ██║  ██║╚██████╗   ██║         ║
║   ╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝         ║
║                                                           ║
║        ██████╗ ██╗██╗      ██████╗ ████████╗             ║
║        ██╔══██╗██║██║     ██╔═══██╗╚══██╔══╝             ║
║        ██████╔╝██║██║     ██║   ██║   ██║                ║
║        ██╔═══╝ ██║██║     ██║   ██║   ██║                ║
║        ██║     ██║███████╗╚██████╔╝   ██║                ║
║        ╚═╝     ╚═╝╚══════╝ ╚═════╝    ╚═╝                ║
║                                                           ║
║     轻量级终端代码智能重构助手 v{}                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """.format(__version__)
    print(colorize(banner, Colors.CYAN))


def cmd_analyze(args: argparse.Namespace) -> int:
    """
    执行分析命令
    
    Args:
        args: 命令行参数
    
    Returns:
        退出码
    """
    path = args.path or '.'
    
    if args.project or os.path.isdir(path):
        # 项目级分析
        print_colored(f"📁 正在分析项目: {path}", Colors.CYAN)
        print()
        
        analyzer = ProjectAnalyzer(path)
        summary = analyzer.analyze()
        
        if args.format == 'json':
            import json
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            # 文本格式输出
            print(create_box(f"项目分析摘要", title="RefactorPilot"))
            print(f"  📄 总文件数: {summary['total_files']}")
            print(f"  ✅ 成功分析: {summary['analyzed_files']}")
            print(f"  ❌ 分析失败: {summary['error_files']}")
            print(f"  📊 总行数: {summary['total_lines']:,}")
            print(f"  🔧 函数数: {summary['total_functions']:,}")
            print(f"  📦 类数: {summary['total_classes']:,}")
            print(f"  📈 平均复杂度: {summary['avg_complexity']}")
            print(f"  ⚠️ 最大复杂度: {summary['max_complexity']}")
            
            # 显示复杂函数
            complex_funcs = analyzer.get_complex_functions(threshold=10)
            if complex_funcs:
                print()
                print_colored("  🔴 高复杂度函数 (Top 5):", Colors.YELLOW)
                for i, (filepath, func) in enumerate(complex_funcs[:5], 1):
                    print(f"     {i}. {func.name}() in {truncate_string(filepath, 40)}")
                    print(f"        复杂度: {func.complexity}, 行数: {func.line_end - func.line_start + 1}")
        
        return 0
    
    else:
        # 单文件分析
        if not is_supported_file(path):
            print_colored(f"❌ 不支持的文件类型: {path}", Colors.RED)
            return 1
        
        print_colored(f"📄 正在分析文件: {path}", Colors.CYAN)
        print()
        
        analyzer = CodeAnalyzer(path)
        info = analyzer.analyze()
        
        if not info:
            print_colored(f"❌ 分析失败: {analyzer.get_parse_error()}", Colors.RED)
            return 1
        
        # 检测坏味道
        tree = ast.parse(analyzer.source)
        detector = SmellDetector()
        smells = detector.detect(analyzer.source, tree)
        
        # 按严重程度筛选
        if args.severity:
            severity_map = {
                'low': SmellSeverity.LOW,
                'medium': SmellSeverity.MEDIUM,
                'high': SmellSeverity.HIGH,
                'critical': SmellSeverity.CRITICAL
            }
            min_severity = severity_map[args.severity]
            severity_order = [SmellSeverity.CRITICAL, SmellSeverity.HIGH, 
                           SmellSeverity.MEDIUM, SmellSeverity.LOW]
            allowed = severity_order[:severity_order.index(min_severity) + 1]
            smells = [s for s in smells if s.severity in allowed]
        
        if args.format == 'json':
            import json
            result = {
                'file': path,
                'info': {
                    'line_count': info.line_count,
                    'function_count': info.function_count,
                    'class_count': info.class_count,
                },
                'smells': [
                    {
                        'type': s.smell_type.value,
                        'severity': s.severity.value,
                        'message': s.message,
                        'line': s.line,
                        'column': s.column,
                        'suggestion': s.suggestion
                    }
                    for s in smells
                ]
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # 文本格式输出
            print(create_box(f"文件: {path}", title="分析结果"))
            print(f"  📊 行数: {info.line_count}")
            print(f"  🔧 函数: {info.function_count}")
            print(f"  📦 类: {info.class_count}")
            print(f"  📥 导入: {info.import_count}")
            print()
            
            if smells:
                print_colored(f"  ⚠️ 发现 {len(smells)} 个问题:", Colors.YELLOW)
                print()
                
                severity_colors = {
                    SmellSeverity.CRITICAL: Colors.BG_RED + Colors.WHITE,
                    SmellSeverity.HIGH: Colors.RED,
                    SmellSeverity.MEDIUM: Colors.YELLOW,
                    SmellSeverity.LOW: Colors.GREEN
                }
                
                for i, smell in enumerate(smells, 1):
                    sev_color = severity_colors.get(smell.severity, Colors.WHITE)
                    sev_text = colorize(f"[{smell.severity.value.upper()}]", sev_color)
                    print(f"  {i}. {sev_text} {smell.message}")
                    print(f"     📍 第 {smell.line} 行 | 💡 {smell.suggestion}")
                    print()
            else:
                print_colored("  ✅ 未发现代码坏味道！", Colors.GREEN)
        
        return 0 if not smells else 1


def cmd_refactor(args: argparse.Namespace) -> int:
    """
    执行重构命令
    
    Args:
        args: 命令行参数
    
    Returns:
        退出码
    """
    path = args.path or '.'
    
    if args.project or os.path.isdir(path):
        # 批量重构
        print_colored(f"🚀 批量重构项目: {path}", Colors.CYAN)
        
        if args.dry_run:
            print_colored("  (模拟运行模式 - 不会实际修改文件)", Colors.YELLOW)
        
        print()
        
        refactorer = BatchRefactorer(path)
        result = refactorer.refactor_all(dry_run=not args.apply and args.dry_run)
        
        print(create_box("批量重构结果", title="RefactorPilot"))
        print(f"  📁 处理文件: {result['files_processed']}")
        print(f"  📝 修改文件: {result['files_modified']}")
        print(f"  🔧 生成补丁: {result['total_patches']}")
        print(f"  ✅ 应用补丁: {result['applied_patches']}")
        
        if result['dry_run']:
            print()
            print_colored("  💡 使用 --apply 选项应用重构", Colors.CYAN)
        
        return 0
    
    else:
        # 单文件重构
        if not is_supported_file(path):
            print_colored(f"❌ 不支持的文件类型: {path}", Colors.RED)
            return 1
        
        print_colored(f"🔧 重构文件: {path}", Colors.CYAN)
        
        if args.dry_run:
            print_colored("  (模拟运行模式)", Colors.YELLOW)
        
        print()
        
        # 分析文件
        analyzer = CodeAnalyzer(path)
        info = analyzer.analyze()
        
        if not info:
            print_colored(f"❌ 分析失败: {analyzer.get_parse_error()}", Colors.RED)
            return 1
        
        # 检测坏味道
        tree = ast.parse(analyzer.source)
        detector = SmellDetector()
        smells = detector.detect(analyzer.source, tree)
        
        if not smells:
            print_colored("  ✅ 未发现需要重构的问题", Colors.GREEN)
            return 0
        
        print_colored(f"  发现 {len(smells)} 个问题，生成重构补丁...", Colors.CYAN)
        print()
        
        # 生成并应用补丁
        engine = RefactoringEngine(path)
        patches = engine.preview_all_patches(smells)
        
        if not patches:
            print_colored("  ℹ️ 暂无可自动应用的补丁", Colors.YELLOW)
            return 0
        
        print(f"  生成 {len(patches)} 个补丁")
        print()
        
        applied = 0
        for i, patch in enumerate(patches, 1):
            print(f"  补丁 {i}/{len(patches)}: {patch.smell.message}")
            
            if args.apply:
                if engine.apply_patch(patch, dry_run=False):
                    print_colored("    ✅ 已应用", Colors.GREEN)
                    applied += 1
                else:
                    print_colored("    ❌ 应用失败", Colors.RED)
            else:
                print("    📋 预览:")
                for line in patch.diff.split('\n')[:10]:
                    if line.startswith('+'):
                        print(colorize(f"      {line}", Colors.GREEN))
                    elif line.startswith('-'):
                        print(colorize(f"      {line}", Colors.RED))
                    else:
                        print(f"      {line}")
        
        if args.apply:
            engine.save()
            print()
            print_colored(f"  ✅ 已应用 {applied}/{len(patches)} 个补丁", Colors.GREEN)
        else:
            print()
            print_colored("  💡 使用 --apply 选项应用重构", Colors.CYAN)
        
        return 0


def cmd_suggest(args: argparse.Namespace) -> int:
    """
    执行建议命令
    
    Args:
        args: 命令行参数
    
    Returns:
        退出码
    """
    path = args.path
    
    if not is_supported_file(path):
        print_colored(f"❌ 不支持的文件类型: {path}", Colors.RED)
        return 1
    
    print_colored(f"💡 生成重构建议: {path}", Colors.CYAN)
    print()
    
    # 分析文件
    analyzer = CodeAnalyzer(path)
    info = analyzer.analyze()
    
    if not info:
        print_colored(f"❌ 分析失败: {analyzer.get_parse_error()}", Colors.RED)
        return 1
    
    # 检测坏味道
    tree = ast.parse(analyzer.source)
    detector = SmellDetector()
    smells = detector.detect(analyzer.source, tree)
    
    # 生成建议
    suggester = RefactoringSuggester()
    suggestions = suggester.generate_suggestions(smells, analyzer.source, tree)
    
    if not suggestions:
        print_colored("  ✅ 无需重构建议", Colors.GREEN)
        return 0
    
    print(create_box(f"重构建议 ({len(suggestions)} 条)", title="RefactorPilot"))
    
    for i, suggestion in enumerate(suggestions[:5], 1):
        print()
        print_colored(f"  {i}. {suggestion.title}", Colors.CYAN + Colors.BOLD)
        print(f"     {suggestion.description}")
        print(f"     工作量: {suggestion.effort} | 风险: {suggestion.risk}")
        print()
        print("     收益:")
        for benefit in suggestion.benefits:
            print(f"       ✓ {benefit}")
    
    if len(suggestions) > 5:
        print()
        print(f"  ... 还有 {len(suggestions) - 5} 条建议")
    
    # 显示快速改进项
    quick_wins = suggester.get_quick_wins()
    if quick_wins:
        print()
        print_colored(f"  🚀 快速改进项 ({len(quick_wins)} 个):", Colors.GREEN)
        for suggestion in quick_wins[:3]:
            print(f"     • {suggestion.title}")
    
    return 0


def cmd_tui(args: argparse.Namespace) -> int:
    """
    启动TUI界面
    
    Args:
        args: 命令行参数
    
    Returns:
        退出码
    """
    def analyze_callback(path: str, project: bool = False):
        if project:
            analyzer = ProjectAnalyzer(path)
            summary = analyzer.analyze()
            tui = create_tui()
            tui.print_analysis_summary(summary)
        else:
            analyzer = CodeAnalyzer(path)
            info = analyzer.analyze()
            if info:
                tree = ast.parse(analyzer.source)
                detector = SmellDetector()
                smells = detector.detect(analyzer.source, tree)
                tui = create_tui()
                tui.print_smell_list(smells)
    
    def refactor_callback(path: str, batch: bool = False):
        if batch:
            refactorer = BatchRefactorer(path)
            result = refactorer.refactor_all(dry_run=True)
            print()
            print_colored(f"批量重构完成: {result['files_modified']} 个文件", Colors.GREEN)
        else:
            analyzer = CodeAnalyzer(path)
            info = analyzer.analyze()
            if info:
                tree = ast.parse(analyzer.source)
                detector = SmellDetector()
                smells = detector.detect(analyzer.source, tree)
                suggester = RefactoringSuggester()
                suggestions = suggester.generate_suggestions(smells, analyzer.source, tree)
                tui = create_tui()
                tui.print_suggestion_list(suggestions)
    
    tui = create_tui()
    tui.run_interactive(analyze_callback, refactor_callback)
    return 0


def main() -> int:
    """
    主入口函数
    
    Returns:
        退出码
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # 禁用颜色
    if args.no_color:
        import sys
        # 简单的禁用颜色方法
        class NoColorColors:
            def __getattr__(self, name):
                return ''
        Colors.__dict__.update(NoColorColors().__dict__)
    
    # 打印横幅（除了tui模式）
    if args.command != 'tui':
        print_banner()
    
    # 执行命令
    if args.command == 'analyze':
        return cmd_analyze(args)
    elif args.command == 'refactor':
        return cmd_refactor(args)
    elif args.command == 'suggest':
        return cmd_suggest(args)
    elif args.command == 'tui':
        return cmd_tui(args)
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
