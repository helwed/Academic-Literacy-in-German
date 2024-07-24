import sys
from Postprocess.ProcessAnnotated import ListAnno, AdditionalAnalyses
from Postprocess.ProcessConnectives import Connective
from Postprocess.ProcessCoreference import Coreference, DetailCoref
import os


#ToDo: Write algorithm that puts the additional data in folders, so that i will not have such a mess there
#ToDo: Repair coreference for L2_f

def unpack_folders(path):
    """
    Unpacks the folders that were created by Inception
    :param path: path to the files
    """
    # for every folder in the directory
    for folder in os.listdir(path):
        if not folder.startswith('.'):
            # for every text annotated
            for file in os.listdir(path + "/" + folder):
                # rewrite file name in new folder
                if not file.startswith('.') and file != "INITIAL_CAS.tsv":
                    # ToDo: Need to write something to delete annotators name (or just not name it in general?)
                    # new = folder.replace(".tsv","") + "_" + file
                    new = folder
                    with open(path + "/" + folder + "/" + file, mode="r", encoding="utf-8") as infile:
                        with open(path + "_new/" + new + "__" + file, mode="w", encoding="utf-8") as outfile:
                            print(infile.read().strip(), file=outfile)
                elif file == "INITIAL_CAS.tsv" and len(os.listdir(path + "/" + folder)) == 1:
                    new = folder
                    with open(path + "/" + folder + "/" + file, mode="r", encoding="utf-8") as infile:
                        with open(path + "_new/" + new + "__CAS.tsv", mode="w", encoding="utf-8") as outfile:
                            print(infile.read().strip(), file=outfile)
                if file == "INITIAL_CAS.tsv":
                    new = folder
                    with open(path + "/" + folder + "/" + file, mode="r", encoding="utf-8") as infile:
                        with open(path + "_raw/" + new, mode="w", encoding="utf-8") as outfile:
                            print(infile.read().strip(), file=outfile)


def makedirs(corpus):
    """
    Function creates all necessary directories
    :param corpus: corpus name
    """
    exists = False
    try:
        os.mkdir(r"Data/" + corpus + r"/tsv_new/")
    except OSError:
        exists = True
        pass
    try:
        os.mkdir(r"Data/" + corpus + r"/tsv_raw/")
    except OSError:
        exists = True
        pass
    try:
        os.mkdir(r"Data/" + corpus + r"/results/")
    except OSError:
        exists = True
        pass
    try:
        os.mkdir(r"Data/" + corpus + r"/results/coref/")
    except OSError:
        exists = True
        pass
    try:
        os.mkdir(r"Data/" + corpus + r"/results/connectives/")
    except OSError:
        exists = True
        pass
    try:
        os.mkdir(r"Data/" + corpus + r"/results/general/")
    except OSError:
        exists = True
        pass
    return exists


def create_lists(pname):
    """
    Creating lists to add more information to the csv files
    :param pname: name of the corpus
    """
    list_texts = []
    # Add all text files to a list
    for text in os.listdir("Data/" + pname + "/tsv/"):
        list_texts.append(text)
    # create list of annotators and of topics
    l = ListAnno(list_texts, ["Annotator"], pname)
    l.list()
    l.list_topics()
    l.list_languages()


def start_analyses(pname):
    """
        Function allows to engage complete pipeline
    """
    # read file and preanalyse
    ana = AdditionalAnalyses(pname)
    ana.read_files("tsv_raw")  # ToDo: Add tsv_new
    ana.analyse_preamble()
    ana.analyse_topics()
    ana.analyse_languages()
    ana.analyse_annotators()
    ana.remove_files("tsv_new")
    ana.read_files("tsv_new")
    # Counting!
    ana.count_nouns()
    ana.count_token()
    ana.print_pos()
    ana.print_corpus()


def connective_analyses(pname):
    """
    Function allows to start the connective pipeline
    :param pname: name of the corpus
    """
    con = Connective(pname)
    con.analyse_topics()
    con.analyse_annotators()
    con.analyse_languages()
    con.read_files("tsv_new")  # ToDo: Add tsv_new
    con.filter_connectives()
    try:
        con.reformat_manual()
        con.write_combi()
        con.adapt_for_r()
    except FileNotFoundError:
        print("\nThe connectives have been sorted into multi_word and single connectives +++ "
              "Please reformat multiwords and change name to 'con_multi_results_manual.csv'")
        print("To do that: Delete numbers in brackets such as '[2]' "
              "and write the connectives belonging together in one line.\n"
              "Example: 01.tsv	um zu	APPR+PTKZU	02_Contingency	00_Multiword	22\n")


def coreference_analyses(pname):
    coref_corpus = Coreference(pname)
    coref_corpus.analyse_languages()
    coref_corpus.analyse_annotators()
    coref_corpus.full_pipeline()

    details = DetailCoref(pname)
    details.pipe()


if __name__ == '__main__':
    try:
        name = sys.argv[1]
    except IndexError:
        name = input("What is the name of the corpus?")
    print("\nWelcome! The program starts to unpack folder {} now.".format(name))
    makedirs(name)
    unpack_folders("Data/" + name + "/tsv")
    print("Creating empty lists to fill with annotators, topics and languages+++ "
          "Please fill if you want it added to the csv-files for R\n")
    create_lists(name)
    print("Processing starts...")
    start_analyses(name)
    print("Counted nouns, tokens and POS +++ New files can be found in Data/{}/results/general".format(name))
    connective_analyses(name)
    print("Listed connectives +++ New files can be found in Data/{}/results/connectives".format(name))
    coreference_analyses(name)
    print("Listed coreference +++ New files can be found in Data/{}/results/coref".format(name))
