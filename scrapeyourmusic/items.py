from scrapy.item import Field, Item


class Album(Item):

    url = Field()
    name = Field()
    artist = Field()
    type = Field()
    releaseDate = Field()
    releaseYear = Field()
    recordedDate = Field()
    rating = Field()
    totalRatings = Field()
    rank = Field()
    rankYear = Field()
    primaryGenres = Field()
    secondaryGenres = Field()
    language = Field()


class Artist(Item):

    url = Field()
    name = Field()
    formed = Field()
    members = Field()
    genres = Field()
    studioAlbums = Field()
    liveAlbums = Field()
    EPs = Field()
    singles = Field()


class Proxy(Item):
    ip_address = Field()
    port = Field()
