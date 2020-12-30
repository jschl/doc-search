from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)
es = Elasticsearch('127.0.0.1', port=9200)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search/results', methods=['GET','POST'])
def request_search():

    search_term = request.values.get('input')

    res = es.search(
	index='searchable_content',
	body={
	"query" : {"match": {"content": search_term}},
	"highlight" : {"pre_tags" : ["<b>"] , "post_tags" : ["</b>"], "fields" : {"content":{}}}})

    res['ST'] = search_term
    for hit in res['hits']['hits']:
        hit['preview'] = hit['highlight']['content'][0][:20] + '...'
    return render_template('results.html', res=res)

if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
