import pandas as pd
import requests
import wikipedia
import concurrent.futures
import numpy as np
import csv
from bs4 import BeautifulSoup

def player_wiki(player_name):
    print("Getting data for %s.." % player_name)
    try:
        search_query = wikipedia.search(player_name + ' volleyball')[0]
    except:
        search_query = player_name
    player_name_split = player_name.split()
    try:
        title = wikipedia.page(search_query).title
        if any(name.lower() in title.lower() for name in player_name_split):
            if 'volleyball' in title.lower():
                return [wikipedia.page(search_query).url, wikipedia.page(search_query).title, player_name]
            else:
                return [wikipedia.page(search_query + ' volleyball').url, wikipedia.page(search_query + ' volleyball').title, player_name]
        else:
            return [np.nan, np.nan, player_name]
    except:
        return [np.nan, np.nan, player_name]
        
# Reading csv file        
vnl21_scorers = pd.read_csv("Best Attackers VNL21.csv")

columns = ['Player Name', 'Team','Apts','Errors','Attempts','Avg Per Match','Success %','Total']
vnl21_scorers.columns = columns

# Creating list of players
player_list = vnl21_scorers['Player Name'].values.tolist()


with concurrent.futures.ThreadPoolExecutor() as executor:
    player_links = executor.map(player_wiki, player_list)

with open('Attacker Data.csv', 'w', encoding='UTF8', newline = '') as f:

    writer = csv.writer(f)
    file_header = ['Player Name', 'Wiki Title', 'Height', 'Spike', 'Block', 'Position']
    writer.writerow(file_header)

    for player_url_query in player_links:

        if np.nan in player_url_query:
            player_info = [player_url_query[2], np.nan, np.nan, np.nan, np.nan, np.nan]
        
        else:
            player_page = requests.get(player_url_query[0])
            player_page_content = player_page.content
            soup = BeautifulSoup(player_page_content, features="html.parser")
            player_info = [player_url_query[2], player_url_query[1]]

            # Loop through Wiki properties
            for item in soup.find_all('th'):
                
                if 'Height' in item.text:
                    while len(player_info) < 2:
                        player_info.append(np.nan)
                    try:
                        height_raw = item.find_next_sibling().text
                        height = float(height_raw.split()[0])
                        if height < 100:
                            player_info.append(round(height * 100))
                        else:
                            player_info.append(round(height))
                    except:
                            player_info.append(np.nan)

                if 'Spike' in item.text:
                    while len(player_info) < 3:
                        player_info.append(np.nan)
                    try:
                        spike_raw = item.find_next_sibling().text
                        spike = float(spike_raw.split()[0])
                        if spike < 100:
                            player_info.append(round(spike * 100))
                        else:
                            player_info.append(round(spike))
                    except:
                        player_info.append(np.nan)
                if 'Block' in item.text:
                    while len(player_info) < 4:
                        player_info.append(np.nan)
                    try:
                        block_raw = item.find_next_sibling().text
                        block = float(block_raw.split()[0])
                        if block < 100:
                            player_info.append(round(block * 100))
                        else:
                            player_info.append(round(block))
                    except:
                        player_info.append(np.nan)
        
                if 'Position' in item.text:
                    while len(player_info) < 5:
                        player_info.append(np.nan)
                    try:
                        position = item.find_next_sibling().text
                        player_info.append(position.split()[0])
                    except:
                        player_info.append(np.nan)
                    
            print('Writing player: %s info..' % player_info[0])
            writer.writerow(player_info)


# print(player_links)


    
    

 




