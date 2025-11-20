#!/usr/bin/env python3
"""
M4B Creator - Ein Tool zum Erstellen von M4B-Hörbuchdateien mit Metadaten und Kapitelunterstützung
"""

import os
import subprocess
import json
import re
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import threading
from PIL import Image, ImageTk


# Mehrsprachige Texte
TRANSLATIONS = {
    'de': {
        # Hauptfenster
        'window_title': 'M4B Creator - Batch-Verarbeitung',

        # Ordnerliste
        'folder_list_title': 'Ordner-Liste (Drag & Drop unterstützt)',
        'add_folder': '+ Ordner',
        'remove_folder': '- Entfernen',
        'clear_list': 'Liste leeren',
        'files_count': '{count} Dateien',

        # Batch-Aktionen
        'batch_actions': 'Batch-Aktionen',
        'apply_metadata_all': 'Metadaten auf alle anwenden',

        # Einstellungen
        'settings': 'Einstellungen',
        'quality': 'Qualität:',
        'original': 'Original',
        'new_aac': 'Neu (AAC 128k)',
        'subfolders': 'Unterordner:',
        'recursive': 'Rekursiv',
        'recursive_checkbox': 'Rekursiv',

        # Ausgabe
        'output': 'Ausgabe',
        'output_folder': 'Ausgabeordner:',
        'empty_source_folder': 'Leer = Quellordner',

        # Buttons
        'start_batch': '⚡ Batch-Verarbeitung starten',
        'status': 'Status',

        # Tabs
        'tab_chapters': 'Kapitel-Reihenfolge',
        'tab_metadata': 'Metadaten',
        'tab_overview': 'Übersicht',
        'no_selection': 'Keine Auswahl',

        # Kapitel-Tab
        'chapters_title': 'Kapitel: {name}',
        'move_up': '↑ Nach oben',
        'move_down': '↓ Nach unten',
        'refresh': '🔄 Aktualisieren',

        # Metadaten-Tab
        'metadata_title': 'Metadaten: {name}',
        'cover_artwork': 'Cover-Artwork',
        'no_cover': 'Kein Cover',
        'change_cover': 'Cover ändern',
        'extract_cover': 'Cover extrahieren',
        'remove_cover': 'Cover entfernen',
        'output_name': 'Ausgabename:',
        'title': 'Titel:',
        'artist': 'Autor:',
        'album': 'Album/Buch:',
        'year': 'Jahr:',
        'genre': 'Genre:',
        'save_changes': '💾 Änderungen speichern',

        # Übersicht-Tab
        'overview_title': 'Übersicht: {name}',
        'folder_name': 'Ordnername',
        'path': 'Pfad',
        'output_filename': 'Ausgabename',
        'file_count': 'Anzahl Dateien',
        'recursive_yes': 'Ja',
        'recursive_no': 'Nein',
        'audio_files': 'Audiodateien',
        'total_duration': 'Gesamtdauer',
        'hours': 'Stunden',
        'minutes': 'Minuten',

        # Dialoge
        'add_multiple_folders': 'Mehrere Ordner hinzufügen?',
        'add_multiple_folders_msg': 'Möchten Sie mehrere Ordner gleichzeitig auswählen?\n\nJa = Mehrere Ordner nacheinander auswählen (mit Abbrechen beenden)\nNein = Nur einen Ordner auswählen',
        'select_folder': 'Ordner auswählen (Abbrechen zum Beenden)',
        'select_audio_folder': 'Ordner mit Audiodateien auswählen',
        'no_files_found': 'Keine Dateien',
        'no_audio_files': 'Keine Audiodateien in {folder} gefunden!',
        'success': 'Erfolg',
        'folders_added': '{count} Ordner hinzugefügt!',
        'folder_added': 'Ordner hinzugefügt!',
        'folders_dropped': '{count} Ordner per Drag & Drop hinzugefügt!',
        'folder_dropped': 'Ordner per Drag & Drop hinzugefügt!',
        'remove_folder_confirm': "'{name}' aus der Liste entfernen?",
        'clear_all_confirm': 'Alle Ordner entfernen?',
        'confirm': 'Bestätigen',
        'no_folders': 'Keine Ordner',
        'add_folders_first': 'Bitte erst Ordner hinzufügen!',
        'metadata_applied': 'Metadaten auf {count} Ordner angewendet!',
        'saved': 'Gespeichert',
        'changes_saved': 'Änderungen wurden gespeichert!',
        'cover_changed': 'Cover wurde geändert!',
        'cover_saved': 'Cover gespeichert:\n{path}',
        'cover_removed': 'Cover wurde entfernt!',
        'no_custom_cover': 'Kein benutzerdefiniertes Cover vorhanden!',
        'no_cover_found': 'Kein Cover',
        'no_cover_to_extract': 'Kein Cover zum Extrahieren gefunden!',
        'error': 'Fehler',
        'add_folder_first': 'Bitte mindestens einen Ordner hinzufügen!',
        'batch_complete': 'Alle {count} M4B-Dateien wurden erfolgreich erstellt!',
        'partial_success': 'Teilweise erfolgreich',
        'partial_success_msg': 'Erfolgreich: {success}\nFehlgeschlagen: {failed}\n\nSiehe Status-Log für Details.',

        # Batch-Metadaten-Dialog
        'batch_metadata_title': 'Metadaten auf alle Ordner anwenden',
        'batch_metadata_info': 'Diese Metadaten werden auf ALLE Ordner angewendet:',
        'batch_metadata_hint': 'Leere Felder werden übersprungen (nicht überschrieben).',
        'batch_metadata_note': 'Hinweis: Der Titel und Albumname werden NICHT überschrieben,\nda diese für jeden Ordner individuell sein sollten.',
        'no_data': 'Keine Daten',
        'fill_one_field': 'Bitte mindestens ein Feld ausfüllen!',
        'cancel': 'Abbrechen',
        'apply': 'Anwenden',

        # Status-Nachrichten
        'creating_concat_list': 'Erstelle Konkatenierungsliste...',
        'extracting_cover': 'Extrahiere Cover-Art...',
        'using_custom_cover': 'Verwende benutzerdefiniertes Cover: {name}',
        'cover_found': 'Cover-Art gefunden in: {name}',
        'creating_metadata': 'Erstelle Metadaten-Datei mit Kapiteln...',
        'creating_m4b_original': 'Erstelle M4B-Datei (Original-Qualität)...',
        'creating_m4b_convert': 'Konvertiere zu M4B...',
        'ffmpeg_running': 'FFmpeg läuft...',
        'm4b_created': 'M4B-Datei erfolgreich erstellt!',
        'batch_started': '=== Batch-Verarbeitung gestartet ===',
        'batch_count': 'Anzahl Ordner: {count}',
        'audio_mode': 'Audio-Modus: {mode}',
        'audio_mode_copy': 'Original kopieren',
        'audio_mode_encode': 'Neu codieren',
        'processing': '[{current}/{total}] Verarbeite: {name}',
        'warning_no_files': 'WARNUNG: Keine Audiodateien!',
        'files': 'Dateien: {count}',
        'chapters': 'Kapitel: {count}',
        'output_file': 'Ausgabe: {path}',
        'success_created': '✓ ERFOLG: {name}.m4b erstellt!',
        'error_failed': '✗ FEHLER: Konnte nicht erstellt werden!',
        'error_msg': '✗ FEHLER: {msg}',
        'batch_completed': '=== Batch-Verarbeitung abgeschlossen ===',
        'total': 'Gesamt: {count} Ordner',
        'successful': 'Erfolgreich: {count}',
        'failed': 'Fehlgeschlagen: {count}',

        # Datei-Dialoge
        'select_cover': 'Cover-Bild auswählen',
        'image_files': 'Bild-Dateien',
        'all_files': 'Alle Dateien',
        'save_cover': 'Cover speichern unter',
        'select_output_folder': 'Ausgabeordner wählen',

        # Sprache
        'language': '🌐 Sprache: Deutsch',
        'switch_language': 'Switch to English',

        # Dialog-Buttons
        'yes': 'Ja',
        'no': 'Nein',
    },
    'en': {
        # Main window
        'window_title': 'M4B Creator - Batch Processing',

        # Folder list
        'folder_list_title': 'Folder List (Drag & Drop supported)',
        'add_folder': '+ Add Folder',
        'remove_folder': '- Remove',
        'clear_list': 'Clear List',
        'files_count': '{count} Files',

        # Batch actions
        'batch_actions': 'Batch Actions',
        'apply_metadata_all': 'Apply Metadata to All',

        # Settings
        'settings': 'Settings',
        'quality': 'Quality:',
        'original': 'Original',
        'new_aac': 'New (AAC 128k)',
        'subfolders': 'Subfolders:',
        'recursive': 'Recursive',
        'recursive_checkbox': 'Recursive',

        # Output
        'output': 'Output',
        'output_folder': 'Output Folder:',
        'empty_source_folder': 'Empty = Source Folder',

        # Buttons
        'start_batch': '⚡ Start Batch Processing',
        'status': 'Status',

        # Tabs
        'tab_chapters': 'Chapter Order',
        'tab_metadata': 'Metadata',
        'tab_overview': 'Overview',
        'no_selection': 'No Selection',

        # Chapters tab
        'chapters_title': 'Chapters: {name}',
        'move_up': '↑ Move Up',
        'move_down': '↓ Move Down',
        'refresh': '🔄 Refresh',

        # Metadata tab
        'metadata_title': 'Metadata: {name}',
        'cover_artwork': 'Cover Artwork',
        'no_cover': 'No Cover',
        'change_cover': 'Change Cover',
        'extract_cover': 'Extract Cover',
        'remove_cover': 'Remove Cover',
        'output_name': 'Output Name:',
        'title': 'Title:',
        'artist': 'Author:',
        'album': 'Album/Book:',
        'year': 'Year:',
        'genre': 'Genre:',
        'save_changes': '💾 Save Changes',

        # Overview tab
        'overview_title': 'Overview: {name}',
        'folder_name': 'Folder Name',
        'path': 'Path',
        'output_filename': 'Output Name',
        'file_count': 'Number of Files',
        'recursive_yes': 'Yes',
        'recursive_no': 'No',
        'audio_files': 'Audio Files',
        'total_duration': 'Total Duration',
        'hours': 'Hours',
        'minutes': 'Minutes',

        # Dialogs
        'add_multiple_folders': 'Add Multiple Folders?',
        'add_multiple_folders_msg': 'Would you like to select multiple folders at once?\n\nYes = Add multiple folders one by one (cancel to finish)\nNo = Add only one folder',
        'select_folder': 'Select Folder (Cancel to finish)',
        'select_audio_folder': 'Select Folder with Audio Files',
        'no_files_found': 'No Files',
        'no_audio_files': 'No audio files found in {folder}!',
        'success': 'Success',
        'folders_added': '{count} folders added!',
        'folder_added': 'Folder added!',
        'folders_dropped': '{count} folders added via Drag & Drop!',
        'folder_dropped': 'Folder added via Drag & Drop!',
        'remove_folder_confirm': "Remove '{name}' from list?",
        'clear_all_confirm': 'Remove all folders?',
        'confirm': 'Confirm',
        'no_folders': 'No Folders',
        'add_folders_first': 'Please add folders first!',
        'metadata_applied': 'Metadata applied to {count} folders!',
        'saved': 'Saved',
        'changes_saved': 'Changes have been saved!',
        'cover_changed': 'Cover has been changed!',
        'cover_saved': 'Cover saved:\n{path}',
        'cover_removed': 'Cover has been removed!',
        'no_custom_cover': 'No custom cover available!',
        'no_cover_found': 'No Cover',
        'no_cover_to_extract': 'No cover found to extract!',
        'error': 'Error',
        'add_folder_first': 'Please add at least one folder!',
        'batch_complete': 'All {count} M4B files created successfully!',
        'partial_success': 'Partially Successful',
        'partial_success_msg': 'Successful: {success}\nFailed: {failed}\n\nSee status log for details.',

        # Batch metadata dialog
        'batch_metadata_title': 'Apply Metadata to All Folders',
        'batch_metadata_info': 'This metadata will be applied to ALL folders:',
        'batch_metadata_hint': 'Empty fields will be skipped (not overwritten).',
        'batch_metadata_note': 'Note: Title and album name will NOT be overwritten,\nas they should be individual for each folder.',
        'no_data': 'No Data',
        'fill_one_field': 'Please fill in at least one field!',
        'cancel': 'Cancel',
        'apply': 'Apply',

        # Status messages
        'creating_concat_list': 'Creating concatenation list...',
        'extracting_cover': 'Extracting cover art...',
        'using_custom_cover': 'Using custom cover: {name}',
        'cover_found': 'Cover art found in: {name}',
        'creating_metadata': 'Creating metadata file with chapters...',
        'creating_m4b_original': 'Creating M4B file (original quality)...',
        'creating_m4b_convert': 'Converting to M4B...',
        'ffmpeg_running': 'FFmpeg running...',
        'm4b_created': 'M4B file created successfully!',
        'batch_started': '=== Batch Processing Started ===',
        'batch_count': 'Number of Folders: {count}',
        'audio_mode': 'Audio Mode: {mode}',
        'audio_mode_copy': 'Copy Original',
        'audio_mode_encode': 'Re-encode',
        'processing': '[{current}/{total}] Processing: {name}',
        'warning_no_files': 'WARNING: No audio files!',
        'files': 'Files: {count}',
        'chapters': 'Chapters: {count}',
        'output_file': 'Output: {path}',
        'success_created': '✓ SUCCESS: {name}.m4b created!',
        'error_failed': '✗ ERROR: Could not be created!',
        'error_msg': '✗ ERROR: {msg}',
        'batch_completed': '=== Batch Processing Completed ===',
        'total': 'Total: {count} Folders',
        'successful': 'Successful: {count}',
        'failed': 'Failed: {count}',

        # File dialogs
        'select_cover': 'Select Cover Image',
        'image_files': 'Image Files',
        'all_files': 'All Files',
        'save_cover': 'Save Cover As',
        'select_output_folder': 'Select Output Folder',

        # Language
        'language': '🌐 Language: English',
        'switch_language': 'Wechsel zu Deutsch',

        # Dialog buttons
        'yes': 'Yes',
        'no': 'No',
    }
}


