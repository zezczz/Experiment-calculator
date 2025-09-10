"""
物理实验科学计算器核心模块

提供Calculator类，支持电路计算、误差分析等功能。
包含交互式命令行界面，支持变量定义、单位后缀、自定义运算符等高级功能。
"""
import re
import readline  # 导入readline可以改善输入体验，如支持历史记录
from circuits import *
from factors import *


class Calculator:
    """物理实验科学计算器
    
    支持功能：
    - 电阻串联/并联计算
    - 百分比误差计算  
    - 单位后缀转换 (G, M, k, m, u, n)
    - 变量定义和使用
    - 交互式命令行界面
    """
    
    def __init__(self, symbols=None, operators=None, suffixes=None):
        """初始化计算器
        
        Args:
            symbols: 内置符号表字典，包含函数和类的映射
            operators: 自定义运算符定义字典
            suffixes: 单位后缀定义字典
        """
        self.history = []
        # 会话变量，用于存储用户定义的变量
        self.session_vars = {}
        
        # 内置符号表 - 如果没有提供则使用默认值
        self.symbols = symbols if symbols is not None else {
            'R': Resistor,
            'quick_parrel': quick_parrel,
            'epercent': epercent,
        }
        
        # 自定义运算符定义 - 如果没有提供则使用默认值
        self.OPERATORS = operators if operators is not None else {
            '+': {'template': '({left} + {right})', 'prec': 1},   # 串联
            '|': {'template': 'quick_parrel({left}, {right})', 'prec': 2},  # 并联
            '%': {'template': 'epercent({left}, {right})', 'prec': 3},      # 误差
        }
        
        # 单位后缀定义和它们的乘数 - 如果没有提供则使用默认值
        self.SUFFIXES = suffixes if suffixes is not None else {
            'G': 1e9, 'M': 1e6, 'k': 1e3,      # 大单位
            'm': 1e-3, 'u': 1e-6, 'n': 1e-9    # 小单位
        }

    def _expand_suffixes(self, expr: str) -> str:
        """预处理器：展开数字后面的单位后缀
        
        Args:
            expr: 包含单位后缀的表达式，如 "10k", "1.5M", "200n"
            
        Returns:
            展开后的表达式，如 "10000.0", "1500000.0", "2e-07"
        """
        # 正则表达式：匹配数字+后缀的模式
        pattern = re.compile(r'(\d+\.?\d*)(' + '|'.join(self.SUFFIXES.keys()) + r')\b')
        
        def replace_suffix(match):
            value_str, suffix = match.groups()
            value = float(value_str) * self.SUFFIXES[suffix]
            return str(value)
            
        return pattern.sub(replace_suffix, expr)

    def _tokenize(self, expr: str) -> list:
        """词法分析器 - 将表达式分解为标记
        
        Args:
            expr: 待分析的表达式
            
        Returns:
            标记列表，包含函数调用、变量名、数字、运算符、括号等
        """
        op_chars = ''.join(re.escape(k) for k in self.OPERATORS.keys())
        pattern = re.compile(
            r'(R\s*\([^)]+\))|'                 # 匹配 R(...)
            r'([a-zA-Z_][a-zA-Z0-9_]*)|'        # 匹配变量名
            r'(\d+\.?\d*(?:e[+-]?\d+)?)|\s*'    # 匹配数字
            r'([' + op_chars + '])|\s*'         # 匹配自定义运算符
            r'(\()|(\))'                        # 匹配括号
        )
        tokens = [t for t in pattern.findall(expr) if any(t)]
        return [''.join(t) for t in tokens]

    def _parse_tokens(self, tokens: list) -> str:
        """语法分析器 - 构建语法树并处理运算符优先级
        
        Args:
            tokens: 标记列表
            
        Returns:
            可执行的Python表达式字符串
        """
        # 处理括号：从内到外递归解析
        while '(' in tokens:
            start = -1
            for i, token in enumerate(tokens):
                if token == '(':
                    start = i
            
            # 找到匹配的右括号
            balance = 0
            for end in range(start + 1, len(tokens)):
                if tokens[end] == '(':
                    balance += 1
                elif tokens[end] == ')':
                    if balance == 0:
                        break
                    balance -= 1
            
            # 递归解析括号内的内容
            sub_tokens = tokens[start+1:end]
            parsed_sub_expr = self._parse_tokens(sub_tokens)
            tokens = tokens[:start] + [f"({parsed_sub_expr})"] + tokens[end+1:]

        # 按运算符优先级处理：从高优先级到低优先级
        for prec in sorted(set(op['prec'] for op in self.OPERATORS.values()), reverse=True):
            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token in self.OPERATORS and self.OPERATORS[token]['prec'] == prec:
                    template = self.OPERATORS[token]['template']
                    left, right = tokens[i-1], tokens[i+1]
                    new_expr = template.format(left=left, right=right)
                    tokens = tokens[:i-1] + [new_expr] + tokens[i+2:]
                    i = 0  # 重新开始扫描
                else:
                    i += 1
        return tokens[0] if tokens else ""

    def parse(self, expr: str) -> str:
        """公开的解析方法，整合所有解析步骤
        
        Args:
            expr: 待解析的表达式
            
        Returns:
            可执行的Python表达式
        """
        if not expr:
            return ""
        
        tokens = self._tokenize(expr)
        intermediate_expr = self._parse_tokens(tokens)
        # 将电阻对象转换为阻值
        final_expr = re.sub(r'(R\s*\([^)]+\))', r'\1.resistance', intermediate_expr)
        return final_expr

    def begin(self):
        """启动交互式计算器主循环"""
        print("=" * 60)
        print("🔬 物理实验科学计算器 - Physics Lab Calculator 🔬")
        print("=" * 60)
        print("💡 专为物理实验设计的智能计算器")
        print()
        print("🚀 快速上手指南:")
        print("  📏 单位后缀: 10k, 1.5M, 200n (支持 G/M/k/m/u/n)")
        print("  ⚡ 串联电阻: R(10k) + R(20k)  [返回 Resistor 对象]")
        print("  🔗 并联电阻: 10k | 20k        [直接数值计算，返回数值]")
        print("  📊 误差计算: 10.5 % 10        [测量值 % 真实值]")
        print("  💾 变量存储: result = 10k | 20k")
        print()
        print("🎯 设计亮点: | 运算符让并联计算更直观，无需创建对象!")
        print("⏰ 退出方式: 输入 'exit' 或按 Ctrl+D")
        print("=" * 60)
        print()
        
        while True:
            try:
                # 组合执行环境，优先使用会话变量
                eval_env = {**self.symbols, **self.session_vars}
                
                expr_input = input(">>> ")
                if expr_input.strip().lower() == 'exit':
                    break

                # 步骤1: 展开单位后缀
                expr_expanded = self._expand_suffixes(expr_input)

                # 步骤2: 检查是否为变量赋值
                if '=' in expr_expanded:
                    var_name, expr_to_calc = [s.strip() for s in expr_expanded.split('=', 1)]
                    
                    # 验证变量名
                    if not var_name.isidentifier():
                        raise ValueError(f"'{var_name}' is not a valid variable name.")
                    
                    # 解析并计算表达式
                    parsed_expr = self.parse(expr_to_calc)
                    result = eval(parsed_expr, {}, eval_env)
                    
                    # 存储到会话变量中
                    self.session_vars[var_name] = result
                    print(f"  {var_name} = {result}")

                # 步骤3: 普通表达式计算
                else:
                    parsed_expr = self.parse(expr_expanded)
                    result = eval(parsed_expr, {}, eval_env)
                    
                    # 记录历史并存储最后结果
                    self.history.append((expr_input, result))
                    self.session_vars['_'] = result  # 最后一个结果存储在 '_' 中
                    print(f"  {result}")

            # 通过捕获 EOFError 来实现 Ctrl+D 退出
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def get_history(self):
        """获取计算历史记录"""
        return self.history.copy()
    
    def get_variables(self):
        """获取当前会话变量"""
        return self.session_vars.copy()
    
    def clear_history(self):
        """清空历史记录"""
        self.history.clear()
    
    def clear_variables(self):
        """清空会话变量"""
        self.session_vars.clear()
