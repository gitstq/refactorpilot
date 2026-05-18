"""
重构建议生成器模块

基于检测到的坏味道生成具体的重构建议
"""

import ast
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from .detectors import CodeSmell, SmellType, SmellSeverity


@dataclass
class RefactoringSuggestion:
    """重构建议数据类"""
    title: str
    description: str
    before_code: str
    after_code: str
    benefits: List[str]
    effort: str  # 'low', 'medium', 'high'
    risk: str  # 'low', 'medium', 'high'
    applicable_smells: List[SmellType]


class RefactoringSuggester:
    """
    重构建议生成器
    
    根据检测到的代码坏味道生成具体的重构方案
    """
    
    def __init__(self):
        """初始化建议生成器"""
        self.suggestions: List[RefactoringSuggestion] = []
    
    def generate_suggestions(self, smells: List[CodeSmell], source: str, tree: ast.AST) -> List[RefactoringSuggestion]:
        """
        基于坏味道生成重构建议
        
        Args:
            smells: 检测到的坏味道列表
            source: 源代码
            tree: AST语法树
        
        Returns:
            重构建议列表
        """
        self.suggestions = []
        
        for smell in smells:
            suggestion = self._generate_for_smell(smell, source, tree)
            if suggestion:
                self.suggestions.append(suggestion)
        
        return self.suggestions
    
    def _generate_for_smell(self, smell: CodeSmell, source: str, tree: ast.AST) -> Optional[RefactoringSuggestion]:
        """
        为特定坏味道生成建议
        
        Args:
            smell: 坏味道
            source: 源代码
            tree: AST语法树
        
        Returns:
            重构建议，如果不适用返回None
        """
        generators = {
            SmellType.LONG_FUNCTION: self._suggest_extract_method,
            SmellType.HIGH_COMPLEXITY: self._suggest_reduce_complexity,
            SmellType.TOO_MANY_ARGUMENTS: self._suggest_introduce_parameter_object,
            SmellType.MAGIC_NUMBER: self._suggest_extract_constant,
            SmellType.UNUSED_VARIABLE: self._suggest_remove_unused,
            SmellType.LONG_LINE: self._suggest_break_line,
            SmellType.NESTED_DEPTH: self._suggest_guard_clauses,
            SmellType.GOD_CLASS: self._suggest_extract_class,
            SmellType.SWITCH_STATEMENTS: self._suggest_replace_conditional_with_polymorphism,
            SmellType.PRIMITIVE_OBSESSION: self._suggest_introduce_data_class,
        }
        
        generator = generators.get(smell.smell_type)
        if generator:
            return generator(smell, source, tree)
        
        return None
    
    def _suggest_extract_method(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议提取方法"""
        return RefactoringSuggestion(
            title="提取方法 (Extract Method)",
            description="将长函数中的逻辑块提取为独立的函数，提高代码可读性和可复用性",
            before_code="""def process_order(order):
    # 验证订单
    if not order.items:
        return None
    if order.total <= 0:
        return None
    
    # 计算折扣
    discount = 0
    if order.customer.is_vip:
        discount = order.total * 0.1
    if order.total > 1000:
        discount += order.total * 0.05
    
    # 生成发票
    invoice = Invoice()
    invoice.order_id = order.id
    invoice.amount = order.total - discount
    invoice.date = datetime.now()
    
    return invoice""",
            after_code="""def process_order(order):
    if not _is_valid_order(order):
        return None
    
    discount = _calculate_discount(order)
    return _generate_invoice(order, discount)

def _is_valid_order(order):
    return order.items and order.total > 0

def _calculate_discount(order):
    discount = 0
    if order.customer.is_vip:
        discount = order.total * 0.1
    if order.total > 1000:
        discount += order.total * 0.05
    return discount

def _generate_invoice(order, discount):
    invoice = Invoice()
    invoice.order_id = order.id
    invoice.amount = order.total - discount
    invoice.date = datetime.now()
    return invoice""",
            benefits=[
                "提高代码可读性，每个函数职责单一",
                "便于单元测试，可以独立测试每个函数",
                "减少重复代码，提取的方法可以被复用",
                "降低函数复杂度，便于理解和维护"
            ],
            effort="medium",
            risk="low",
            applicable_smells=[SmellType.LONG_FUNCTION]
        )
    
    def _suggest_reduce_complexity(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议降低复杂度"""
        return RefactoringSuggestion(
            title="降低圈复杂度",
            description="通过提取函数、使用卫语句和简化条件来降低圈复杂度",
            before_code="""def calculate_price(product, customer, quantity):
    if product and customer:
        if quantity > 0:
            base_price = product.price * quantity
            if customer.is_vip:
                if quantity > 10:
                    return base_price * 0.8
                else:
                    return base_price * 0.9
            else:
                if quantity > 20:
                    return base_price * 0.95
                else:
                    return base_price
        else:
            return 0
    else:
        return 0""",
            after_code="""def calculate_price(product, customer, quantity):
    if not product or not customer or quantity <= 0:
        return 0
    
    base_price = product.price * quantity
    return base_price * _get_discount_rate(customer, quantity)

def _get_discount_rate(customer, quantity):
    if customer.is_vip:
        return 0.8 if quantity > 10 else 0.9
    return 0.95 if quantity > 20 else 1.0""",
            benefits=[
                "显著降低圈复杂度，提高代码可测试性",
                "使用卫语句提前返回，减少嵌套层级",
                "提取折扣逻辑，便于修改和扩展",
                "代码更加扁平，易于理解"
            ],
            effort="medium",
            risk="low",
            applicable_smells=[SmellType.HIGH_COMPLEXITY, SmellType.NESTED_DEPTH]
        )
    
    def _suggest_introduce_parameter_object(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议引入参数对象"""
        return RefactoringSuggestion(
            title="引入参数对象 (Introduce Parameter Object)",
            description="将多个相关参数封装为一个对象，简化函数签名",
            before_code="""def create_user(
    first_name, last_name, email, phone,
    street, city, state, zip_code,
    is_active, is_verified, created_at
):
    pass

# 调用时
user = create_user(
    "John", "Doe", "john@example.com", "123-456-7890",
    "123 Main St", "New York", "NY", "10001",
    True, False, datetime.now()
)""",
            after_code="""@dataclass
class UserInfo:
    first_name: str
    last_name: str
    email: str
    phone: str

@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str

@dataclass
class UserStatus:
    is_active: bool
    is_verified: bool
    created_at: datetime

def create_user(info: UserInfo, address: Address, status: UserStatus):
    pass

# 调用时
user = create_user(
    UserInfo("John", "Doe", "john@example.com", "123-456-7890"),
    Address("123 Main St", "New York", "NY", "10001"),
    UserStatus(True, False, datetime.now())
)""",
            benefits=[
                "减少函数参数数量，提高可读性",
                "相关数据封装在一起，便于传递",
                "可以添加验证逻辑到数据类中",
                "便于扩展，添加新字段不需要修改函数签名"
            ],
            effort="medium",
            risk="medium",
            applicable_smells=[SmellType.TOO_MANY_ARGUMENTS]
        )
    
    def _suggest_extract_constant(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议提取常量"""
        return RefactoringSuggestion(
            title="提取常量 (Extract Constant)",
            description="将魔法数字提取为有意义的命名常量",
            before_code="""def calculate_shipping(weight):
    if weight <= 1:
        return 5.0
    elif weight <= 5:
        return 10.0
    elif weight <= 10:
        return 15.0
    else:
        return 15.0 + (weight - 10) * 1.5""",
            after_code="""# 运费常量
SHIPPING_TIER_1_MAX_WEIGHT = 1  # kg
SHIPPING_TIER_1_COST = 5.0

SHIPPING_TIER_2_MAX_WEIGHT = 5
SHIPPING_TIER_2_COST = 10.0

SHIPPING_TIER_3_MAX_WEIGHT = 10
SHIPPING_TIER_3_COST = 15.0

SHIPPING_OVERAGE_RATE = 1.5

def calculate_shipping(weight):
    if weight <= SHIPPING_TIER_1_MAX_WEIGHT:
        return SHIPPING_TIER_1_COST
    elif weight <= SHIPPING_TIER_2_MAX_WEIGHT:
        return SHIPPING_TIER_2_COST
    elif weight <= SHIPPING_TIER_3_MAX_WEIGHT:
        return SHIPPING_TIER_3_COST
    else:
        return SHIPPING_TIER_3_COST + (weight - SHIPPING_TIER_3_MAX_WEIGHT) * SHIPPING_OVERAGE_RATE""",
            benefits=[
                "提高代码可读性，常量的含义一目了然",
                "便于维护，修改常量值只需改一处",
                "避免魔法数字带来的困惑",
                "便于配置化管理"
            ],
            effort="low",
            risk="low",
            applicable_smells=[SmellType.MAGIC_NUMBER]
        )
    
    def _suggest_remove_unused(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议删除未使用变量"""
        return RefactoringSuggestion(
            title="删除未使用代码",
            description="删除未使用的变量或在其名称前加下划线表示有意忽略",
            before_code="""def process_data(data):
    result = []
    temp = []  # 从未使用
    
    for item in data:
        processed = transform(item)
        result.append(processed)
    
    unused_var = 42  # 从未使用
    return result""",
            after_code="""def process_data(data):
    result = []
    
    for item in data:
        processed = transform(item)
        result.append(processed)
    
    return result""",
            benefits=[
                "减少代码混乱，提高可读性",
                "避免维护未使用的代码",
                "减少内存占用",
                "消除潜在的bug来源"
            ],
            effort="low",
            risk="low",
            applicable_smells=[SmellType.UNUSED_VARIABLE]
        )
    
    def _suggest_break_line(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议拆分长行"""
        return RefactoringSuggestion(
            title="拆分长行",
            description="将过长的代码行拆分为多行，提高可读性",
            before_code="""result = calculate_something(very_long_parameter_name_1, very_long_parameter_name_2, very_long_parameter_name_3, very_long_parameter_name_4)""",
            after_code="""result = calculate_something(
    very_long_parameter_name_1,
    very_long_parameter_name_2,
    very_long_parameter_name_3,
    very_long_parameter_name_4
)""",
            benefits=[
                "提高代码可读性",
                "便于版本控制，单行修改更易追踪",
                "符合PEP 8规范"
            ],
            effort="low",
            risk="low",
            applicable_smells=[SmellType.LONG_LINE]
        )
    
    def _suggest_guard_clauses(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议使用卫语句"""
        return RefactoringSuggestion(
            title="使用卫语句 (Guard Clauses)",
            description="使用卫语句提前返回，减少嵌套层级",
            before_code="""def get_discount(order):
    if order.is_valid:
        if order.customer.is_active:
            if order.total > 100:
                return order.total * 0.1
            else:
                return 0
        else:
            return 0
    else:
        return 0""",
            after_code="""def get_discount(order):
    if not order.is_valid:
        return 0
    if not order.customer.is_active:
        return 0
    if order.total <= 100:
        return 0
    
    return order.total * 0.1""",
            benefits=[
                "减少嵌套层级，代码更扁平",
                "每个条件独立，易于理解",
                "减少else分支，简化逻辑",
                "提高代码可读性"
            ],
            effort="low",
            risk="low",
            applicable_smells=[SmellType.NESTED_DEPTH]
        )
    
    def _suggest_extract_class(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议提取类"""
        return RefactoringSuggestion(
            title="提取类 (Extract Class)",
            description="将大类的职责拆分给多个小类",
            before_code="""class OrderManager:
    # 订单相关
    def create_order(self, items): pass
    def cancel_order(self, order_id): pass
    def get_order_status(self, order_id): pass
    
    # 库存相关
    def check_inventory(self, product_id): pass
    def update_stock(self, product_id, quantity): pass
    def get_stock_level(self, product_id): pass
    
    # 支付相关
    def process_payment(self, order, method): pass
    def refund_payment(self, order): pass
    def get_payment_status(self, order): pass
    
    # 物流相关
    def schedule_delivery(self, order): pass
    def track_shipment(self, tracking_id): pass
    def update_delivery_status(self, order, status): pass""",
            after_code="""class OrderService:
    def create_order(self, items): pass
    def cancel_order(self, order_id): pass
    def get_order_status(self, order_id): pass

class InventoryService:
    def check_inventory(self, product_id): pass
    def update_stock(self, product_id, quantity): pass
    def get_stock_level(self, product_id): pass

class PaymentService:
    def process_payment(self, order, method): pass
    def refund_payment(self, order): pass
    def get_payment_status(self, order): pass

class LogisticsService:
    def schedule_delivery(self, order): pass
    def track_shipment(self, tracking_id): pass
    def update_delivery_status(self, order, status): pass""",
            benefits=[
                "每个类职责单一，符合单一职责原则",
                "便于测试，每个类可以独立测试",
                "提高代码可维护性",
                "便于团队协作，不同模块可由不同开发者维护"
            ],
            effort="high",
            risk="medium",
            applicable_smells=[SmellType.GOD_CLASS]
        )
    
    def _suggest_replace_conditional_with_polymorphism(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议用多态替代条件"""
        return RefactoringSuggestion(
            title="用多态替代条件 (Replace Conditional with Polymorphism)",
            description="使用策略模式或多态替代复杂的条件分支",
            before_code="""class Employee:
    def __init__(self, type, salary):
        self.type = type
        self.salary = salary
    
    def calculate_bonus(self):
        if self.type == "engineer":
            return self.salary * 0.1
        elif self.type == "manager":
            return self.salary * 0.2
        elif self.type == "sales":
            return self.salary * 0.15
        else:
            return 0""",
            after_code="""from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, salary):
        self.salary = salary
    
    @abstractmethod
    def calculate_bonus(self):
        pass

class Engineer(Employee):
    def calculate_bonus(self):
        return self.salary * 0.1

class Manager(Employee):
    def calculate_bonus(self):
        return self.salary * 0.2

class Sales(Employee):
    def calculate_bonus(self):
        return self.salary * 0.15""",
            benefits=[
                "消除复杂的条件分支",
                "新增类型时无需修改现有代码（开闭原则）",
                "每个类型的行为封装在自己的类中",
                "便于扩展和维护"
            ],
            effort="high",
            risk="medium",
            applicable_smells=[SmellType.SWITCH_STATEMENTS]
        )
    
    def _suggest_introduce_data_class(self, smell: CodeSmell, source: str, tree: ast.AST) -> RefactoringSuggestion:
        """建议引入数据类"""
        return RefactoringSuggestion(
            title="引入数据类 (Introduce Data Class)",
            description="将相关的基本类型参数封装为数据类",
            before_code="""def move_rectangle(x, y, width, height, dx, dy):
    new_x = x + dx
    new_y = y + dy
    return (new_x, new_y, width, height)

# 调用
rect = move_rectangle(10, 20, 100, 50, 5, 5)""",
            after_code="""from dataclasses import dataclass

@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float
    
    def move(self, dx: float, dy: float) -> 'Rectangle':
        return Rectangle(
            x=self.x + dx,
            y=self.y + dy,
            width=self.width,
            height=self.height
        )

# 调用
rect = Rectangle(10, 20, 100, 50)
moved_rect = rect.move(5, 5)""",
            benefits=[
                "相关数据封装在一起，表达更清晰的概念",
                "可以在数据类中添加行为方法",
                "提高类型安全性",
                "便于验证和约束"
            ],
            effort="medium",
            risk="low",
            applicable_smells=[SmellType.PRIMITIVE_OBSESSION]
        )
    
    def get_suggestions_by_effort(self, effort: str) -> List[RefactoringSuggestion]:
        """按工作量筛选建议"""
        return [s for s in self.suggestions if s.effort == effort]
    
    def get_suggestions_by_risk(self, risk: str) -> List[RefactoringSuggestion]:
        """按风险筛选建议"""
        return [s for s in self.suggestions if s.risk == risk]
    
    def get_quick_wins(self) -> List[RefactoringSuggestion]:
        """获取快速改进项（低工作量低风险）"""
        return [
            s for s in self.suggestions
            if s.effort == 'low' and s.risk == 'low'
        ]
