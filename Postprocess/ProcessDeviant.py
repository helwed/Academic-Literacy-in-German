from Preprocess.Skeleton import Skeleton


class Deviant(Skeleton):
    """
    Deviant Skeleton
    """

    def __init__(self, pcorpus):
        super().__init__(pcorpus)
        self.sentences = {}
        self.deviant = {}

    def analyse_deviant(self):
        """
        Analyse deviant
        """
        for file in self.corpus:
            if file not in self.sentences:
                self.sentences[file] = {}
            if file not in self.deviant:
                self.deviant[file] = {}
            for line in self.corpus[file]:
                if line[0].split('-')[0] not in self.sentences[file]:
                    self.sentences[file][line[0].split('-')[0]] = []
                if line[0].split('-')[0] not in self.deviant[file]:
                    self.deviant[file][line[0].split('-')[0]] = []
                self.sentences[file][line[0].split('-')[0]].append(line[2])
                for el in line:
                    if ("deviant" in el or "redundant" in el or "missing" in el) and "[" not in el and "]" not in el and \
                            line[7] != "_":
                        self.deviant[file][line[0].split('-')[0]].append(line)

    def print_deviant(self):
        """
        Print deviant
        """
        with open("Data/" + self.name + "/results/connectives/deviant_" + self.name + ".csv", mode='w',
                  encoding="utf-8") as outfile:
            for file in self.deviant:
                for sentence in self.deviant[file]:
                    if len(self.deviant[file][sentence]) > 0:
                        print("--", file=outfile)
                        for el in self.deviant[file][sentence]:
                            print("Deviant annotiert:", "\t".join(el), file=outfile)
                        print("", file=outfile)
                        try:
                            print("Vorheriger Satz: ", file, str(int(sentence) - 1),
                                  " ".join(self.sentences[file][str(int(sentence) - 1)]), file=outfile)
                        except KeyError:
                            print("Vorheriger Satz: ", file, int(sentence) - 1, file=outfile)
                        print("Betroffener Satz: ", file, sentence, " ".join(self.sentences[file][sentence]),
                              file=outfile)
                        try:
                            print("Folgender Satz: ", file, str(int(sentence) + 1),
                                  " ".join(self.sentences[file][str(int(sentence) + 1)]), file=outfile)
                        except KeyError:
                            print("Folgender Satz: ", file, int(sentence) + 1, file=outfile)
