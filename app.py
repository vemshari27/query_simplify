from flask import Flask, render_template, url_for, redirect, request
from forms import SearchForm
app = Flask(__name__)

from querytree import Run_Search_Engine

@app.route("/")
@app.route('/search')
def search():
  return render_template('search.html')

@app.route('/search_results', methods=['POST','GET'])
def search_results():
  if request.method == 'POST':
    query = request.form
    result = Run_Search_Engine.run_query_processor(query) 
    return render_template('search_results.html', result=result)


if __name__ == '__main__':
    app.run(debug = True)

