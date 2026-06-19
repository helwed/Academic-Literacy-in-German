"""
Pipeline to start preparing the files to annotate them
"""

# Import public packages
import os
import spacy
import sys

# Import project packages
import Preprocess.Annotate as Annotate
import Preprocess.Parse as Parse




def makedirs(corpus):
    """
    Function creates all necessary directories
    :param corpus: corpus name
    """
    exists = False
    try:
        os.mkdir(r"Data/" + corpus + r"/orig/")
    except OSError:
        pass
    try:
        os.mkdir(r"Data/" + corpus + r"/orig+orig/")
    except OSError:
        exists = True
        pass
    try:
        os.mkdir(r"Data/" + corpus + r"/tsv/")
    except OSError:
        pass
    try:
        os.mkdir(r"Additional_Data/" + corpus + r"/")
    except OSError:
        pass

    return exists


if __name__ == '__main__':
    try:
        name = sys.argv[1]
    except IndexError:
        name = input("What is the name of the corpus?")
    try:
        lang = sys.argv[2]
    except IndexError:
        lang = input("Which language needs to be processed (de, fr, nl or en)?")
    if lang == "de":
        # Prepare language model de
        nlp = spacy.load('de_core_news_sm')
    elif lang == "fr":
        # Prepare language model fr
        nlp = spacy.load('fr_core_news_sm')
    elif lang == "nl":
        # Prepare language model nl
        nlp = spacy.load('nl_core_news_sm')
    elif lang == "en":
        # Prepare language model nl
        nlp = spacy.load('en_core_web_sm')
    else:
        print("I cannot find a language with the name" + lang)
    try:
        opt_con = sys.argv[3]
    except IndexError:
        opt_con = input("Do you wish to annotate connectives? (yes/no)")

    test = os.path.isdir(r"Data/" + name + r"/raw/")
    if test:
        print("Welcome! The program starts to process folder {} now.".format(name))
        pre = makedirs(name)
        if pre:
            print("I see that the corpus has been processed before. Checking for normalisation now...")
            p = Parse.Parse(nlp, name, "Data/" + name)
            p.read_content()
        else:
            print("I see that the corpus has not been processed before. I will start the pipeline.")
            p = Parse.Parse(nlp, name, "Data/" + name)
            p.parse_txt()

        norm = os.path.isdir(r"Data/" + name + r"/orig+target/")
        if norm:
            print("The corpus is normalised. I will start parsing the data now...")
            p.parse_target()
            if opt_con == "yes":
                dimlex = Parse.ReadDimlex()
                a = Annotate.Annotation(nlp, name, p.get_corpus(), dimlex.get_dict())
            else:
                a = Annotate.Annotation(nlp, name, p.get_corpus(), None)
            a.annotate_simple()
            a.print_tsv()
            print(
                "The corpus has been annotated. If you want to change the sentence boundaries manually, please start Boundaries.py.")
        else:
            print("The corpus is not normalised (yet).")
            print("Please normalise the files ++ Copy folder orig+orig ++ Change new name to orig+target ++"
                  " normalise third row of every file in the new folder")
    else:
        print("I cannot find a folder with the name {}! Please add the corpus to the Data folder (Data/{}/raw).".format(
            name, name))
