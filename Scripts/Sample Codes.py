import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
#import unidecode


player_data = pd.read_csv('player data.csv')

for row in player_data:
    print(row[1])






# df.loc[df['Player Name'] == 'Souza Alan', 'Position'] = 'test'
# print(df.loc[df['Player Name'] == 'Souza Alan'])


# unaccented_string = unidecode.unidecode(accented_string)