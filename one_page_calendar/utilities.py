def ordinal(number: int):
    """
    Converts an integer to its ordinal representation

    :param number: integer to be converted
    :type number: int
    :return: ordinal form of the specified number
    :rtype: str

    """

    if number not in [11, 12, 13]:
        mask = (number // 10 * 10)
        ones = number - mask
        if 0 <= ones < 4:
            match ones:
                case 0:
                    if mask > 0:
                        out = f'{number:2d}th'
                    else:
                        out = f'{number:d}th'
                case 1:
                    if mask > 0:
                        out = f'{number:2d}st'
                    else:
                        out = f'{number:d}st'
                case 2:
                    if mask > 0:
                        out = f'{number:2d}nd'
                    else:
                        out = f'{number:d}nd'
                case 3:
                    if mask > 0:
                        out = f'{number:2d}rd'
                    else:
                        out = f'{number:d}rd'
        else:
            if mask > 0:
                out = f'{number:<2d}th'
            else:
                out = f'{number:d}th'
    else:
        out = f'{number:<2d}th'
    return out
