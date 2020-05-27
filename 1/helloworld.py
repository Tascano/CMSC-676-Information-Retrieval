import os
from os import listdir
from os.path import isfile, join
import codecs
from bs4 import BeautifulSoup
import nltk
import time
from nltk.corpus import stopwords

#import sys
stop_words = set(stopwords.words('english'))



def sorted_by_frequency(entire_corpus):
    tokens_new_1=[]
    for i in tokens_new:
        if i not in stop_words:
            tokens_new_1.append(i)
    wordfreq = [tokens_new_1.count(p) for p in tokens_new]
    print(dict(list(zip(tokens_new_1, wordfreq))))
    freqdict=dict(list(zip(tokens_new_1, wordfreq)))
    #aux = [(freqdict[key], key) for key in freqdict]
    a = sorted(freqdict.items(), key=lambda x: x[1], reverse=True)
    print(a)
    file = open('Data/Sorted_by_freq.txt', 'w+')
    for word in a:
        if word not in stop_words:
            file.write(' %s\n' % (str(word)))
    file.close()
    file = open('Data/Sorted_by_token.txt', 'w+')
    for key in sorted(freqdict.keys()):
        if key not in stop_words:
            print(key, " :: ", freqdict[key])
            file.write(str(key)+ " :: "+ str(freqdict[key])+'\n')
    file.close()


def create_token_files(individual_file_name,data):
    if not os.path.exists('Data/Tokenized_documents'):
        os.makedirs('Data/Tokenized_documents')
    tokens = nltk.word_tokenize(data)
    tokens_new = [word.lower() for word in tokens if word.isalpha() and word not in stop_words]
    file = open('Data/Tokenized_documents/'+os.path.basename(individual_file_name)+'.txt', 'w+')
    for word in tokens_new:
        if word not in stop_words:
            file.write(' %s\n' % (word))
    file.close()



def dir_check():
    input_dir = 'Data/input_files/'
    onlyfiles = [join(input_dir, f) for f in listdir(input_dir) if isfile(join(input_dir, f))]
    #print(onlyfiles)
    entire_corpus=''
    for individual_file in onlyfiles[:20]:
            print(individual_file)
            f = codecs.open(individual_file, 'rb')
            document = BeautifulSoup(f.read()).get_text()
            #print(document)
            entire_corpus = entire_corpus + ' ' + document
            create_token_files(individual_file , document)

dir_check()

'''
if __name__ == " main ":
    if len(sys.argv)>1:
        dir_check(sys.argv[1],sys.argv[2])
    else:
        print("please")
'''