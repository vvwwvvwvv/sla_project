import csv
import json
import lyricsgenius
import re




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


albums = {}
song_df = []
for song in artist.songs:
    song_df.append({'Album': song.album, 'Title': song.title, 'Lyrics': song.lyrics})

# print(song_df)

# exclude_sym = ["\n","&","/","...","[","]"]




with open('song_dataset_test.csv', 'w', encoding='utf-8') as csv_file:
    fieldnames = ['Album', 'Title', 'Lyrics']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for song in song_df:
        writer.writerow(song)


csv_file = 'song_dataset_test.csv'
json_file = 'song_dataset_test.csv.json'
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