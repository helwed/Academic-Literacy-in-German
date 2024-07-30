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

def change_factors(pfile):
    """
    Changes the names of some variables in the files (e.g. everything with a + to either COMPLEX or PHRASE)
    :param pfile: name of file
    """
    with open("Data/Convert/combined.csv", 'r', encoding='utf8') as infile:
        with open("Data/Convert/combined_new.csv", 'w', encoding='utf8') as outfile:
            content = infile.readlines()
            for line in content:
                new_line = []
                line = line.strip().split("\t")
                for el in line:
                    new_el = el
                    if el == "_":
                        new_el = "NA"
                    if "+" in el and "M" in line[-1]:
                        new_el = "COMPLEX"
                    elif "+" in el and "P" in line[-1]:
                        new_el = "PHRASE"
                    new_line.append(new_el)
                print("\t".join(new_line), file= outfile)

def rel_freq_per_word():
    count = {}
    pre = {}
    with open("Data/Convert/combined_new.csv", 'r', encoding='utf8') as infile:
        content = infile.readlines()
    pre[0] = content[0].split("\t")[0:-1]
    for line in content[1:]:
        line = line.split("\t")
        file = line[8]
        connective = line[12]
        tok = line[10]
        if file not in count:
            count[file] = {}
        if connective not in count[file]:
            count[file][connective] = {}
        if tok not in count[file][connective]:
            count[file][connective][tok] = 0
        count[file][connective][tok] += 1
    with open("Data/Convert/combined_sum.csv", 'r', encoding='utf8') as infile:
        content2 = infile.readlines()
    for line2 in content2[1:]:
        line2 = line2.split("\t")
        sum = int(line2[9].strip('\n'))
        file = line2[8] + ".tsv"
        for el in count[file]:
            for el2 in count[file][el]:
                print(sum, count[file][el][el2], el)
                count[file][el][el2] = (count[file][el][el2]/sum)*100
        participant = line2[8].replace("_T1", "").replace("_T2", "").replace("_T3", "")
        pre[file] = [line2[0].replace("token_sum_","")] + line2[1:-1] + [participant]
    with open("Data/Convert/new.csv", 'w', encoding='utf8') as outfile:
        print("CORPUS", "L1_1", "L1_2", "L1_3", "L2_1", "L2_2" ,"L2_3", "TOPIC", "FILE", "SPEAKER", "CON", "TOK", "RELFREQ", sep = "\t", file=outfile)

        for file in count:
            for el in count[file]:
                for el2 in count[file][el]:
                    print("\t".join(pre[file] + [el, el2, str(count[file][el][el2])]), file = outfile)


def count_connectives_per_text():
    count = {}
    with open("Data/Convert/combined_new.csv", 'r', encoding='utf8') as infile:
        content = infile.readlines()
    for line in content:
        line = line.split("\t")
        file = line[8]
        connective = line[12]
        pos = line[11]
        if file not in count:
            count[file] = {}
            # Connectives
            count[file]["total"] = 0
            count[file]["expansion"] = 0
            count[file]["contingency"] = 0
            count[file]["comparison"] = 0
            count[file]["temporal"] = 0
            # POS
            count[file]["adverbial"] = 0
            count[file]["coordinating"] = 0
            count[file]["subordinating"] = 0
            count[file]["phrase"] = 0
            count[file]["complex"] = 0
            count[file]["other"] = 0
        #POS
        if pos in ["ADJD", "ADV", "PAV", "ADJA"]:
            count[file]["adverbial"] += 1
        elif pos in ["KON", "KOKOM"]:
            count[file]["coordinating"] += 1
        elif pos in ["KOUS", "KOUI"]:
            count[file]["subordinating"] += 1
        elif pos in ["PHRASE"]:
            count[file]["phrase"] += 1
        elif pos in ["COMPLEX"]:
            count[file]["complex"] += 1
        else:
            count[file]["other"] += 1
        # Connectives
        if "Expansion" in connective:
            count[file]["expansion"] += 1
        elif "Contingency" in connective:
            count[file]["contingency"] += 1
        elif "Comparison" in connective:
            count[file]["comparison"] += 1
        elif "Temporal" in connective:
            count[file]["temporal"] += 1
        count[file]["total"] += 1
    return count

