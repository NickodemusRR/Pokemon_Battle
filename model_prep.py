import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

combats = pd.read_csv('./Datasets/combats.csv')    # result of battle between pokemon
# print(len(combats))
# print(combats.info())

pokemon = pd.read_csv('./Datasets/pokemon.csv')
pokemon['Overall'] = pokemon['HP'] + pokemon['Attack'] + pokemon['Defense'] + pokemon['Sp. Atk'] + pokemon['Sp. Def'] + pokemon['Speed']
# print(pokemon[pokemon['#']==266])

# combining both tables 
name_dict = dict(zip(pokemon['#'], pokemon['Name']))
hp_dict = dict(zip(pokemon['#'], pokemon['HP']))
attack_dict = dict(zip(pokemon['#'], pokemon['Attack']))
defense_dict = dict(zip(pokemon['#'], pokemon['Defense']))
spattack_dict = dict(zip(pokemon['#'], pokemon['Sp. Atk']))
spdefense_dict = dict(zip(pokemon['#'], pokemon['Sp. Def']))
speed_dict = dict(zip(pokemon['#'], pokemon['Speed']))
overall_dict = dict(zip(pokemon['#'], pokemon['Overall']))

battle_result = combats.copy()
battle_result['First_pokemon_name'] = battle_result['First_pokemon'].replace(name_dict)
battle_result['First_pokemon_hp'] = battle_result['First_pokemon'].replace(hp_dict)
battle_result['First_pokemon_attack'] = battle_result['First_pokemon'].replace(attack_dict)
battle_result['First_pokemon_defense'] = battle_result['First_pokemon'].replace(defense_dict)
battle_result['First_pokemon_spattack'] = battle_result['First_pokemon'].replace(spattack_dict)
battle_result['First_pokemon_spdefense'] = battle_result['First_pokemon'].replace(spdefense_dict)
battle_result['First_pokemon_speed'] = battle_result['First_pokemon'].replace(speed_dict)
battle_result['First_pokemon_overall'] = battle_result['First_pokemon'].replace(overall_dict)

battle_result['Second_pokemon_name'] = battle_result['Second_pokemon'].replace(name_dict)
battle_result['Second_pokemon_hp'] = battle_result['Second_pokemon'].replace(hp_dict)
battle_result['Second_pokemon_attack'] = battle_result['Second_pokemon'].replace(attack_dict)
battle_result['Second_pokemon_defense'] = battle_result['Second_pokemon'].replace(defense_dict)
battle_result['Second_pokemon_spattack'] = battle_result['Second_pokemon'].replace(spattack_dict)
battle_result['Second_pokemon_spdefense'] = battle_result['Second_pokemon'].replace(spdefense_dict)
battle_result['Second_pokemon_speed'] = battle_result['Second_pokemon'].replace(speed_dict)
battle_result['Second_pokemon_overall'] = battle_result['Second_pokemon'].replace(overall_dict)

battle_result['First_win'] = battle_result.apply(lambda col: 1 if col['Winner'] == col['First_pokemon'] else 0, axis=1)

# print(battle_result[['First_pokemon', 'First_pokemon_name', 'Second_pokemon', 'Second_pokemon_name', 'First_pokemon_overall', 'Second_pokemon_overall', 'Winner', 'First_win']].head(5))

# data preparation
X = battle_result.drop(['First_pokemon', 'First_pokemon_name', 'Second_pokemon', 'Second_pokemon_name', 'Winner', 'First_win'], axis=1)
y = battle_result['First_win']

# print(X.head())
# print(y.head())
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
# print(X_train.head(2))


# Machine Learning model
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(solver='lbfgs')
logreg.fit(X_train, y_train)
predictions = logreg.predict(X_test)

# Model Testing
from sklearn.metrics import confusion_matrix, classification_report
print(logreg.score(X_test, y_test))
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
# model seems has a high prediction score.

# Battle prediction
name1 = 'Charmander'
name2 = 'Bulbasaur'

def battle(name1, name2):
    """Given two inputs name of pokemon the function will predict the probabilty of the match result"""

    if name1 in pokemon['Name'].values and name2 in pokemon['Name'].values:
        pokemon1 = pokemon[pokemon['Name']==name1][['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Overall']]
        pokemon2 = pokemon[pokemon['Name']==name2][['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Overall']]
        battle = np.concatenate([pokemon1.values, pokemon2.values], axis=1)
        prediction = logreg.predict(battle)[0] 
        if prediction == 1:
            prob = round(logreg.predict_proba(battle)[0][1] * 100)
            print('{}% {} Wins!'.format(prob, name1))
        else:
            prob = round(logreg.predict_proba(battle)[0][0] * 100)
            print('{}% {} Wins!'.format(prob, name2))
    else:
        print('Nama Pokemon tidak terdaftar')

battle(name1,name2)