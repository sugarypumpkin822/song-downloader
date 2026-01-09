#!/usr/bin/env python3
"""
Enhanced YouTube Music Downloader for Eminem Songs
Features:
- High-quality audio download
- Metadata enrichment
- Progress tracking
- Error handling and retries
- Playlist support
- Duplicate detection
- Organized file structure
"""

import os
import re
import time
import json
import logging
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

import yt_dlp
from yt_dlp.utils import DownloadError
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configuration
@dataclass
class Config:
    artist_name: str = "Eminem"
    download_dir: str = "Eminem_Music"
    max_songs: int = 100
    quality: str = "bestaudio/best"
    format: str = "mp3"
    sample_rate: int = 44100
    bitrate: int = 320
    embed_thumbnail: bool = True
    embed_metadata: bool = True
    skip_existing: bool = True
    max_retries: int = 3
    delay_between_downloads: float = 2.0
    
    # Spotify API (optional for enhanced metadata)
    spotify_client_id: Optional[str] = None
    spotify_client_secret: Optional[str] = None

class Logger:
    """Enhanced logging setup"""
    
    def __init__(self, log_file: str = "eminem_downloader.log"):
        self.logger = logging.getLogger("EminemDownloader")
        self.logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def debug(self, message: str):
        self.logger.debug(message)

class SpotifyMetadata:
    """Fetch enhanced metadata from Spotify"""
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.sp = None
        if client_id and client_secret:
            try:
                client_credentials_manager = SpotifyClientCredentials(
                    client_id=client_id, 
                    client_secret=client_secret
                )
                self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            except Exception as e:
                print(f"Spotify API initialization failed: {e}")
    
    def get_artist_top_tracks(self, artist_name: str, limit: int = 50) -> List[Dict]:
        """Get top tracks for an artist from Spotify"""
        if not self.sp:
            return []
        
        try:
            # Search for the artist
            results = self.sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
            if not results['artists']['items']:
                return []
            
            artist_id = results['artists']['items'][0]['id']
            
            # Get artist's top tracks
            tracks = self.sp.artist_top_tracks(artist_id)
            
            track_info = []
            for track in tracks['tracks'][:limit]:
                track_info.append({
                    'name': track['name'],
                    'album': track['album']['name'],
                    'release_date': track['album']['release_date'],
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity'],
                    'explicit': track['explicit'],
                    'track_number': track['track_number']
                })
            
            return track_info
        except Exception as e:
            print(f"Error fetching Spotify metadata: {e}")
            return []

