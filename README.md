# 🎵 Lyrics Genius API

A Python-based lyrics downloader that uses the Genius API to search for artists and retrieve song lyrics. The project provides a simple command-line interface for downloading lyrics and saving them to a text file.

## ✨ Features

- 🔍 Search for songs by artist name.
- 🎶 Download lyrics for multiple artists.
- 🔢 Set the maximum number of songs to retrieve per artist.
- 📄 Save downloaded lyrics in a text file.
- 🛡️ Load API credentials securely from environment variables.
- ⚠️ Handle API errors and missing configuration.
- 📁 Prevent accidental overwriting of existing output files.
- 🧪 Include unit tests for core functionality.

## 🛠️ Technologies Used

- Python 3
- [LyricsGenius](https://github.com/johnwmillr/LyricsGenius)
- [Genius API](https://genius.com/api-clients)
- python-dotenv
- unittest

## 📋 Prerequisites

Before running the project, ensure you have:

- Python 3 installed.
- A Genius API access token.
- Git (optional, for cloning the repository).

## 🚀 Installation

**1. Clone the repository**

```bash
git clone https://github.com/RaavanHrishi07/Lyrics-Genius-API.git
cd Lyrics-Genius-API
```

**2. Install the dependencies**

```bash
python -m pip install -r requirements.txt
```

**3. Configure your API token**

Create a `.env` file in the project root directory and add:

```env
GENIUS_ACCESS_TOKEN=your_genius_access_token_here
```

Replace the placeholder with your actual Genius API access token. Keep your `.env` file private and never commit it to GitHub.

## 💻 Usage

Download lyrics for one artist:

```bash
python lyrics.py -a "Coldplay"
```

Download lyrics for multiple artists:

```bash
python lyrics.py -a "Coldplay" "Arijit Singh"
```

Specify the maximum number of songs per artist:

```bash
python lyrics.py -a "Coldplay" -n 5
```

Choose a custom output filename:

```bash
python lyrics.py -a "Coldplay" -n 5 -o "coldplay_lyrics.txt"
```

### Command-Line Arguments

| Argument | Description | Default |
|---|---|---|
| `-a`, `--artists` | One or more artist names | Required |
| `-n`, `--max-songs` | Maximum songs per artist | `3` |
| `-o`, `--output` | Output text file | `Lyrics.txt` |
| `-h`, `--help` | Display help information | — |

If the requested output filename already exists, the program selects an available numbered filename to avoid overwriting it.

## 🧪 Running Tests

Run the unit tests with:

```bash
python -m unittest -v test_lyrics.py
```

The tests cover API-token validation, successful downloads using mock data, API errors, and output-file protection.

## 📁 Project Structure

```text
Lyrics-Genius-API/
├── lyrics.py
├── lyrics.txt
├── test_lyrics.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env                 # Local file; not committed
```

## ⚠️ Notes

- A valid Genius API token is required to retrieve lyrics from the live API.
- Internet access is required for live API requests.
- Lyrics availability depends on the Genius API and its search results.
- This project is intended for learning and personal use. Respect applicable copyright laws and Genius API terms.

## 👨‍💻 Author

**HRISHIKESH SHARMA**

GitHub: [@RaavanHrishi07](https://github.com/RaavanHrishi07)

---

⭐ If you find this project useful, consider giving the repository a star.
