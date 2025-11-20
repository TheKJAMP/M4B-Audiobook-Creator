# M4B Creator

A user-friendly GUI tool for creating M4B audiobook files with metadata and chapter support, featuring batch processing capabilities.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## Features

### Core Functionality
- **Batch Processing** - Process multiple folders simultaneously
- **Split-Screen GUI** - Left side: Folder list, Right side: Live details
- **Chapter Management** - Rearrange chapter order with up/down buttons
- **Metadata Editor** - Full control over all metadata fields
- **Recursive Folder Support** - Include subfolders in processing

### Cover Artwork Management
- **Cover Preview** - 300x300 pixel thumbnail display
- **Custom Cover** - Upload your own artwork
- **Cover Extraction** - Extract and save embedded cover art
- **Cover Removal** - Remove custom artwork

### Quality Options
- **Original Quality** - Copy audio streams without re-encoding
- **AAC Encoding** - Convert to AAC 128k for smaller file sizes
- **Multiple Input Formats** - MP3, M4A, M4B, AAC, OGG, FLAC, WAV, WMA

### Batch Operations
- **Batch Metadata** - Apply common metadata to all folders at once
- **Drag & Drop Support** - Drop folders directly into the application
- **Multi-Folder Selection** - Add multiple folders in one operation

## Screenshots

*Coming soon - Add screenshots of your application here*

## Requirements

- **Python 3.7 or higher**
- **FFmpeg** - Must be installed and available in system PATH

### FFmpeg Installation

#### Windows
1. Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
2. Extract the archive
3. Add the `bin` folder to your system PATH

Or use winget:
```bash
winget install Gyan.FFmpeg
```

#### macOS
```bash
brew install ffmpeg
```

