
import html2text as ht
import os, codecs, sys, time, math

# check for command line arguments, must have input and output directory path
if len(sys.argv) != 3:
    print("2 arguments required: input and output directory path.")
    exit()

# input directory
input_dir = sys.argv[1]
# output directory
out_dir = sys.argv[2]

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

# https://www.geeksforgeeks.org/python-removing-unwanted-characters-from-string/
badchars = ["\n","\t","\r",",",".","-","_","'",'"',":","`","[","]","(",")","?","|","*",";","!","{","}",">","$","=","%","#","+","<","&","\\","0","1","2","3","4","5","6","7","8","9"]

#initialize frequeny dictionaries
docfreq = {}
freqdict = {}
tf = {}

start = time.time()

fid=0

#set a list of stopwords(inspiration from https://stackoverflow.com/questions/51873067/remove-stop-words-in-text-file-without-nltk)
stopwrd = open("stopwords.txt", "r")
stlist = stopwrd.read()

#read files
files = os.listdir(input_dir)
print("Time for Preprocessing:")
for file in files:
    if file.endswith(".html"):
        fht = open(os.path.join(input_dir, file), "r",  encoding="ascii", errors="ignore")
        html = fht.read()
        #use html2text to parse:  https://www.programcreek.com/python/example/86006/html2text.HTML2Text
        text = ht.HTML2Text()
        text.ignore_links = True
        text.ignore_images = True
        text.images_to_alt = True
        text.protect_links = True
        text.ignore_anchors = True
        text.inline_links = False
        texts = text.handle(html)
        for bad in badchars:
            texts = texts.replace(bad, " ")  #remove characters which dont give any value out of them
        token = texts.split(' ')
        tokens = [word.lower() for word in token if word.isalpha() and word not in stlist]    #remove stop words before calculating freq hash table. For alternate aproach use calcwts1.py

        # Term Frequency (tf): gives us the frequency of the word in each document in the corpus.
        # It is the ratio of number of times the word appears in a document compared to the total number of words in that document.
        freqdict[file] = {}
        tf[file] = {}

        for i in tokens:
            if len(i) > 1:
                # create file frequency hashmap https://www.geeksforgeeks.org/counting-the-frequencies-in-a-list-using-dictionary-in-python/
                #http://homepages.math.uic.edu/~jan/mcs507f11/freqdict.py
                if i in freqdict[file]:
                    freqdict[file][i] += 1
                else:
                    freqdict[file][i] = 1

                # create document with particular token in them frequency hashmap
                if i in docfreq:
                    if file not in docfreq[i]:
                        docfreq[i].append(file)
                else:
                    docfreq[i] = [file]

        for i in freqdict[file]:
            #tf = f(w)/|D|
            wordtf = freqdict[file][i]/len(tokens)
            tf[file][i] = wordtf

        if fid in [10, 20, 40, 60, 80, 100, 200, 300, 400, 500]:
            print(fid,time.time() - start)
        

        fid += 1

#nod = number of documents
nod = fid

fid = 0
# get programs start time
start = time.time()
#https://www.freecodecamp.org/news/how-to-process-textual-data-using-tf-idf-in-python-cd2bbc0a94a3/
print("Calculate weights:")
# calculate and store tf-idf weights of tokens
for file in freqdict:
    # conatins tf-idf for each token
    tfidf = {}
    tokens = freqdict[file]
    for tokens_new in tokens:
        #Inverse Data Frequency (idf): used to calculate the weight of rare words across all documents in the corpus.
        #The words that occur rarely in the corpus have a high IDF score
        #idf = |c|/df(w)
        idf = math.log(nod/len(docfreq[tokens_new]))
        #tfidf is the product of tf and idf
        #tfidf = tf(d,w) * idf(w)
        tfidf[tokens_new] = tf[file][tokens_new] * idf

    if fid in [10, 20, 40, 60, 80, 100, 200, 300, 400, 500]:
        print(fid,time.time() - start)

    fid += 1


    newfiles= codecs.open(os.path.join(out_dir, file) +".wts", 'w', encoding='ascii',errors="ignore")
    sortf = sorted(tfidf.items(), key=lambda kv: kv[1], reverse=True)
    for tokens_new, tfidf in sortf:
        newfiles.write(tokens_new + "\t \t" + str(tfidf) + "\n")
    newfiles.close()