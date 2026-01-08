import os
import math
import string
from bs4 import BeautifulSoup
import json
# -----------------------------
# CONFIGURATION
# -----------------------------

PAGES_DIR = "../pages"
INDEX_FILE = "inverted_index.json"
IDF_FILE = "idf.json"

# -----------------------------
# STEP 1: PARSE HTML → TEXT
# -----------------------------
def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    # Remove script and style elements
    for tag in soup(["script", "style"]):
        tag.decompose()   #removes style and script because they don't have meaningful text
    text = soup.get_text(separator=" ")  #extracts text from html and add spaces to avoid sticking b/w the words
    return text

# -----------------------------
# STEP 2: CLEAN & TOKENIZE
# -----------------------------
def tokenize(text):
    text = text.lower()
    # Remove punctuation
    translator = str.maketrans("", "", string.punctuation)   # removes punctuations
    text = text.translate(translator)
    tokens = text.split()
    return tokens
 
# -----------------------------
# STEP 3: READ DOCUMENTS
# -----------------------------
def load_documents():
    documents = {}    #dictionary to store documents
    for filename in os.listdir(PAGES_DIR):
        if filename.endswith(".html"):
            path = os.path.join(PAGES_DIR, filename)    #creates full path
            with open(path, "r", encoding="utf-8") as f:
                documents[filename] = f.read()
    return documents
 
# -----------------------------
# STEP 4: TERM FREQUENCY
# -----------------------------
def compute_tf(tokens):     #to count word frequency in one document
    tf = {}     #Dictionary to store word counts
    for word in tokens:
        tf[word] = tf.get(word, 0) + 1    #counts how many times a word appears
    return tf
 
# -----------------------------
# STEP 5: BUILD INVERTED INDEX
# -----------------------------
def build_inverted_index(documents):
    inverted_index = {}    #word → list of (document, frequency)
    document_tf = {}    #stores TF per document
    for doc_id, html in documents.items():
        text = extract_text_from_html(html)
        tokens = tokenize(text)
        tf = compute_tf(tokens)
        document_tf[doc_id] = tf
        for word, freq in tf.items():
            if word not in inverted_index:
                inverted_index[word] = []    #Creates a list for the word if it doesn’t exist.
            inverted_index[word].append((doc_id, freq))
    return inverted_index, document_tf
 
# -----------------------------
# STEP 6: CALCULATE IDF
# -----------------------------
def compute_idf(inverted_index, total_docs):
    idf = {}
    for word, postings in inverted_index.items():
        doc_count = len(postings)    #Counts how many documents contain the word
        idf[word] = math.log(total_docs / doc_count)
    return idf
 
# -----------------------------
# STEP 7: SAVE TO DISK
# -----------------------------
def save_to_disk(inverted_index, idf):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(inverted_index, f, indent=2)
    with open(IDF_FILE, "w", encoding="utf-8") as f:
        json.dump(idf, f, indent=2)
 
# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main():
    print("[INFO] Loading documents...")
    documents = load_documents()
    total_docs = len(documents)
    print(f"[INFO] Total documents: {total_docs}")
    print("[INFO] Building inverted index...")
    inverted_index, _ = build_inverted_index(documents)
    print("[INFO] Computing IDF...")
    idf = compute_idf(inverted_index, total_docs)
    print("[INFO] Saving index to disk...")
    save_to_disk(inverted_index, idf)
    print("[DONE] Milestone 3 completed successfully!")
    print(f"[OUTPUT] {INDEX_FILE}, {IDF_FILE}")
 
if __name__ == "__main__":
    main()

