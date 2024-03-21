from Preprocess.Skeleton import Skeleton


class Coreference(Skeleton):
    def __init__(self, pcorpus):
        super().__init__(pcorpus)

    def count_distance_length(self):
        """
        Function to save distances
        """
        # for every file in the system
        for file in self.corpus:
            # save dictionary to save lengths of chains
            self.lengths[file] = {}
            j = 0
            # for every token combination - save distance
            for tok1 in self.corpus[file]:
                for tok2 in self.corpus[file]:
                    # if token is the token itself, save 0
                    if tok1 == tok2:
                        j = 0
                    # if token comes before other token, save 0
                    if int(tok2[1].split("-")[0]) < int(tok1[1].split("-")[0]):
                        j = 0
                        continue
                    # save token distance
                    else:
                        self.lengths[file][(tok1[0], tok2[0])] = j
                        self.lengths[file][(tok2[0], tok1[0])] = j
                        j += 1

    # Achtung: Die Zahlenkombination bei Koreferenz z.B. 6-1 bezieht sich nicht auf ein Element, sondern auf die Nummer in der Kette
    def filter_chain(self):
        """
        Function saves important information of chain
        """
        # for every file in the corpus
        index, token, expl, ref, rel, type_rel = "_", "_", "_", "_", "_", "_"
        for file in self.corpus:
            self.coref[file] = []
            # for every token
            for tok in self.corpus[file]:
                """['22-15', '5096-5101', 'beide', 'PIS', 'PRON', 'beide', 'pronoun', 'personal',
                                      'unsure', '*->5-1', 'coreferential expression[5]']"""
                # filter index
                try:
                    index = self.categories[file]['index']
                    token = self.categories[file]['tok']
                    expl = self.categories[file]['Explicity']
                    ref = self.categories[file]['Referent']
                    rel = self.categories[file]['referenceRelation']
                    type_rel = self.categories[file]['referenceType']
                except:
                    print("Error", file)
                # if all three positions not annotated, skip
                try:
                    if tok[expl] == "_" and tok[ref] == "_" and tok[rel] == "_" and tok[type_rel] == "_":
                        continue
                    # else: save annotation
                    else:
                        self.coref[file].append((tok[index], tok[token], tok[expl], tok[ref], tok[rel], tok[type_rel]))
                except:
                    pass
                    # print(file, tok, self.categories[file])

    def sort_groups(self):
        """
        Function analyses annotation
        """
        self.chain = {}
        # for every file
        for file in self.coref:
            # create entry in sort dictionary as dictionary
            self.chain[file] = {}
            # for every token
            for tok in self.coref[file]:
                # if line in token > two annotation found
                if "|" in tok[4]:
                    # start sequence
                    sequence = {}
                    # for annotation found in the sequence, save information
                    for anno in range(len(tok)):
                        if "|" in tok[anno]:
                            for el in range(len(tok[anno].split("|"))):
                                if el not in sequence:
                                    sequence[el] = []
                                sequence[el].append((anno, tok[anno].split("|")[el]))
                    for entry in sequence:
                        new_tok = list(tok)
                        for level in sequence[entry]:
                            new_tok[level[0]] = level[1]
                        if 'coreferential expression' not in new_tok[5]:
                            new_tok[2] = "_"
                            new_tok[3] = "_"
                        tok = new_tok

                # else: save chain!
                if not tok[4] == "_":
                    new = (
                        tok[4].split("->")[0], tok[4].split("->")[1].split("-")[0], tok[4].split("->")[1].split("-")[1])
                else:
                    print(file)
                    print("error", tok)
                    break

                # if new chain not saved yet
                if new[1] not in self.chain[file]:
                    self.chain[file][new[1]] = {}
                if new[2] not in self.chain[file][new[1]]:
                    self.chain[file][new[1]][new[2]] = []
                self.chain[file][new[1]][new[2]].append(tok)

            # for element in chain: add annotation
            for el1 in self.chain[file]:
                for el2 in sorted(self.chain[file][el1]):
                    if len(self.chain[file][el1][el2]) > 1:
                        # save annotation in variables to ease new string
                        # tok[index], tok[token], tok[expl], tok[ref], tok[rel], tok[type]
                        new_index = self.chain[file][el1][el2][0][0]
                        new_token = ""
                        new_expl = self.chain[file][el1][el2][0][2]
                        new_ref = self.chain[file][el1][el2][0][3]
                        new_rel = self.chain[file][el1][el2][0][4]
                        new_type = self.chain[file][el1][el2][0][5]
                        for part in self.chain[file][el1][el2]:
                            new_token += part[1] + " "
                        # save important info
                        self.chain[file][el1][el2] = [
                            (new_index, new_token.strip(), new_expl, new_ref, new_rel, new_type)]

    def correct(self, tuple_w):
        """
        Function saves clean output
        :param tuple_w: tuple to be cleaned
        :return: cleaned tuple
        """
        new_output = []
        # delete for every annotation...
        for anno in tuple_w[0]:
            # ..brackets
            if "[" in anno:
                new_output.append(anno.split("[")[0])
            # ...and arrows
            elif "->" in anno:
                new_output.append(anno.split("->")[0])
            else:
                new_output.append(anno)
        return new_output

    def statistics(self):
        """
        prints out results
        :return:
        """
        # create the two files to save the results in
        with open("Data/" + self.name + "/results/coref/statistics.csv", mode="w", encoding="utf-8") as out_file:
            print("lang\tfile\tchain\tposition\tsenid\tid\ttok\texpl\tref\trel\ttype\tdis_ant\tdis_prior",
                  file=out_file)
            with open("Data/" + self.name + "/results/coref/statistics_chain_length.csv", mode="w",
                      encoding="utf-8") as out_file2:
                print("lang\tfile\tchain\tlength", file=out_file2)
                # for every file in the chain
                for file in self.chain:
                    # for every element saved in the chain
                    for el1 in sorted(self.chain[file]):
                        length_chain = len(self.chain[file][el1])
                        # print chain info in the file
                        print(file.split("_")[0], file, el1, length_chain, file=out_file2, sep="\t")
                        # for every element - calculate distance between antecedent and element and element and prior element
                        for el2 in sorted(self.chain[file][el1]):
                            # distance to antecedent (tuple)
                            try:
                                distance_ante = (
                                    self.chain[file][el1][str(length_chain)][0][0], self.chain[file][el1][el2][0][0])
                            except:
                                distance_ante = (self.chain[file][el1][el2][0][0], self.chain[file][el1][el2][0][0])
                            try:
                                # try to find out the distance to next element (tuple)
                                if self.lengths[file][distance_ante] != 0:
                                    distance_next = (
                                        self.chain[file][el1][str(int(el2) + 1)][0][0],
                                        self.chain[file][el1][el2][0][0])
                                else:
                                    distance_next = (self.chain[file][el1][el2][0][0], self.chain[file][el1][el2][0][0])
                            except:
                                distance_next = (self.chain[file][el1][el2][0][0], self.chain[file][el1][el2][0][0])
                            # clean output
                            output = self.correct(self.chain[file][el1][el2])
                            output = [output[0].split("-")[0]] + output[0:]
                            # extract distance antecedent and normalise it (delete length reference)
                            try:
                                dis_ant = self.lengths[file][distance_ante]
                            except KeyError:
                                dis_ant = 0
                            if dis_ant != 0:
                                dis_ant = int(dis_ant) - int(len(el1.split(" ")))
                            if dis_ant == 0:
                                dis_ant = "_"
                            # extract distance prior and normalise it (delete length reference)
                            dis_next = self.lengths[file][distance_next]
                            if dis_next != 0:
                                dis_next = int(dis_next) - int(len(el1.split(" ")))
                            if dis_next == 0:
                                dis_next = "_"
                            # print results
                            print("\t".join(
                                [file.split("_")[0], file, el1, el2] + output + [str(dis_ant), str(dis_next)]),
                                file=out_file)

    def full_pipeline(self):
        """
        Function allows to engange complete pipeline
        """
        # read file and preanalyse
        self.read_files("tsv_new")
        self.analyse_preamble()
        # analyse the distances and filter in chains
        self.count_distance_length()
        self.filter_chain()
        self.sort_groups()
        # print out statistics
        self.statistics()


