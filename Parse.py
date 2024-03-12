import os
import xml.etree.ElementTree as ElT
import sys

class Parse:

    def __init__(self, nlp, name, path):
        """
        Initializes the parsing component of the pipeline
        :param name: name of the corpus
        :param nlp: nlp module (spacy)
        :param path: path to the directory
        """
        self.name = name
        self.corpus = {}   # dictionary to save the corpus
        self.path = path
        self.nlp = nlp

    def parse_txt(self):
        """
            Method allows to read text files to process them
        """
        # START Loop 1: for every text in the corpus
        for text in os.listdir(self.path + "/raw/"):
            if not text.startswith("."):  # to avoid trying to process hidden files
                # create dictionary entry
                self.corpus[text] = {}
                # open the file and read the content (and clean a bit)
                with open(self.path + "/raw/" + text, mode="r", encoding="utf-8") as input_file:
                    self.corpus[text]["full_text"] = input_file.read().replace("﻿", "")
                # analyse text with spacy
                doc = self.nlp(self.corpus[text]["full_text"])
                # save spacy annotation
                self.corpus[text]["spacy_orig"] = doc
                # print new file in order to allow adding target
                with open(self.path + "/orig/" + text, mode="w", encoding="utf-8") as output_file:
                    with open(self.path + "/orig+orig/" + text, mode="w", encoding="utf-8") as output_file2:
                        # enumeration to find tokens back after adding target
                        i = 1
                        # START Loop 2: for every token in the text, add entry in the files
                        for token in self.corpus[text]["spacy_orig"]:
                            if token.text.strip() != "":
                                print(i, token.text, file=output_file, sep="\t")  # add it to the "orig" files
                                print(i, token.text, token.text, file=output_file2,
                                      sep="\t")  # add it to the orig+orig files
                                i += 1  # add 1 to index
                        # END Loop 2
        # END Loop 1

    def read_content(self):
        for text in os.listdir(self.path + "/raw/"):
            if not text.startswith("."):
                self.corpus[text] = {}

    def parse_target(self):
        """
            Method parses orig+target files to save target in a seperate entry in the dictionary
        """
        # for every text in that is annotated with target
        for text in os.listdir(self.path + "/orig+target/"):
            if text != ".DS_Store":
                # open the file
                with open(self.path + "/orig+target/" + text, mode="r", encoding="utf-8") as infile:
                    i = 1
                    # dictionary entry to save the annotations till now
                    self.corpus[text]["target_file"] = []
                    # dictionary entry with text as string
                    self.corpus[text]["target_text"] = ""
                    # for every line: save content of file
                    for line in infile.readlines():
                        # split the line at the right position (due to some manual adding of target it can vary)
                        if len(line.strip().split("\t")) >= 2:
                            line = line.strip().split("\t")
                        elif len(line.strip().split("   ")) >= 2:
                            line = "".join(line).split("   ")
                        elif len(line.strip().split("  ")) >= 2:
                            line = "".join(line).split("  ")
                        else:
                            print(line.strip().split("\t"))
                        # differentiates between with index and without
                        if len(line) > 2:
                            self.corpus[text]["target_text"] += " " + line[2].strip()
                            self.corpus[text]["target_file"].append(line)
                        else:
                            print(line)
                            self.corpus[text]["target_text"] += " " + line[1].strip()
                            self.corpus[text]["target_file"].append(str(i) + line)
                        i += 1

    def get_corpus(self):
        """
        Method returns the corpus
        :return: corpus
        """
        return self.corpus

class ReadDimlex:
    """ Class helps to read the DimLex - an XML file full of German connectives"""

    def __init__(self):
        """
        Initiates DimLex and starts to read the data
        """
        try:
            self.tree = ElT.parse('Data/Additional_Data/DimLex.xml')
        except FileNotFoundError:
            print("Please add the DimLex.xml file to the folder 'Data/Additional_Data'")
            sys.exit(1)
        self.root = self.tree.getroot()
        self.connective_dict = {}
        self.save_dict()

    def save_dict(self):
        """
        Reads data and saves the connectives together with their tags, their sense and their non-connective
        tag in a dictionary
        :return: None
        """
        # Read XML-Tree and saves every word in the dictionary
        for child in self.root:
            self.connective_dict[child.attrib.get('word')] = {}
            # looks at all the children of the word-element to save the several layers
            for grandchild in child:
                if grandchild.tag == 'syn':
                    for c in grandchild:
                        # save senses
                        if c.tag == 'sem':
                            self.connective_dict[child.attrib.get('word')]['sense'] = []
                            for d in c:
                                freq = 0
                                if d.attrib.get('freq') != '':
                                    freq = int(d.attrib.get('freq'))
                                if freq == 'None':
                                    freq = 0
                                if freq is None:
                                    freq = 0
                                self.connective_dict[child.attrib.get('word')]['sense'].append(
                                    (d.attrib.get('sense'), freq))
                # save stts-tags
                if grandchild.tag == 'stts':
                    for c in grandchild:
                        if c.tag == 'example':
                            if c.attrib.get('type') != 'None':
                                self.connective_dict[child.attrib.get('word')]['tag'] = c.attrib.get('type')
                # saves non-connective tag
                if grandchild.tag == 'non_conn_reading':
                    for c in grandchild:
                        if c.tag == 'example':
                            if c.attrib.get('type') is not None:
                                self.connective_dict[child.attrib.get('word')]['non_connective'] = c.attrib.get('type')

    def get_dict(self):
        """
        Saves getter method for the dictionary in question
        :return: dictionary with all the connectives
        """
        return self.connective_dict

