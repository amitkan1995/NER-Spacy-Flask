from flask import Flask, render_template, url_for, request
import re
import pandas as pd
import spacy
#import en_core_web_sm

nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process',methods = ["POST"])
def process():
    if request.method == 'POST':
        try:
            choice = request.form['taskoption']
            rawtext = request.form['rawtext']
            doc = nlp(rawtext)
            d = []
            for ent in doc.ents:
                d.append((ent.label_,ent.text))
                df = pd.DataFrame(d, columns = ('named entity', 'output'))
                ORG_named_entity = df.loc[df['named entity'] == 'ORG']['output']
                PERSON_named_entity = df.loc[df['named entity'] == 'PERSON']['output']
                GPE_named_entity = df.loc[df['named entity'] == 'GPE']['output']
                MONEY_named_entity = df.loc[df['named entity'] == 'MONEY']['output']
                if choice == 'organization':
                    results = ORG_named_entity
                    num_of_results = len(results)
                elif choice == 'person':
                    results = PERSON_named_entity
                    num_of_results = len(results)
                elif choice == 'geopolitical':
                    results = GPE_named_entity
                    num_of_results = len(results)
                elif choice == 'money':
                    results = MONEY_named_entity
                    num_of_results = len(results)
            return render_template("index.html",results=results,num_of_results=num_of_results )
        except Exception as e:
            print("Exception occured as ", e)

if __name__ == '__main__':
    app.run(debug=True)
