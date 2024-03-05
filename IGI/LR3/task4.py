def solve_task4():
    """ Solve the 4-th task of the laboratory work.
    """

    str_list = get_split_string_input()

    title_word_count  = get_title_word_count(str_list)
    the_longest_startswith_I = find_the_longest_startswith_I(str_list)
    duplicate_set = get_duplicate_words(str_list)
    
    print_task4_solution(title_word_count, the_longest_startswith_I, duplicate_set)


def get_split_string_input():
    """ Get string and split it. Return list of the strings
    """

    str_list = input("Enter your string: ").split(" ")
    return str_list


def get_title_word_count(str_list: list) -> int:
    """ Determine the count of words which starts with the upper character and return it.
    """

    count = 0
    for word in str_list:
        if word.istitle():
            count += 1

    return count


def find_the_longest_startswith_I(str_list: list) -> str:
    """ Find the longest string starts with character 'I' and return it.
    """

    answer = ""
    for word in str_list:
        if word.startswith('I') and len(word) > len(answer):
            answer = word

    return answer


def get_duplicate_words(str_list: list) -> str:
    """ Find all the duplicates and return it.
    """

    duplicate_set = set()
    for word in str_list:
        if str_list.count(word) > 1:
            duplicate_set.add(word)

    return duplicate_set

def print_task4_solution(title_word_count: int, find_the_longest_startswith_I: str, duplicate_word_set: set):
    print(f"The count of the title words: {title_word_count}\n"
          f"The longest word starts with 'I': {find_the_longest_startswith_I}\n"
          f"All the duplicate words: {duplicate_word_set}")