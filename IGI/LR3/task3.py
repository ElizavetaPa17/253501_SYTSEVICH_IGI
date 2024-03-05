def solve_task3():
    """ Solve the 3-rd task of the laboratory work
    """

    try:
        hex_number = try_get_hex_number()
        print("The entered string is a hexadecimal number.")
    except:
        print("The entered string is not a hexadecimal number.")


def try_get_hex_number() -> int:
    """ Get a hexadecimal number. Return it or raise exception
    """

    hex_number = input("Enter hexadecimal number: ")

    # convert from hexadecimal to decimal. If we receive any failure
    # then the input isn't hexadecimal
    dec_number = int(hex_number, 16)
    return hex_number