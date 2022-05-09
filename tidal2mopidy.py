from pathlib import Path

import tidalapi
from tidalapi.models import Playlist

session = tidalapi.Session()
user = session.user
playlists = user.playlists()

outdir = Path("~/Music/playlists").expanduser()


def mopidy_uri(track):
    return f"tidal:track:{track.artist.id}:{track.album.id}:{track.id}"


def get_tracks(playlist: Playlist) -> list[str]:
    tracks = session.get_playlist_tracks(playlist.id)
    return [mopidy_uri(t) for t in tracks]


def convert_playlist(playlist):
    tracks = get_tracks(playlist)
    outf = outdir / (playlist.name + ".m3u8")
    if outf.exists():
        outf = outf.with_stem(outf.stem + "-tidal")
    with outf.open("w") as f:
        f.write("\n".join(tracks))


def convert_all():
    for playlist in playlists:
        convert_playlist(playlist)


if __name__ == "__main__":
    session.login_oauth_simple()
    convert_all()
