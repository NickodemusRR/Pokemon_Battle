from flask import Flask, render_template, request, abort, send_from_directory
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

@app.route('/')
def home():
    return render_template('home.html')        

@app.route('/hasil', methods=['POST'])
def hasil():
    name1 = request.form['name1'].title()
    name2 = request.form['name2'].title()
    
    if name1 in pokemon['Name'].values and name2 in pokemon['Name'].values:
        pokemon1 = pokemon[pokemon['Name']==name1][['Name' ,'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Overall']]
        pokemon2 = pokemon[pokemon['Name']==name2][['Name' ,'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Overall']]
        battle = np.concatenate([pokemon1.drop('Name', axis=1).values, pokemon2.drop('Name', axis=1).values], axis=1)
        prediction = model.predict(battle)[0] 

        # membuat grafik
        compare = pd.concat([pokemon1, pokemon2])
        plt.close()
        plt.figure(figsize=(12,4))
        ax = plt.subplot(161)
        plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['HP'], color=['red', 'blue'])
        ax.set_title('HP')
        for p in ax.patches:
            ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.20, p.get_height()-7.8), fontsize=15)
        ax = plt.subplot(162)
        plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Attack'], color=['red', 'blue'])
        ax.set_title('Attack')
        for p in ax.patches:
            ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.20, p.get_height()-7.8), fontsize=15)
        ax = plt.subplot(163)
        plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Defense'], color=['red', 'blue'])
        ax.set_title('Defense')
        for p in ax.patches:
            ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.20, p.get_height()-7.8), fontsize=15)
        ax = plt.subplot(164)
        plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Sp. Atk'], color=['red', 'blue'])
        ax.set_title('Sp. Attack')
        for p in ax.patches:
            ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.20, p.get_height()-7.8), fontsize=15)
        ax = plt.subplot(165)
        plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Sp. Def'], color=['red', 'blue'])
        ax.set_title('Sp. Defense')
        for p in ax.patches:
            ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.20, p.get_height()-7.8), fontsize=15)
        ax = plt.subplot(166)
        plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Speed'], color=['red', 'blue'])
        ax.set_title('Speed')
        for p in ax.patches:
            ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.18, p.get_height()-7.8), fontsize=15)
        plt.tight_layout()
        
        # menyimpan grafik yang sudah dibuat dalam bentuk IO objek
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        graph = 'data:image/png;base64,{}'.format(graph_url)
        
        # mengambil pokemon sprite dari API
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
            prob = round(model.predict_proba(battle)[0][1] * 100)
            win = name1
            result = {'prob':prob, 'win':win, 'graph':graph}
            return render_template('hasil.html', result=result, name1=name1, name2=name2, gambar1=gambar1, gambar2=gambar2)
        else:
            prob = round(model.predict_proba(battle)[0][0] * 100)
            win = name2
            result = {'prob':prob, 'win':win, 'graph':graph}
            return render_template('hasil.html', result=result, name1=name1, name2=name2, gambar1=gambar1, gambar2=gambar2)
    else:
        abort(404)

@app.route('/file/<path:nama>')
def staticfile(nama):
    return send_from_directory('images', nama)

@app.errorhandler(404)
def error(error):
    return render_template('error.html')

if __name__ == "__main__":
    model = joblib.load('MLmodel')
    app.run(debug=True)