#### Linux
```bash
# Debian/Ubuntu
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

### Verify FFmpeg Installation
```bash
ffmpeg -version
```

## Installation

### Option 1: From Source

1. Clone or download this repository
   ```bash
   git clone https://github.com/yourusername/m4b-creator.git
   cd m4b-creator
   ```

2. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application
   ```bash
   python m4b_creator.py
   ```

### Option 2: Standalone Executable (Windows)

1. Download the latest release from the [Releases](https://github.com/yourusername/m4b-creator/releases) page
2. Extract the archive
3. Run `m4b_creator.exe`
4. **Note:** FFmpeg must still be installed separately

## Usage Guide

### Quick Start

1. **Launch the application**
   ```bash
   python m4b_creator.py
   ```

2. **Add folders**
   - Click "+ Ordner" (Add Folder) button
   - Select one or multiple folders containing audio files
   - Or drag and drop folders into the list

3. **Configure settings**
   - Select quality mode: Original or Re-encode (AAC 128k)
   - Enable "Rekursiv" if you want to include subfolders
   - Choose output directory (leave empty to use source folder)

4. **Edit metadata** (optional)
   - Select a folder from the list
   - Switch to "Metadaten" tab
   - Edit title, artist, album, year, genre
   - Upload custom cover artwork if desired
   - Click "💾 Änderungen speichern" to save changes

5. **Manage chapters** (optional)
   - Select a folder from the list
   - Switch to "Kapitel-Reihenfolge" tab
   - Select a chapter and use ↑/↓ buttons to reorder

6. **Start batch processing**
   - Click "⚡ Batch-Verarbeitung starten"
   - Monitor progress in the status window
   - Output files will be created in the specified directory

### Batch Metadata Application

To apply the same metadata (author, year, genre) to all folders:

1. Click "Metadaten auf alle anwenden"
2. Fill in the common fields (leave empty to skip)
3. Click "Anwenden"
4. Note: Title and Album are NOT overwritten as they should be unique per folder

### Drag & Drop Support

The application supports drag and drop for folders:
- Simply drag folders from Windows Explorer onto the folder list
- Multiple folders can be dropped at once

**Note:** Drag & Drop requires `windnd` (Windows) or `tkinterdnd2` (cross-platform)

## Output Format

The tool creates M4B (MPEG-4 Audio Book) files with:
- **Codec:** AAC (original or re-encoded)
- **Container:** MP4/M4B
- **Chapters:** One chapter per input file
- **Metadata:** Complete metadata embedding
- **Cover Art:** Embedded as attached picture (PNG format)
- **Compatibility:** Optimized for Plex Media Server and audiobook players

### Plex Compatibility Features
- `media_type=2` (Audiobook)
- `track=1` metadata
- `M4A` brand with proper formatting
- Year format compatible with Plex (YYYY only)

## Supported Input Formats

- MP3 (.mp3)
- M4A (.m4a)
- M4B (.m4b)
- AAC (.aac)
- OGG Vorbis (.ogg)
- FLAC (.flac)
- WAV (.wav)
- WMA (.wma)

## Technical Details

### How It Works

1. **File Discovery**
   - Scans selected folders for audio files
   - Sorts files alphabetically
   - Optionally includes subfolders recursively

2. **Metadata Extraction**
   - Uses FFprobe to extract existing metadata
   - Reads embedded cover art from audio files
   - Calculates total duration

3. **Chapter Creation**
   - Each input file becomes one chapter
   - Chapter titles are numbered (Chapter 1, Chapter 2, etc.)
   - Timestamps are calculated based on file durations

4. **M4B Assembly**
   - Creates FFmpeg concat file list
   - Generates FFMETADATA1 format metadata file
   - Extracts or uses custom cover art (converted to PNG)
   - Concatenates audio streams
   - Embeds metadata and chapters
   - Adds cover as attached picture

5. **Output**
   - Single M4B file per folder
   - Temporary files are automatically cleaned up

## Building from Source

See [BUILD.md](BUILD.md) for detailed build instructions including:
- How to build the Windows executable
- Dependencies and requirements
- Troubleshooting common build issues

## File Size Estimation

| Bitrate | Quality | Size per Hour | Use Case |
|---------|---------|---------------|----------|
| 32k | Low | ~14 MB | Podcasts, tight storage |
| 48k | Good | ~21 MB | Spoken word audiobooks |
| 64k | Very Good | ~28 MB | Standard audiobooks |
| 96k | Excellent | ~42 MB | High-quality audiobooks |
| 128k | Premium | ~56 MB | Music audiobooks |
| Original | Varies | Varies | No quality loss |

## Troubleshooting

### FFmpeg Not Found
```
Error: FFmpeg is not installed or not in PATH
```
**Solution:** Install FFmpeg and ensure it's in your system PATH. Test with `ffmpeg -version`

### No Audio Files Found
```
Keine Audiodateien in [folder] gefunden!
```
**Solution:** Verify the folder contains supported audio files (.mp3, .m4a, etc.)

### Permission Denied
```
Permission denied
```
**Solution:** Ensure you have write permissions for the output directory

### GUI Does Not Start
```
ModuleNotFoundError: No module named 'tkinter'
```
**Solution:**
- **Windows:** Reinstall Python with tkinter support
- **Linux:** `sudo apt install python3-tk`
- **macOS:** tkinter is included with Python

### Drag & Drop Not Working
Drag & Drop is optional. If not available:
- Use the "+ Ordner" button instead
- Install `windnd` for Windows: `pip install windnd`
- Or install `tkinterdnd2` for cross-platform: `pip install tkinterdnd2`

## Known Limitations

- **GUI Language:** Currently German (English version planned)
- **Chapter Titles:** Automatically numbered (custom titles planned)
- **Large Files:** Very large audiobooks (100+ hours) may take time to process
- **Drag & Drop:** Requires optional dependency installation

## Roadmap

- [ ] English language version
- [ ] Custom chapter title editing
- [ ] Progress bar during processing
- [ ] Audio preview/playback
- [ ] Automatic chapter detection from silence
- [ ] Batch cover download from online sources
- [ ] Command-line interface (CLI) mode
- [ ] Preset templates for common audiobook formats

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and tkinter
- Audio processing powered by [FFmpeg](https://ffmpeg.org/)
- Image handling by [Pillow](https://python-pillow.org/)
- Drag & Drop support via [windnd](https://github.com/Eliav2/pywindnd) and [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)

## Support

If you encounter any issues:
1. Check that FFmpeg is installed: `ffmpeg -version`
2. Verify input files are valid audio files
3. Check the status log in the GUI for detailed error messages
4. Review the console output for additional information
5. Open an issue on GitHub with error details

## Author

Created for audiobook enthusiasts who want a simple, powerful batch conversion tool.

---

**Star this repository if you find it useful!**
