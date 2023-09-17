def hex2signedDecimal(num):
    
    if (isinstance(num, str)):
        decimal = int(num, 16)
    else:
        decimal = num
    
    if decimal & (1 << 7):
        decimal = -(decimal ^ 0xFF) - 1    
    return decimal

def asHex(num ,digits):
    numStr = hex(num)[2:]
    prefix = "0" * (digits - len(numStr))
    return prefix + numStr

def set_bit(byte, bit_position):
    """Set the specified bit (bit_position) of the given byte."""
    return byte | (1 << bit_position)

def clear_bit(byte, bit_position):
    """Clear the specified bit (bit_position) of the given byte."""
    return byte & ~(1 << bit_position)

def get_bit(byte, bit_position):
    """Get the value of the specified bit (bit_position) of the given byte."""
    return (byte >> bit_position) & 1