class YouTubeSearcher:
    """Enhanced YouTube search functionality"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_songs(self, artist: str, max_results: int = 50) -> List[Dict]:
        """Search for songs by artist on YouTube"""
        self.logger.info(f"Searching for {artist} songs on YouTube...")
        
        search_queries = [
            f"{artist} official music video",
            f"{artist} audio",
            f"{artist} lyrics",
            f"{artist} clean version",
            f"{artist} explicit"
        ]
        
        all_songs = []
        seen_titles = set()
        
        for query in search_queries:
            if len(all_songs) >= max_results:
                break
            
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': True,
                    'ignoreerrors': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    search_url = f"ytsearch{max_results - len(all_songs)}:{query}"
                    result = ydl.extract_info(search_url, download=False)
                    
                    if 'entries' in result:
                        for entry in result['entries']:
                            if entry and len(all_songs) < max_results:
                                title = entry.get('title', '').lower()
                                
                                # Skip duplicates and non-music content
                                if any(skip in title for skip in ['interview', 'behind the scenes', 'making of', 'reaction']):
                                    continue
                                
                                if title not in seen_titles:
                                    seen_titles.add(title)
                                    all_songs.append({
                                        'title': entry.get('title', ''),
                                        'url': entry.get('url', ''),
                                        'duration': entry.get('duration', 0),
                                        'view_count': entry.get('view_count', 0),
                                        'uploader': entry.get('uploader', ''),
                                        'upload_date': entry.get('upload_date', ''),
                                        'description': entry.get('description', ''),
                                        'id': entry.get('id', '')
                                    })
                
                self.logger.info(f"Found {len(all_songs)} songs so far...")
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                self.logger.error(f"Error searching with query '{query}': {e}")
                continue
        
        # Sort by view count (popularity)
        all_songs.sort(key=lambda x: x.get('view_count', 0), reverse=True)
        
        self.logger.info(f"Total unique songs found: {len(all_songs)}")
        return all_songs[:max_results]

class EnhancedDownloader:
    """Main downloader class with enhanced features"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = Logger()
        self.searcher = YouTubeSearcher(self.logger)
        self.spotify = SpotifyMetadata(config.spotify_client_id, config.spotify_client_secret)
        
        # Create download directory
        self.download_path = Path(config.download_dir)
        self.download_path.mkdir(exist_ok=True)
        
        # Download statistics
        self.stats = {
            'total_attempted': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': None,
            'end_time': None
        }
    
    def clean_filename(self, filename: str) -> str:
        """Clean filename for safe file system usage"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'\s+', ' ', filename).strip()
        
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename
    
    def get_ydl_options(self, song_info: Dict) -> Dict:
        """Get yt-dlp options for download"""
        clean_title = self.clean_filename(f"{song_info['title']}")
        output_path = str(self.download_path / f"{clean_title}.%(ext)s")
        
        ydl_opts = {
            'format': self.config.quality,
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.config.format,
                'preferredquality': str(self.config.bitrate),
            }],
            'writethumbnail': self.config.embed_thumbnail,
            'embedthumbnail': self.config.embed_thumbnail,
            'embedmetadata': self.config.embed_metadata,
            'addmetadata': self.config.embed_metadata,
            'ignoreerrors': True,
            'no_warnings': True,
            'quiet': True,
            'progress_hooks': [self.progress_hook],
        }
        
        # Add metadata
        if self.config.embed_metadata:
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            })
            
            # Add metadata fields
            metadata = {
                'title': song_info['title'],
                'artist': self.config.artist_name,
                'genre': 'Hip-Hop/Rap',
                'description': song_info.get('description', ''),
            }
            
            if song_info.get('upload_date'):
                metadata['date'] = song_info['upload_date'][:4]  # Year only
            
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegMetadata',
                'metadata': metadata
            })
        
        return ydl_opts
    
    def progress_hook(self, d: Dict):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%').strip()
            speed = d.get('_speed_str', '0B/s').strip()
            eta = d.get('_eta_str', 'Unknown').strip()
            self.logger.info(f"Downloading: {percent} - Speed: {speed} - ETA: {eta}")
        
        elif d['status'] == 'finished':
            self.logger.info(f"Download completed: {d['filename']}")
    
    def is_file_exists(self, song_info: Dict) -> bool:
        """Check if file already exists"""
        clean_title = self.clean_filename(song_info['title'])
        expected_file = self.download_path / f"{clean_title}.{self.config.format}"
        return expected_file.exists()
    
    def download_song(self, song_info: Dict) -> bool:
        """Download a single song with retry logic"""
        if self.config.skip_existing and self.is_file_exists(song_info):
            self.logger.info(f"Skipping existing file: {song_info['title']}")
            self.stats['skipped'] += 1
            return True
        
        for attempt in range(self.config.max_retries):
            try:
                self.logger.info(f"Downloading (attempt {attempt + 1}): {song_info['title']}")
                
                ydl_opts = self.get_ydl_options(song_info)
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([song_info['url']])
                
                self.stats['successful'] += 1
                return True
                
            except DownloadError as e:
                self.logger.warning(f"Download failed (attempt {attempt + 1}): {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.logger.error(f"Failed to download after {self.config.max_retries} attempts: {song_info['title']}")
                    self.stats['failed'] += 1
                    return False
            
            except Exception as e:
                self.logger.error(f"Unexpected error downloading {song_info['title']}: {e}")
                self.stats['failed'] += 1
                return False
        
        return False
    
    def create_playlist_file(self, songs: List[Dict]):
        """Create an M3U playlist file"""
        playlist_path = self.download_path / f"{self.config.artist_name}_Playlist.m3u"
        
        with open(playlist_path, 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n")
            f.write(f"#PLAYLIST: {self.config.artist_name} Songs\n")
            f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for song in songs:
                clean_title = self.clean_filename(song['title'])
                filename = f"{clean_title}.{self.config.format}"
                if (self.download_path / filename).exists():
                    f.write(f"#EXTINF:-1,{song['title']}\n")
                    f.write(f"{filename}\n")
        
        self.logger.info(f"Created playlist: {playlist_path}")
    
    def save_statistics(self):
        """Save download statistics to JSON file"""
        stats_file = self.download_path / "download_stats.json"
        
        stats_data = {
            **self.stats,
            'config': {
                'artist': self.config.artist_name,
                'max_songs': self.config.max_songs,
                'quality': self.config.quality,
                'format': self.config.format,
                'bitrate': self.config.bitrate
            },
            'success_rate': (self.stats['successful'] / max(self.stats['total_attempted'], 1)) * 100
        }
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved statistics to: {stats_file}")
    
    def run(self):
        """Main execution method"""
        self.logger.info(f"Starting enhanced download for {self.config.artist_name}")
        self.stats['start_time'] = datetime.now()
        
        try:
            # Search for songs
            songs = self.searcher.search_songs(self.config.artist_name, self.config.max_songs)
            
            if not songs:
                self.logger.error("No songs found!")
                return
            
            self.logger.info(f"Found {len(songs)} songs to download")
            
            # Download songs
            for i, song in enumerate(songs, 1):
                self.stats['total_attempted'] += 1
                self.logger.info(f"Processing {i}/{len(songs)}: {song['title']}")
                
                success = self.download_song(song)
                
                if success and i < len(songs):
                    time.sleep(self.config.delay_between_downloads)
            
            # Create playlist and save statistics
            self.create_playlist_file(songs)
            self.save_statistics()
            
        except KeyboardInterrupt:
            self.logger.info("Download interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.stats['end_time'] = datetime.now()
            self.print_summary()
    
    def print_summary(self):
        """Print download summary"""
        duration = self.stats['end_time'] - self.stats['start_time'] if self.stats['end_time'] else None
        
        self.logger.info("\n" + "="*50)
        self.logger.info("DOWNLOAD SUMMARY")
        self.logger.info("="*50)
        self.logger.info(f"Artist: {self.config.artist_name}")
        self.logger.info(f"Total Attempted: {self.stats['total_attempted']}")
        self.logger.info(f"Successful: {self.stats['successful']}")
        self.logger.info(f"Failed: {self.stats['failed']}")
        self.logger.info(f"Skipped: {self.stats['skipped']}")
        
        if self.stats['total_attempted'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_attempted']) * 100
            self.logger.info(f"Success Rate: {success_rate:.1f}%")
        
        if duration:
            self.logger.info(f"Duration: {duration}")
        
        self.logger.info(f"Download Directory: {self.download_path.absolute()}")
        self.logger.info("="*50)

def main():
    """Main entry point"""
    print("🎵 Enhanced Eminem YouTube Downloader")
    print("=" * 50)
    
    # Configuration
    config = Config(
        artist_name="Eminem",
        download_dir="Eminem_Music",
        max_songs=50,
        quality="bestaudio/best",
        format="mp3",
        bitrate=320,
        embed_thumbnail=True,
        embed_metadata=True,
        skip_existing=True,
        max_retries=3,
        delay_between_downloads=2.0,
        # Add your Spotify API credentials for enhanced metadata (optional)
        spotify_client_id=None,
        spotify_client_secret=None
    )
    
    # Create and run downloader
    downloader = EnhancedDownloader(config)
    downloader.run()

if __name__ == "__main__":
    main()
