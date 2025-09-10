# 物理实验科学计算器 - 开发文档

## 简单说明（first read）
**以下内容我觉得比较重要但是ai没有写出来，其他的详细解释我是用ai生成的**

### 我想做一个什么东西
我想的是立足于华科，做一个专门用于实验的计算器和画图快捷控制器，这种脚本解析往深了做可以做出了一个python-- or matlab-- , 但是这样做并没有什么意义。我的想法是在一个基座下（我们可以把这个基座打造的非常好，就是语言解析calculator＋一个兼容性高的ui，同时要求这个基座非常容易扩展，下一个人只需要把想要运算的函数or绘图过程实现了，然后再调用一下接口即可）生长出各种各样针对某个实验的demo

### 一些我认为比较重要的思想
- 首先是模块化，在实现这个程序中，最后希望能够实现各计算器一键转化（比如某些计算器是物理实验，某些是电路实验），最后搭建几个专门应用于某些实验的快捷运算
- 其次是尊重自己的体验，这个计算器最重要的可能还是给我们自己用，我希望编写出的内容可以之间被我们流畅的使用

### 库的简单说明
如果是计算各种常用系数（比如线性相关度，百分比误差，方差等等，优先放在factor这个库里面
如果是电路相关的，放在circuits里面
其他内容可以请另外创建库

### 有待开发的能力
目前核心函数是calculator.py，已经能完成大部分操作
还有一些我觉得可以提升的地方：
- 首先是键位映射，进入计算器模式可以使用某些键替换某些键，比如我敲入的是a，实际终端显示的是^，这样的好处是可以极大的方便在键盘中使用计算器，这个功能已经有了，但是还没有进行实例化（也就是没有放上多少有用的键位映射）
- 其次是多变量解析，目前适用的主要是二元运算，我觉得将功能扩展为任意元运算会更加有用，
    例如：我敲入 D 10 20 30 10 30 d 表示计算D 到d 之间这些数的方差
- 然后我想加入计算器的继承（将计算器的各种约束看作是一个类，我们可以方便的再前一个demo中扩展新能力，同时不影响原来那个计算器的单独运作
- 绘图以及和绘图有关命令的兼容



## 项目架构

### 整体结构
```
Experiment data compute/
├── cir_exper.py         # 主启动文件，包含配置定义
├── calculator.py        # 核心计算器类
├── circuits.py          # 电路元件和计算功能
├── factors.py           # 误差分析功能
├── README.md           # 用户文档
└── DEVELOPER.md        # 开发文档（本文件）
```

### 模块依赖关系
```
cir_exper.py
    ├── calculator.py
    │   ├── circuits.py
    │   └── factors.py
    ├── circuits.py (直接导入用于配置)
    └── factors.py (直接导入用于配置)
```

## 核心组件详解

### 1. Calculator 类 (`calculator.py`)

#### 类设计理念
Calculator类采用了配置化设计，将符号表、运算符和单位后缀作为可配置参数，提高了代码的灵活性和可扩展性。

#### 构造函数详解
```python
def __init__(self, symbols=None, operators=None, suffixes=None):
```

**设计模式**: 策略模式 + 默认配置模式
- 允许运行时配置不同的符号表和运算符
- 提供合理的默认值，确保向后兼容性

#### 核心算法流程

##### 表达式处理流水线
```
用户输入 → 单位后缀展开 → 词法分析 → 语法分析 → 代码生成 → 执行
```

##### 1. 单位后缀展开 (`_expand_suffixes`)
```python
def _expand_suffixes(self, expr: str) -> str:
    # 正则表达式匹配：数字 + 后缀
    pattern = re.compile(r'(\d+\.?\d*)(' + '|'.join(self.SUFFIXES.keys()) + r')\b')
    
    def replace_suffix(match):
        value_str, suffix = match.groups()
        value = float(value_str) * self.SUFFIXES[suffix]
        return str(value)
        
    return pattern.sub(replace_suffix, expr)
```

