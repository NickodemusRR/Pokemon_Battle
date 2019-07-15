import numpy as np 
import pandas as pd 

combats = pd.read_csv('./Datasets/combats.csv')
pokemon = pd.read_csv('./Datasets/pokemon.csv')
pokemon['Overall'] = pokemon['HP'] + pokemon['Attack'] + pokemon['Defense'] + pokemon['Sp. Atk'] + pokemon['Sp. Def'] + pokemon['Speed']

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

X = battle_result.drop(['First_pokemon', 'First_pokemon_name', 'Second_pokemon', 'Second_pokemon_name', 'Winner', 'First_win'], axis=1)
y = battle_result['First_win']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(solver='lbfgs')
logreg.fit(X_train, y_train)

import joblib
joblib.dump(logreg, 'MLmodel')