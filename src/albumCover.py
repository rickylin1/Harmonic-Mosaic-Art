class AlbumCover:
    def __init__(self, album_name, artist, red, green, blue, color_group, x_tiles, y_tiles):
        self.album_name = album_name
        self.artist = artist
        self.red = red
        self.green = green
        self.blue = blue
        self.color_group = color_group
        self.x_tiles = x_tiles
        self.y_tiles = y_tiles

    def __repr__(self):
        return (f"AlbumCover(album_name='{self.album_name}', artist='{self.artist}', "
                f"red={self.red}, green={self.green}, blue={self.blue}, "
                f"color_group='{self.color_group}', x_tiles={self.x_tiles}, y_tiles={self.y_tiles})")
    