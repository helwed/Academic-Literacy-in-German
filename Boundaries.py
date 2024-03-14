import os
from Preprocess.Skeleton import Skeleton
from Preprocess.Align import SentenceAligner
import sys


def make_directories(corpus):
    """
    Function creates all necessary directories
    :param corpus:
    :return:
    """
    file_exists = False
    try:
        os.mkdir(r"Data/" + corpus + r"/flex_boun/")
    except OSError:
        file_exists = True
        pass
    try:
        os.mkdir(r"Data/" + corpus + r"/tsv_new_boun/")
    except OSError:
        file_exists = True
        pass
    return file_exists


if __name__ == '__main__':
    try:
        name = sys.argv[1]
    except IndexError:
        name = input("What is the name of the corpus?")
    test = os.path.isdir(r"Data/" + name + r"/tsv/")
    if test:
        # reads anno_tsv folder and combines annotations
        pre = Skeleton(name + "/tsv")
        pre.pipe()
        print("I will start making new directories to allow for changes (flex_boun, tsv_new_boun, csv)")
        exists = make_directories(name)
        if exists:
            print("I see that the data has been processed before! Checking for new boundaries now...")
            bounds = os.path.isdir(r"Data/" + name + r"/m_sen_boun/")
            if bounds:
                print("I have found new sentence boundaries. Adapting the tsv files now...")
                sen = SentenceAligner(name)
                sen.read_pre_anno()
                sen.analyse_files()
                sen.adopt_boun("m")
                sen.create_new_files("m", [".tsv"], pre.preamble, False)
                print("The new sentence boundaries have been added! Please check 'tsv_new_boun'.")
            else:
                print("No new sentence boundaries found!")
                print("Please add manual boundaries +++ copy flex_boun +++ rename to m_sen_boun +++ "
                      "adapt sentence boundaries (and delete empty lines at the beginning and at the end)")
        else:
            print("Starting to prepare for manual sentence boundary annotation...")
            sen = SentenceAligner(name)
            sen.read_pre_anno()
            sen.analyse_files()
            print("New files have been added! Please continue with manual adaption of sentence boundaries.")
            print("Please add manual boundaries +++ copy flex_boun +++ rename to m_sen_boun +++ "
                  "adapt sentence boundaries (and delete empty lines at the beginning and at the end)")
    else:
        print(
            "I cannot find a tsv-folder with the name {}! Please add the corpus to the Data folder (Data/{}/tsv).".format(
                name, name))
