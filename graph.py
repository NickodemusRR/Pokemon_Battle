import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

combats = pd.read_csv('./Datasets/combats.csv')
pokemon = pd.read_csv('./Datasets/pokemon.csv')
pokemon['Overall'] = pokemon['HP'] + pokemon['Attack'] + pokemon['Defense'] + pokemon['Sp. Atk'] + pokemon['Sp. Def'] + pokemon['Speed']

name1 = 'Pikachu'
name2 = 'Charizard'

pokemon1 = pokemon[pokemon['Name']==name1][['Name', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']]
pokemon2 = pokemon[pokemon['Name']==name2][['Name', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']]

compare = pd.concat([pokemon1, pokemon2])

# print(compare)
plt.figure(figsize=(12,8))
ax = plt.subplot(161)
plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['HP'], color=['red', 'blue'])
ax.set_title('HP')
for p in ax.patches:
    ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.24, p.get_height()-3.3), fontsize=15)

ax = plt.subplot(162)
plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Attack'], color=['red', 'blue'])
ax.set_title('Attack')
for p in ax.patches:
    ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.24, p.get_height()-3.3), fontsize=15)

ax = plt.subplot(163)
plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Defense'], color=['red', 'blue'])
ax.set_title('Defense')
for p in ax.patches:
    ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.24, p.get_height()-3.3), fontsize=15)

ax = plt.subplot(164)
plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Sp. Atk'], color=['red', 'blue'])
ax.set_title('Sp. Attack')
for p in ax.patches:
    ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.18, p.get_height()-4.3), fontsize=15)

ax = plt.subplot(165)
plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Sp. Def'], color=['red', 'blue'])
ax.set_title('Sp. Defense')
for p in ax.patches:
    ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.21, p.get_height()-3.5), fontsize=15)

ax = plt.subplot(166)
plt.bar([compare.iloc[0]['Name'], compare.iloc[1]['Name']], compare['Speed'], color=['red', 'blue'])
ax.set_title('Speed')
for p in ax.patches:
    ax.annotate('{}'.format(p.get_height()), (p.get_x()+0.18, p.get_height()-4.3), fontsize=15)

plt.tight_layout()
plt.show()