import sys


def read_table(pfile):
    """
    Reads a conversion table from a file.
    :param pfile: file name
    :return: conversion dictionary
    """
    conversion = {}
    with open("Data/Additional_Data/" + pfile, 'r', encoding='utf8') as in_file:
        content = in_file.readlines()
    for line in content:
        line = line.strip().split(';')
        old = line[1].replace("\ufeff", "")
        new = line[0].replace("\ufeff", "")
        conversion[old] = new
    return conversion


def convert_in_file(pfile, ptab):
    """
    Converts the content of a file given a conversion dictionary.
    :param pfile: file to convert
    :param ptab: conversion dictionary
    :return: NONE
    """
    with open("Data/Convert/" + pfile, 'r', encoding='utf8') as infile:
        content = infile.readlines()
    with open("Data/Convert/" + pfile.replace(".csv", "") + "_converted.csv", 'w', encoding='utf8') as outfile:
        print(content[0], end="", file=outfile)
        for line in content[1:]:
            list_line = line.strip().split('\t')
            line = line.replace(list_line[0], ptab[list_line[0]])
            print(line, end="", file=outfile)


def combine_files(pfiles):
    """
    Combines multiple csv files .
    :param pfiles: list of files to be combined
    :return: NONE
    """
    first = False
    with open("Data/Convert/combined.csv", 'w', encoding='utf8') as outfile:
        for file in pfiles:
            with open("Data/Convert/" + file, 'r', encoding='utf8') as infile:
                content1 = infile.readlines()
                if not first:
                    print("Corpus\t" + content1[0], end="", file=outfile)
                    first = True
                for line in content1[1:]:
                    print(file.replace(".csv", "") + "\t" + line, end="", file=outfile)


if __name__ == '__main__':
    """
    Main function
    """
    try:
        ans = sys.argv[1]
    except IndexError:
        ans = input("Do you want to convert names?")
    if ans == "Yes" or ans == "Y":
        try:
            name = sys.argv[1]
        except IndexError:
            name = input("What is the name of the conversion file?")
        c_tab = read_table(name)
        try:
            c_file = sys.argv[1]
        except IndexError:
            c_file = input("Where should we convert?")
        convert_in_file(c_file, c_tab)
    else:
        try:
            files = sys.argv[1]
        except IndexError:
            files = input("Which three files do you want to combine? (separated by comma)")
        files = files.split(",")
        # files = ["B.csv", "L2.csv", "L1.csv"]
        combine_files(files)
