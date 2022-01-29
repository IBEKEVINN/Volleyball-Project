import pandas as pd

attackers = pd.read_csv('Best Attackers.csv')

lst = []

for player in attackers['Player Name']:
    lst.append(player)

data = pd.read_csv('player data.csv')

for player in data['Player Name']:
    lst.remove(player)


print(lst)


