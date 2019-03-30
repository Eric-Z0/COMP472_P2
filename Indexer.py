import re
from pathlib import Path
from CompressTech import remove_empty_strings, lower_case_words

"""
The value for a given word (key) in __index dictionary is composed of four parts:

__index[term][0]: the frequency of a word in the class ham
__index[term][1]: the smoothed conditional probability of a word in the class ham
__index[term][2]: the frequency of a word in the class spam
__index[term][3]: the smoothed conditional probability of a word in the class spam

"""


class Indexer:

    def __init__(self):
        self.__index = dict()
        self.__ham_words = 0            # total number of ham words
        self.__spam_words = 0           # total number of spam words
        self.__vocab_size = 0           # total number of terms recorded in the dictionary
        self.__ham_file_num = 0         # total number of ham files trained
        self.__spam_file_num = 0        # total number of spam files trained

    # Build a dictionary with a set of training files
    def build_dictionary(self):
        # Read files / documents
        path_list = Path("train").glob('*.txt')
        for file_path in path_list:
            with open(file_path, mode="r", encoding="latin-1") as file:
                file_data = file.read()
                # Tokenize documents
                words_list = re.split('[^a-zA-Z]', file_data)
                words_list = remove_empty_strings(words_list)
                words_list = lower_case_words(words_list)

                # Check the type of training file is ham or spam
                is_ham = True if "ham" in str(file_path) else False
                is_spam = True if "spam" in str(file_path) else False

                if is_ham:
                    for word in words_list:
                        if word in self.__index:
                            self.__index[word][0] += 1
                        else:
                            self.__index[word] = [1, 0, 0, 0]
                    self.__ham_file_num += 1

                if is_spam:
                    for word in words_list:
                        if word in self.__index:
                            self.__index[word][2] += 1
                        else:
                            self.__index[word] = [0, 0, 1, 0]
                    self.__spam_file_num += 1

        self.__vocab_size = len(self.__index)
        self.__ham_words = self.calc_total_num_words('ham')
        self.__spam_words = self.calc_total_num_words('spam')
        self.calc_conditional_probability(0.5)

        print("Vocabulary Size: {}".format(self.__vocab_size))

    # Calculate the total number of words in the class ham or spam
    def calc_total_num_words(self, class_name):
        total_num_of_words = 0

        is_ham = True if class_name == 'ham' else False
        is_spam = True if class_name == 'spam' else False

        if is_ham:
            for term in self.__index:
                total_num_of_words += self.__index[term][0]

        if is_spam:
            for term in self.__index:
                total_num_of_words += self.__index[term][2]

        return total_num_of_words

    # Calculate conditional probability of a word in the class ham and spam
    def calc_conditional_probability(self, factor):
        for term in self.__index:
            self.__index[term][1] = (self.__index[term][0] + factor) / (self.__ham_words + self.__vocab_size * factor)
            self.__index[term][3] = (self.__index[term][2] + factor) / (self.__spam_words + self.__vocab_size * factor)

    # Calculate the probability for a given class
    def calc_class_probability(self, class_name):
        is_ham = True if class_name == 'ham' else False
        is_spam = True if class_name == 'spam' else False

        if is_ham:
            return self.__ham_words / (self.__ham_words + self.__spam_words)

        if is_spam:
            return self.__spam_words / (self.__ham_words + self.__spam_words)

    # Get the term conditional probability in the class ham
    def get_term_cp_ham(self, term):
        return self.__index[term][1]

    # Get the term conditional probability in the class spam
    def get_term_cp_spam(self, term):
        return self.__index[term][3]

    # Check if a term exists in the dictionary
    def term_in_dict(self, term):
        if term in self.__index:
            return True
        else:
            return False

    # Write dictionary to a file
    def write_dict_to_file(self):
        dict_file_path = "model.txt"
        with open(dict_file_path, "w") as file:
            counter = 1
            sorted_index = sorted(self.__index)
            for term in sorted_index:
                term_freq_ham = self.__index[term][0]      # frequency of word in the class ham
                term_cp_ham = self.__index[term][1]        # conditional probability of word in the class ham
                term_freq_spam = self.__index[term][2]     # frequency of word in the class spam
                term_cp_spam = self.__index[term][3]       # conditional probability of word in the class spam
                file.write("{}  {}  {}  {}  {}  {}\n".format(counter, term, term_freq_ham, term_cp_ham,
                                                             term_freq_spam, term_cp_spam))
                counter += 1                               # update counter


