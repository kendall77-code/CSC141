# 8-8. User Albums

def make_album(artist, title, songs=None):
    """Build a dictionary describing a music album."""
    album = {'artist': artist.title(), 'title': title.title()}
    if songs:
        album['songs'] = songs
    return album

print("Enter 'quit' at any time to stop.\n")

while True:
    artist = input("Enter the artist's name: ")
    if artist.lower() == 'quit':
        break

    title = input("Enter the album title: ")
    if title.lower() == 'quit':
        break

    album = make_album(artist, title)
    print(f"\nAlbum created: {album}\n")