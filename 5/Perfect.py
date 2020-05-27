"""
Find me at:
atuscan1@umbc.edu
Files from here: https://www.csee.umbc.edu/courses/graduate/676/term%20project/?C=N;O=A

"""

import codecs, sys, time, math,os
import codecs, sys, time, math,os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

inpath = sys.argv[1]
outpath = sys.argv[2]

if not os.path.exists(outpath):
   os.mkdir(outpath)

files  = sorted(os.listdir(inpath))
print("Preprocessing:")
documents = {}
centroid = {}

for file in files:
        # check for html files only
        if file.endswith(".html"):
            # open the file with ascii encoding and ignore encoding errors
            fr = open(os.path.join(inpath, file), "r", encoding="ascii", errors="ignore")
            # read html content of the file
            html = fr.read()
            # Use Nltk Word Tokenize function to create tokens
            text = nltk.word_tokenize(html)
            tokens = [word.lower() for word in text if word.isalpha() and not word in stop_words ]
            documents[file] = str(tokens)
            centroid[file] = [file]
print(documents.keys())

tfidf_vectorizer = TfidfVectorizer()
# Referenced from https://sites.temple.edu/tudsc/2017/03/30/measuring-similarity-between-texts-in-python/
# https://stackoverflow.com/questions/12118720/python-tf-idf-cosine-to-find-document-similarity answers
similarity_matrix = {}
for file in documents:
    print(file)
    similarity_matrix[file] = {}
    for otherfile in documents:
        if file == otherfile:
            break
        tfidf_matrix = tfidf_vectorizer.fit_transform([documents[file], documents[otherfile]])
        similarity_matrix[file][otherfile] = ((tfidf_matrix * tfidf_matrix.T).A)[0,1]

clusteredfiles = set()
numberclusters = len(centroid.keys())
while numberclusters - len(clusteredfiles) - 1:
        clustername = str(numberclusters)+".html"
        cosinescore = -1
        for file1 in similarity_matrix.keys():
            for file2 in similarity_matrix[file1].keys():
              if file1 not in clusteredfiles and file2 not in clusteredfiles and file1 != file2:
                  score = similarity_matrix[file1][file2]
                  if score > cosinescore:
                      cosinescore = score
                      c1 = file1 
                      c2 = file2
        
        if cosinescore != -1:
            newcluster = [c1, c2]
            clusteredfiles.update(newcluster)
            centroid[clustername] = newcluster
            similarity_matrix[clustername] = {}

            for cluster in centroid:
                if cluster not in clusteredfiles:
                    cluster1 = centroid[clustername]
                    cluster2 = centroid[cluster]
                    documents = len(cluster1) + len(cluster2)
                    score = 0
                    for document1 in cluster1:
                        for document2 in cluster2:
                            if document1 in similarity_matrix and document2 in similarity_matrix[document1]:
                                score = score + similarity_matrix[document1][document2]
                        similarity_matrix[clustername][cluster] = score/documents
            numberclusters = numberclusters + 1

        if cosinescore < 0.4:
          break    
        print(c1 + "\t clusters with \t" + c2 + "\t to \t" + clustername + "\t with similarity ----||" + str(cosinescore)+"||")


output_file = open(os.path.join(outpath, "cluster.txt"),"w")
output_file.write(str(centroid))
output_file.close()

#similarity_matrix

