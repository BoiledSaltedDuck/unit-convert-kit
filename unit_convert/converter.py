#!/usr/bin/env python3
"""
unit-convert-kit - 单位换算工具
功能：长度、重量、温度、面积、体积、数据大小等单位换算，批量文件单位替换
用法：unit-convert [数值] [源单位] [目标单位]
      unit-convert list
      unit-convert batch [文件] [源单位] [目标单位]
"""
import sys
import re
from pathlib import Path

# ========== 单位换算表 ==========

# 长度 (基准: 米)
LENGTH = {
    "mm": 0.001, "cm": 0.01, "dm": 0.1, "m": 1.0, "km": 1000.0,
    "in": 0.0254, "inch": 0.0254, "ft": 0.3048, "foot": 0.3048,
    "yard": 0.9144, "yd": 0.9144, "mile": 1609.344, "mi": 1609.344,
    "li": 500.0, "zhang": 3.33333, "chi": 0.33333, "cun": 0.03333,
}

# 重量 (基准: 克)
WEIGHT = {
    "mg": 0.001, "g": 1.0, "kg": 1000.0, "t": 1000000.0,
    "oz": 28.3495, "lb": 453.592, "stone": 6350.29,
    "jin": 500.0, "liang": 50.0, "carat": 0.2, "ct": 0.2,
}

# 温度 (特殊处理)
TEMPERATURE_UNITS = {"c", "celsius", "f", "fahrenheit", "k", "kelvin"}

# 面积 (基准: 平方米)
AREA = {
    "mm2": 0.000001, "cm2": 0.0001, "dm2": 0.01, "m2": 1.0,
    "km2": 1000000.0, "ha": 10000.0, "acre": 4046.86,
    "mu": 666.667, "sqft": 0.092903, "sqin": 0.00064516,
}

# 体积 (基准: 升)
VOLUME = {
    "ml": 0.001, "l": 1.0, "m3": 1000.0,
    "gal": 3.78541, "qt": 0.946353, "pt": 0.473176,
    "cup": 0.236588, "floz": 0.0295735,
}

# 数据大小 (基准: 字节)
DATA = {
    "b": 1, "byte": 1, "kb": 1024, "mb": 1024**2, "gb": 1024**3,
    "tb": 1024**4, "pb": 1024**5,
    "kib": 1024, "mib": 1024**2, "gib": 1024**3, "tib": 1024**4,
}

CATEGORIES = {
    "length": ("长度", LENGTH, ""),
    "weight": ("重量", WEIGHT, ""),
    "temperature": ("温度", TEMPERATURE_UNITS, "°"),
    "area": ("面积", AREA, ""),
    "volume": ("体积", VOLUME, ""),
    "data": ("数据大小", DATA, ""),
}


def convert_value(value, from_unit, to_unit):
    """执行单位换算"""
    from_u = from_unit.lower()
    to_u = to_unit.lower()

    # 检查温度
    if from_u in TEMPERATURE_UNITS and to_u in TEMPERATURE_UNITS:
        return _convert_temperature(value, from_u, to_u)

    # 检查各类别
    for cat_name, (cat_label, units, prefix) in CATEGORIES.items():
        if from_u in units and to_u in units:
            if isinstance(units, dict):
                base = value * units[from_u]
                result = base / units[to_u]
                return result
            break

    raise ValueError(f"不支持的单位: {from_unit} -> {to_unit}")


def _convert_temperature(value, from_u, to_u):
    """温度特殊换算"""
    # 统一到摄氏度
    if from_u in ("c", "celsius"):
        c = value
    elif from_u in ("f", "fahrenheit"):
        c = (value - 32) * 5 / 9
    elif from_u in ("k", "kelvin"):
        c = value - 273.15
    else:
        raise ValueError(f"不支持的温度单位: {from_u}")

    # 从摄氏度转换到目标
    if to_u in ("c", "celsius"):
        return c
    elif to_u in ("f", "fahrenheit"):
        return c * 9 / 5 + 32
    elif to_u in ("k", "kelvin"):
        return c + 273.15
    raise ValueError(f"不支持的温度单位: {to_u}")


def _find_unit_category(unit):
    """查找单位所属类别"""
    u = unit.lower()
    for cat_name, (cat_label, units, prefix) in CATEGORIES.items():
        if isinstance(units, dict):
            if u in units:
                return cat_name, cat_label
        elif isinstance(units, set):
            if u in units:
                return cat_name, cat_label
    return None, None