def combine_count_sum(pcount):
    names_pos = ["adverbial", "coordinating", "subordinating", "phrase", "complex", "other"]
    with open("Data/Convert/combined_sum.csv", 'r', encoding='utf8') as infile:
        content = infile.readlines()
    with open("Data/Convert/combined_sum_new.csv", 'w', encoding='utf8') as outfile:
        with open("Data/Convert/sum_per_cat_con.csv", 'w', encoding='utf8') as outfile2:
            with open("Data/Convert/sum_per_cat_pos.csv", 'w', encoding='utf8') as outfile3:
                print("\t".join(content[0].strip("\n").split("\t")[0:-1] + ['participant','expansion', 'contingency', 'comparison', 'temporal', 'total'] + names_pos),
                      file=outfile)
                print("\t".join(
                    content[0].strip("\n").split("\t")[0:-1] + ['participant', 'category', 'rel_sum']),file=outfile2)
                print("\t".join(
                    content[0].strip("\n").split("\t")[0:-1] + ['participant', 'category', 'rel_sum']), file=outfile3)
                for line in content[1:]:
                    line = line.strip("\n").replace("token_sum_", "").split("\t")
                    file = line[8] + ".tsv"
                    sum = int(line[9].strip('\n'))
                    # Connectives
                    expansion = (count[file]['expansion']/sum)*100
                    contingency = (count[file]['contingency']/sum)*100
                    comparison = (count[file]['comparison']/sum)*100
                    temporal = (count[file]['temporal']/sum)*100
                    total = (count[file]['total']/sum)*100
                    participant = line[8].replace("_T1","").replace("_T2","").replace("_T3","")
                    # POS
                    adv = (count[file]["adverbial"]/sum)*100
                    coord = (count[file]["coordinating"]/sum)*100
                    sub = (count[file]["subordinating"]/sum)*100
                    phr = (count[file]["phrase"]/sum)*100
                    comp = (count[file]["complex"]/sum)*100
                    oth = (count[file]["other"]/sum)*100
                    list_pos = [str(adv), str(coord), str(sub), str(phr), str(comp), str(oth)]


                    print("\t".join(line[0:-1] + [participant  , str(expansion), str(contingency), str(comparison), str(temporal), str(total)] + list_pos), file= outfile)
                    print("\t".join(line[0:-1] + [participant  ,"expansion", str(expansion)]), file= outfile2)
                    print("\t".join(line[0:-1] + [participant  ,"contingency", str(contingency)]), file=outfile2)
                    print("\t".join(line[0:-1] + [participant  ,"comparison", str(comparison)]), file=outfile2)
                    print("\t".join(line[0:-1] + [participant  ,"temporal", str(temporal)]), file=outfile2)
                    print("\t".join(line[0:-1] + [participant  ,"total", str(total)]), file=outfile2)

                    print("\t".join(line[0:-1] + [participant, "adverbial", str(adv)]), file=outfile3)
                    print("\t".join(line[0:-1] + [participant, "coordinating", str(coord)]), file=outfile3)
                    print("\t".join(line[0:-1] + [participant, "subordinating", str(sub)]), file=outfile3)
                    print("\t".join(line[0:-1] + [participant, "phrase", str(phr)]), file=outfile3)
                    print("\t".join(line[0:-1] + [participant, "complex", str(comp)]), file=outfile3)
                    print("\t".join(line[0:-1] + [participant, "other", str(oth)]), file=outfile3)





if __name__ == '__main__':
    """
    Main function
    """
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
        #files = ["B.csv", "L2.csv", "L1.csv"]
        files = ["token_sum_B.csv", "token_sum_L1.csv", "token_sum_L2.csv"]
        combine_files(files)
        try:
            files = sys.argv[1]
        except IndexError:
            files = input("Which file would you like to format?")
        change_factors("combined.csv")
    """
    #count = count_connectives_per_text()
    #combine_count_sum(count)
    rel_freq_per_word()
