# ALiG - Academic literacy in German

This project contains the two pipelines: 
1. Pipeline to pre-annotate txt-files to import them into Inception and annotate them with the Beldeko and GerSumCo annotation guidelines.
2. Pipeline to receive Inception file and clean in it, so that it is ready to be analysed via R

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