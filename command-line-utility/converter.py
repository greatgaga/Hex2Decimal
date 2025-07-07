from state import *

def convert_single_hex(hex_str):
    # strip 0x, pad to even length
    s = hex_str.lower().replace("0x", "")
    if len(s) % 2:
        s = "0" + s

    if state["reverse_endian"]:
        # split to bytes and reverse
        bytes_list = []
        for i in range(0, len(s) - 1, 2):
            bytes_list.append(s[i] + s[i + 1])
        bytes_list = reversed(bytes_list)
        s = ''.join(bytes_list)

    return int(s, 16)

def convert_multiple_hexes(hex_list):
    # route through convert_single_hex so reverse-endian is honored
    return [convert_single_hex(h) for h in hex_list]

def convert_single_byte(byte_str):
    # Pad to full bytes (8 bits)
    length = len(byte_str)
    padded_length = ((length + 7) // 8) * 8  # round up to nearest multiple of 8
    padded = byte_str.zfill(padded_length)

    byte_list = []

    for i in range(0, len(padded), 8):
        byte_list.append(padded[i : i + 8])

    result = []
    for i in range(len(byte_list)):
        result.append(int(byte_list[i], 2))
    return result

def convert_multiple_bytes(byte_list):
    result = []
    for i in range(len(byte_list)):
        result.append(convert_single_byte(byte_list[i]))
    if state["reverse_endian"]:
        result = list(reversed(result))
    return result

def convert_single_decimal_to_byte(decimal_str):
    byte = bin(int(decimal_str))[2:].zfill(8)
    return byte

def convert_multiple_decimal_to_byte(decimal_list):
    result = [convert_single_decimal_to_byte(decimal_list[i]) for i in range(len(decimal_list))]
    if state["reverse_endian"]:
        result = list(reversed(result))
    return result

def convert_single_decimal_to_hex(decimal_str):
    result = hex(int(decimal_str))
    if (state["reverse_endian"]):
        result = (str(result))[2:].lower()
        if (len(result) % 2 == 1):
            result = '0' + result
        splited = []
        for i in range(0, len(result), 2):
            splited.append(result[i : i + 2])
        result = ''.join(reversed(splited))
        result = "0x" + result
    return result

def convert_multiple_decimal_to_hex(decimal_list):
    return [convert_single_decimal_to_hex(decimal_list[i]) for i in range(len(decimal_list))]

def single_ascii_decode(decimal_str):
    return chr(int(decimal_str))

def multiple_ascii_decode(decimal_list):
    return [single_ascii_decode(decimal_list[i]) for i in range(len(decimal_list))]