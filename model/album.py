from dataclasses import dataclass, field

@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    tracks: list = field(default_factory=list)


    def __str__(self):
        return f"{self.Title} - brani : {len(self.tracks)}"


    def __eq__(self, other):

        if isinstance(other, Album):
            return self.AlbumId == other.AlbumId
        return False

    def __hash__(self):
        return hash(self.AlbumId)
