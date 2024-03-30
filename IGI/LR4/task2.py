import utility
import re
import copy
import zipfile

def solve_task2():
    """ Solve the second task of the 4-th laboratory work.
    """
    
    while (True):
        try:
            filename_dst = input("Enter the source filename: ")
            filename_src = input("Enter the destination filename: ")
            arhievename = input("Enter the arhievename: ")

            dst_content = utility.read_from_file(filename_dst)
            answer = analize_text(dst_content)
            utility.write_to_file(filename_src, answer)

            print(utility.DELIMETER)
            utility.make_verbose_arhieve(arhievename, filename_src)

            return
        except OSError as err:
            continue
    

def analize_text(text) -> str:
    """ Manage the text analysis.
        Parameters:
        text - content to analyse
    """

    answer = ""

    sentences_result = count_centences(text)
    answer += f"The number of general     sentences: {sentences_result[0]}.\n" \
              f"The number of narrative   sentences: {sentences_result[1]}.\n" \
              f"The number of question    sentences: {sentences_result[2]}.\n" \
              f"The number of exclamation sentences: {sentences_result[3]}.\n"

    answer += f"The average number of words in the sentence: {get_average_sentence_size(text)}.\n"
    answer += "The average word size: {:.5}.\n".format(get_average_word_size(text))
    answer += f"The number of smiles: {count_smile(text)}.\n"
    answer += f"The number of GUID strings: {count_GUID(text)}.\n"
    answer += f"The number of triple words: {count_triple_words(text)}.\n"
    answer += f"The words with equal number of vowels and consonats: {get_special_words(text)}\n"
    answer += f"The sorted words of the text: {get_sorted_words(text)}.\n"
    answer += f"Replaced text:\n{replace_symbol(text)}"
    
    return answer


def count_centences(text) -> tuple:
    """ Count the number of different centences in the text and return it as a tuple:
        (general_sentence_count,
         narrative_sentence_count,
         question_sentence_count,
         exclamation_sentence_count)

         Parameters:
         text - the content to analyse
    """

    result = re.findall(r"[\.?!(...)]", text)
    gen_sz = len(result)
    nar_sz = result.count('.') + result.count('...')
    qst_sz = result.count('?')
    exc_sz = result.count('!')

    return gen_sz, nar_sz, qst_sz, exc_sz


def get_average_sentence_size(text) -> float:
    """ Determine the average sentence size and return it

        Parameters:
        text - the content to analyse
    """

    sentences = re.findall(r"[A-ZА-Я][^\.?!(...)]*[\.?!(...)]", text)
    all_words_count = 0    
    for sentence in sentences:
        all_words_count += sentence.count(' ') + 1

    return all_words_count / len(sentences)


def get_average_word_size(text) -> float:
    """ Determine the average word size in the text and return it.

        Parameters:
        text - the content to analyse
    """ 

    words = re.findall(r"[A-Za-zА-Яа-я]+", text)
    all_words_size = 0
    for word in words:
        all_words_size += len(word)

    return all_words_size / len(words)


def count_smile(text) -> int:
    """ Determine the count of smiles in the text and return it.

        Parameters:
        text - the content to analyse
    """

    return len(re.findall(r"\s*([;:]{1}[-]*((\])+|(\[)+|(\))+|(\()+))\s*", text))


def replace_symbol(text) -> str:
    """ Replace spaces by user symbol in the text and return its copy.
    """

    new_text = copy.copy(text)
    user_symbol = ""

    while (True):
        user_symbol = input("Enter the symbol to replace all the spaces: ")

        if (len(user_symbol) != 1):
            print("Please, enter one symbol!")
        else:
            break

    return re.sub(r'[ ]{1}', user_symbol, text)
    

def count_GUID(text) -> int:
    """ Count the number of GUID string and return it.

        Parameters:
        text - the content to analyse
    """

    return len(re.findall(r"\s*([0-9A-Fa-f]){8}-([0-9A-Fa-f]{4}-){3}[0-9A-Fa-f]{12}\s*", text))


def count_triple_words(text) -> int:
    """ Count the number of words with 3 letters and return it.

        Parameters:
        text - the content to analyse
    """

    return len(re.findall(r"[\s*][A-Za-zА-Яа-я]{3}[\s?.!?]", text))


def get_special_words(text) -> list:
    """ Find the number of words with equal count of vowels and consonants.
        Return the list like [(order number, word)]

        Parameters: 
        text - the content to analyse
    """
    answer = []
    words = re.findall(r"[A-Za-zА-Яа-я]+", text)
    for i, word in enumerate(words):
        if (len(re.findall(r"[ауоиэыяюеё]", word, re.IGNORECASE))
            == len(re.findall(r"[бвгджзйклмнпрстфхцчшщ]", word, re.IGNORECASE))):
            answer.append((i, word))

    return answer


def get_sorted_words(text) -> list:
    """ Return the text words in alphabetical order.

        Parameters: 
        text - the content to analyse
    """
    
    return sorted(re.findall(r"[A-Za-zА-Яа-я]+", text))