class DetailCoref:
    def __init__(self, corpus):
        """
        Initialize class
        :param corpus: name of corpus
        """
        self.name = corpus
        self.corpus = {}
        self.intra_sen = {}

    def read_statistics(self):
        """
        read the statistics that have already been saved
        :return:
        """
        # read file
        with open("Data/" + self.name + "/results/coref/statistics.csv", mode="r", encoding="utf-8") as input_file:
            content = input_file.readlines()
        # for every analysed coreferential element
        for line in content[1:]:
            line = line.strip().split("\t")
            if line[1] not in self.corpus:
                self.corpus[line[1]] = {}
            if line[2] not in self.corpus[line[1]]:
                self.corpus[line[1]][line[2]] = []
            # save to corpus
            self.corpus[line[1]][line[2]].append(line[3:])

    def sort_intra(self):
        """
        Count the intra and intersentence relations
        """
        # for every file in the corpus
        for file in self.corpus:
            if file not in self.intra_sen:
                self.intra_sen[file] = {}
            for chain in self.corpus[file]:
                sentence = {}
                # save token in new dictionary
                for token in self.corpus[file][chain]:
                    if token[1] not in sentence:
                        sentence[token[1]] = 0
                    sentence[token[1]] += 1
                self.intra_sen[file][chain] = sentence

    def count_relation_type(self):
        """
        Count all the existing relations
        :return:
        """
        rel_type = {}
        for file in self.intra_sen:
            # dictionary to save all relations
            rel_type[file] = {"intra": 0, "inter": 0, "total": 0}
            # for existing chains
            for chain in self.intra_sen[file]:
                # save amount of intra and intersentence relations
                if len(self.intra_sen[file][chain]) > 1:
                    rel_type[file]["inter"] += len(self.intra_sen[file][chain]) - 1
                for token in self.intra_sen[file][chain]:
                    rel_type[file]["total"] += self.intra_sen[file][chain][token]
                    if self.intra_sen[file][chain][token] > 1:
                        rel_type[file]["intra"] += self.intra_sen[file][chain][token] - 1
        # print results in file
        with open("Data/" + self.name + "/results/coref/relations.csv", mode="w", encoding="utf-8") as output_file:
            print("file", "intra", "inter", 'total', file=output_file, sep="\t")
            for file in rel_type:
                print(file, rel_type[file]["intra"], rel_type[file]["inter"], rel_type[file]["total"], file=output_file,
                      sep="\t")

    def pipe(self):
        """
        Perform all tasks
        """
        self.read_statistics()
        self.sort_intra()
        self.count_relation_type()
