#!/usr/bin/env python3
"""
物理实验科学计算器 - 主启动文件

这是一个专为物理实验设计的交互式科学计算器。
支持电路计算、误差分析、单位后缀转换等功能。

使用方法：
    python cir_exper.py

示例：
    >>> R(10k) + R(20k)      # 串联电阻
    >>> R(10k) | R(20k)      # 并联电阻  
    >>> 10.5 % 10            # 百分比误差
    >>> r1 = R(1.5M)         # 变量定义
"""

from calculator import Calculator
from circuits import Resistor, quick_parrel
from factors import epercent


# 计算器配置定义
CALCULATOR_SYMBOLS = {
    'R': Resistor,
    'quick_parrel': quick_parrel,
    'epercent': epercent,
}

CALCULATOR_OPERATORS = {
    '+': {'template': '({left} + {right})', 'prec': 1},   # 串联电阻
    '|': {'template': 'quick_parrel({left}, {right})', 'prec': 2},  # 并联电阻
    '%': {'template': 'epercent({left}, {right})', 'prec': 3},      # 百分比误差
}

CALCULATOR_SUFFIXES = {
    'G': 1e9, 'M': 1e6, 'k': 1e3,      # 大单位: Giga, Mega, kilo
    'm': 1e-3, 'u': 1e-6, 'n': 1e-9    # 小单位: milli, micro, nano
}


def main():
    """主函数 - 创建并启动计算器"""
    try:
        # 使用自定义配置创建计算器实例
        calc = Calculator(
            symbols=CALCULATOR_SYMBOLS,
            operators=CALCULATOR_OPERATORS,
            suffixes=CALCULATOR_SUFFIXES
        )
        calc.begin()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1
    return 0


if __name__ == '__main__':
    exit(main())