**算法特点:**
- 使用正则表达式进行模式匹配
- 支持浮点数和整数
- 单词边界确保准确匹配

##### 2. 词法分析 (`_tokenize`)
```python
def _tokenize(self, expr: str) -> list:
    op_chars = ''.join(re.escape(k) for k in self.OPERATORS.keys())
    pattern = re.compile(
        r'(R\s*\([^)]+\))|'                 # 函数调用
        r'([a-zA-Z_][a-zA-Z0-9_]*)|'        # 变量名  
        r'(\d+\.?\d*(?:e[+-]?\d+)?)|\s*'    # 数字（包含科学记数法）
        r'([' + op_chars + '])|\s*'         # 运算符
        r'(\()|(\))'                        # 括号
    )
    # ... 处理逻辑
```

**设计要点:**
- 优先匹配函数调用（如`R(...)`）
- 支持标准的标识符命名规则
- 处理科学记数法
- 动态构建运算符字符集

##### 3. 语法分析 (`_parse_tokens`) 
使用**递归下降解析器**实现：

```python
def _parse_tokens(self, tokens: list) -> str:
    # 第一步：处理括号（递归）
    while '(' in tokens:
        # 找到最内层括号
        # 递归解析括号内容
        # 替换为解析结果
    
    # 第二步：按优先级处理运算符（从高到低）
    for prec in sorted(..., reverse=True):
        # 扫描并替换同优先级运算符
```

**算法复杂度:**
- 时间复杂度: O(n²) （最坏情况下嵌套括号）
- 空间复杂度: O(n)

#### 会话管理系统

```python
self.session_vars = {}    # 用户变量
self.history = []         # 计算历史
```

**特殊变量:**
- `_`: 自动保存最后一次计算结果
- 支持用户自定义变量名（符合Python标识符规则）

### 2. 配置系统 (`cir_exper.py`)

#### 配置结构设计

##### 符号表配置
```python
CALCULATOR_SYMBOLS = {
    'R': Resistor,                    # 类引用
    'quick_parrel': quick_parrel,     # 函数引用  
    'epercent': epercent,             # 函数引用
}
```

##### 运算符配置
```python
CALCULATOR_OPERATORS = {
    '+': {'template': '({left} + {right})', 'prec': 1},
    '|': {'template': 'quick_parrel({left}, {right})', 'prec': 2},
    '%': {'template': 'epercent({left}, {right})', 'prec': 3},
}
```

**运算符配置说明:**
- `template`: 代码生成模板，使用`{left}`和`{right}`占位符
- `prec`: 优先级，数字越大优先级越高

##### 单位后缀配置
```python
CALCULATOR_SUFFIXES = {
    'G': 1e9, 'M': 1e6, 'k': 1e3,      # 10^n形式
    'm': 1e-3, 'u': 1e-6, 'n': 1e-9    # 10^-n形式
}
```

### 3. 电路模块 (`circuits.py`)

#### Resistor 类设计

```python
class Resistor:
    def __init__(self, resistance_ohms):
        self.resistance = resistance_ohms

    def __add__(self, other):          # 串联运算
        if isinstance(other, Resistor):
            return Resistor(self.resistance + other.resistance)
        # ...

    def __mul__(self, other):          # 并联运算（重载*）
        if isinstance(other, Resistor):
            return Resistor((self.resistance * other.resistance) / 
                          (self.resistance + other.resistance))
        # ...
```

**设计模式**: 运算符重载
- `__add__`: 实现串联逻辑
- `__mul__`: 实现并联逻辑  
- 支持类型检查和错误处理

#### 快速并联函数
```python
def quick_parrel(r1, r2):
    return (r1 * r2) / (r1 + r2)
```

**注意**: 返回数值而非Resistor对象，用于`|`运算符

### 4. 误差分析模块 (`factors.py`)

