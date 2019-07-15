import numpy as np 
import pandas as pd 

pokemon = pd.read_csv('pokemon.csv')
pokemon['Overall'] = pokemon['HP'] + pokemon['Attack'] + pokemon['Defense'] + pokemon['Sp. Atk'] + pokemon['Sp. Def'] + pokemon['Speed']
'''
def battle(name1, name2):
    """Given two inputs name of pokemon the function will predict the probabilty of the match result"""

    if name1 in pokemon['Name'].values and name2 in pokemon['Name'].values:
        pokemon1 = pokemon[pokemon['Name']==name1][['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Overall']]
        pokemon2 = pokemon[pokemon['Name']==name2][['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Overall']]
        battle = np.concatenate([pokemon1.values, pokemon2.values], axis=1)
        prediction = rfc.predict(battle)[0] 
        if prediction == 1:
            prob = rfc.predict_proba(battle)[0][1] * 100
            print('{}% {} Wins'.format(prob, name1))
        else:
            prob = rfc.predict_proba(battle)[0][0] * 100
            print('{}% {} Wins'.format(prob, name2))
    else:
        print('Nama Pokemon tidak terdaftar')

battle(name1,name2)
'''