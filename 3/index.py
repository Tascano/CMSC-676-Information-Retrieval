

import html2text as h2t
import os, codecs, sys, time, math, nltk


# check for command line arguments, must have input and output directory path
if len(sys.argv) != 3:
    print("2 arguments required: input and output directory path.")
    exit()

# get input directory
input_dir = sys.argv[1]
# get output directory
out_dir = sys.argv[2]

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

badchars = ["~","ü","\n","\t","\r",",",".","-","_","'",'"'," ","`","[","]","(",")","?","|","*",";","!","{","}",">","$","=","%","#","+","<","&","\\","0","1","2","3","4","5","6","7","8","9","","/","//","@", ":"]

stfile = open("stopwords.txt", "r")
stopwordslist = stfile.read()



#https://dbader.org/blog/records-structs-and-data-transfer-objects-in-python
class mystruc:
    def __init__(self, word, postings, post_no):
        self.word = word
        self.postings = postings
        self.post_no = post_no

files  = os.listdir(input_dir)


def prepop(idx, filefreq,tokenfreq,tf):
    for file in files:
        # if number of files processed == batch size
        if idx == batch:
            break

        # check for html files only
        if file.endswith(".html"):
            # open the file with ascii encoding and ignore encoding errors
            fr = open(os.path.join(input_dir, file), "r", encoding="ascii", errors="ignore")
            # read html content of the file
            html = fr.read()
            # Use Nltk Word Tokenize function to create tokens
            text = nltk.word_tokenize(html)
            tokens = [word.lower() for word in text if word.isalpha() ]

            # contains token frequency for each file
            tokenfreq[file] = {}
            # contains term frequency weight of tokens for each file
            tf[file] = {}

            # iterate all tokens and create hashmap with frequency and document count
            for i in tokens:
                # lower case all characters
                i = i.lower()
                # ignore empty tokens and stopwords
                if len(i) > 1 and i not in stopwordslist:
                    # create frequency distrbution hashmap
                    if i in tokenfreq[file]:
                        tokenfreq[file][i] += 1
                    else:
                        tokenfreq[file][i] = 1

                    # create document frequency hashmap
                    if i not in filefreq:
                        filefreq[i] = set()
                    filefreq[i].add(file)

            for i in tokenfreq[file]:
                # calculate term frequency weights, tf = f(d,w)/|D|
                wordtf = tokenfreq[file][i] / len(tokens)
                tf[file][i] = wordtf
            # increment file counter
            idx += 1

    return idx, filefreq, tokenfreq, tf

def tfidfcalc(tfidf, filefreq,tokenfreq,tf):
    for file in sorted(tokenfreq):
        # conatins tf-idf for each token
        tokens = tokenfreq[file]
        tfidf[file] = {}
        for token in tokens:
            # calculate idf = |c|/df(w)
            idf = math.log(collection/len(filefreq[token]))
            # calculate tfidf = tf(d,w) * idf(w)
            tfidf[file][token] = tf[file][token] * idf
    return tfidf

def indpos(index, postings,filefreq,tfidf):

    for token in sorted(filefreq):
        docs = filefreq[token]
        data = mystruc(token, len(docs), len(postings) + 1)
        index.append(data)
        for doc in docs:
            weight = tfidf[doc][token]
            postings.append((doc, weight))
    return index, postings

xyz = time.time()
# select files in
for batch in [10,20,40,60,80,100,200,300,400,503]:
    filefreq = {}
    tokenfreq = {}
    tf = {}

    # get programs start time
    start = time.time()
    print("Preprocessing:", batch)

    # file counter
    idx=0
    #Preprocessing Function call
    idx, filefreq,tokenfreq,tf = prepop(idx, filefreq,tokenfreq,tf)


    # find elapsed CPU time of files proccessed
    print(time.time() - start)

    # total number of filefreq
    collection = idx

    # get programs start time
    start = time.time()

    print("Calculate weights:", batch)
    # calculate and store tf-idf weights of tokens
    tfidf = {}
    #tfidf function call
    tfidf = tfidfcalc(tfidf, filefreq,tokenfreq,tf)
    # find elapsed CPU time of tfidf calculation
    print(time.time() - start)

    #start indexing
    index = []
    postings = []

    # get programs start time
    start = time.time()

    print("Indexing:", batch)
    #indexing function call
    index, postings = indpos(index, postings, filefreq, tfidf)


    # create postings.txt file
    fn_posting = os.path.join(out_dir, "postings") +".txt"
    fw = codecs.open(fn_posting, 'w', encoding='ascii',errors="ignore")
    for doc, tfidf in postings:
        # store (document, weight) pairs for each token
        fw.write("Token is in document with tfidf : "+ doc + "\t" + str(tfidf) + "\n")
    # close file
    fw.close()

    # create index.txt file
    fn_index = os.path.join(out_dir, "index") +".txt"
    fw = codecs.open(fn_index, 'w', encoding='ascii',errors="ignore")
    for data in index:
        # store (word, # filefreq, start position in postings file) datas
        fw.write("Token : " + data.word + "\n" + "Number of Occurences : " + str(data.postings) + "\n" + "Position in Posting File : " + str(data.post_no) + "\n")
    fw.close()

    # find elapsed CPU time for Indexing
    print(time.time() - start)


print("Total time", time.time() - xyz, os.path.getsize(fn_index)/1024, os.path.getsize(fn_posting)/1024)