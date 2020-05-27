
import html2text as h2t
import os, codecs, sys, time

def input():
    file = open(os.path.join("out", "postings.txt"), "r", encoding="ascii", errors="ignore")
    postings = file.read()
    file.close()
    file = open(os.path.join("out", "index.txt"), "r", encoding="ascii", errors="ignore")
    index = file.read()
    #print(type(index))
    file.close()

    postings = postings.split("\n")
    # print(postings[10])
    index = index.split("\n")
    # print(index[10])
    return postings, index

def retv(query,index,postings):
    for word, weight in query.items():
        if word in index:
            token = index.index(word) #location of token in token index array
            no_postings = int(index[token + 1]) # +1 for no of posting
            index_posts = int(index[token + 2]) # +2 for location of starting posting
            documents = postings[index_posts: index_posts + no_postings+1] #find the documents in posting in the range of indexs
            for entry in documents:
                [document, idf] = entry.split("\t") #posting had doc \n weight so had to break it down
                #print(type(doc)) = str
                if document:
                    retrieved[document] = float(idf) * weight #weighted query

    return retrieved
prev = time.time()
postings, index = input()

arguments = len(sys.argv)
if arguments < 2:
    print("Query required!")
    exit()

query = {}
if sys.argv[1] == "Wt":
    for i in range(3 ,arguments ,2): #arguments are ret.py Wt 0.4 query, so take from argv[3] as query
        word = sys.argv[i].lower()
        query[word] = float(sys.argv[ i -1])  # GETS WEIGHT(0.3/0.4)
else:
    for i in range(1 ,arguments):
        word = sys.argv[i].lower()
        query[word] = 1  #set weight 1

retrieved = {}
retrieved = retv(query,index,postings)
#print(retrieved)
#print(type(retrieved))
sort = sorted(retrieved.items(), key=lambda idf: idf[1], reverse=True)
#print(type(sort))
print(query)
print("Is found in " + str(len(sort)) + " documents")
if len(sort):
    for i in range(min(10, len(sort))):
        print(sort[i][0], sort[i][1])

else:
    print("Word not found in documents indexed")

print("Time :", time.time()- prev)
