# Clean the words list by removing all its empty string
def remove_empty_strings(words_list):
    # nes = no empty string
    words_list_nes = [word for word in words_list if word != '']
    return words_list_nes


# Lower case all the words in a given text
def lower_case_words(words_list):
    # lc = lower case
    word_list_lc = []
    for word in words_list:
        word_list_lc.append(word.lower())

    return word_list_lc

def remove_stop_words(words_list):
    stop_words = {}

    with open("english-stop-words.txt", mode="r", encoding="latin-1") as file:
        for line in file:
            stop_words[line.strip().lower()] = False

    new_word_list = []

    for word in words_list:
        if word.lower() not in stop_words:
            new_word_list.append(word.lower())

    return new_word_list


def remove_big_and_small_words(word_list):
    new_word_list = []

    for word in word_list:
        if len(word) > 2 and len(word) < 9:
            new_word_list.append(word)

    return new_word_list