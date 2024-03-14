import sys
from Postprocess.ProcessAnnotated import ListAnno
from Postprocess.ProcessAnnotated import AdditionalAnalyses
import os

def unpack_folders(path):
    for folder in os.listdir(path):
        if not folder.startswith('.'):
            for file in os.listdir(path + "/" + folder):
                if not file.startswith('.') and file != "INITIAL_CAS.tsv":
                    #ToDo: Need to write something to delete annotators name (or just not name it in general?)
                    #new = folder.replace(".tsv","") + "_" + file
                    new = folder
                    with open(path + "/" + folder + "/" + file, mode = "r", encoding = "utf-8") as infile:
                        with open(path + "_new/" + new, mode="w", encoding="utf-8") as outfile:
                            print(infile.read(), file = outfile)

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
        os.mkdir(r"Data/" + corpus + r"/results/")
    except OSError:
        exists = True
        pass
    return exists

def create_lists(name):
    list_texts = []
    for text in os.listdir("Data/" + name + "/tsv/"):
        list_texts.append(text)
    l = ListAnno(list_texts, ["Annotator"], name)
    l.list()
    l.list_topics()

def start_analyses(pname):
    """
        Function allows to engange complete pipeline
    """
    # read file and preanalyse
    Ana = AdditionalAnalyses(pname)
    Ana.read_files("tsv_new")
    Ana.analyse_preamble()
    Ana.analyse_topics()
    # Counting!
    Ana.count_nouns()
    Ana.count_token()
    Ana.print_POS()

if __name__ == '__main__':
    try:
        name = sys.argv[1]
    except IndexError:
        name = input("What is the name of the corpus?")
    print("Welcome! The program starts to unpack folder {} now.".format(name))
    makedirs(name)
    unpack_folders("Data/" + name + "/tsv")
    print("Creating empty lists to fill with annotators and topics +++ Please fill if you want it added to the csv-files for R")
    create_lists(name)
    start_analyses(name)
    print("Counted nouns, tokens and POS +++ New files can be found in Data/{}/results".format(name))

