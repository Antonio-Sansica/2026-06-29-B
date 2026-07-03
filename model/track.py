from dataclasses import dataclass


@dataclass
class Track:
    TrackId: int
    Name: str
    AlbumId: int
    MediaTypeId: int
    GenreId: int
    Composer: str
    Milliseconds: int
    Bytes: int
    UnitPrice: int


    def __str__(self):
        return f"{self.TrackId} {self.Name}"

    def __eq__(self, other):
        if isinstance(other, Track):
            return self.TrackId == other.TrackId
        return False

    def __hash__(self):
        return hash(self.TrackId)

