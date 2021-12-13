from ytmusicapi import YTMusic as yt
from icecream import ic
import json

session = yt("headers_auth.json")


def test():
    songList = session.get_library_songs()
    ic("This is the first song {}".format(songList[0]))

def retrieve_library_songs(limit=5000):
    cleanlist = []
    songlist = session.get_library_songs(limit)
    for song in songlist:
        try:
            cleanlist.append({'title': song['title'],
                              'artist': song['artists'][0]['name'],
                              'album': song['album']['name'],
                              'ID': song['videoId']})
        except:
            ic("Error in {}".format(song['title']))
    return cleanlist

def retrieve_uploaded_songs(limit=5000):
    cleanlist = []
    songlist = session.get_library_upload_songs(limit)
    for song in songlist:
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

            songDict = {'title': title,
                              'artist': artist,
                              'album': album,
                              'ID': id_num}
            cleanlist.append(songDict)
        except TypeError as err:
            ic("{} error, not available".format(song['title']))
            ic(song,err)

    return cleanlist

def create_master_list():
    playlistId = 0
    songlist = []
    playlists = session.get_library_playlists()
    for playlist in playlists:
        if(playlist['title'] == "Master List"):
            ic("List found, ID {}".format(playlist['playlistId']))
            playlistId = playlist['playlistId']
    if(playlistId == 0):
        ic("List not found, creating...")
        playlistId = session.create_playlist("Master List", "List with all my songs")
        ic("List created, ID {}".format(playlistId))
    library = retrieve_library_songs(5000)
    uploads = retrieve_uploaded_songs(5000)
    masterlist = library + uploads
    ic("{} elements in master list \n{} elements in library \n{} elements in uploads".format(len(masterlist),
                                                                                                len(library),
                                                                                                len(uploads)))
    for song in masterlist:
        songlist.append(song['ID'])
    ic(session.add_playlist_items(playlistId, songlist, duplicates=False))

def export_list():
    all_songs = retrieve_library_songs() + retrieve_uploaded_songs()
    with open("song_list.csv", 'w', encoding='utf-8') as output:
        output.write("title;artist;album;ID\n")
        for song in all_songs:
            line = song['title'] + ";" + song['artist'] + ";" + song['album'] + ";" + song['ID'] + "\n"
            output.write(line)

def update_libary():
    uploads = retrieve_uploaded_songs(10)
    for song in uploads:
        results = session.search("{} {}".format(song['title'], song['artist']), limit=2)
        ic(results)

if __name__ == "__main__":
    import sys
    
    args = sys.argv[1:]
    ic(args)
    
    if(args[0] == "test"):
        test()
    elif(args[0] == "setup"):
        yt.setup(filepath="headers_auth.json")
    elif(args[0] == "export"):
        export_list()
    elif(args[0] == "masterlist"):
        create_master_list()

    ic("End")
