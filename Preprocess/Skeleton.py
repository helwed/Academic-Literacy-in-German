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
        for file in os.listdir("Data/" + self.name + "/" + folder):
            # open file and save text and preamble in lists
            with open("Data/" + self.name + "/" + folder + "/" + file, mode="r", encoding="utf-8") as inc_file:
                self.preamble[file], self.corpus[file], self.raw[file] = [], [], []
                # for every line: if line long enough, save text amd preamble
                for line in inc_file.readlines():
                    if len(line) > 1:
                        if not line.startswith("#"):
                            self.corpus[file].append(line.strip().split("\t"))
                        elif line.startswith("#T_"):
                            self.preamble[file].append(line.strip())
                        self.raw[file].append(line.strip())

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