class AudioFile:
    """Repräsentiert eine Audiodatei mit Metadaten"""

    def __init__(self, path: str):
        self.path = path
        self.metadata = {}
        self.duration = 0.0
        self.has_cover = False
        self.cover_stream_index = None
        self.extract_metadata()

    def extract_metadata(self):
        """Extrahiert Metadaten aus der Audiodatei mit FFprobe"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                self.path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)

                # Dauer extrahieren
                if 'format' in data and 'duration' in data['format']:
                    self.duration = float(data['format']['duration'])

                # Metadaten extrahieren
                if 'format' in data and 'tags' in data['format']:
                    self.metadata = data['format']['tags']

                # Cover-Art prüfen
                if 'streams' in data:
                    for idx, stream in enumerate(data['streams']):
                        if stream.get('codec_type') == 'video' or stream.get('codec_name') in ['mjpeg', 'png', 'jpg']:
                            self.has_cover = True
                            self.cover_stream_index = idx
                            break

        except Exception as e:
            print(f"Fehler beim Extrahieren der Metadaten aus {self.path}: {e}")


class FolderData:
    """Repräsentiert einen Ordner mit allen Audiodateien und Einstellungen"""

    def __init__(self, folder_path: str, recursive: bool = False):
        self.folder_path = folder_path
        self.folder_name = Path(folder_path).name
        self.recursive = recursive
        self.audio_files: List[AudioFile] = []
        self.metadata = {}
        self.output_name = self.folder_name
        self.custom_artwork_path: Optional[str] = None  # Benutzerdefiniertes Artwork
        self.load_files()

    def load_files(self):
        """Lädt alle Audiodateien aus dem Ordner"""
        audio_extensions = {'.mp3', '.m4a', '.m4b', '.aac', '.ogg', '.flac', '.wav', '.wma'}
        file_paths = []

        if self.recursive:
            for root, dirs, files in os.walk(self.folder_path):
                for file in files:
                    if Path(file).suffix.lower() in audio_extensions:
                        file_paths.append(os.path.join(root, file))
        else:
            for file in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, file)
                if os.path.isfile(file_path) and Path(file).suffix.lower() in audio_extensions:
                    file_paths.append(file_path)

        # Sortiert hinzufügen
        for path in sorted(file_paths):
            audio_file = AudioFile(path)
            self.audio_files.append(audio_file)

        # Metadaten aus erster Datei extrahieren
        if self.audio_files:
            first_file = self.audio_files[0]
            self.metadata = {
                'title': first_file.metadata.get('album', first_file.metadata.get('title', self.folder_name)),
                'artist': first_file.metadata.get('artist', ''),
                'album': first_file.metadata.get('album', ''),
                'date': first_file.metadata.get('date', ''),
                'genre': first_file.metadata.get('genre', ''),
            }

    def move_file_up(self, index: int):
        """Verschiebt eine Datei nach oben"""
        if 0 < index < len(self.audio_files):
            self.audio_files[index], self.audio_files[index - 1] = \
                self.audio_files[index - 1], self.audio_files[index]

    def move_file_down(self, index: int):
        """Verschiebt eine Datei nach unten"""
        if 0 <= index < len(self.audio_files) - 1:
            self.audio_files[index], self.audio_files[index + 1] = \
                self.audio_files[index + 1], self.audio_files[index]


class M4BCreator:
    """Hauptklasse zum Erstellen von M4B-Dateien"""

    def __init__(self):
        pass

    def create_m4b(self, folder_data: FolderData, output_path: str, copy_audio: bool = True, callback=None) -> bool:
        """Erstellt die M4B-Datei aus FolderData"""
        try:
            if not folder_data.audio_files:
                raise ValueError("Keine Eingabedateien vorhanden")

            # Temporäre Dateien
            temp_dir = Path(output_path).parent
            concat_file = temp_dir / "concat_list.txt"
            metadata_file = temp_dir / "metadata.txt"
            cover_file = None

            if callback:
                callback("Erstelle Konkatenierungsliste...")

            # Erstelle Konkatenierungsliste
            with open(concat_file, 'w', encoding='utf-8') as f:
                for audio_file in folder_data.audio_files:
                    safe_path = audio_file.path.replace("\\", "/").replace("'", "'\\''")
                    f.write(f"file '{safe_path}'\n")

            if callback:
                callback("Extrahiere Cover-Art...")

            # Cover-Art: Entweder benutzerdefiniert oder aus Datei extrahieren
            if folder_data.custom_artwork_path and os.path.exists(folder_data.custom_artwork_path):
                # Benutzerdefiniertes Artwork verwenden und als PNG konvertieren
                cover_file = temp_dir / "cover.png"
                convert_cmd = [
                    'ffmpeg',
                    '-i', folder_data.custom_artwork_path,
                    '-vcodec', 'png',
                    '-y',
                    str(cover_file)
                ]
                subprocess.run(convert_cmd, capture_output=True)
                if callback:
                    callback(f"Verwende benutzerdefiniertes Cover: {Path(folder_data.custom_artwork_path).name}")
            else:
                # Cover-Art aus der ersten Datei extrahieren und als PNG konvertieren
                for audio_file in folder_data.audio_files:
                    if audio_file.has_cover:
                        cover_file = temp_dir / "cover.png"

                        extract_cmd = [
                            'ffmpeg',
                            '-i', audio_file.path,
                            '-an',
                            '-vcodec', 'png',
                            '-y',
                            str(cover_file)
                        ]
                        subprocess.run(extract_cmd, capture_output=True)

                        if callback:
                            callback(f"Cover-Art gefunden in: {Path(audio_file.path).name}")
                        break

            if callback:
                callback("Erstelle Metadaten-Datei mit Kapiteln...")

            # Erstelle Metadaten-Datei mit Kapiteln
            cumulative_time = 0.0
            with open(metadata_file, 'w', encoding='utf-8') as f:
                f.write(";FFMETADATA1\n")

                # Globale Metadaten
                for key, value in folder_data.metadata.items():
                    if value:
                        # Datum auf Jahr reduzieren für Plex-Kompatibilität
                        if key == 'date' and 'T' in value:
                            value = value.split('-')[0]  # Nur Jahr behalten (z.B. "2011")
                        f.write(f"{key}={value}\n")

                # Kapitel
                for index, audio_file in enumerate(folder_data.audio_files, start=1):
                    chapter_title = f"Chapter {index}"
                    f.write("\n[CHAPTER]\n")
                    f.write("TIMEBASE=1/1000\n")
                    f.write(f"START={int(cumulative_time * 1000)}\n")
                    f.write(f"END={int((cumulative_time + audio_file.duration) * 1000)}\n")
                    f.write(f"title={chapter_title}\n")
                    cumulative_time += audio_file.duration

            if callback:
                if copy_audio:
                    callback("Erstelle M4B-Datei (Original-Qualität)...")
                else:
                    callback("Konvertiere zu M4B...")

            # Erstelle M4B-Datei
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-i', str(metadata_file),
            ]

            # Cover-Art hinzufügen, falls vorhanden
            if cover_file and cover_file.exists():
                cmd.extend(['-i', str(cover_file)])
                cmd.extend(['-map', '0:a'])
                cmd.extend(['-map', '2:v'])
                cmd.extend(['-map_metadata', '1'])

                if copy_audio:
                    cmd.extend(['-c:a', 'copy'])
                    cmd.extend(['-c:v', 'copy'])
                else:
                    cmd.extend(['-c:a', 'aac', '-b:a', '128k'])
                    cmd.extend(['-c:v', 'copy'])

                cmd.extend(['-disposition:v:0', 'attached_pic'])
            else:
                cmd.extend(['-map_metadata', '1'])

                if copy_audio:
                    cmd.extend(['-c', 'copy'])
                else:
                    cmd.extend(['-c:a', 'aac', '-b:a', '128k'])

            # Plex-kompatible Metadaten hinzufügen
            cmd.extend(['-metadata', 'media_type=2'])  # Audiobook
            cmd.extend(['-metadata', 'track=1'])        # Track-Nummer

            # M4A Brand für bessere Plex-Kompatibilität
            cmd.extend(['-brand', 'M4A '])  # Wichtig: mit Leerzeichen am Ende!

            cmd.extend([
                '-f', 'mp4',
                '-movflags', '+faststart',
                '-y',
                output_path
            ])

            if callback:
                callback("FFmpeg läuft...")

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise Exception(f"FFmpeg Fehler:\n{result.stderr}")

            # Aufräumen
            if concat_file.exists():
                concat_file.unlink()
            if metadata_file.exists():
                metadata_file.unlink()
            if cover_file and cover_file.exists():
                cover_file.unlink()

            if callback:
                callback("M4B-Datei erfolgreich erstellt!")

            return True

        except Exception as e:
            if callback:
                callback(f"Fehler: {str(e)}")
            return False


class BatchMetadataDialog:
    """Dialog zum Anwenden von Metadaten auf alle Ordner"""

    def __init__(self, parent, language='de'):
        self.metadata = {}
        self.result = False
        self.language = language

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(self.t('batch_metadata_title'))
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.setup_ui()

    def t(self, key: str, **kwargs) -> str:
        """Übersetzt einen Schlüssel"""
        text = TRANSLATIONS[self.language].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text

    def setup_ui(self):
        """Erstellt die Benutzeroberfläche"""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text=self.t('batch_metadata_info'),
                 font=('TkDefaultFont', 10, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        ttk.Label(main_frame, text=self.t('batch_metadata_hint'),
                 font=('TkDefaultFont', 9), foreground='gray').pack(anchor=tk.W, pady=(0, 10))

        # Metadaten-Felder
        self.metadata_entries = {}
        metadata_fields = [
            ('artist', self.t('artist')),
            ('date', self.t('year')),
            ('genre', self.t('genre')),
        ]

        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        for key, label in metadata_fields:
            field_frame = ttk.Frame(fields_frame)
            field_frame.pack(fill=tk.X, pady=5)
            ttk.Label(field_frame, text=label, width=15).pack(side=tk.LEFT, padx=(0, 5))
            entry = ttk.Entry(field_frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.metadata_entries[key] = entry

        # Info
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(info_frame, text=self.t('batch_metadata_note'), font=('TkDefaultFont', 8),
                 foreground='gray', justify=tk.LEFT).pack(anchor=tk.W)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(button_frame, text=self.t('cancel'), command=self.cancel).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text=self.t('apply'), command=self.apply).pack(side=tk.RIGHT, padx=5)

    def apply(self):
        """Wendet die Metadaten an"""
        self.metadata = {}
        for key, entry in self.metadata_entries.items():
            value = entry.get().strip()
            if value:
                self.metadata[key] = value

        if not self.metadata:
            messagebox.showwarning(self.t('no_data'), self.t('fill_one_field'))
            return

        self.result = True
        self.dialog.destroy()

    def cancel(self):
        """Bricht ab"""
        self.result = False
        self.dialog.destroy()


class M4BCreatorGUI:
    """GUI für den M4B Creator"""

    def __init__(self, root):
        self.root = root
        self.current_language = 'de'  # Standard: Deutsch
        self.root.title("M4B Creator - Batch-Verarbeitung")
        self.root.geometry("1400x800")

        self.folder_data_list: List[FolderData] = []
        self.selected_folder_index: Optional[int] = None

        # UI-Referenzen für Sprachumschaltung
        self.ui_elements = {}

        self.setup_ui()

    def t(self, key: str, **kwargs) -> str:
        """Übersetzt einen Schlüssel in die aktuelle Sprache"""
        text = TRANSLATIONS[self.current_language].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text

    def switch_language(self):
        """Wechselt zwischen Deutsch und Englisch"""
        self.current_language = 'en' if self.current_language == 'de' else 'de'
        self.update_ui_language()

    def _ask_yes_no(self, title, message):
        """Zeigt einen Ja/Nein-Dialog mit übersetzten Buttons"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.grab_set()

        result = [None]  # Use list to store result from button callbacks

        # Nachricht
        msg_frame = ttk.Frame(dialog, padding="20")
        msg_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(msg_frame, text=message, wraplength=400, justify=tk.LEFT).pack()

        # Buttons
        btn_frame = ttk.Frame(dialog, padding="10")
        btn_frame.pack(fill=tk.X)

        def on_yes():
            result[0] = True
            dialog.destroy()

        def on_no():
            result[0] = False
            dialog.destroy()

        ttk.Button(btn_frame, text=self.t('no'), command=on_no).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text=self.t('yes'), command=on_yes).pack(side=tk.RIGHT, padx=5)

        # Zentriere Dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # Warte auf Antwort
        self.root.wait_window(dialog)
        return result[0] if result[0] is not None else False

    def setup_ui(self):
        """Erstellt die Benutzeroberfläche"""

        # Sprach-Button oben rechts
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(fill=tk.X, padx=5, pady=(5, 0))

        self.lang_button = ttk.Button(lang_frame, text=self.t('switch_language'),
                                      command=self.switch_language)
        self.lang_button.pack(side=tk.RIGHT)

        self.lang_label = ttk.Label(lang_frame, text=self.t('language'),
                 font=('TkDefaultFont', 9))
        self.lang_label.pack(side=tk.RIGHT, padx=5)

        # Hauptframe mit PanedWindow für linke/rechte Seite
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # LINKE SEITE: Ordnerliste und Einstellungen
        left_frame = ttk.Frame(main_paned, padding="5")
        main_paned.add(left_frame, weight=1)

        # Ordner-Liste
        self.folders_frame = ttk.LabelFrame(left_frame, text=self.t('folder_list_title'), padding="5")
        self.folders_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.ui_elements['folder_list_title'] = self.folders_frame

        btn_frame = ttk.Frame(self.folders_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 5))

        self.add_folder_btn = ttk.Button(btn_frame, text=self.t('add_folder'), command=self.add_batch_folder)
        self.add_folder_btn.pack(side=tk.LEFT, padx=2)
        self.ui_elements['add_folder'] = self.add_folder_btn

        self.remove_folder_btn = ttk.Button(btn_frame, text=self.t('remove_folder'), command=self.remove_folder)
        self.remove_folder_btn.pack(side=tk.LEFT, padx=2)
        self.ui_elements['remove_folder'] = self.remove_folder_btn

        self.clear_list_btn = ttk.Button(btn_frame, text=self.t('clear_list'), command=self.clear_batch_folders)
        self.clear_list_btn.pack(side=tk.LEFT, padx=2)
        self.ui_elements['clear_list'] = self.clear_list_btn

        # Listbox mit Scrollbar
        list_frame = ttk.Frame(self.folders_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.folder_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.folder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.folder_listbox.yview)
        self.folder_listbox.bind('<<ListboxSelect>>', self.on_folder_select)

        # Drag & Drop Unterstützung
        self.setup_drag_and_drop()

        # Batch-Metadaten
        self.batch_meta_frame = ttk.LabelFrame(left_frame, text=self.t('batch_actions'), padding="5")
        self.batch_meta_frame.pack(fill=tk.X, pady=(0, 5))
        self.ui_elements['batch_actions'] = self.batch_meta_frame

        self.apply_metadata_btn = ttk.Button(self.batch_meta_frame, text=self.t('apply_metadata_all'),
                  command=self.apply_batch_metadata)
        self.apply_metadata_btn.pack(fill=tk.X, pady=2)
        self.ui_elements['apply_metadata_all'] = self.apply_metadata_btn

        # Einstellungen
        self.settings_frame = ttk.LabelFrame(left_frame, text=self.t('settings'), padding="5")
        self.settings_frame.pack(fill=tk.X, pady=(0, 5))
        self.ui_elements['settings'] = self.settings_frame

        self.quality_label = ttk.Label(self.settings_frame, text=self.t('quality'))
        self.quality_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.ui_elements['quality'] = self.quality_label

        self.copy_audio_var = tk.BooleanVar(value=True)
        self.original_radio = ttk.Radiobutton(self.settings_frame, text=self.t('original'),
                       variable=self.copy_audio_var, value=True)
        self.original_radio.grid(row=0, column=1, sticky=tk.W)
        self.ui_elements['original'] = self.original_radio

        self.new_aac_radio = ttk.Radiobutton(self.settings_frame, text=self.t('new_aac'),
                       variable=self.copy_audio_var, value=False)
        self.new_aac_radio.grid(row=1, column=1, sticky=tk.W)
        self.ui_elements['new_aac'] = self.new_aac_radio

        self.subfolders_label = ttk.Label(self.settings_frame, text=self.t('subfolders'))
        self.subfolders_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.ui_elements['subfolders'] = self.subfolders_label

        self.recursive_var = tk.BooleanVar(value=False)
        self.recursive_check = ttk.Checkbutton(self.settings_frame, text=self.t('recursive_checkbox'),
                       variable=self.recursive_var)
        self.recursive_check.grid(row=2, column=1, sticky=tk.W)
        self.ui_elements['recursive_checkbox'] = self.recursive_check

        # Ausgabe
        self.output_frame = ttk.LabelFrame(left_frame, text=self.t('output'), padding="5")
        self.output_frame.pack(fill=tk.X, pady=(0, 5))
        self.ui_elements['output'] = self.output_frame

        self.output_folder_label = ttk.Label(self.output_frame, text=self.t('output_folder'))
        self.output_folder_label.pack(anchor=tk.W, padx=5)
        self.ui_elements['output_folder'] = self.output_folder_label

        output_entry_frame = ttk.Frame(self.output_frame)
        output_entry_frame.pack(fill=tk.X, padx=5, pady=2)

        self.output_dir_entry = ttk.Entry(output_entry_frame)
        self.output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(output_entry_frame, text="...", width=3,
                  command=self.browse_output_dir).pack(side=tk.RIGHT)

        self.empty_source_label = ttk.Label(self.output_frame, text=self.t('empty_source_folder'),
                 font=('TkDefaultFont', 8), foreground='gray')
        self.empty_source_label.pack(anchor=tk.W, padx=5)
        self.ui_elements['empty_source_folder'] = self.empty_source_label

        # Start-Button
        self.start_batch_btn = ttk.Button(left_frame, text=self.t('start_batch'),
                  command=self.create_batch)
        self.start_batch_btn.pack(fill=tk.X, pady=5)
        self.ui_elements['start_batch'] = self.start_batch_btn

        # Status
        self.status_frame = ttk.LabelFrame(left_frame, text=self.t('status'), padding="5")
        self.status_frame.pack(fill=tk.BOTH, expand=True)
        self.ui_elements['status'] = self.status_frame

        self.status_text = scrolledtext.ScrolledText(self.status_frame, height=8, state='disabled')
        self.status_text.pack(fill=tk.BOTH, expand=True)

        # RECHTE SEITE: Detail-Ansicht
        right_frame = ttk.Frame(main_paned, padding="5")
        main_paned.add(right_frame, weight=2)

        # Notebook für Tabs
        self.detail_notebook = ttk.Notebook(right_frame)
        self.detail_notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Kapitel
        self.chapters_tab = ttk.Frame(self.detail_notebook, padding="10")
        self.detail_notebook.add(self.chapters_tab, text=self.t('tab_chapters'))

        ttk.Label(self.chapters_tab, text=self.t('no_selection'),
                 font=('TkDefaultFont', 12)).pack(pady=50)

        # Tab 2: Metadaten
        self.metadata_tab = ttk.Frame(self.detail_notebook, padding="10")
        self.detail_notebook.add(self.metadata_tab, text=self.t('tab_metadata'))

        ttk.Label(self.metadata_tab, text=self.t('no_selection'),
                 font=('TkDefaultFont', 12)).pack(pady=50)

        # Tab 3: Übersicht
        self.overview_tab = ttk.Frame(self.detail_notebook, padding="10")
        self.detail_notebook.add(self.overview_tab, text=self.t('tab_overview'))

        ttk.Label(self.overview_tab, text=self.t('no_selection'),
                 font=('TkDefaultFont', 12)).pack(pady=50)

    def add_batch_folder(self):
        """Fügt einen oder mehrere Ordner zur Batch-Liste hinzu"""
        # Erstelle einen benutzerdefinierten Dialog für Multi-Select
        import tkinter.filedialog as fd

        # Nutze einen Trick: Zeige Dialog für Dateien, aber erlaube nur Ordner-Auswahl
        folders = []

        # Windows: Nutze askdirectory mehrfach mit Hinweis
        # Verwende einen eigenen Dialog mit übersetzten Buttons
        result = self._ask_yes_no(
            self.t('add_multiple_folders'),
            self.t('add_multiple_folders_msg')
        )

        if result:  # Mehrere Ordner
            while True:
                folder = filedialog.askdirectory(title=self.t('select_folder'))
                if not folder:
                    break
                if folder not in folders:
                    folders.append(folder)
        else:  # Nur ein Ordner
            folder = filedialog.askdirectory(title=self.t('select_audio_folder'))
            if folder:
                folders.append(folder)

        # Verarbeite alle ausgewählten Ordner
        added_count = 0
        for folder in folders:
            if any(fd.folder_path == folder for fd in self.folder_data_list):
                continue  # Überspringe bereits vorhandene

            recursive = self.recursive_var.get()
            folder_data = FolderData(folder, recursive)

            if not folder_data.audio_files:
                messagebox.showwarning(self.t('no_files_found'), self.t('no_audio_files', folder=folder))
                continue  # Überspringe diesen Ordner

            self.folder_data_list.append(folder_data)
            added_count += 1

        if added_count > 0:
            self.update_folder_list()
            if added_count > 1:
                messagebox.showinfo(self.t('success'), self.t('folders_added', count=added_count))
            else:
                messagebox.showinfo(self.t('success'), self.t('folder_added'))

    def remove_folder(self):
        """Entfernt den ausgewählten Ordner"""
        if self.selected_folder_index is None:
            messagebox.showinfo(self.t('no_selection'), self.t('no_selection'))
            return

        folder_name = self.folder_data_list[self.selected_folder_index].folder_name

        if self._ask_yes_no(self.t('confirm'), self.t('remove_folder_confirm', name=folder_name)):
            del self.folder_data_list[self.selected_folder_index]
            self.selected_folder_index = None
            self.update_folder_list()
            self.clear_detail_view()

    def clear_batch_folders(self):
        """Leert die Ordnerliste"""
        if self.folder_data_list and self._ask_yes_no(self.t('confirm'), self.t('clear_all_confirm')):
            self.folder_data_list = []
            self.selected_folder_index = None
            self.update_folder_list()
            self.clear_detail_view()

    def setup_drag_and_drop(self):
        """Richtet Drag & Drop für die Ordnerliste ein"""
        try:
            # Versuche tkinterdnd2 zu verwenden
            from tkinterdnd2 import DND_FILES

            # Aktiviere Drag & Drop für die Listbox
            self.folder_listbox.drop_target_register(DND_FILES)
            self.folder_listbox.dnd_bind('<<Drop>>', self.on_drop)
            print("✓ Drag & Drop aktiviert (tkinterdnd2)")
        except ImportError:
            # Fallback: Versuche windnd (nur Windows)
            try:
                import windnd
                windnd.hook_dropfiles(self.folder_listbox, func=self.on_drop_windnd)
                print("✓ Drag & Drop aktiviert (windnd)")
            except ImportError:
                print("Info: Drag & Drop nicht verfügbar.")
                print("Installiere eines der folgenden Pakete:")
                print("  - pip install tkinterdnd2")
                print("  - pip install windnd")
        except Exception as e:
            print(f"Drag & Drop konnte nicht aktiviert werden: {e}")

    def on_drop(self, event):
        """Verarbeitet Drag & Drop Events (tkinterdnd2)"""
        # Parse die gedropten Pfade
        files = self.root.tk.splitlist(event.data)

        added_count = 0
        recursive = self.recursive_var.get()

        for file_path in files:
            # Bereinige Pfad (entferne geschweifte Klammern falls vorhanden)
            file_path = file_path.strip('{}')

            # Prüfe ob es ein Ordner ist
            if os.path.isdir(file_path):
                # Prüfe ob bereits vorhanden
                if any(fd.folder_path == file_path for fd in self.folder_data_list):
                    continue

                folder_data = FolderData(file_path, recursive)

                if folder_data.audio_files:
                    self.folder_data_list.append(folder_data)
                    added_count += 1

        if added_count > 0:
            self.update_folder_list()
            if added_count > 1:
                messagebox.showinfo(self.t('success'), self.t('folders_dropped', count=added_count))
            else:
                messagebox.showinfo(self.t('success'), self.t('folder_dropped'))

    def on_drop_windnd(self, files):
        """Verarbeitet Drag & Drop Events (windnd)"""
        added_count = 0
        recursive = self.recursive_var.get()

        for file_path in files:
            # Dekodiere Bytes zu String falls nötig
            if isinstance(file_path, bytes):
                file_path = file_path.decode('utf-8')

            # Prüfe ob es ein Ordner ist
            if os.path.isdir(file_path):
                # Prüfe ob bereits vorhanden
                if any(fd.folder_path == file_path for fd in self.folder_data_list):
                    continue

                folder_data = FolderData(file_path, recursive)

                if folder_data.audio_files:
                    self.folder_data_list.append(folder_data)
                    added_count += 1

        if added_count > 0:
            self.update_folder_list()
            if added_count > 1:
                messagebox.showinfo(self.t('success'), self.t('folders_dropped', count=added_count))
            else:
                messagebox.showinfo(self.t('success'), self.t('folder_dropped'))

    def update_folder_list(self):
        """Aktualisiert die Ordnerliste"""
        self.folder_listbox.delete(0, tk.END)
        for folder_data in self.folder_data_list:
            file_count = len(folder_data.audio_files)
            display = f"{folder_data.output_name} ({self.t('files_count', count=file_count)})"
            self.folder_listbox.insert(tk.END, display)

    def on_folder_select(self, event):
        """Wird aufgerufen wenn ein Ordner ausgewählt wird"""
        selection = self.folder_listbox.curselection()
        if selection:
            self.selected_folder_index = selection[0]
            self.show_folder_details()

    def show_folder_details(self):
        """Zeigt die Details des ausgewählten Ordners"""
        if self.selected_folder_index is None:
            return

        folder_data = self.folder_data_list[self.selected_folder_index]

        # Tab 1: Kapitel aufbauen
        for widget in self.chapters_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.chapters_tab, text=self.t('chapters_title', name=folder_data.output_name),
                 font=('TkDefaultFont', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        # Buttons
        btn_frame = ttk.Frame(self.chapters_tab)
        btn_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(btn_frame, text=self.t('move_up'), command=self.move_chapter_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text=self.t('move_down'), command=self.move_chapter_down).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text=self.t('refresh'), command=self.show_folder_details).pack(side=tk.LEFT, padx=2)

        # Kapitel-Liste
        list_frame = ttk.Frame(self.chapters_tab)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chapter_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=('Courier', 9))
        self.chapter_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chapter_listbox.yview)

        for idx, audio_file in enumerate(folder_data.audio_files, 1):
            filename = Path(audio_file.path).name
            duration = f"{audio_file.duration / 60:.1f} min"
            display = f"{idx:3d}. {filename:<70} ({duration})"
            self.chapter_listbox.insert(tk.END, display)

        # Tab 2: Metadaten aufbauen
        for widget in self.metadata_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.metadata_tab, text=self.t('metadata_title', name=folder_data.output_name),
                 font=('TkDefaultFont', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        # Hauptcontainer mit zwei Spalten: Links Artwork, Rechts Metadaten
        main_container = ttk.Frame(self.metadata_tab)
        main_container.pack(fill=tk.BOTH, expand=True)

        # LINKE SPALTE: Artwork
        artwork_frame = ttk.LabelFrame(main_container, text=self.t('cover_artwork'), padding="10")
        artwork_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Artwork-Anzeige
        self.artwork_label = ttk.Label(artwork_frame, text=self.t('no_cover'), relief=tk.RIDGE)
        self.artwork_label.pack(pady=5)

        # Lade und zeige Artwork
        self.load_and_display_artwork(folder_data)

        # Artwork-Buttons
        artwork_btn_frame = ttk.Frame(artwork_frame)
        artwork_btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(artwork_btn_frame, text=self.t('change_cover'),
                  command=self.change_artwork).pack(fill=tk.X, pady=2)
        ttk.Button(artwork_btn_frame, text=self.t('extract_cover'),
                  command=self.extract_artwork).pack(fill=tk.X, pady=2)
        ttk.Button(artwork_btn_frame, text=self.t('remove_cover'),
                  command=self.remove_artwork).pack(fill=tk.X, pady=2)

        # RECHTE SPALTE: Metadaten
        metadata_container = ttk.Frame(main_container)
        metadata_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Ausgabename
        name_frame = ttk.Frame(metadata_container)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text=self.t('output_name'), width=15).pack(side=tk.LEFT, padx=(0, 5))
        self.output_name_entry = ttk.Entry(name_frame)
        self.output_name_entry.insert(0, folder_data.output_name)
        self.output_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Metadaten
        self.metadata_entries = {}
        metadata_fields = [
            ('title', self.t('title')),
            ('artist', self.t('artist')),
            ('album', self.t('album')),
            ('date', self.t('year')),
            ('genre', self.t('genre')),
        ]

        for key, label in metadata_fields:
            field_frame = ttk.Frame(metadata_container)
            field_frame.pack(fill=tk.X, pady=3)
            ttk.Label(field_frame, text=label, width=15).pack(side=tk.LEFT, padx=(0, 5))
            entry = ttk.Entry(field_frame)
            entry.insert(0, folder_data.metadata.get(key, ''))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.metadata_entries[key] = entry

        # Speichern-Button
        ttk.Button(metadata_container, text=self.t('save_changes'),
                  command=self.save_folder_metadata).pack(pady=20)

        # Tab 3: Übersicht aufbauen
        for widget in self.overview_tab.winfo_children():
            widget.destroy()

        ttk.Label(self.overview_tab, text=self.t('overview_title', name=folder_data.output_name),
                 font=('TkDefaultFont', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        info_text_widget = tk.Text(self.overview_tab, wrap=tk.WORD, state='disabled')
        info_text_widget.pack(fill=tk.BOTH, expand=True)

        info_lines = [
            f"{self.t('folder_name')}: {folder_data.folder_name}",
            f"{self.t('path')}: {folder_data.folder_path}",
            f"{self.t('output_filename')}: {folder_data.output_name}.m4b",
            f"{self.t('file_count')}: {len(folder_data.audio_files)}",
            f"{self.t('recursive')}: {self.t('recursive_yes') if folder_data.recursive else self.t('recursive_no')}",
            "",
            f"{self.t('audio_files')}:",
            "-" * 80
        ]

        total_duration = 0.0
        for idx, af in enumerate(folder_data.audio_files, 1):
            duration_str = f"{af.duration / 60:.1f} min"
            info_lines.append(f"{idx:3d}. {Path(af.path).name} ({duration_str})")
            total_duration += af.duration

        info_lines.append("-" * 80)
        info_lines.append(f"{self.t('total_duration')}: {total_duration / 3600:.2f} {self.t('hours')} ({total_duration / 60:.1f} {self.t('minutes')})")

        info_text_widget.config(state='normal')
        info_text_widget.insert('1.0', '\n'.join(info_lines))
        info_text_widget.config(state='disabled')

    def clear_detail_view(self):
        """Leert die Detail-Ansicht"""
        for widget in self.chapters_tab.winfo_children():
            widget.destroy()
        ttk.Label(self.chapters_tab, text=self.t('no_selection'), font=('TkDefaultFont', 12)).pack(pady=50)

        for widget in self.metadata_tab.winfo_children():
            widget.destroy()
        ttk.Label(self.metadata_tab, text=self.t('no_selection'), font=('TkDefaultFont', 12)).pack(pady=50)

        for widget in self.overview_tab.winfo_children():
            widget.destroy()
        ttk.Label(self.overview_tab, text=self.t('no_selection'), font=('TkDefaultFont', 12)).pack(pady=50)

    def move_chapter_up(self):
        """Verschiebt Kapitel nach oben"""
        if self.selected_folder_index is None:
            return

        if not hasattr(self, 'chapter_listbox'):
            return

        selection = self.chapter_listbox.curselection()
        if selection:
            index = selection[0]
            if index > 0:
                folder_data = self.folder_data_list[self.selected_folder_index]
                folder_data.move_file_up(index)
                self.show_folder_details()
                self.chapter_listbox.selection_set(index - 1)
                self.chapter_listbox.see(index - 1)

    def move_chapter_down(self):
        """Verschiebt Kapitel nach unten"""
        if self.selected_folder_index is None:
            return

        if not hasattr(self, 'chapter_listbox'):
            return

        selection = self.chapter_listbox.curselection()
        if selection:
            index = selection[0]
            folder_data = self.folder_data_list[self.selected_folder_index]
            if index < len(folder_data.audio_files) - 1:
                folder_data.move_file_down(index)
                self.show_folder_details()
                self.chapter_listbox.selection_set(index + 1)
                self.chapter_listbox.see(index + 1)

    def load_and_display_artwork(self, folder_data: FolderData):
        """Lädt und zeigt das Artwork an"""
        artwork_path = None

        # Prüfe ob benutzerdefiniertes Artwork existiert
        if folder_data.custom_artwork_path and os.path.exists(folder_data.custom_artwork_path):
            artwork_path = folder_data.custom_artwork_path
        else:
            # Versuche Cover aus erster Datei zu extrahieren
            for audio_file in folder_data.audio_files:
                if audio_file.has_cover:
                    # Extrahiere Cover temporär
                    temp_cover = Path(folder_data.folder_path) / ".temp_cover.jpg"
                    extract_cmd = [
                        'ffmpeg',
                        '-i', audio_file.path,
                        '-an',
                        '-vcodec', 'copy',
                        '-y',
                        str(temp_cover)
                    ]
                    result = subprocess.run(extract_cmd, capture_output=True)
                    if result.returncode == 0 and temp_cover.exists():
                        artwork_path = str(temp_cover)
                    break

        # Zeige Artwork
        if artwork_path and os.path.exists(artwork_path):
            try:
                img = Image.open(artwork_path)
                # Resize für Anzeige (max 300x300)
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.artwork_label.configure(image=photo, text="")
                self.artwork_label.image = photo  # Referenz behalten
            except Exception as e:
                self.artwork_label.configure(text=f"Fehler beim\nLaden: {str(e)}", image="")
        else:
            self.artwork_label.configure(text="Kein Cover\nverfügbar", image="")

    def change_artwork(self):
        """Ändert das Artwork des ausgewählten Ordners"""
        if self.selected_folder_index is None:
            return

        folder_data = self.folder_data_list[self.selected_folder_index]

        file_path = filedialog.askopenfilename(
            title=self.t('select_cover'),
            filetypes=[
                (self.t('image_files'), "*.jpg *.jpeg *.png *.bmp *.gif"),
                (self.t('all_files'), "*.*")
            ]
        )

        if file_path:
            folder_data.custom_artwork_path = file_path
            self.load_and_display_artwork(folder_data)
            messagebox.showinfo(self.t('success'), self.t('cover_changed'))

    def extract_artwork(self):
        """Extrahiert das Cover und speichert es"""
        if self.selected_folder_index is None:
            return

        folder_data = self.folder_data_list[self.selected_folder_index]

        # Finde Quelle für Cover
        source_path = None
        if folder_data.custom_artwork_path and os.path.exists(folder_data.custom_artwork_path):
            source_path = folder_data.custom_artwork_path
        else:
            # Suche in Audiodateien
            for audio_file in folder_data.audio_files:
                if audio_file.has_cover:
                    # Extrahiere temporär
                    temp_cover = Path(folder_data.folder_path) / ".temp_extract_cover.jpg"
                    extract_cmd = [
                        'ffmpeg',
                        '-i', audio_file.path,
                        '-an',
                        '-vcodec', 'copy',
                        '-y',
                        str(temp_cover)
                    ]
                    result = subprocess.run(extract_cmd, capture_output=True)
                    if result.returncode == 0 and temp_cover.exists():
                        source_path = str(temp_cover)
                    break

        if not source_path:
            messagebox.showwarning(self.t('no_cover_found'), self.t('no_cover_to_extract'))
            return

        # Speichern-Dialog
        save_path = filedialog.asksaveasfilename(
            title=self.t('save_cover'),
            defaultextension=".jpg",
            initialfile=f"{folder_data.output_name}_cover.jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                (self.t('all_files'), "*.*")
            ]
        )

        if save_path:
            try:
                shutil.copy2(source_path, save_path)
                messagebox.showinfo(self.t('success'), self.t('cover_saved', path=save_path))
            except Exception as e:
                messagebox.showerror(self.t('error'), f"{self.t('error')}: {str(e)}")

            # Aufräumen
            if source_path.endswith('.temp_extract_cover.jpg'):
                try:
                    os.remove(source_path)
                except:
                    pass

    def remove_artwork(self):
        """Entfernt das benutzerdefinierte Artwork"""
        if self.selected_folder_index is None:
            return

        folder_data = self.folder_data_list[self.selected_folder_index]

        if folder_data.custom_artwork_path:
            if self._ask_yes_no(self.t('confirm'), self.t('remove_cover') + "?"):
                folder_data.custom_artwork_path = None
                self.load_and_display_artwork(folder_data)
                messagebox.showinfo(self.t('success'), self.t('cover_removed'))
        else:
            messagebox.showinfo(self.t('no_cover_found'), self.t('no_custom_cover'))

    def save_folder_metadata(self):
        """Speichert die Metadaten des aktuellen Ordners"""
        if self.selected_folder_index is None:
            return

        folder_data = self.folder_data_list[self.selected_folder_index]

        # Metadaten aktualisieren
        for key, entry in self.metadata_entries.items():
            folder_data.metadata[key] = entry.get()

        # Ausgabename aktualisieren
        folder_data.output_name = self.output_name_entry.get().strip()
        if not folder_data.output_name:
            folder_data.output_name = folder_data.folder_name

        self.update_folder_list()
        messagebox.showinfo(self.t('saved'), self.t('changes_saved'))

    def apply_batch_metadata(self):
        """Öffnet Dialog zum Anwenden von Metadaten auf alle Ordner"""
        if not self.folder_data_list:
            messagebox.showinfo(self.t('no_folders'), self.t('add_folders_first'))
            return

        dialog = BatchMetadataDialog(self.root, self.current_language)
        self.root.wait_window(dialog.dialog)

        if dialog.result and dialog.metadata:
            count = 0
            for folder_data in self.folder_data_list:
                for key, value in dialog.metadata.items():
                    folder_data.metadata[key] = value
                count += 1

            messagebox.showinfo(self.t('success'), self.t('metadata_applied', count=count))

            # Aktualisiere Ansicht falls ein Ordner ausgewählt ist
            if self.selected_folder_index is not None:
                self.show_folder_details()

    def browse_output_dir(self):
        """Öffnet Dialog zur Auswahl des Ausgabeordners"""
        folder = filedialog.askdirectory(title=self.t('select_output_folder'))
        if folder:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, folder)

    def log_status(self, message):
        """Fügt eine Statusmeldung hinzu"""
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')
        self.root.update()

    def create_batch(self):
        """Startet die Batch-Verarbeitung"""
        if not self.folder_data_list:
            messagebox.showerror(self.t('error'), self.t('add_folder_first'))
            return

        output_dir = self.output_dir_entry.get().strip()

        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state='disabled')

        def run_batch():
            copy_audio = self.copy_audio_var.get()

            total_folders = len(self.folder_data_list)
            successful = 0
            failed = 0

            self.log_status(f"=== Batch-Verarbeitung gestartet ===")
            self.log_status(f"Anzahl Ordner: {total_folders}")
            self.log_status(f"Audio-Modus: {'Original kopieren' if copy_audio else 'Neu codieren'}")
            self.log_status("")

            creator = M4BCreator()

            for idx, folder_data in enumerate(self.folder_data_list, 1):
                self.log_status(f"[{idx}/{total_folders}] Verarbeite: {folder_data.output_name}")
                self.log_status("-" * 60)

                try:
                    if not folder_data.audio_files:
                        self.log_status(f"WARNUNG: Keine Audiodateien!")
                        self.log_status("")
                        continue

                    self.log_status(f"Dateien: {len(folder_data.audio_files)}")
                    self.log_status(f"Kapitel: {len(folder_data.audio_files)}")

                    if output_dir:
                        output_path = os.path.join(output_dir, f"{folder_data.output_name}.m4b")
                    else:
                        output_path = os.path.join(folder_data.folder_path, f"{folder_data.output_name}.m4b")

                    self.log_status(f"Ausgabe: {output_path}")

                    success = creator.create_m4b(folder_data, output_path, copy_audio, self.log_status)

                    if success:
                        successful += 1
                        self.log_status(f"✓ ERFOLG: {folder_data.output_name}.m4b erstellt!")
                    else:
                        failed += 1
                        self.log_status(f"✗ FEHLER: Konnte nicht erstellt werden!")

                except Exception as e:
                    failed += 1
                    self.log_status(f"✗ FEHLER: {str(e)}")

                self.log_status("")

            self.log_status("=" * 60)
            self.log_status(f"=== Batch-Verarbeitung abgeschlossen ===")
            self.log_status(f"Gesamt: {total_folders} Ordner")
            self.log_status(f"Erfolgreich: {successful}")
            self.log_status(f"Fehlgeschlagen: {failed}")

            if failed == 0:
                self.root.after(0, lambda: messagebox.showinfo(self.t('success'),
                    self.t('batch_complete', count=successful)))
            else:
                self.root.after(0, lambda: messagebox.showwarning(self.t('partial_success'),
                    self.t('partial_success_msg', success=successful, failed=failed)))

        thread = threading.Thread(target=run_batch, daemon=True)
        thread.start()

    def update_ui_language(self):
        """Aktualisiert die Sprache aller UI-Elemente"""
        # Fenstertitel
        self.root.title(self.t('window_title'))

        # Sprach-Button und Label
        self.lang_button.config(text=self.t('switch_language'))
        self.lang_label.config(text=self.t('language'))

        # Aktualisiere alle gespeicherten UI-Elemente
        for key, widget in self.ui_elements.items():
            if isinstance(widget, dict):
                for sub_key, sub_widget in widget.items():
                    self._update_widget_text(sub_widget, sub_key)
            else:
                self._update_widget_text(widget, key)

        # Aktualisiere Notebook-Tabs
        self.detail_notebook.tab(0, text=self.t('tab_chapters'))
        self.detail_notebook.tab(1, text=self.t('tab_metadata'))
        self.detail_notebook.tab(2, text=self.t('tab_overview'))

        # Aktualisiere Detail-Ansicht wenn etwas ausgewählt ist
        if self.selected_folder_index is not None:
            self.show_folder_details()
        else:
            # Aktualisiere "Keine Auswahl" Labels
            self.clear_detail_view()

        # Aktualisiere Ordnerliste
        self.update_folder_list()

    def _update_widget_text(self, widget, key):
        """Hilfsfunktion zum Aktualisieren eines einzelnen Widgets"""
        try:
            if isinstance(widget, (ttk.LabelFrame, ttk.Label)):
                if hasattr(widget, 'cget') and widget.cget('text'):
                    widget.config(text=self.t(key))
            elif isinstance(widget, (ttk.Button, tk.Button)):
                widget.config(text=self.t(key))
            elif isinstance(widget, (ttk.Radiobutton, ttk.Checkbutton)):
                widget.config(text=self.t(key))
        except:
            pass


def main():
    """Hauptfunktion"""
    # Versuche TkinterDnD zu verwenden für Drag & Drop Support
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        root = tk.Tk()

    app = M4BCreatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
