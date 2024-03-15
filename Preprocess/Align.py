import os


class SentenceAligner:
    """
    Class allows to add the annotations and align the sentences (according to new boundaries)
    """

    def __init__(self, corpus):
        self.corpus = corpus
        self.texts = {}
        self.boun_texts = {}
        self.anno_lex = {}

    def read_files(self):
        """
        Method reads file and saves annotation in dictionary
        """
        # for every available annotated file (for every text, one folder exists)
        for folder in os.listdir("Data/" + self.corpus + "/post/anno_tsv"):
            # if the folder is not DS.Store
            if not folder.startswith("."):
                # Create a entry in the dictionary for the folder
                self.texts[folder] = dict()
                # for every annotator
                for file in os.listdir("Data/" + self.corpus + "/post/anno_tsv/" + folder):
                    if not file.startswith("."):
                        # open dictionary for annotator
                        self.texts[folder][file] = dict()
                        # read the file and save it in the dictonary
                        with open("Data/" + self.corpus + "/post/anno_tsv/" + folder + "/" + file, mode="r",
                                  encoding="utf-8") as incoming:
                            # seperate the file saved in preamble and text: Only save text
                            self.texts[folder][file]["full_content"] = incoming.read().split("\n\n\n")[1]

    def indices(self, text_dict):
        raw = text_dict["full_content"].split("\n")
        # new will contain the new word
        text_dict["filtered_text"] = []
        # dictionary to save index combinations
        text_dict["indices"] = dict()
        # start with index 1
        i = 1
        # for every line in the text
        for line in raw:
            # if we have an empty line or a line containing the sentence, ignore
            if line.startswith("#") or line == "":
                continue
            # else: save element with index and word in the new list
            else:
                text_dict["filtered_text"].append(str(i) + "\t" + line)
                # save corresponding index combination
                text_dict["indices"][line.split("\t")[0]] = str(i)
                # add one to index
                i += 1
        # return new text
        return text_dict

    def dissolve_sentences(self, text_dict, name):
        """
        method changes indices in the coreference annotations of the text
        :param text_dict: texts from all annotators
        :param name: text name
        :return: changed texts
        """
        # create dictionary with saved indices
        # index_lex = dict()
        # new placeholder in the overall dictionary
        text_dict["without_sen_index"] = []
        # for every line in text
        for line in text_dict["filtered_text"]:
            # append the new line to the new list of words
            text_dict["without_sen_index"].append(line)
            text_dict["all"] = text_dict["without_sen_index"]

        # save file in folder flex_boun
        with open("Data/" + self.corpus + "/flex_boun/" + name, mode="w", encoding="utf-8") as outi:
            # for every word
            for line in text_dict["without_sen_index"]:
                # when first element: add a newline beforehand to suggest sentence boundary
                if line.split("\t")[1].endswith("-1"):
                    print("", file=outi)
                    # print new line
                print(line, file=outi)
        # return changed text
        return text_dict

    def analyse_files(self):
        """
        method adapts indices in texts and print new version
        :return: no return
        """
        # self.read_annotator()
        for text in self.texts:
            self.texts[text] = self.indices(self.texts[text])
            self.texts[text] = self.dissolve_sentences(self.texts[text], text)

    def read_adapted_files(self, type_f):
        """
        method reads files with new sentence boundaries
        :param: type of file to print
        :return:
        """
        # for every adapted file
        for file in os.listdir("Data/" + self.corpus + "/m_sen_boun".replace("m", type_f)):
            self.boun_texts[file] = dict()
            # save content in dictionary
            with open("Data/" + self.corpus + "/m_sen_boun/".replace("m", type_f) + file, mode="r",
                      encoding="utf-8") as file_in:
                content = file_in.readlines()
            if content[0] == "\n":
                self.boun_texts[file]["full_file"] = content[1:]
            else:
                self.boun_texts[file]["full_file"] = content

    def new_sentences(self):
        """
        Method adapts indices to new marked sentence boundaries
        :return:
        """
        for text in self.boun_texts:
            # sentence_number
            s_i = 1
            # list_of_sentences
            sentences = dict()
            # dictionary containing the old indexes and the new ones (as values)
            new_index = dict()
            # initiate first sentence
            sentences[s_i] = []
            # dictionary containing the new elements
            sentences_new = dict()
            # separate file into new sentences
            for line in self.boun_texts[text]["full_file"]:
                if line != "\n":
                    sentences[s_i].append(line)
                else:
                    s_i += 1
                    sentences[s_i] = []

            # for every new sentence
            for sentence in sentences:
                # dictionary entry for the sentence
                sentences_new[sentence] = dict()
                # word_number
                w_i = 1
                # sentence_string
                sentences_new[sentence]["string"] = ""
                # new list of words
                sentences_new[sentence]["words"] = []
                # for every word
                for w in sentences[sentence]:
                    # word split in annotation
                    word = w.split("\t")
                    # new id to use
                    id_sen = (str(sentence) + "-" + str(w_i))
                    # change annotation to new sentence
                    word[1] = id_sen
                    # new string for sentence
                    sentences_new[sentence]["string"] += " " + word[3]
                    # add new index combi to dictionary
                    new_index[word[0]] = id_sen
                    sentences_new[sentence]["words"].append(word)
                    # word number
                    w_i += 1

            self.boun_texts[text]["new_sentences"] = sentences_new

    def parse_texts(self, file_format, preamble, target):
        # if tsv was chosen
        if file_format == ".tsv":
            # add preamble for every text first
            for text in self.boun_texts:
                with open('Data/' + self.corpus + '/tsv_new_boun/' + text, mode="w", encoding="utf-8") as new_file:
                    print("#FORMAT=WebAnno TSV 3.3", file=new_file)
                    # if you added target form:
                    if target:
                        print("#T_SP=webanno.custom.Target|Targetform", file=new_file)
                    for amb in preamble[text]:
                        print(amb, file=new_file)
                    print("", file=new_file)
                    # print every sentence
                    for sentence in self.boun_texts[text]["new_sentences"]:
                        print("", file=new_file)
                        # second pre-text: full sentence
                        print("#Text=" + self.boun_texts[text]["new_sentences"][sentence]["string"].strip(),
                              file=new_file)
                        # print word of sentence (without index)
                        for word in self.boun_texts[text]["new_sentences"][sentence]["words"]:
                            print("\t".join(word[1:]).strip(), "", file=new_file, sep="\t")
        # if csv was chosen
        elif file_format == ".csv":
            print("csv")
            # for every text
            for text in self.boun_texts:
                # print sentence and words
                with open('Data/' + self.corpus + '/csv/' + text.replace(".tsv", ".csv"), mode="w",
                          encoding="utf-8") as new_file:
                    for sentence in self.boun_texts[text]["new_sentences"]:
                        for word in self.boun_texts[text]["new_sentences"][sentence]["words"]:
                            print("\t".join([word[0], word[1], word[3], word[4], word[5], word[6]]), file=new_file)

    def create_new_files(self, type_f, format_list, preamble, target):
        """
        Method allows to cleanly create new files with new sentence boundaries
        :param target: target annotation
        :param preamble: preamble of file
        :param type_f: csv or tsv
        :param format_list: lists of format that the user wants to print in
        """
        # read the new files
        self.read_adapted_files(type_f)
        # create new sentences
        self.new_sentences()
        # print in chosen formats
        for file_format in format_list:
            self.parse_texts(file_format, preamble, target)

    def adopt_boun(self, type_f):
        """
        method helps to adopt the already manually adapted sentence boundaries
        :return:
        """
        # read the new files
        self.read_adapted_files(type_f)
        # for every text in the found texts
        for text in self.boun_texts:
            # other is the non-aligned sentences
            other = self.texts[text]["all"]
            # aligned sentences
            marked = self.boun_texts[text]["full_file"]
            # indexes to compare boundaries (newlines)
            line_m = 0
            line_o = 0
            # open file to print in
            with open("Data/" + self.corpus + "/a_sen_boun/".replace("a", type_f) + text, mode="w",
                      encoding="utf-8") as outfile:
                # look at both the lines and compare
                while line_o < len(other):
                    if line_m < len(marked):
                        if other[line_o].split("\t")[0] == marked[line_m].split("\t")[0]:
                            print(other[line_o].strip(), file=outfile)
                            # if they are the same, both indexes go up
                            line_m += 1
                            line_o += 1
                        # if not, add newline and only add on to the marked line
                        else:
                            print("", file=outfile)
                            line_m += 1
                    else:
                        break

    def read_pre_anno(self):
        # for every available annotated file (for every text, one folder exists)
        for file in os.listdir("Data/" + self.corpus + "/tsv"):
            # Create a entry in the dictionary for the folder
            if not file.startswith("."):
                self.texts[file] = dict()
                # read the file and save it in the dictonary
                with open("Data/" + self.corpus + "/tsv/" + file, mode="r",
                          encoding="utf-8") as incoming:
                    # seperate the file saved in preamble and text: Only save text
                    self.texts[file]["full_content"] = incoming.read().split("\n\n\n")[1]
