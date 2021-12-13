"""
This module aims to ease the process of managing the songs in a
YouTube Music account. See docstrings for further information
"""
from icecream import ic
from ytmusicapi import YTMusic as yt

SESSION = yt("headers_auth.json")


def test():
    """This is a test function to probe authentication"""
    song_list = SESSION.get_library_songs()
    ic(f"This is the first song {song_list[0]}")

def retrieve_library_songs(limit=5000):
    """Function queries all library songs an returns a list with all of them"""
    cleanlist = []
    songlist = SESSION.get_library_songs(limit)
    for song in songlist:
        try:
            cleanlist.append({'title': song['title'],
                              'artist': song['artists'][0]['name'],
                              'album': song['album']['name'],
                              'ID': song['videoId']})
        except TypeError as err:
            ic(f"Error in {song['title']}")
            ic(song, err)
    return cleanlist

def retrieve_uploaded_songs(limit=5000):
    """Function queries all uploaded songs an returns a list with all of them"""
    clean_list = []
    song_list = SESSION.get_library_upload_songs(limit)
    for song in song_list:
        try:
            title = ""
            artist = ""
            album = ""
            id_num = ""
            if 'title' in song:
                title = song['title']
            if 'artists' in song:
                artist = song['artists'][0]['name']
            if 'album' in song:
                if song['album'] is not None:
                    album = song['album']['name']
            if 'videoId' in song:
                id_num = song['videoId']

            song_dict = {'title': title,
                        'artist': artist,
                        'album': album,
                        'ID': id_num}
            clean_list.append(song_dict)
        except TypeError as err:
            ic(f"{song['title']} error, not available")
            ic(song, err)
    return clean_list

def create_master_list():
    """Creates a playlist containing all songs from uploads and library"""
    playlist_id = 0
    song_list = []
    playlists = SESSION.get_library_playlists()
    for playlist in playlists:
        if playlist['title'] == "Master List":
            ic(f"List found, ID {playlist['playlistId']}")
            playlist_id = playlist['playlistId']
    if playlist_id == 0:
        ic("List not found, creating...")
        playlist_id = SESSION.create_playlist("Master List", "List with all my songs")
        ic(f"List created, ID {playlist_id}")
    library = retrieve_library_songs(5000)
    uploads = retrieve_uploaded_songs(5000)
    masterlist = library + uploads
    ic(f"{len(masterlist)} elements in master list\n" +
       f"{len(library)} elements in library\n" +
       f"{len(uploads)} elements in uploads")
    for song in masterlist:
        song_list.append(song['ID'])
    ic(SESSION.add_playlist_items(playlist_id, song_list, duplicates=False))

def export_list():
    """Creates a csv file with all the songs from library and uploads"""
    all_songs = retrieve_library_songs() + retrieve_uploaded_songs()
    with open("song_list.csv", 'w', encoding='utf-8') as output:
        output.write("title;artist;album;ID\n")
        for song in all_songs:
            line = song['title'] + ";" + song['artist'] + ";" + \
                   song['album'] + ";" + song['ID'] + "\n"
            output.write(line)

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    ic(args)
    if args[0] == "test":
        test()
    elif args[0] == "setup":
        yt.setup(filepath="headers_auth.json")
    elif args[0] == "export":
        export_list()
    elif args[0] == "masterlist":
        create_master_list()

    ic("End")
