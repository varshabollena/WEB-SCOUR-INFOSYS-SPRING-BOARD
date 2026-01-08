from flask import Flask, render_template, request
import json   #loads inverted index and IDF files
import string  #used to remove punctuation

app = Flask(__name__)   #Creates a Flask web app

# Load index data
with open("../indexer/inverted_index.json", "r", encoding="utf-8") as f:
    inverted_index = json.load(f)    #tells which word appears in which document and how many times
 
with open("../indexer/idf.json", "r", encoding="utf-8") as f:
    idf = json.load(f)    #tells how important each word is
 
def tokenize(text):
    text = text.lower()
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    return text.split()
 
def search(query, top_k=5):  #search document for given input and returns top 5 results
    scores = {}
    tokens = tokenize(query)
    for word in tokens:
        if word not in inverted_index:
            continue   #skip words not found in the index
        
        for doc_id, tf in inverted_index[word]:
            score = tf * idf.get(word, 0)
            scores[doc_id] = scores.get(doc_id, 0) + score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
 
@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query")
        results = search(query) 
    return render_template("index.html", query=query, results=results) 
 
if __name__ == "__main__":
    app.run(debug=True)
