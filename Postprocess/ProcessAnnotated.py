from Preprocess.Skeleton import Skeleton


class ListAnno:
    def __init__(self, texts, annotators, name):
        """
        Initializes object of the class ListAnno
        :param texts: texts to be listed
        :param annotators: annotators that worked on the texts
        :param name: name of the corpus
        """
        self.texts = texts
        self.annotators = annotators
        self.name = name

    def list(self):
        """
        Method lists all annotators in a text file
        """
        # Open text file to save annotators
        with open("Data/Additional_Data/annotator_overview_" + self.name + ".txt", mode="w",
                  encoding="utf-8") as outfile:
            # print row headers
            print("textfile", "Annotated_by", sep="\t", file=outfile)
            # print default annotator for every text
            for text in sorted(self.texts):
                if not text.startswith("."):
                    print(text, "Annotator.tsv", sep="\t", file=outfile)

    def list_topics(self):
        """
        Method lists all topics in a text file
        """
        # Open text file to save topics
        with open("Data/Additional_Data/topic_" + self.name + ".txt", mode="w", encoding="utf-8") as outfile:
            # print row headers
            print("textfile", "topic", sep="\t", file=outfile)
            # print default topic for every file
            for text in sorted(self.texts):
                if not text.startswith("."):
                    print(text, "Topic", sep="\t", file=outfile)


class AdditionalAnalyses(Skeleton):
    def __init__(self, pcorpus):
        super().__init__(pcorpus)

    def count_nouns(self):
        """
        Function counts existing nouns in file
        """
        with open("Data/" + self.name + "/results/nouns.csv", mode="w", encoding="utf-8") as outfile:
            print("file\tnoun\tfrequency", file=outfile)
            # for every file int he corpus
            for file in self.corpus:
                # dictionary to count nouns
                countdict = {}
                # for every token in the text file
                for tok in self.corpus[file]:
                    pos = self.categories[file]["PosValue"]
                    # if annotated as noun: count
                    if tok[pos] in ["NN", "NE", "N"]:
                        if tok[2] not in countdict:
                            countdict[tok[2]] = 1
                        else:
                            countdict[tok[2]] += 1
                # print frequencies in file
                for element in countdict:
                    if countdict[element] > 1:
                        print(file, element, countdict[element], file=outfile)

    def count_token(self):
        """
        function counts token per text and per sentence
        """
        # new file to save counting results
        with open("Data/" + self.name + "/results/sentence_length.csv", mode="w",
                  encoding="utf-8") as outfile:
            with open("Data/" + self.name + "/results/token_sum.csv", mode="w",
                      encoding="utf-8") as outfile2:
                print("topic\tfile\tsenid\tlength", file=outfile)
                print("topic\tfile\tsum", file=outfile2)
                # for every file in the corpus
                for file in self.corpus:
                    topic = self.topics[file]
                    # save length of every sentence in the dictionary
                    freq = {}
                    sums = 0
                    # for every token in the corpus, add to sentence length (and to sum)
                    for tok in self.corpus[file]:
                        if tok[0].split("-")[0] not in freq:
                            freq[tok[0].split("-")[0]] = 1
                        else:
                            freq[tok[0].split("-")[0]] += 1
                        sums += 1
                    # print results
                    for sen in freq:
                        print(topic + "\t" + str(file) + "\t" + "s" + str(sen) + "\t" + str(freq[sen]), file=outfile)
                    print(topic + "\t" + file.replace(".tsv", "") + "\t" + str(sums), file=outfile2)

    def print_pos(self):
        """
                function counts token per text and per sentence
                """
        # new file to save counting results
        with open("Data/" + self.name + "/results/" + self.name + "_POS.csv", mode="w",
                  encoding="utf-8") as outfile:
            print("topic\tfile\ttok\tPOS1", file=outfile)
            # for every file in the corpus
            for file in self.corpus:
                topic = self.topics[file]
                for tok in self.corpus[file]:
                    print(topic + "\t" + file + "\t" + tok[2] + "\t" + tok[3], file=outfile)