```python
def epercent(value, true):
    if true == 0:
        raise ValueError("True value cannot be zero for percentage error calculation.")
    return abs((value - true) / true)
```

**数学公式**: |测量值 - 真实值| / |真实值|

## 扩展开发指南

### 1. 添加新的运算符

#### 步骤1: 在配置中定义运算符
```python
CALCULATOR_OPERATORS = {
    # 现有运算符...
    '**': {'template': 'pow({left}, {right})', 'prec': 4},  # 幂运算
    '//': {'template': '{left} // {right}', 'prec': 2},     # 整除
}
```

#### 步骤2: 实现后端函数（如果需要）
```python
def power_calculation(base, exponent):
    return pow(base, exponent)

# 添加到符号表
CALCULATOR_SYMBOLS['pow'] = power_calculation
```

### 2. 添加新的元件类型

#### 步骤1: 创建新类
```python
class Capacitor:
    def __init__(self, capacitance_farads):
        self.capacitance = capacitance_farads
    
    def __add__(self, other):  # 串联公式：1/C_total = 1/C1 + 1/C2
        if isinstance(other, Capacitor):
            total_inv = 1/self.capacitance + 1/other.capacitance
            return Capacitor(1/total_inv)
        raise ValueError("Can only add another Capacitor")
    
    def __mul__(self, other):  # 并联公式：C_total = C1 + C2  
        if isinstance(other, Capacitor):
            return Capacitor(self.capacitance + other.capacitance)
        raise ValueError("Can only multiply with another Capacitor")
```

#### 步骤2: 添加到符号表
```python
CALCULATOR_SYMBOLS['C'] = Capacitor
```

### 3. 扩展单位系统

```python
# 电容单位
CAPACITOR_SUFFIXES = {
    'F': 1,      # 法拉
    'mF': 1e-3,  # 毫法
    'uF': 1e-6,  # 微法
    'nF': 1e-9,  # 纳法  
    'pF': 1e-12, # 皮法
}

# 合并到主配置
CALCULATOR_SUFFIXES.update(CAPACITOR_SUFFIXES)
```

## 测试策略

### 1. 单元测试建议

```python
import unittest
from calculator import Calculator
from circuits import Resistor

class TestCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_suffix_expansion(self):
        self.assertEqual(self.calc._expand_suffixes("10k"), "10000.0")
        self.assertEqual(self.calc._expand_suffixes("1.5M"), "1500000.0")
    
    def test_resistor_operations(self):
        r1 = Resistor(1000)
        r2 = Resistor(2000)
        self.assertEqual((r1 + r2).resistance, 3000)
        self.assertAlmostEqual((r1 * r2).resistance, 666.67, places=2)
    
    def test_expression_parsing(self):
        # 测试复杂表达式
        result = self.calc.parse("R(1k) + R(2k)")
        self.assertIn("Resistor", result)
```

### 2. 集成测试

```python
def test_full_calculation_workflow():
    calc = Calculator()
    # 模拟用户输入序列
    test_cases = [
        ("R(1k) + R(2k)", "Resistor(3000.0 Ω)"),
        ("R(10k) | R(10k)", "5000.0"),
        ("100 % 95", "0.05263157894736842"),
    ]
    
    for expr, expected in test_cases:
        # 测试完整流程...
```

## 性能优化

### 1. 已知性能瓶颈

1. **正则表达式编译**: 每次调用都重新编译
   - **优化方案**: 类级别预编译正则表达式

2. **字符串操作**: 大量字符串拼接和替换
   - **优化方案**: 使用字符串构建器或模板引擎

3. **递归解析**: 深度嵌套时栈溢出风险
   - **优化方案**: 迭代式解析或尾递归优化

### 2. 优化建议