def format_result(value, from_unit, to_unit, result):
    """格式化输出"""
    cat_name, cat_label = _find_unit_category(from_unit)
    prefix = CATEGORIES.get(cat_name, ("", {}, ""))[2] if cat_name else ""

    # 格式化数值
    if abs(result) < 0.001 or abs(result) > 1e9:
        result_str = f"{result:.6e}"
    elif result == int(result):
        result_str = f"{int(result)}"
    else:
        # 智能小数位
        if abs(result) < 1:
            result_str = f"{result:.6f}".rstrip('0').rstrip('.')
        elif abs(result) < 100:
            result_str = f"{result:.4f}".rstrip('0').rstrip('.')
        elif abs(result) < 10000:
            result_str = f"{result:.2f}".rstrip('0').rstrip('.')
        else:
            result_str = f"{result:.2f}"

    return f"{value} {from_unit} = {result_str} {to_unit}"


def list_units():
    """列出所有支持的单位"""
    for cat_name, (cat_label, units, prefix) in CATEGORIES.items():
        print(f"\n[{cat_label}]")
        if isinstance(units, dict):
            for unit in sorted(units.keys(), key=lambda x: units[x]):
                base = units[unit]
                base_str = f"{base:.6e}".rstrip('0').rstrip('.')
                print(f"  {unit:12s} = {base_str} {cat_label == '温度' and '°' or cat_label == '数据大小' and 'bytes' or f'基准单位'}")
        elif isinstance(units, set):
            for unit in sorted(units):
                print(f"  {unit}")
    print()


def batch_convert(input_file, from_unit, to_unit, output_file=None):
    """批量转换文件中的数值单位"""
    p = Path(input_file)
    if not p.exists():
        print(f"错误：文件 {input_file} 不存在")
        return False

    try:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"错误：读取文件失败: {e}")
        return False

    # 匹配数值+单位模式
    escaped_from = re.escape(from_unit)
    pattern = rf'(\d+(?:\.\d+)?)\s*{escaped_from}'
    
    def repl(match):
        val = float(match.group(1))
        try:
            result = convert_value(val, from_unit, to_unit)
            # 格式化结果
            if result == int(result):
                return f"{int(result)}{to_unit}"
            else:
                return f"{result:.4f}{to_unit}".rstrip('0').rstrip('.') + to_unit if isinstance(to_unit, str) else f"{result:.4f}{to_unit}"
        except Exception:
            return match.group(0)

    pattern_compiled = re.compile(r'(\d+(?:\.\d+)?)\s*' + re.escape(from_unit))
    count_before = len(pattern_compiled.findall(content))
    
    new_content = pattern_compiled.sub(repl, content)

    count_after = len(re.compile(r'(\d+(?:\.\d+)?)\s*' + re.escape(to_unit)).findall(new_content))

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"已保存到: {output_file}")
    else:
        print(new_content)

    print(f"\n完成！替换了 {count_after} 处单位 ({from_unit} → {to_unit})")
    return True


def _show_promotion():
    print("\n" + "=" * 55)
    print("  🔧 unit-convert-kit - 单位换算工具")
    print("  📦 pip install unit-convert-kit")
    print("  ☕ 如果帮到了您，欢迎打赏支持:")
    print("     USDT(TRC20): TMPQygMkv42QPeyYnkxMkPwsqs7udbD2Aa")
    print("  ⭐ https://github.com/BoiledSaltedDuck/unit-convert-kit")
    print("=" * 55)


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  单位换算:   unit-convert [数值] [源单位] [目标单位]")
        print("  列出单位:   unit-convert list")
        print("  批量替换:   unit-convert batch [文件] [源单位] [目标单位]")
        print()
        print("示例:")
        print("  unit-convert 100 cm m")
        print("  unit-convert 32 f c")
        print("  unit-convert 1.5 kg lb")
        print("  unit-convert 1024 mb gb")
        print("  unit-convert list")
        print("  unit-convert batch data.txt inch cm")
        sys.exit(1)

    if sys.argv[1] == "list":
        list_units()
        _show_promotion()
        sys.exit(0)

    if sys.argv[1] == "batch":
        if len(sys.argv) < 5:
            print("用法: unit-convert batch [文件] [源单位] [目标单位]")
            sys.exit(1)
        output = sys.argv[5] if len(sys.argv) > 5 else None
        success = batch_convert(sys.argv[2], sys.argv[3], sys.argv[4], output)
        if success:
            _show_promotion()
        sys.exit(0 if success else 1)

    if len(sys.argv) < 4:
        print("用法: unit-convert [数值] [源单位] [目标单位]")
        sys.exit(1)

    try:
        value = float(sys.argv[1])
    except ValueError:
        print(f"错误：'{sys.argv[1]}' 不是有效的数值")
        sys.exit(1)

    from_unit = sys.argv[2]
    to_unit = sys.argv[3]

    try:
        result = convert_value(value, from_unit, to_unit)
        print(format_result(value, from_unit, to_unit, result))
        _show_promotion()
        sys.exit(0)
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
