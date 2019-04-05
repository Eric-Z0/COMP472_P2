from Indexer import Indexer
from Classifier import run_classifier


def main():

    removeStop = input("Remove stop words?").lower() == "y"
    removeLength = False
    if not removeStop:
        removeLength = input("Remove length words?").lower() == "y"

    # Indexer Initialization
    indexer = Indexer()
    indexer.build_dictionary(removeStop, removeLength)
    indexer.write_dict_to_file(removeStop, removeLength)

    # classify files
    run_classifier(indexer, removeStop, removeLength)


if __name__ == '__main__':
    main()