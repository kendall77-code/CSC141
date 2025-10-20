# 8-7. Album

def make_album(artist, title, songs=None):
    """Build a dictionary describing a music album."""
    album = {'artist': artist.title(), 'title': title.title()}
    if songs:
        album['songs'] = songs
    return album

# Create three albums
album1 = make_album('Mary J Blige', '411')
album2 = make_album('Rod wave', 'Last lap')
album3 = make_album('Bc Tae', 'Abg', songs=25)

# Print each album dictionary
print(album1)
print(album2)
print(album3)