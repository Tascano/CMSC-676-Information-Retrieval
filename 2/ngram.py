
import html2text as h2t
import os
import codecs
import sys
import time
import math
import re
if len(sys.argv) != 3:
    print("2 arguments required: input and output directory path.")
    exit()

input_dir = sys.argv[1]
out_dir = sys.argv[2]

if not os.path.exists(out_dir):
    os.mkdir(out_dir)
badchars = ["\n", "\t", "\r", ",", ".", "-", "_", "'", '"', ":", "`", "[", "]", "(", ")", "?", "|", "*", ";", "!", "{",
            "}", ">", "$", "=", "%", "#", "+", "<", "&", "\\", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
docfreq = {}
freqdict = {}
tf = {}
start = time.time()
fid = 0

ngrams = int(input("Enter n:"))
#ngram code reference: https://stackoverflow.com/questions/13423919/computing-n-grams-using-python

files = os.listdir(input_dir)
print("Preprocessing:")
for file in files:
    if file.endswith(".html"):
        fr = open(os.path.join(input_dir, file), "r",
                  encoding="ascii", errors="ignore")
        html = fr.read()
        text_maker = h2t.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True
        text_maker.images_to_alt = True
        text_maker.protect_links = True
        text_maker.ignore_anchors = True
        text_maker.inline_links = False
        text = text_maker.handle(html)
        for esc in badchars:
            text = text.replace(esc, " ")
        text = re.sub(r'\s+', ' ', text)
        freqdict[file] = {}
        tf[file] = {}

        length = len(text) - ngrams
        for i in range(length):
            token = text[i:i+ngrams]
            token = token.lower()
            if token in freqdict[file]:
                freqdict[file][token] += 1
            else:
                freqdict[file][token] = 1
            if token in docfreq:
                if file not in docfreq[token]:
                    docfreq[token].append(file)
            else:
                docfreq[token] = [file]
        for token in freqdict[file]:
            wordtf = (freqdict[file][token] * ngrams)/length
            tf[file][token] = wordtf
        if fid in [10, 20, 40, 80, 100, 200, 300, 400, 500]:
            print(time.time() - start)
        fid += 1

collection = fid

fid = 0
start = time.time()

print("Calculate weights:")
for file in freqdict:
    # conatins tf-idf for each token
    tfidf = {}
    tokens = freqdict[file]
    for tok in tokens:
        idf = math.log(collection/len(docfreq[tok]))
        tfidf[tok] = tf[file][tok] * idf

    if fid in [10, 20, 40, 80, 100, 200, 300, 400, 500]:
        print(time.time() - start)

    fid += 1

    fw = codecs.open(os.path.join(out_dir, file) + ".ngram.wts",
                     'w', encoding='ascii', errors="ignore")
    sortedvals = sorted(tfidf.items(), key=lambda kv: kv[1], reverse=True)
    for tok, tfidf in sortedvals:
          fw.write(tok + "=" + str(tfidf) + "\n")
    fw.close()
