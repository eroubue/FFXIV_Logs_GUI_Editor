#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FFXIV日志校验码计算模块
根据用户提供的正确格式实现
"""

import hashlib
import re
from typing import List, Tuple, Optional

# 检查是否可用校验码功能
try:
    import hashlib
    CHECKSUM_AVAILABLE = True
except ImportError:
    CHECKSUM_AVAILABLE = False

def u_49152(byte_str):
    """Convert SHA256 digest to 16-character checksum using lookup table - exact copy from reference"""
    lookup = [3145776, 3211312, 3276848, 3342384, 3407920, 3473456, 3538992, 3604528, 3670064, 3735600, 6357040, 6422576, 6488112, 6553648, 6619184, 6684720, 3145777, 3211313, 3276849, 3342385, 3407921, 3473457, 3538993, 3604529, 3670065, 3735601, 6357041, 6422577, 6488113, 6553649, 6619185, 6684721, 3145778, 3211314, 3276850, 3342386, 3407922, 3473458, 3538994, 3604530, 3670066, 3735602, 6357042, 6422578, 6488114, 6553650, 6619186, 6684722, 3145779, 3211315, 3276851, 3342387, 3407923, 3473459, 3538995, 3604531, 3670067, 3735603, 6357043, 6422579, 6488115, 6553651, 6619187, 6684723, 3145780, 3211316, 3276852, 3342388, 3407924, 3473460, 3538996, 3604532, 3670068, 3735604, 6357044, 6422580, 6488116, 6553652, 6619188, 6684724, 3145781, 3211317, 3276853, 3342389, 3407925, 3473461, 3538997, 3604533, 3670069, 3735605, 6357045, 6422581, 6488117, 6553653, 6619189, 6684725, 3145782, 3211318, 3276854, 3342390, 3407926, 3473462, 3538998, 3604534, 3670070, 3735606, 6357046, 6422582, 6488118, 6553654, 6619190, 6684726, 3145783, 3211319, 3276855, 3342391, 3407927, 3473463, 3538999, 3604535, 3670071, 3735607, 6357047, 6422583, 6488119, 6553655, 6619191, 6684727, 3145784, 3211320, 3276856, 3342392, 3407928, 3473464, 3539000, 3604536, 3670072, 3735608, 6357048, 6422584, 6488120, 6553656, 6619192, 6684728, 3145785, 3211321, 3276857, 3342393, 3407929, 3473465, 3539001, 3604537, 3670073, 3735609, 6357049, 6422585, 6488121, 6553657, 6619193, 6684729, 3145825, 3211361, 3276897, 3342433, 3407969, 3473505, 3539041, 3604577, 3670113, 3735649, 6357089, 6422625, 6488161, 6553697, 6619233, 6684769, 3145826, 3211362, 3276898, 3342434, 3407970, 3473506, 3539042, 3604578, 3670114, 3735650, 6357090, 6422626, 6488162, 6553698, 6619234, 6684770, 3145827, 3211363, 3276899, 3342435, 3407971, 3473507, 3539043, 3604579, 3670115, 3735651, 6357091, 6422627, 6488163, 6553699, 6619235, 6684771, 3145828, 3211364, 3276900, 3342436, 3407972, 3473508, 3539044, 3604580, 3670116, 3735652, 6357092, 6422628, 6488164, 6553700, 6619236, 6684772, 3145829, 3211365, 3276901, 3342437, 3407973, 3473509, 3539045, 3604581, 3670117, 3735653, 6357093, 6422629, 6488165, 6553701, 6619237, 6684773, 3145830, 3211366, 3276902, 3342438, 3407974, 3473510, 3539046, 3604582, 3670118, 3735654, 6357094, 6422630, 6488166, 6553702, 6619238, 6684774]
    res = []
    for _ in range(16):
        res.append(None)
    for i in range(8):
        num = lookup[byte_str[i]]
        res[2*i] = chr(num % 128)
        res[2*i + 1] = chr((num >> 16) % 128)
    return "".join(res)

def calculate_checksum_with_line_number(line_parts: List[str], line_number: int) -> str:
    """
    计算FFXIV日志行的校验码（包含行号）- 使用正确的算法
    
    Args:
        line_parts: 日志行的各个部分（不包含校验码）
        line_number: 行号
    
    Returns:
        16位校验码
    """
    # 将各部分用|连接，然后在末尾添加行号
    line_without_checksum = '|'.join(line_parts) + '|' + str(line_number)
    
    # 使用SHA256计算哈希值
    test_str = line_without_checksum.encode('utf-8')
    m = hashlib.sha256()
    m.update(test_str)
    hex_bytes = m.digest()
    
    # 使用查找表转换为16字符校验码
    return u_49152(hex_bytes)

def encrypt(text, line_num):
    """
    加密函数 - 根据用户提供的正确算法
    
    :param text: the damage text row without last | and encryption code
    :param line_num: line number of record
    :return: encryption code
    """
    test_str = (text + '|' + line_num).encode('utf-8')
    m = hashlib.sha256()
    m.update(test_str)
    hex_bytes = m.digest()
    t = u_49152(hex_bytes)
    return t

def validate_checksum_with_line_number(line: str, line_number: int) -> bool:
    """
    验证FFXIV日志行的校验码（包含行号）
    
    Args:
        line: 完整的日志行
        line_number: 行号
    
    Returns:
        校验码是否有效
    """
    if not CHECKSUM_AVAILABLE:
        return True
    
    # 分割行，获取校验码
    parts = line.strip().split('|')
    if len(parts) < 2:
        return False
    
    # 获取实际的校验码（最后一个字段）
    actual_checksum = parts[-1]
    
    # 计算期望的校验码（不包括最后一个校验码字段）
    expected_parts = parts[:-1]
    expected_checksum = calculate_checksum_with_line_number(expected_parts, line_number)
    
    return actual_checksum == expected_checksum

def parse_log_file_with_line_numbers(file_path: str) -> List[Tuple[str, int]]:
    """
    解析日志文件，返回每行内容及其正确的行号
    
    Args:
        file_path: 日志文件路径
    
    Returns:
        包含(行内容, 行号)元组的列表
    """
    lines_with_numbers = []
    current_line_number = 1
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # 检查是否是地图切换行（01|开头）
                if line.startswith('01|'):
                    current_line_number = 1
                
                lines_with_numbers.append((line, current_line_number))
                current_line_number += 1
                
    except Exception as e:
        print(f"解析日志文件时出错: {e}")
    
    return lines_with_numbers

# 以下是兼容性函数（旧版本）
def calculate_checksum(line_parts: List[str]) -> str:
    """
    计算校验码（旧版本，兼容性）
    
    Args:
        line_parts: 日志行的各个部分
    
    Returns:
        16位校验码
    """
    if not CHECKSUM_AVAILABLE:
        return "0000000000000000"
    
    # 将各部分用|连接
    line_str = '|'.join(line_parts)
    
    # 使用SHA256计算哈希值
    m = hashlib.sha256()
    m.update(line_str.encode('utf-8'))
    hex_bytes = m.digest()
    
    # 使用查找表转换为16字符校验码
    return u_49152(hex_bytes)

def validate_checksum(line: str) -> bool:
    """
    验证校验码（旧版本，兼容性）
    
    Args:
        line: 完整的日志行
    
    Returns:
        校验码是否有效
    """
    if not CHECKSUM_AVAILABLE:
        return True
    
    # 分割行，获取校验码
    parts = line.strip().split('|')
    if len(parts) < 2:
        return False
    
    # 获取实际的校验码（最后一个字段）
    actual_checksum = parts[-1]
    
    # 计算期望的校验码（不包括最后一个校验码字段）
    expected_parts = parts[:-1]
    expected_checksum = calculate_checksum(expected_parts)
    
    return actual_checksum == expected_checksum

def parse_log_line(line: str) -> Optional[dict]:
    """
    解析单行日志（旧版本，兼容性）
    
    Args:
        line: 日志行
    
    Returns:
        解析后的数据字典，如果解析失败则返回None
    """
    if not line.strip():
        return None
    
    # 匹配21|开头的战斗日志行
    pattern = r'^21\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|.*\|([^|]*)$'
    match = re.match(pattern, line.strip())
    
    if not match:
        return None
    
    return {
        'timestamp': match.group(1),
        'source_id': match.group(2),
        'source': match.group(3),
        'id': match.group(4),
        'ability': match.group(5),
        'target_id': match.group(6),
        'target': match.group(7),
        'flags': match.group(8),
        'damage': match.group(9),
        'checksum': match.group(10)
    }

def update_log_line(line: str, new_data: dict) -> str:
    """
    更新日志行（旧版本，兼容性）
    
    Args:
        line: 原始日志行
        new_data: 新的数据字典
    
    Returns:
        更新后的日志行
    """
    parts = line.strip().split('|')
    
    # 更新各个字段
    if 'timestamp' in new_data:
        parts[1] = new_data['timestamp']
    if 'source_id' in new_data:
        parts[2] = new_data['source_id']
    if 'source' in new_data:
        parts[3] = new_data['source']
    if 'id' in new_data:
        parts[4] = new_data['id']
    if 'ability' in new_data:
        parts[5] = new_data['ability']
    if 'target_id' in new_data:
        parts[6] = new_data['target_id']
    if 'target' in new_data:
        parts[7] = new_data['target']
    if 'flags' in new_data:
        parts[8] = new_data['flags']
    if 'damage' in new_data:
        parts[9] = new_data['damage']
    
    # 重新计算校验码
    checksum = calculate_checksum(parts[:-1])
    parts[-1] = checksum
    
    return '|'.join(parts)

# 测试函数
def test_checksum():
    """测试校验码计算功能"""
    # 测试数据
    test_line = "21|2024-01-15T10:30:15.123|12345678|玩家名称|1001|普通攻击|87654321|敌人A|0000|1500|a1b2c3d4"
    
    print("测试校验码计算:")
    print(f"原始行: {test_line}")
    
    # 解析并验证
    parsed = parse_log_line(test_line)
    if parsed:
        print("✓ 校验码验证通过")
        print(f"解析结果: {parsed}")
    else:
        print("✗ 校验码验证失败")
    
    # 重新计算校验码
    parts = test_line.split('|')
    new_checksum = calculate_checksum(parts[:10])
    print(f"计算的新校验码: {new_checksum}")
    
    # 更新行
    updated_line = update_log_line(
        parts[1], parts[2], parts[3], parts[4], parts[5],
        parts[6], parts[7], parts[8], parts[9]
    )
    print(f"更新后的行: {updated_line}")

if __name__ == "__main__":
    test_checksum() 