# ALiG - Academic literacy in German

This project contains the two pipelines: 
1. Pipeline to pre-annotate txt-files to import them into Inception and annotate them with the Beldeko and GerSumCo annotation guidelines.
2. Pipeline to receive Inception file and clean in it, so that it is ready to be analysed via R

# Installation
Steps:
1. Create a new virtual environment in conda using requirements.txt in the ALiG folder (Terminal: conda create --name NAME --file requirements.txt)
2. Activate the new environment (Terminal: conda activate NAME)
3. Install the spacy libraries
   1. Terminal: python -m spacy download de_core_news_lg
   2. Terminal: python -m spacy download fr_core_news_sm
   3. Terminal: python -m spacy download nl_core_news_sm
4. Create a folder with the name of the corpus
5. Paste the corpus in a subfolder called 'raw'

# Preprocessing pipeline
Steps:
1. Start Preprocess.py to start analysing files
2. The program will ask you to add orig+target to the directory
3. Start Preprocess.py again

If you want to add new sentence boundaries:
1. Use Boundaries.py
2. The program will ask you to add new boundaries to m_sen_boun
3. Start Boundaries.py anew

# Postprocessing pipeline
Steps:
1. Start Postprocess.py to start processing files
2. The program will ask you to fill in lists of topics and annotators
3. Start Postprocess.py again
4. Connectives: The program will ask you to merge all connective constructions
5. Start Postprocess.py again