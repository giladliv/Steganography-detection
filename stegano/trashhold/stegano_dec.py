

def get_messages(pix_list: list):
    msg = ''
    for i in range(0, len(pix_list), 3):
        three_pix = pix_list[i: i + 3]
        is_end, char = extract_data_list_pix(three_pix)
        msg += char
        if is_end:
            break
    return msg


def extract_data_list_pix(pix_list: list):
    str_bin = ''

    for pix in pix_list:
        for num in pix:
            str_bin += str(num % 2)

    print(str_bin[:-1])

    is_end = (int(str_bin[-1]) == 1)
    char = chr(int(str_bin[:-1], 2))
    return is_end, char

# binary_int = int("11000010110001001100011", 2)
# byte_number = binary_int.bit_length() + 7 // 8
#
# binary_array = binary_int.to_bytes(byte_number, "big")
# ascii_text = binary_array.decode()
#
# print(ascii_text)
