import csv
import json
import lyricsgenius
import pandas as pd
import seaborn as sns

lyricsgenius.remove_section_headers = True  #Remove section headers (e.g. [Chorus]) from lyrics when searching
lyricsgenius.skip_non_songs = True  #Include hits thought to be non-songs (e.g. track lists)
lyricsgenius.excluded_terms = [
    "Remix", "Live", "Unplugged", "Demo", "Bonus",
    "Remastered", "Promo", "Version", "Instrumental"
    ]  #Exclude songs with these words in their title


client_access_token = 'ke3Pnl3QrBw7R6QhKv_BieE80GfHg2CryO1Lru-Kdrvp9Kr78jngScx-5otrk0WV'
genius = lyricsgenius.Genius(client_access_token)
genius.verbose = True  # Turn off status messages
# artist = genius.search_artist("Electric Wizard", sort="title")
artist = genius.search_artist("Electric Wizard", max_songs=3, sort="title")
artist.save_lyrics()


#cleaning data
def clean_str(raw_str):
    exclude_sym = ["&", "/", "+", "-", "[", "]", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "(", ")"]
    exclude_word = ["Chorus", "Instrumental", "Verse", "Solo", "Hook"]
    # exclude_nan = ["NaN"]
    # for nan_excl in exclude_nan:
    #     raw_str = raw_str.replace(nan_excl, 'None')
    for word_to_excl in exclude_word:
        raw_str = raw_str.replace(word_to_excl, ' ')
    for sym_to_excl in exclude_sym:
        raw_str = raw_str.replace(sym_to_excl, ' ')
    return raw_str

#save data to csv
albums = {}
song_df = []
for song in artist.songs:
    clean_lyrics = clean_str(song.lyrics)
    if clean_lyrics:
        song_df.append({
            'Album': clean_str(song.album),
            'Title': clean_str(song.title),
            'Lyrics': clean_lyrics,
        })
# print(song_df)

with open('song_dataset_test.csv', 'w', encoding='utf-8') as csv_file:
    fieldnames = ['Album', 'Title', 'Lyrics']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for song in song_df:
        writer.writerow(song)

#convert csv to json
csv_file = 'song_dataset_test.csv'
json_file = 'song_dataset_test.json'
fieldnames = ['Album', 'Title', 'Lyrics']
def read_csv(csv_file, json_file):
    csv_rows = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        field = reader.fieldnames
        for row in reader:
            csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])
        convert_to_json(csv_rows, json_file)

#Convert csv into json
def convert_to_json(data, json_file):
    with open(json_file, "w") as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        f.write(json.dumps(data))

read_csv(csv_file,json_file)


# #open data for analysis
# nrc = 'NRC_Emotion_Lexicon.csv'
# with open (nrc, 'r', encoding = 'utf-8') as nrc_emotion:
#     fields = ['English (en)', 'Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness',
#               'Surprise', 'Trust']
#     reader = csv.DictReader(nrc_emotion, fields)
#     # for row in reader:
#     #     print(row)


dic = pd.read_csv('NRC_Emotion_Lexicon.csv')[['English (en)', 'Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness',
              'Surprise', 'Trust']]

#example
dic[dic['English (en)'].isin(['doom', 'death', 'lie', 'loath'])]


#
def calc_ind(csv_file):
    total = 0
    negative = 0
    for word in csv_file:
        if word in dic['English (en)'].values:
            negative += ((dic[dic['English (en)'] == word]['Negative']).values[0] == 1).astype(int)
            total += 1
    return negative / (total+1)



with open('song_dataset_an.csv', 'w', encoding='utf-8') as result:
    fieldnames = ['Album', 'Title', 'Lyrics', 'Negative_Ind']
    writer = csv.DictWriter(result, fieldnames=fieldnames)
    writer.writeheader()
    for song in song_df:
        writer.writerow(song)


sns.boxplot(x='Negative_Ind', y='Album', data=result )
sns.swarmplot(x='Negative_Ind', y='Album', data=result, color='b')