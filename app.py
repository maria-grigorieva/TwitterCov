from flask import Flask, render_template, request
from flask import render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

terms = pd.read_csv('db/all_terms.csv')
bigrams = pd.read_csv('db/all_bigrams.csv', header=0, names=['term','counts','date'])
trigrams = pd.read_csv('db/all_trigrams.csv', header=0, names=['term','counts','date'])
freq_terms = pd.read_csv('db/frequent_terms.csv').to_json(orient='records')
freq_bigrams = pd.read_csv('db/frequent_bigrams.csv').to_json(orient='records')
freq_trigrams = pd.read_csv('db/frequent_trigrams.csv').to_json(orient='records')

@app.route('/')
def index():
    return render_template('index.html',
                           freq_terms=freq_terms,
                           freq_bigrams=freq_bigrams,
                           freq_trigrams=freq_trigrams)


@app.route('/scatterplot')
def scatterplot():
    termname = request.args.get('termname')
    if len(termname.split(' ')) == 1:
        graphJSON = visualize_term(termname, terms)
    elif len(termname.split(' ')) == 2:
        graphJSON = visualize_term(termname, bigrams)
    elif len(termname.split(' ')) == 3:
        graphJSON = visualize_term(termname, trigrams)

    return render_template('scatterplot.html',
                           termname=termname,
                           graphJSON=graphJSON)


def visualize_term(term, df):
    term_df = df[df['term']==term].sort_values(by=['date'])
    trace = px.scatter(term_df, x="date", y="counts",
                  hover_name="term")
    return trace.to_html(full_html=False)


if __name__ == '__main__':
    app.run()
