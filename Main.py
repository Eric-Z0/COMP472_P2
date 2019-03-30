from Indexer import Indexer
from Classifier import run_classifier


def main():
    # Indexer Initialization
    indexer = Indexer()
    indexer.build_dictionary()
    # indexer.write_dict_to_file()

    # classify files
    run_classifier(indexer)


if __name__ == '__main__':
    main()