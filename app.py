from flask import Flask, render_template, request, abort
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64 
import requests
import json

import matplotlib 
matplotlib.use('agg')

app = Flask(__name__)

pokemon = pd.read_csv('./Datasets/pokemon.csv')
pokemon['Overall'] = pokemon['HP'] + pokemon['Attack'] + pokemon['Defense'] + pokemon['Sp. Atk'] + pokemon['Sp. Def'] + pokemon['Speed']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        name1 = request.form['name1']
        name2 = request.form['name2']
        
        if name1 in pokemon['Name'].values and name2 in pokemon['Name'].values:
            pokemon1 = pokemon[pokemon['Name']==name1][['Name' ,'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Overall']]
            pokemon2 = pokemon[pokemon['Name']==name2][['Name' ,'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Overall']]
            battle = np.concatenate([pokemon1.drop('Name', axis=1).values, pokemon2.drop('Name', axis=1).values], axis=1)
            prediction = model.predict(battle)[0] 

            # membuat grafik
            
            compare = pd.concat([pokemon1, pokemon2])
            plt.close()
            plt.figure(figsize=(12,8))
            plt.subplot(161)
            plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['HP'], color=['red', 'blue'])
            plt.title('HP')
            plt.subplot(162)
            plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Attack'], color=['red', 'blue'])
            plt.title('Attack')
            plt.subplot(163)
            plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Defense'], color=['red', 'blue'])
            plt.title('Defense')
            plt.subplot(164)
            plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Sp. Atk'], color=['red', 'blue'])
            plt.title('Sp. Attack')
            plt.subplot(165)
            plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Sp. Def'], color=['red', 'blue'])
            plt.title('Sp. Defense')
            plt.subplot(166)
            plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Speed'], color=['red', 'blue'])
            plt.title('Speed')
            plt.tight_layout()
            
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            graph_url = base64.b64encode(img.getvalue()).decode()
            graph = 'data:image/png;base64,{}'.format(graph_url)
            
            url1='https://pokeapi.co/api/v2/pokemon/'+pokemon1['Name'].values[0].lower()
            url2='https://pokeapi.co/api/v2/pokemon/'+pokemon2['Name'].values[0].lower()
            web1=requests.get(url1)
            web2=requests.get(url2)

            if str(web1)=='<Response [404]>':
                abort(404)
            else:
                gambar1=web1.json()['sprites']['front_default']
            
            if str(web2)=='<Response [404]>':
                abort(404)
            else:
                gambar2=web2.json()['sprites']['front_default']

            if prediction == 1:
                prob = model.predict_proba(battle)[0][1] * 100
                win = name1
                result = {'prob':prob, 'win':win, 'graph':graph}
                return render_template('hasil.html', result=result, gambar1=gambar1, gambar2=gambar2)
            else:
                prob = model.predict_proba(battle)[0][0] * 100
                win = name2
                result = {'prob':prob, 'win':win, 'graph':graph}
                return render_template('hasil.html', result=result, gambar1=gambar1, gambar2=gambar2)
        else:
            abort(404)

@app.errorhandler(404)
def error(error):
    return render_template('error.html')

if __name__ == "__main__":
    model = joblib.load('MLmodel')
    app.run(debug=True)