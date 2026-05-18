"""
TUI界面模块

提供终端用户交互界面
"""

import sys
import os
from typing import List, Optional, Dict, Any, Callable, Tuple
from .utils import Colors, colorize, center_text, create_box, get_terminal_width, truncate_string
from .detectors import CodeSmell, SmellSeverity, SmellType
from .suggesters import RefactoringSuggestion


class TUI:
    """
    终端用户界面
    
    提供交互式的重构体验
    """
    
    def __init__(self):
        """初始化TUI"""
        self.width = get_terminal_width()
        self.running = True
        self.current_menu = "main"
        self.history: List[str] = []
    
    def clear(self) -> None:
        """清屏"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_header(self, title: str) -> None:
        """打印标题"""
        print()
        print(colorize(center_text(f" RefactorPilot - {title} ", self.width, "="), Colors.CYAN + Colors.BOLD))
        print()
    
    def print_footer(self, hint: str = "") -> None:
        """打印底部信息"""
        print()
        if hint:
            print(colorize(center_text(f" {hint} ", self.width), Colors.DIM))
        print(colorize("=" * self.width, Colors.CYAN))
        print()
    
    def print_menu(self, options: List[Tuple[str, str]], title: str = "Menu") -> None:
        """
        打印菜单选项
        
        Args:
            options: (选项键, 选项描述) 列表
            title: 菜单标题
        """
        self.print_header(title)
        
        for i, (key, desc) in enumerate(options, 1):
            num = colorize(f"[{i}]", Colors.YELLOW + Colors.BOLD)
            print(f"  {num} {desc}")
        
        print()
        quit_opt = colorize("[0]", Colors.RED + Colors.BOLD)
        print(f"  {quit_opt} 退出 / Quit")
        
        self.print_footer("请输入选项编号")
    
    def get_input(self, prompt: str = "") -> str:
        """获取用户输入"""
        if prompt:
            print(colorize(prompt + " ", Colors.CYAN), end="")
        try:
            return input().strip()
        except (EOFError, KeyboardInterrupt):
            return "0"
    
    def print_smell(self, smell: CodeSmell, index: int = 0) -> None:
        """
        打印坏味道信息
        
        Args:
            smell: 坏味道对象
            index: 序号
        """
        # 根据严重程度选择颜色
        severity_colors = {
            SmellSeverity.CRITICAL: Colors.BG_RED + Colors.WHITE + Colors.BOLD,
            SmellSeverity.HIGH: Colors.RED,
            SmellSeverity.MEDIUM: Colors.YELLOW,
            SmellSeverity.LOW: Colors.GREEN,
        }
        
        sev_color = severity_colors.get(smell.severity, Colors.WHITE)
        sev_text = colorize(f"[{smell.severity.value.upper()}]", sev_color)
        
        type_text = colorize(f"[{smell.smell_type.value}]", Colors.CYAN)
        
        print(f"\n  {colorize(f'#{index}', Colors.YELLOW + Colors.BOLD)} {sev_text} {type_text}")
        print(f"  📍 位置: 第 {smell.line} 行, 第 {smell.column} 列")
        print(f"  📝 描述: {smell.message}")
        print(f"  💡 建议: {smell.suggestion}")
        
        if smell.confidence < 0.8:
            conf_text = colorize(f"{smell.confidence:.0%}", Colors.YELLOW)
        else:
            conf_text = colorize(f"{smell.confidence:.0%}", Colors.GREEN)
        print(f"  🎯 置信度: {conf_text}")
    
    def print_smell_list(self, smells: List[CodeSmell], title: str = "检测到的代码坏味道") -> None:
        """
        打印坏味道列表
        
        Args:
            smells: 坏味道列表
            title: 标题
        """
        self.print_header(title)
        
        if not smells:
            print(colorize("  ✅ 未发现代码坏味道！代码质量很好。", Colors.GREEN + Colors.BOLD))
            return
        
        # 统计信息
        severity_counts = {}
        for smell in smells:
            severity_counts[smell.severity.value] = severity_counts.get(smell.severity.value, 0) + 1
        
        print(f"  📊 共发现 {colorize(str(len(smells)), Colors.YELLOW + Colors.BOLD)} 个问题:")
        for sev, count in sorted(severity_counts.items()):
            print(f"     • {sev}: {count}")
        print()
        
        # 打印前10个
        for i, smell in enumerate(smells[:10], 1):
            self.print_smell(smell, i)
        
        if len(smells) > 10:
            print(f"\n  ... 还有 {len(smells) - 10} 个问题未显示")
        
        self.print_footer()
    
    def print_suggestion(self, suggestion: RefactoringSuggestion, index: int = 0) -> None:
        """
        打印重构建议
        
        Args:
            suggestion: 重构建议
            index: 序号
        """
        effort_colors = {
            'low': Colors.GREEN,
            'medium': Colors.YELLOW,
            'high': Colors.RED
        }
        
        risk_colors = {
            'low': Colors.GREEN,
            'medium': Colors.YELLOW,
            'high': Colors.RED
        }
        
        print(f"\n  {colorize(f'#{index}', Colors.YELLOW + Colors.BOLD)} {colorize(suggestion.title, Colors.CYAN + Colors.BOLD)}")
        print(f"  📝 {suggestion.description}")
        
        effort_text = colorize(suggestion.effort.upper(), effort_colors.get(suggestion.effort, Colors.WHITE))
        risk_text = colorize(suggestion.risk.upper(), risk_colors.get(suggestion.risk, Colors.WHITE))
        print(f"  ⏱️ 工作量: {effort_text}  |  ⚠️ 风险: {risk_text}")
        
        print(f"\n  {colorize('重构前:', Colors.RED)}")
        for line in suggestion.before_code.split('\n')[:5]:
            print(f"    {colorize('|', Colors.RED)} {line}")
        if len(suggestion.before_code.split('\n')) > 5:
            print(f"    {colorize('|', Colors.RED)} ...")
        
        print(f"\n  {colorize('重构后:', Colors.GREEN)}")
        for line in suggestion.after_code.split('\n')[:5]:
            print(f"    {colorize('|', Colors.GREEN)} {line}")
        if len(suggestion.after_code.split('\n')) > 5:
            print(f"    {colorize('|', Colors.GREEN)} ...")
        
        print(f"\n  {colorize('收益:', Colors.CYAN)}")
        for benefit in suggestion.benefits:
            print(f"    ✓ {benefit}")
    
    def print_suggestion_list(self, suggestions: List[RefactoringSuggestion], title: str = "重构建议") -> None:
        """
        打印重构建议列表
        
        Args:
            suggestions: 建议列表
            title: 标题
        """
        self.print_header(title)
        
        if not suggestions:
            print(colorize("  ℹ️ 暂无重构建议", Colors.YELLOW))
            return
        
        # 分类统计
        quick_wins = [s for s in suggestions if s.effort == 'low' and s.risk == 'low']
        
        print(f"  📊 共 {len(suggestions)} 条建议")
        if quick_wins:
            print(f"  🚀 {colorize(str(len(quick_wins)), Colors.GREEN + Colors.BOLD)} 个快速改进项")
        print()
        
        for i, suggestion in enumerate(suggestions[:5], 1):
            self.print_suggestion(suggestion, i)
        
        if len(suggestions) > 5:
            print(f"\n  ... 还有 {len(suggestions) - 5} 条建议未显示")
        
        self.print_footer()
    
    def print_analysis_summary(self, summary: Dict[str, Any]) -> None:
        """
        打印分析摘要
        
        Args:
            summary: 分析摘要字典
        """
        self.print_header("项目分析摘要")
        
        print(f"  📁 目录: {summary.get('directory', 'N/A')}")
        print(f"  📄 总文件数: {colorize(str(summary.get('total_files', 0)), Colors.CYAN)}")
        print(f"  ✅ 成功分析: {colorize(str(summary.get('analyzed_files', 0)), Colors.GREEN)}")
        print(f"  ❌ 分析失败: {colorize(str(summary.get('error_files', 0)), Colors.RED)}")
        print()
        
        print(f"  📊 代码统计:")
        print(f"     总行数: {summary.get('total_lines', 0):,}")
        print(f"     函数数: {summary.get('total_functions', 0):,}")
        print(f"     类数: {summary.get('total_classes', 0):,}")
        print(f"     导入数: {summary.get('total_imports', 0):,}")
        print()
        
        print(f"  📈 复杂度:")
        print(f"     平均圈复杂度: {summary.get('avg_complexity', 0)}")
        print(f"     最大圈复杂度: {summary.get('max_complexity', 0)}")
        print()
        
        lang_stats = summary.get('language_stats', {})
        if lang_stats:
            print(f"  🌐 语言分布:")
            for lang, count in lang_stats.items():
                print(f"     • {lang}: {count} 文件")
        
        self.print_footer()
    
    def print_progress(self, current: int, total: int, message: str = "") -> None:
        """
        打印进度条
        
        Args:
            current: 当前进度
            total: 总数
            message: 进度消息
        """
        percent = current / total if total > 0 else 0
        bar_width = 40
        filled = int(bar_width * percent)
        bar = "█" * filled + "░" * (bar_width - filled)
        
        print(f"\r  [{bar}] {percent:.0%} {message}", end="", flush=True)
        
        if current >= total:
            print()
    
    def confirm(self, message: str) -> bool:
        """
        确认对话框
        
        Args:
            message: 确认消息
        
        Returns:
            是否确认
        """
        print()
        response = self.get_input(f"{message} (y/n): ").lower()
        return response in ('y', 'yes', '是', '确认')
    
    def show_message(self, message: str, msg_type: str = "info") -> None:
        """
        显示消息
        
        Args:
            message: 消息内容
            msg_type: 消息类型 (info/success/warning/error)
        """
        colors = {
            'info': Colors.CYAN,
            'success': Colors.GREEN,
            'warning': Colors.YELLOW,
            'error': Colors.RED
        }
        
        icons = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }
        
        color = colors.get(msg_type, Colors.WHITE)
        icon = icons.get(msg_type, '•')
        
        print(f"\n  {icon} {colorize(message, color)}")
    
    def wait_for_key(self, message: str = "按 Enter 键继续...") -> None:
        """等待用户按键"""
        print()
        try:
            input(colorize(f"  {message}", Colors.DIM))
        except (EOFError, KeyboardInterrupt):
            pass
    
    def run_interactive(self, analyze_callback: Callable, refactor_callback: Callable) -> None:
        """
        运行交互式主循环
        
        Args:
            analyze_callback: 分析回调函数
            refactor_callback: 重构回调函数
        """
        while self.running:
            self.clear()
            
            options = [
                ("analyze", "🔍 分析代码文件"),
                ("analyze_project", "📁 分析整个项目"),
                ("refactor", "🔧 重构代码文件"),
                ("batch", "🚀 批量重构项目"),
                ("help", "❓ 帮助信息"),
            ]
            
            self.print_menu(options, "主菜单")
            
            choice = self.get_input()
            
            if choice == "0":
                self.running = False
                self.show_message("感谢使用 RefactorPilot！", "success")
            elif choice in ("1", "analyze"):
                filepath = self.get_input("请输入文件路径: ")
                if filepath:
                    analyze_callback(filepath)
                    self.wait_for_key()
            elif choice in ("2", "analyze_project"):
                directory = self.get_input("请输入项目目录: ")
                if directory:
                    analyze_callback(directory, project=True)
                    self.wait_for_key()
            elif choice in ("3", "refactor"):
                filepath = self.get_input("请输入文件路径: ")
                if filepath:
                    refactor_callback(filepath)
                    self.wait_for_key()
            elif choice in ("4", "batch"):
                directory = self.get_input("请输入项目目录: ")
                if directory:
                    refactor_callback(directory, batch=True)
                    self.wait_for_key()
            elif choice in ("5", "help"):
                self.show_help()
                self.wait_for_key()
            else:
                self.show_message("无效选项，请重试", "error")
                self.wait_for_key()
    
    def show_help(self) -> None:
        """显示帮助信息"""
        self.print_header("帮助信息")
        
        help_text = """
RefactorPilot 是一款轻量级终端代码智能重构助手。

功能说明:
  🔍 分析 - 检测代码中的坏味道和问题
  🔧 重构 - 生成并应用重构建议
  🚀 批量 - 对整个项目进行批量重构

支持的坏味道检测:
  • 过长函数
  • 高圈复杂度
  • 参数过多
  • 魔法数字
  • 未使用变量
  • 代码行过长
  • 嵌套过深
  • 上帝类
  • 基本类型偏执

快捷键:
  Ctrl+C - 退出程序
  Enter  - 确认选择
"""
        print(help_text)
        self.print_footer()


def create_tui() -> TUI:
    """创建TUI实例"""
    return TUI()
