# Changelog

All notable changes to M4B Creator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-20

### Added
- **Multi-Language Support**
  - Complete German/English language switching
  - Language toggle button in top-right corner
  - All UI elements, dialogs, and messages translated
  - Custom Yes/No dialog with translated buttons
  - Language preference maintained throughout application
- **Enhanced User Interface**
  - Improved language switcher with current language indicator
  - All buttons, labels, and status messages are now translatable
  - Better internationalization architecture for future languages

### Changed
- Updated executable name from `M4B-Audiobook-Creator.exe` to `M4B_Creator.exe`
- Improved dialog system with language-aware message boxes
- Enhanced translation system with 170+ translatable strings

### Fixed
- Dialog buttons now properly display in selected language
- Status messages and error dialogs respect language setting
- File dialog titles now translate correctly

### Technical Details
- Added `TRANSLATIONS` dictionary with 'de' and 'en' language support
- Implemented `switch_language()` method for runtime language switching
- Added `update_ui_language()` to refresh all UI elements dynamically
- Custom `_ask_yes_no()` dialog with translated buttons

## [1.0.0] - 2025-01-20

### Added
- Initial release of M4B Creator
- **Batch Processing System**
  - Process multiple folders simultaneously
  - Add folders via button or drag & drop
  - Multi-folder selection support
  - Progress tracking for batch operations
- **Split-Screen GUI**
  - Left panel: Folder list and settings
  - Right panel: Tabbed detail view (Chapters, Metadata, Overview)
  - Responsive layout with resizable panels
- **Chapter Management**
  - View all chapters from audio files
  - Reorder chapters with up/down buttons
  - Automatic chapter numbering
  - Duration display for each chapter
- **Metadata Editor**
  - Edit title, artist/author, album, year, genre
  - Custom output filename
  - Batch metadata application to all folders
  - Metadata extraction from audio files
- **Cover Artwork Management**
  - 300x300 pixel cover preview
  - Upload custom cover images
  - Extract cover art from audio files
  - Save cover art to disk
  - Remove custom cover
  - Automatic PNG conversion for compatibility
- **Audio Processing**
  - Original quality mode (copy streams, no re-encoding)
  - AAC 128k encoding mode
  - Support for multiple input formats (MP3, M4A, M4B, AAC, OGG, FLAC, WAV, WMA)
  - Automatic audio concatenation
  - Chapter timestamp calculation
- **Plex Media Server Compatibility**
  - Audiobook media type tag
  - M4A brand formatting
  - Year-only date format
  - Track metadata
  - FastStart flag for streaming
- **User Interface Features**
  - Drag & Drop support (Windows with windnd)
  - Multi-folder dialog with repeated selection
  - Scrollable status log with real-time updates
  - Folder overview with file details
  - Recursive folder scanning option
  - Custom output directory selection
- **Technical Features**
  - FFmpeg integration for audio processing
  - FFprobe for metadata extraction
  - Threaded batch processing
  - Automatic temporary file cleanup
  - Error handling and reporting

### Technical Details
- Built with Python 3.x and tkinter
- Uses FFmpeg for audio processing
- Pillow for image handling
- windnd for drag & drop support (Windows)
- PyInstaller compatible for executable builds

### Known Limitations
- Chapter titles are auto-numbered (custom titles planned)
- Drag & Drop requires optional windnd package
- No progress bar (shows status messages only)

## [Unreleased]

### Planned Features
- [✅] Additional language support (English, German)
- [❌] Language preference saving between sessions
- [✅ ] Custom chapter title editing
- [❌] Progress bar with percentage
- [❌] Audio preview/playback
- [❌] Automatic chapter detection from silence
- [❌] Batch cover art download
- [❌] Command-line interface (CLI)
- [❌] Preset templates
- [✅ ] Dark mode theme
- [❌] Undo/Redo functionality
- [❌] Drag & Drop for chapter reordering
- [❌] Portable mode (no installation)

### Future Enhancements
- [❌] Automatic bitrate detection
- [❌] Variable bitrate (VBR) support
- [❌] Split large audiobooks
- [❌] Merge multiple M4B files
- [❌] Metadata templates
- [❌] Cover art search integration
- [❌] Quality presets (Low, Medium, High)
- [❌] Resume interrupted processing
- [❌] Duplicate detection
- [❌] File size calculator

---

## Version History

### Version Numbering
- **Major.Minor.Patch** format (Semantic Versioning)
- **Major**: Breaking changes or major new features
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes and minor improvements

### Categories
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features to be removed
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

---

For more information, see:
- [README.md](README.md) - User guide
- [BUILD.md](BUILD.md) - Build instructions
- [GitHub Releases](https://github.com/yourusername/m4b-creator/releases) - Download releases

