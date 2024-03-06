def solve_task3():
    """ Solve the 3-rd task of the laboratory work
    """

    hex_number = 0
    dec_number = 0
    try:
        hex_number, dec_number = try_get_hex_number()
        print(f"The entered string is a hexadecimal number: {dec_number}.")
    except:
        print("The entered string is not a hexadecimal number.")


def try_get_hex_number() -> tuple:
    """ Get a hexadecimal number. Return tuple of (hex_number, dec_number) or raise exception
    """

    hex_number = input("Enter hexadecimal number: ")

    # convert from hexadecimal to decimal. If we receive any failure
    # then the input isn't hexadecimal
    dec_number = int(hex_number, 16)
    return (hex_number, dec_number)