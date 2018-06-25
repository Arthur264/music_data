import musicbrainzngs
musicbrainzngs.set_useragent("music", "1.0.0")
musicbrainzngs.auth("Artyr264", "feduniv264")
result = musicbrainzngs.search_artists(artist="Sting", limit=1)
# image = musicbrainzngs.get_cover_art_list('10560d1a-35a0-4b72-867b-609b8bff2e62')
# print("result", result)
print("image", musicbrainzngs.get_image_list('4edb7c9c-2ce5-4b4d-8527-51268eae946e'))
# for artist in result['artist-list']:
#     print("artict", artist)
    # print(u"{id}: {name}".format(id=artist['id'], name=artist["name"]))