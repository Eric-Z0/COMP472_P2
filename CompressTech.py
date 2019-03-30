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

