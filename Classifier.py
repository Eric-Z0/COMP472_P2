import re
import math
from pathlib import Path
from CompressTech import remove_empty_strings, lower_case_words


def run_classifier(indexer):

    prob_ham = indexer.calc_class_probability('ham')
    prob_spam = indexer.calc_class_probability('spam')
    file_ctr = 0

    # Read files / documents
    path_list = Path("test").glob('*.txt')
    for file_path in path_list:
        ham_score = 0.0
        spam_score = 0.0
        file_ctr += 1
        with open(file_path, mode="r", encoding="latin-1") as file:
            file_data = file.read()
            # Tokenize files, the process should be consistent with what were done to training files
            words_list = re.split('[^a-zA-Z]', file_data)
            words_list = remove_empty_strings(words_list)
            words_list = lower_case_words(words_list)

            # Start calculating probability in logarithmic form
            ham_score += math.log10(prob_ham)
            spam_score += math.log10(prob_spam)
            for word in words_list:
                # Check if the word is in the dictionary
                if indexer.term_in_dict(word):
                    ham_score += math.log10(indexer.get_term_cp_ham(word))
                    spam_score += math.log10(indexer.get_term_cp_spam(word))

            write_classification_to_file(file_ctr, file_path, ham_score, spam_score)


# Write classification result to a file
def write_classification_to_file(file_ctr, test_file, ham_val, spam_val):

    class_file_path = "baseline-result.txt"
    class_file = Path(class_file_path)
    output_mode = "a" if class_file.is_file() else "w"

    with open(class_file_path, output_mode) as file:
        file_name = str(test_file)
        # How to handle the situation when two values are equal?
        file_classified = 'ham' if ham_val > spam_val else 'spam'
        file_labeled = 'ham' if "ham" in str(test_file) else 'spam'
        class_result = 'right' if file_classified == file_labeled else 'wrong'
        file.write("{}  {}  {}  {}  {}  {}  {}\n".format(file_ctr, file_name, file_classified,
                                                         ham_val, spam_val, file_labeled, class_result))


# Experiment 2
def experiment_stopwords_filtering():
    pass


# Experiment 3
def experiment_word_len_filtering():
    pass


# Experiment 4 (optional)
def experiment_infrequent_words_filtering():
    pass


# Experiment 5 (optional)
def experiment_smoothing():
    pass

