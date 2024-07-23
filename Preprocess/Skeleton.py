import os


class Skeleton:
    def __init__(self, pcorpus):
        self.name = pcorpus  # is used to name the files
        self.corpus = {}  # Saves the raw text per file
        self.lengths = {}  # Saves lengths from one to another token
        self.coref = {}  # saves coreferential information
        self.preamble = {}  # saves preamble
        self.categories = {}  # translation between preamble and categories saves (name > index)
        self.chain = {}  # contains all annotated chains
        self.raw = {}
        self.tok = 0  # amount of token
        self.topics = {}  # contains the files and their topics
        self.firsts = {}
        self.seconds = {}
        self.annotators = {}

    def pipe(self):
        """
        Method reads files and extracts preamble
        :return:
        """
        self.read_files("tsv")
        self.analyse_preamble()

    def read_files(self, folder):
        """
        Function reads files and preamble
        """
        # for every file in the corpus file
        for fname in os.listdir("Data/" + self.name + "/" + folder):
            # open file and save text and preamble in lists
            with open("Data/" + self.name + "/" + folder + "/" + fname, mode="r", encoding="utf-8") as inc_file:
                self.preamble[fname], self.corpus[fname], self.raw[fname] = [], [], []
                # for every line: if line long enough, save text amd preamble
                for line in inc_file.readlines():
                    if len(line) > 1:
                        if not line.startswith("#"):
                            self.corpus[fname].append(line.strip().split("\t"))
                        elif line.startswith("#T_"):
                            self.preamble[fname].append(line.strip())
                        self.raw[fname].append(line.strip())


    def analyse_preamble(self):
        """
        For every saved preamble: dissect
        """
        # for every preamble saved
        for file in self.preamble:
            # start a new entry in category dictionary to save individual indices
            self.categories[file] = {}
            # add the three elements which are not in the preamble but still in the file format
            list_file = ['index', 'sen', 'tok']
            # new list of categories
            new_list = []
            # for every element found in the preamble: save
            for el in self.preamble[file]:
                # if "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.SurfaceForm" not in el:
                list_file.append(el.split("|")[1:])
            # for every element: save in new list
            for l in list_file:
                if isinstance(l, list):
                    for cat in l:
                        if cat not in new_list:
                            new_list.append(cat)
                        else:
                            new_list.append(cat + "2")
                else:
                    new_list.append(l)
            # for every element: save index as index in list of categories
            for element in range(len(new_list)):
                self.categories[file][new_list[element]] = element

    def analyse_topics(self):
        """
        Function reads file with topics
        """
        # Read topic file
        with open("Data/Additional_Data/topic_" + self.name + "_filled.txt") as infile:
            content = infile.readlines()
        # save topics in dictionary
        for line in content[1:]:
            zoomin = line.strip().split("\t")
            self.topics[zoomin[0]] = zoomin[1]

    def analyse_annotators(self):
        """
                Method reads all annotators in a text file
                """
        # Open text file to save annotators
        with open("Data/Additional_Data/annotator_overview_" + self.name + "_filled.txt", mode="r",
                  encoding="utf-8") as infile:
            files = infile.readlines()
            for row in files:
                self.annotators[row.split("\t")[0].strip()] = row.split("\t")[1].strip()
    def remove_files(self, folder):

        for file in os.listdir("Data/" + self.name + "/" + folder):
            fname, anno = file.split("__")[0], file.split("__")[1]
            if self.annotators[fname] == anno:
                os.rename("Data/" + self.name + "/" + folder + "/" + file, "Data/" + self.name + "/" + folder + "/" + fname)
            else:
                os.remove("Data/" + self.name + "/" + folder + "/" + file)

    def analyse_languages(self):
        """
        Function reads file with topics
        """
        # FIRST LANGUAGES
        # Read topic file
        with open("Data/Additional_Data/FirstLanguages_" + self.name + "_filled.csv") as infile:
            content = infile.readlines()
        # save first languages in dictionary
        for line in content[1:]:
            zoomin = line.strip().split("\t")
            self.firsts[zoomin[0]] = zoomin[1:]
        # SECOND LANGUAGES
        with open("Data/Additional_Data/SecondLanguages_" + self.name + "_filled.csv") as infile2:
            content = infile2.readlines()
        # save second languages in dictionary
        for line in content[1:]:
            zoomin2 = line.strip().split("\t")
            self.seconds[zoomin2[0]] = zoomin2[1:]



