from numpy.core.shape_base import block
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

player_data = pd.read_csv('player data.csv')

# columns are [Player Name,Wiki Title,Height,Spike,Block,Position]

df = pd.DataFrame(player_data)
null_df = df.isnull().any(axis=1)
nulled_df = df[null_df].reset_index(drop=True)
print(nulled_df)

prefix = 'https://mvolley.com/player/'

player = 'Watten Dustin'

if len(player.split()) == 2:
    true_name = player.split()[1] + ' ' + player.split()[0]
    webpage = prefix + true_name.replace(' ', '-')
    page = requests.get(webpage)
    soup = BeautifulSoup(page.content, "html.parser")

    for item in soup.select('h6'):
        if 'Height' in item.text:
            try:
                height_raw = item.find_next_sibling().text
                height = height_raw.split()[0]
            except:
                height = np.nan
                
        if 'Spike' in item.text:
            try:
                spike_raw = item.find_next_sibling().text
                spike = spike_raw.split()[0]
            except:
                spike = np.nan
        if 'Block' in item.text:
            try:
                block_raw = item.find_next_sibling().text
                block = block_raw.split()[0]
            except:
                block = np.nan
        if 'Position' in item.text:
            try:
                position = item.find_next_sibling().text
            except:
                position = np.nan



    print([player, true_name, height, spike, block, position])

        
