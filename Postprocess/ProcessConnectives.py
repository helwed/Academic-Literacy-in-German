from Preprocess.Skeleton import Skeleton


class Connective(Skeleton):
    def __init__(self, pcorpus):
        super().__init__(pcorpus)

    def filter_connectives(self):
        """
        Method sorts all connectives into single connectives and connective constructions (phrases or multi_word)
        """
        position = set()
        # open two files to store new data
        with open("Data/" + self.name + "/results/connectives/con_results.csv", mode='w', encoding="utf-8") as outfile:
            with open("Data/" + self.name + "/results/connectives/con_multi_results.csv", mode='w',
                      encoding="utf-8") as multi_outfile:
                # for every file and line in the file
                for file in self.corpus:
                    for line in self.corpus[file]:
                        index = line[0].split("-")[1]
                        # for every saved annotation
                        for anno in range(len(line)):
                            line[anno] = line[anno].replace("Unsure", "001\\_Unsure")
                            # Save annotation
                            if "01\\_Comparison" in line[anno] or "02\\_Contingency" in line[
                                anno] or "03\\_Expansion" in line[anno] or "04\\_Temporal" in line[anno]:
                                position.add(anno)
                                if line[anno] == "01\\_Comparison" or line[anno] == "02\\_Contingency" or line[
                                    anno] == "03\\_Expansion" or line[anno] == "04\\_Temporal":
                                    print(file, line[2].lower(), line[3], line[anno], index, "S", file=outfile,
                                          sep="\t")
                                else:
                                    print(file, line[2].lower(), line[3],
                                          "\t".join(sorted(line[anno].split("|"), reverse=True)), index,
                                          file=multi_outfile, sep="\t")

    def reformat_manual(self):
        """
        Method reformats the manually adapted files into a readable format
        """
        # Open manually adapted files
        with open("Data/" + self.name + "/results/connectives/con_multi_results_manual.csv", mode="r",
                  encoding="utf-8") as infile:
            content = infile.readlines()
            # Open new file
            with open("Data/" + self.name + "/results/connectives/con_multi_results_fixed.csv", mode="w",
                      encoding="utf-8") as outfile:
                # for every line...
                for line in content:
                    # ...shorten name of  info and write the elements in line
                    line = line.replace("001\\_Unsure", "U").replace("00\\_Multiword", "M").replace("00\\_Phrase",
                                                                                                    "P").replace(
                        "001\\_Unsur", "U")
                    new = line.strip().split("\t")
                    el = -2
                    short = ""
                    while "\\_" not in new[el]:
                        short += str(new[el])
                        el = el - 1
                    # print in new file
                    print("\t".join(new[0:4] + [new[5]] + [short]), file=outfile)

    def write_combi(self):
        """
        Method merges single connectives and multi-word connectives (and phrases) in one file
        """
        with open("Data/" + self.name + "/results/connectives/con_multi_results_fixed.csv", mode="r",
                  encoding="utf-8") as infile1:
            content1 = infile1.readlines()
        with open("Data/" + self.name + "/results/connectives/con_results.csv", mode="r", encoding="utf-8") as infile2:
            content2 = infile2.readlines()
        with open("Data/" + self.name + "/results/connectives/con_combined.csv", mode="w", encoding="utf-8") as outfile:
            for line in content1:
                print(line.strip(), file=outfile)
            for line in content2:
                print(line.strip(), file=outfile)

    def adapt_for_r(self):
        """
        Method prepares results to be read in R
        """
        with open("Data/" + self.name + "/results/connectives/con_combined.csv", mode="r", encoding="utf-8") as infile:
            content = infile.readlines()
        with open("Data/" + self.name + "/results/connectives/" + self.name + "_connectives.csv", mode="w",
                  encoding="utf-8") as outfile:
            print("participant\tfile\ttopic\ttoken\tPOS\tConnective\tIndex\tExtra", file=outfile)
            for line in content:
                line_content = line.strip().split("\t")
                file = line_content[0]
                topic = self.topics[file]
                print(file.replace(".tsv", "") + "\t" + line_content[0] + "\t" + topic + "\t" + "\t".join(
                    line_content[1:]), file=outfile)
