
import argparse
import os
import sys
from pathlib import Path

import lyricsgenius
from dotenv import load_dotenv


def create_genius_client():
    """Create a Genius API client using an environment variable."""
    load_dotenv()
    token = os.getenv("GENIUS_ACCESS_TOKEN", "").strip()

    if not token or token == "your_genius_access_token_here":
        raise ValueError(
            "A valid Genius API token is required. Set "
            "GENIUS_ACCESS_TOKEN in your .env file."
        )

    return lyricsgenius.Genius(
        token,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
        remove_section_headers=False,
        timeout=15,
        retries=2,
    )


def get_available_output_path(output_file):
    """Return a filename that does not overwrite an existing file."""
    output_file = Path(output_file).expanduser()

    if not output_file.exists():
        return output_file

    counter = 1
    while True:
        candidate = output_file.with_name(
            f"{output_file.stem}_{counter}{output_file.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def download_lyrics(artists, max_songs, output_file, genius):
    """Download lyrics without overwriting existing output files."""
    output_file = get_available_output_path(output_file)
    total_songs = 0
    failed_artists = []

    try:
        with output_file.open("w", encoding="utf-8") as file:
            for artist_name in artists:
                try:
                    print(f"\nSearching for artist: {artist_name}")

                    artist = genius.search_artist(
                        artist_name,
                        max_songs=max_songs,
                        sort="popularity",
                    )

                    if artist is None or not artist.songs:
                        print(f"No songs found for: {artist_name}")
                        continue

                    for song in artist.songs:
                        file.write(f"Artist: {artist.name}\n")
                        file.write(f"Song: {song.title}\n\n")
                        file.write(song.lyrics or "[Lyrics unavailable]")
                        file.write("\n\n" + "=" * 60 + "\n\n")

                    total_songs += len(artist.songs)
                    print(
                        f"Downloaded {len(artist.songs)} songs "
                        f"for {artist_name}"
                    )

                except Exception as error:
                    message = str(error)
                    print(
                        f"Error processing '{artist_name}': {message}",
                        file=sys.stderr,
                    )
                    failed_artists.append(artist_name)

                    if "401" in message or "invalid_token" in message.lower():
                        print(
                            "Authentication failed. Check your Genius API "
                            "token in the .env file.",
                            file=sys.stderr,
                        )
                        break

    except OSError as error:
        print(f"Could not write output file: {error}", file=sys.stderr)
        return 1

    print(f"\nSongs saved: {total_songs}")
    print(f"Output file: {output_file.resolve()}")

    if failed_artists:
        print(f"Artists with errors: {', '.join(failed_artists)}")

    if total_songs == 0:
        print("No lyrics were downloaded.", file=sys.stderr)
        return 1

    return 1 if failed_artists else 0


def main():
    parser = argparse.ArgumentParser(
        description="Download song lyrics from Genius."
    )
    parser.add_argument(
        "-a",
        "--artists",
        nargs="+",
        required=True,
        help='Artist names, for example: -a "Coldplay" "Arijit Singh"',
    )
    parser.add_argument(
        "-n",
        "--max-songs",
        type=int,
        default=3,
        help="Maximum songs per artist (default: 3)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="Lyrics.txt",
        help="Output text file (a numbered filename is used if it exists)",
    )

    args = parser.parse_args()

    if args.max_songs < 1:
        parser.error("--max-songs must be at least 1")

    try:
        genius = create_genius_client()
    except ValueError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 1

    return download_lyrics(
        args.artists,
        args.max_songs,
        Path(args.output).expanduser(),
        genius,
    )


if __name__ == "__main__":
    raise SystemExit(main())