```python
class Calculator:
    # 类级别编译正则表达式
    _SUFFIX_PATTERN = re.compile(r'(\d+\.?\d*)([GMkumn])\b')
    _TOKEN_PATTERN = re.compile(r'...')  # 预编译词法模式
    
    def _expand_suffixes_optimized(self, expr):
        # 使用预编译的模式
        return self._SUFFIX_PATTERN.sub(self._replace_suffix, expr)
```

## 错误处理策略

### 1. 分层错误处理

```python
# 底层：基础验证错误
class CalculatorError(Exception):
    pass

class ParsingError(CalculatorError):
    pass

class EvaluationError(CalculatorError):  
    pass

# 应用层：用户友好的错误消息
def safe_evaluate(self, expr):
    try:
        return self.parse_and_evaluate(expr)
    except ParsingError as e:
        return f"语法错误: {e}"
    except EvaluationError as e:
        return f"计算错误: {e}"
    except Exception as e:
        return f"未知错误: {e}"
```

### 2. 输入验证

```python
def validate_expression(self, expr):
    # 括号匹配检查
    if expr.count('(') != expr.count(')'):
        raise ParsingError("括号不匹配")
    
    # 运算符合法性检查
    # 变量名合法性检查
    # ...
```

## 代码质量标准

### 1. 编码规范
- 遵循 PEP 8 Python编码规范
- 使用类型提示（Python 3.6+）
- 添加详细的文档字符串

### 2. 代码示例
```python
from typing import Dict, List, Optional, Union

def _tokenize(self, expr: str) -> List[str]:
    """词法分析器 - 将表达式分解为标记
    
    Args:
        expr: 待分析的表达式字符串
        
    Returns:
        标记列表，包含函数调用、变量名、数字、运算符、括号等
        
    Raises:
        ParsingError: 当表达式包含无法识别的字符时
        
    Example:
        >>> calc._tokenize("R(10k) + R(20k)")
        ['R(10000.0)', '+', 'R(20000.0)']
    """
```

## 部署和分发

### 1. 打包配置 (`setup.py`)
```python
from setuptools import setup, find_packages

setup(
    name="physics-calculator",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[],  # 无外部依赖
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'physics-calc=cir_exper:main',
        ],
    },
    # ... 其他元数据
)
```

### 2. 虚拟环境建议
```bash
# 创建虚拟环境
python -m venv physics-calc-env

# 激活环境
# Windows:
physics-calc-env\Scripts\activate
# Unix/Linux:  
source physics-calc-env/bin/activate

# 安装依赖（如果有）
pip install -r requirements.txt
```

## 贡献指南

### 1. 开发流程
1. Fork 项目到个人仓库
2. 创建功能分支 (`git checkout -b feature/new-feature`)
3. 编写代码和测试
4. 提交更改 (`git commit -am 'Add new feature'`)
5. 推送分支 (`git push origin feature/new-feature`)
6. 创建 Pull Request

### 2. 代码审查标准
- 代码功能完整性
- 测试覆盖率 > 80%
- 文档完整性
- 性能影响评估
- 向后兼容性

### 3. Issue 模板

```markdown
## Bug 报告
**描述**: 简要描述问题
**重现步骤**: 
1. 步骤1
2. 步骤2
**期望行为**: 描述期望的正确行为
**实际行为**: 描述实际观察到的行为
**环境信息**: Python版本、操作系统等
**附加信息**: 错误堆栈、截图等
```

## 路线图

### 短期目标 (v1.2)
- [ ] 增加电容器支持
- [ ] 改进错误提示信息
- [ ] 添加单元测试套件
- [ ] 性能优化

### 中期目标 (v2.0)  
- [ ] 图形用户界面
- [ ] 复数运算支持
- [ ] 公式推导功能
- [ ] 批量计算模式

### 长期目标 (v3.0)
- [ ] 插件系统
- [ ] Web界面
- [ ] 实验数据导入/导出
- [ ] 可视化图表生成

---

**注意**: 本文档会随着项目发展持续更新。如有疑问请提交Issue或联系维护团队。
