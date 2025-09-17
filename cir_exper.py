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

"""
bug 速记
>>> 2%3
         0.3333333333333333
>>> 3   
Goodbye!
(base) l-iang@monkey:/mnt/d/code/py-code/Experiment data compute$ p cir_exper.py 
============================================================
🔬 物理实验科学计算器 - Physics Lab Calculator 🔬
============================================================
💡 专为物理实验设计的智能计算器

🚀 快速上手指南:
  📏 单位后缀: 10k, 1.5M, 200n (支持 G/M/k/m/u/n)
  ⚡ 串联电阻: R(10k) + R(20k)  [返回 Resistor 对象]
  🔗 并联电阻: 10k | 20k        [直接数值计算，返回数值]
  📊 误差计算: 10.5 % 10        [测量值 % 真实值]
  💾 变量存储: result = 10k | 20k

🎯 设计亮点: | 运算符让并联计算更直观，无需创建对象!
⏰ 退出方式: 输入 'exit' 或按 Ctrl+D
============================================================

>>> 3.309%3.25
                0.018153846153846204
>>> 0.1972%0.188
                  0.04893617021276588
>>> 0.7%0.668
               0.04790419161676634
>>> 0.503%0.48
                0.04791666666666671
>>> 1.067%1.085
                 0.01658986175115209
>>> r=1k+2k+5.1k+330
                      r = 8430.0
>>> 1k/r
          0.11862396204033215
>>> _*5
         0.5931198102016608
>>> *2


2"""
from calculator import * 
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
    '-': {'template': '({left} - {right})', 'prec': 1},   # 减法
    '*': {'template': '({left} * {right})', 'prec': 2},   # 乘法
    '/': {'template': '({left} / {right})', 'prec': 2},   # 除法
    '^': {'template': '({left} ** {right})', 'prec': 3},  # 幂运算
    '|': {'template': 'quick_parrel({left}, {right})', 'prec': 2},  # 并联电阻
    '%': {'template': 'epercent({left}, {right})', 'prec': 3},      # 百分比误差
}

CALCULATOR_SUFFIXES = {
    'G': 1e9, 'M': 1e6, 'k': 1e3,      # 大单位: Giga, Mega, kilo
    'm': 1e-3, 'u': 1e-6, 'n': 1e-9    # 小单位: milli, micro, nano
}

REMAP_KEYS = {
    '\\': '|',  # 当用户按下反斜杠，我们视为竖线
    '\'':'%',  # 当用户按下单引号，我们视为百分号
    '<':'(',  # 当用户按下逗号，我们视为左括号
    '>':')',  # 当用户按下句号，我们视为右括号
}

def main():
    """主函数 - 创建并启动计算器"""
    try:
        # 使用自定义配置创建计算器实例
        calc = Calculator(
            symbols=CALCULATOR_SYMBOLS,
            operators=CALCULATOR_OPERATORS,
            suffixes=CALCULATOR_SUFFIXES,
            remap=Remap(REMAP_KEYS)
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