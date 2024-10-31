from spacy.tokenizer import Tokenizer
import re


class Annotation:
    def __init__(self, nlp, name, corpus, dimlex):
        self.name = name
        self.corpus = corpus
        self.nlp = nlp
        self.nlp.tokenizer = Tokenizer(nlp.vocab, token_match=re.compile(r'\S+').match)
        self.dimlex = dimlex
        self.sentences = {}

    def check_connectives(self, token):
        """
        Checks whether token has an entry in dimlex
        :param token: target form
        :return connective annotation
        """
        # if token has an entry...
        if token in self.dimlex.keys():
            # ignore when part of list
            if token in ["und", "oder", "durch", "für", "als", "dass", "ob"]:
                return "_"
            # process
            else:
                if 'sense' in self.dimlex[token].keys():
                    # save highest frequency
                    freq = 0
                    # save meaning with highest frequency
                    mean = ""
                    # output dummy
                    output = "_"
                    # for every possible meaning
                    for sense in self.dimlex[token]['sense']:
                        # see if it the most common one
                        if sense[1] > freq:
                            freq = sense[1]
                            mean = sense[0].split(".")[0]
                    # generate output
                    if mean == "Comparison":
                        output = "01_" + mean
                    elif mean == "Contingency":
                        output = "02_" + mean
                    elif mean == "Expansion":
                        output = "03_" + mean
                    elif mean == "Temporal":
                        output = "04_" + mean
                    # return annotation
                    return output
                else:
                    return "_"
        else:
            return "_"

    def annotate_simple(self):
        """
            Add the simple annotation provided by spacy
        """
        for text in self.corpus:
            # dictionary entry to save annotated texts
            self.corpus[text]["annotated"] = []
            self.sentences[text] = {}
            # processing of the data with spacy
            doc = self.nlp(self.corpus[text]["target_text"])
            # index to refer back to annotation (i - index word (for targetfile); s = index sentence)
            i = 0
            s = 1
            chr_id = 0
            # for every sentence
            for sent in doc.sents:
                # if the sentence is not empty
                if sent.text.strip() != "":
                    self.sentences[text][s] = {"text": "", "annotation": []}
                    self.sentences[text][s]["text"] = sent.text.strip()
                    t = 1  # index in sent
                    # for every sentence
                    for token in sent:
                        if token.text.strip() != "":
                            if token.text.strip() == self.corpus[text]["target_file"][i][2].strip():
                                # save all necessary spacy annotation
                                token_tag = token.tag_
                                if "|" in token_tag:
                                    token_tag = token_tag.split("|")[0]
                                annotation = [str(self.corpus[text]["target_file"][i][0])] + [str(s) + "-" + str(t)] + [
                                    str(chr_id) + "-" + str(chr_id + len(self.corpus[text]["target_file"][i][1]))] + \
                                             [self.corpus[text]["target_file"][i][1]] + [
                                                 self.corpus[text]["target_file"][i][2]] + [token_tag, token.pos_]
                                chr_id += len(self.corpus[text]["target_file"][i][1]) + 1
                                # add the lemma
                                if token.lemma_ == "--":
                                    annotation.append(token.text)
                                else:
                                    annotation.append(token.lemma_)
                                # Add the connective
                                connective = self.check_connectives(token.text.lower())
                                annotation.append(connective)
                                # append the annotated token to the annotated corpus
                                self.corpus[text]["annotated"].append(annotation)
                                self.sentences[text][s]["annotation"].append(annotation)
                                t += 1  # increase index in sentence
                            else:
                                print("Error", token.text, self.corpus[text]["target_file"][i])
                            i += 1  # increase overall index
                    s += 1  # increase index of sentence

    def print_tsv(self):
        """
        prints sentences in tsv format
        :return:
        """
        # for every file and every sentence in the file
        for file in self.sentences:
            with open("Data/" + self.name + "/tsv/" + file.replace("txt", "tsv"), mode="w",
                      encoding="utf-8") as outfile:
                # print header
                print("#FORMAT=WebAnno TSV 3.3", file=outfile)
                print('#T_SP=webanno.custom.Target|Targetform', file=outfile)
                print("#T_SP=de.tudarmstadt.ukp.dkpro.core.api.lexmorph.type.pos.POS|PosValue|coarseValue",
                      file=outfile)
                print("#T_SP=de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Lemma|value", file=outfile)
                print("#T_SP=webanno.custom.Connectives|Con", file=outfile, end="\n\n")
                for sent in self.sentences[file]:
                    print("", file=outfile)
                    # print sentence as texts and annotated words in file
                    print("#Text=" + self.sentences[file][sent]["text"], file=outfile)
                    for word in self.sentences[file][sent]["annotation"]:
                        print("\t".join(word[1:]), file=outfile)
