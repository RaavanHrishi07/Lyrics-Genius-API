
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

from lyrics import (
    create_genius_client,
    download_lyrics,
    get_available_output_path,
)


class TestLyricsDownloader(unittest.TestCase):
    def test_missing_token_is_rejected(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("lyrics.load_dotenv"):
                with self.assertRaisesRegex(
                    ValueError, "valid Genius API token is required"
                ):
                    create_genius_client()

    def test_placeholder_token_is_rejected(self):
        with patch.dict(
            os.environ,
            {"GENIUS_ACCESS_TOKEN": "your_genius_access_token_here"},
            clear=True,
        ):
            with patch("lyrics.load_dotenv"):
                with self.assertRaisesRegex(
                    ValueError, "valid Genius API token is required"
                ):
                    create_genius_client()

    def test_valid_token_creates_client(self):
        with patch.dict(
            os.environ,
            {"GENIUS_ACCESS_TOKEN": "test-token"},
            clear=True,
        ):
            with patch("lyrics.load_dotenv"):
                with patch("lyrics.lyricsgenius.Genius") as mock_genius:
                    client = create_genius_client()

        mock_genius.assert_called_once()
        self.assertIs(client, mock_genius.return_value)

    def test_successful_download_writes_lyrics(self):
        genius = MagicMock()
        song = MagicMock()
        song.title = "Test Song"
        song.lyrics = "Test lyrics"

        artist = MagicMock()
        artist.name = "Test Artist"
        artist.songs = [song]
        genius.search_artist.return_value = artist

        with TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "lyrics.txt"

            result = download_lyrics(
                ["Test Artist"], 1, output_file, genius
            )

            self.assertEqual(result, 0)
            self.assertIn(
                "Test Song",
                output_file.read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Test lyrics",
                output_file.read_text(encoding="utf-8"),
            )

    def test_api_failure_returns_error(self):
        genius = MagicMock()
        genius.search_artist.side_effect = Exception("401 invalid_token")

        with TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "lyrics.txt"

            result = download_lyrics(
                ["Test Artist"], 1, output_file, genius
            )

            self.assertEqual(result, 1)
            self.assertEqual(
                output_file.read_text(encoding="utf-8"), ""
            )

    def test_existing_output_gets_numbered_filename(self):
        with TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "lyrics.txt"
            output_file.write_text(
                "Original lyrics", encoding="utf-8"
            )

            available = get_available_output_path(output_file)

            self.assertEqual(
                available,
                Path(temp_dir) / "lyrics_1.txt",
            )
            self.assertEqual(
                output_file.read_text(encoding="utf-8"),
                "Original lyrics",
            )

    def test_multiple_existing_outputs_get_next_number(self):
        with TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "lyrics.txt"
            output_file.write_text("Original", encoding="utf-8")
            (Path(temp_dir) / "lyrics_1.txt").write_text(
                "First copy", encoding="utf-8"
            )

            available = get_available_output_path(output_file)

            self.assertEqual(
                available,
                Path(temp_dir) / "lyrics_2.txt",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
