from dataclasses import dataclass, field


@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    # 1. Dichiariamo che è una lista
    # 2. default_factory=list dice a Python di creare una nuova lista vuota [] per ogni istanza
    tracks: list = field(default_factory=list)




    def __str__(self):
        return f"{self.AlbumId} {self.Title}: {len(self.tracks)} tracks "

    def __eq__(self, other):
        if isinstance(other, Album):
            return self.AlbumId == other.AlbumId
        return False

    def __hash__(self):
        return hash(self.AlbumId)

