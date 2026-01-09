#!/usr/bin/env python3
"""
Advanced King Von YouTube Music Downloader
Features:
- Drill/Trap music optimized search
- Discography-aware downloading
- Collaborations and features detection
- Album/EP organization
- Advanced metadata with drill scene context
- Quality prioritization for rap music
- Duplicate detection across variations
- Smart filtering for non-music content
"""

import os
import re
import time
import json
import logging
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import yt_dlp
from yt_dlp.utils import DownloadError
import requests
from bs4 import BeautifulSoup

class ReleaseType(Enum):
    ALBUM = "Album"
    EP = "EP"
    MIXTAPE = "Mixtape"
    SINGLE = "Single"
    COLLABORATION = "Collaboration"

@dataclass
class KingVonConfig:
    artist_name: str = "King Von"
    download_dir: str = "King_Von_Music"
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
    organize_by_album: bool = True
    include_collaborations: bool = True
    prefer_official_videos: bool = True
    
    # King Von specific
    known_albums: List[str] = field(default_factory=lambda: [
        "Grandson", "Levon James", "Welcome to O'Block", "What It Means to Be King"
    ])
    known_collaborators: List[str] = field(default_factory=lambda: [
        "Lil Durk", "Famous Dex", "Booka600", "Mick Jenkins", "G Herbo", 
        "Polo G", "Lil Tjay", "Fivio Foreign", "Moneybagg Yo"
    ])

class AdvancedLogger:
    """Enhanced logging with drill music context"""
    
    def __init__(self, log_file: str = "king_von_downloader.log"):
        self.logger = logging.getLogger("KingVonDownloader")
        self.logger.setLevel(logging.INFO)
        
        # Console handler with drill-themed formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('🎤 %(asctime)s - KING VON - %(levelname)s - %(message)s')
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
    
    def drill(self, message: str):
        """Special drill-themed logging"""
        self.logger.info(f"🔫 {message}")

class KingVonDiscography:
    """King Von's discography knowledge base"""
    
    def __init__(self):
        self.albums = {
            "Grandson": {
                "type": ReleaseType.MIXTAPE,
                "year": 2019,
                "tracks": [
                    "Crazy Story", "Crazy Story 2.0", "Bank Account", "Twin", "Took Her",
                    "Problems", "Jet Lag", "On It", "War With Us", "Grandson for President"
                ]
            },
            "Levon James": {
                "type": ReleaseType.MIXTAPE,
                "year": 2020,
                "tracks": [
                    "2 AM", "Broke Opps", "Trust Issues", "Mad Dog", "Dedication",
                    "All These Niggas", "Why He Told", "Rolling", "Wayne's Story", "Get It Done"
                ]
            },
            "Welcome to O'Block": {
                "type": ReleaseType.ALBUM,
                "year": 2020,
                "tracks": [
                    "Armed & Dangerous", "Welcome to O'Block", "Gleesh", "I Am What I Am",
                    "The Code", "Slime", "Mine Too", "Twin Nem", "Demon", "Back It Up",
                    "How It Go", "Went Silly", "Take It", "Message", "All I Do"
                ]
            },
            "What It Means to Be King": {
                "type": ReleaseType.ALBUM,
                "year": 2022,
                "tracks": [
                    "Grandson", "Too Real", "Don't Miss", "Soul Snatcher", "Tuff Out Here",
                    "Get It Done", "From the Hood", "My Story", "Heartless", "When I Die",
                    "Robberies", "Struggle", "Trust God", "Family Dedication", "Grandson for President"
                ]
            }
        }
        
        self.popular_singles = [
            "Crazy Story", "Crazy Story 2.0", "Crazy Story 3.0", "Took Her", "Problems",
            "2 AM", "Broke Opps", "Armed & Dangerous", "Welcome to O'Block", "The Code",
            "Twin Nem", "Grandson", "Too Real", "Don't Miss", "Soul Snatcher"
        ]
        
        self.known_collaborations = [
            ("Lil Durk", "Still Trappin'"), ("Famous Dex", "Turn Up"), ("Booka600", "Make It Out"),
            ("Mick Jenkins", "Gang Gang"), ("G Herbo", "On My Soul"), ("Polo G", "The Code"),
            ("Lil Tjay", "War"), ("Fivio Foreign", "Broke Opps Remix"), ("Moneybagg Yo", "Scared")
        ]

class AdvancedYouTubeSearcher:
    """Advanced YouTube search optimized for King Von's music"""
    
    def __init__(self, logger: AdvancedLogger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.discography = KingVonDiscography()
    
    def generate_search_queries(self, artist: str, max_results: int) -> List[str]:
        """Generate comprehensive search queries for King Von"""
        queries = []
        
        # Official releases priority
        queries.extend([
            f"{artist} official music video",
            f"{artist} official audio",
            f"{artist} clean version",
            f"{artist} explicit version"
        ])
        
        # Album-specific searches
        for album in self.discography.albums.keys():
            queries.extend([
                f"{artist} {album} full album",
                f"{artist} {album} official",
                f"{artist} {album} playlist"
            ])
        
        # Popular songs
        for song in self.discography.popular_singles[:10]:
            queries.append(f"{artist} {song} official")
        
        # Drill-specific queries
        queries.extend([
            f"{artist} drill music",
            f"{artist} chicago drill",
            f"{artist} o'block",
            f"{artist} 600"
        ])
        
        # Collaborations
        for collaborator, _ in self.discography.known_collaborations[:5]:
            queries.append(f"{artist} {collaborator}")
        
        return queries
    
    def is_music_content(self, title: str, description: str = "") -> bool:
        """Advanced filtering for actual music content"""
        title_lower = title.lower()
        desc_lower = description.lower()
        
        # Skip non-music content
        skip_patterns = [
            'interview', 'reaction', 'review', 'analysis', 'behind the scenes',
            'making of', 'documentary', 'news', 'tribute', 'rip', 'funeral',
            'explaining', 'breakdown', 'meaning', 'reaction video', 'commentary',
            'live performance', 'concert', 'freestyle session', 'studio session'
        ]
        
        for pattern in skip_patterns:
            if pattern in title_lower or pattern in desc_lower:
                return False
        
        # Music indicators
        music_indicators = [
            'official music video', 'official audio', 'lyrics', 'visualizer',
            'remix', 'clean version', 'explicit', 'radio edit', 'instrumental'
        ]
        
        return any(indicator in title_lower for indicator in music_indicators) or \
               any(song in title_lower for song in self.discography.popular_singles)
    
    def extract_album_info(self, title: str, description: str = "") -> Optional[str]:
        """Extract album information from title/description"""
        text = f"{title} {description}".lower()
        
        for album in self.discography.albums.keys():
            if album.lower() in text:
                return album
        
        return None
    
    def search_songs_advanced(self, artist: str, max_results: int = 100) -> List[Dict]:
        """Advanced search with drill music optimization"""
        self.logger.drill(f"Starting advanced search for {artist} drill tracks...")
        
        queries = self.generate_search_queries(artist, max_results)
        all_songs = []
        seen_titles = set()
        seen_urls = set()
        
        for i, query in enumerate(queries):
            if len(all_songs) >= max_results:
                break
            
            self.logger.info(f"Searching with query {i+1}/{len(queries)}: {query}")
            
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': True,
                    'ignoreerrors': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    search_url = f"ytsearch{min(20, max_results - len(all_songs))}:{query}"
                    result = ydl.extract_info(search_url, download=False)
                    
                    if 'entries' in result:
                        for entry in result['entries']:
                            if not entry or len(all_songs) >= max_results:
                                continue
                            
                            title = entry.get('title', '')
                            url = entry.get('url', '')
                            
                            # Skip duplicates
                            title_key = re.sub(r'[^\w\s]', '', title.lower()).strip()
                            if title_key in seen_titles or url in seen_urls:
                                continue
                            
                            # Filter for music content
                            if not self.is_music_content(title, entry.get('description', '')):
                                continue
                            
                            seen_titles.add(title_key)
                            seen_urls.add(url)
                            
                            song_info = {
                                'title': title,
                                'url': url,
                                'duration': entry.get('duration', 0),
                                'view_count': entry.get('view_count', 0),
                                'uploader': entry.get('uploader', ''),
                                'upload_date': entry.get('upload_date', ''),
                                'description': entry.get('description', ''),
                                'id': entry.get('id', ''),
                                'album': self.extract_album_info(title, entry.get('description', '')),
                                'search_query': query
                            }
                            
                            all_songs.append(song_info)
                
                self.logger.drill(f"Found {len(all_songs)} tracks so far...")
                time.sleep(1.5)  # Rate limiting
                
            except Exception as e:
                self.logger.error(f"Error with query '{query}': {e}")
                continue
        
        # Sort by view count and relevance
        all_songs.sort(key=lambda x: (
            -x.get('view_count', 0),
            'official' in x.get('title', '').lower(),
            'music video' in x.get('title', '').lower()
        ))
        
        self.logger.drill(f"Total unique drill tracks found: {len(all_songs)}")
        return all_songs[:max_results]

class AdvancedKingVonDownloader:
    """Advanced downloader with King Von specific features"""
    
    def __init__(self, config: KingVonConfig):
        self.config = config
        self.logger = AdvancedLogger()
        self.searcher = AdvancedYouTubeSearcher(self.logger)
        self.discography = KingVonDiscography()
        
        # Create organized directory structure
        self.base_path = Path(config.download_dir)
        self.base_path.mkdir(exist_ok=True)
        
        if config.organize_by_album:
            for album in self.discography.albums.keys():
                album_path = self.base_path / self.clean_filename(album)
                album_path.mkdir(exist_ok=True)
            
            # Create directories for singles and collaborations
            (self.base_path / "Singles").mkdir(exist_ok=True)
            (self.base_path / "Collaborations").mkdir(exist_ok=True)
        
        # Statistics
        self.stats = {
            'total_attempted': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'by_album': {},
            'start_time': None,
            'end_time': None
        }
    
    def clean_filename(self, filename: str) -> str:
        """Enhanced filename cleaning for drill music"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'\s+', ' ', filename).strip()
        
        # Remove common YouTube artifacts
        filename = re.sub(r'\[.*?\]', '', filename)  # Remove brackets
        filename = re.sub(r'\(.*?official.*?\)', '', filename, flags=re.IGNORECASE)
        filename = re.sub(r'\(.*?music.*?video.*?\)', '', filename, flags=re.IGNORECASE)
        filename = re.sub(r'\s+', ' ', filename).strip()
        
        # Limit length
        if len(filename) > 150:
            filename = filename[:150]
        
        return filename
    
    def get_download_path(self, song_info: Dict) -> Path:
        """Get organized download path based on album/type"""
        if not self.config.organize_by_album:
            return self.base_path
        
        album = song_info.get('album')
        title = song_info['title'].lower()
        
        # Check for collaborations
        for collaborator, collab_track in self.discography.known_collaborations:
            if collaborator.lower() in title and collab_track.lower() in title:
                return self.base_path / "Collaborations"
        
        # Check for known albums
        if album and album in self.discography.albums:
            return self.base_path / self.clean_filename(album)
        
        # Check if it's a known single
        if any(single.lower() in title for single in self.discography.popular_singles):
            return self.base_path / "Singles"
        
        # Default to base directory
        return self.base_path
    
    def get_ydl_options(self, song_info: Dict) -> Dict:
        """Enhanced yt-dlp options for drill music"""
        download_path = self.get_download_path(song_info)
        clean_title = self.clean_filename(song_info['title'])
        output_path = str(download_path / f"{clean_title}.%(ext)s")
        
        ydl_opts = {
            'format': self.config.quality,
            'outtmpl': output_path,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.config.format,
                    'preferredquality': str(self.config.bitrate),
                }
            ],
            'writethumbnail': self.config.embed_thumbnail,
            'embedthumbnail': self.config.embed_thumbnail,
            'embedmetadata': self.config.embed_metadata,
            'addmetadata': self.config.embed_metadata,
            'ignoreerrors': True,
            'no_warnings': True,
            'quiet': True,
            'progress_hooks': [self.progress_hook],
        }
        
        # Enhanced metadata for drill music
        if self.config.embed_metadata:
            metadata = {
                'title': song_info['title'],
                'artist': self.config.artist_name,
                'genre': 'Hip-Hop/Drill',
                'description': song_info.get('description', ''),
            }
            
            # Add album info if available
            if song_info.get('album'):
                metadata['album'] = song_info['album']
                album_info = self.discography.albums.get(song_info['album'])
                if album_info:
                    metadata['date'] = str(album_info['year'])
                    metadata['albumartist'] = self.config.artist_name
            
            # Add release date if available
            if song_info.get('upload_date'):
                if not metadata.get('date'):
                    metadata['date'] = song_info['upload_date'][:4]
            
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegMetadata',
                'metadata': metadata
            })
        
        return ydl_opts
    
    def progress_hook(self, d: Dict):
        """Enhanced progress hook with drill theme"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%').strip()
            speed = d.get('_speed_str', '0B/s').strip()
            eta = d.get('_eta_str', 'Unknown').strip()
            self.logger.drill(f"🎵 Downloading: {percent} - Speed: {speed} - ETA: {eta}")
        
        elif d['status'] == 'finished':
            self.logger.drill(f"✅ Download completed: {Path(d['filename']).name}")
    
    def is_file_exists(self, song_info: Dict) -> bool:
        """Check if file already exists in organized structure"""
        download_path = self.get_download_path(song_info)
        clean_title = self.clean_filename(song_info['title'])
        expected_file = download_path / f"{clean_title}.{self.config.format}"
        return expected_file.exists()
    
    def download_song(self, song_info: Dict) -> bool:
        """Download song with advanced retry logic"""
        if self.config.skip_existing and self.is_file_exists(song_info):
            self.logger.info(f"⏭️  Skipping existing: {song_info['title']}")
            self.stats['skipped'] += 1
            return True
        
        for attempt in range(self.config.max_retries):
            try:
                self.logger.drill(f"🎤 Downloading (attempt {attempt + 1}): {song_info['title']}")
                
                ydl_opts = self.get_ydl_options(song_info)
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([song_info['url']])
                
                self.stats['successful'] += 1
                
                # Track by album
                album = song_info.get('album', 'Unknown')
                self.stats['by_album'][album] = self.stats['by_album'].get(album, 0) + 1
                
                return True
                
            except DownloadError as e:
                self.logger.warning(f"❌ Download failed (attempt {attempt + 1}): {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.logger.error(f"💀 Failed to download: {song_info['title']}")
                    self.stats['failed'] += 1
                    return False
            
            except Exception as e:
                self.logger.error(f"💀 Unexpected error: {e}")
                self.stats['failed'] += 1
                return False
        
        return False
    
    def create_advanced_playlist(self, songs: List[Dict]):
        """Create organized playlists by album"""
        if not self.config.organize_by_album:
            return
        
        # Create main playlist
        main_playlist = self.base_path / "King_Von_Complete.m3u"
        with open(main_playlist, 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n")
            f.write(f"#PLAYLIST: King Von Complete Discography\n")
            f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for song in songs:
                download_path = self.get_download_path(song)
                clean_title = self.clean_filename(song['title'])
                filename = f"{clean_title}.{self.config.format}"
                full_path = download_path / filename
                
                if full_path.exists():
                    relative_path = full_path.relative_to(self.base_path)
                    f.write(f"#EXTINF:-1,{song['title']}\n")
                    f.write(f"{relative_path}\n")
        
        # Create album-specific playlists
        for album_name in self.discography.albums.keys():
            album_path = self.base_path / self.clean_filename(album_name)
            album_playlist = album_path / f"{album_name}.m3u"
            
            album_songs = [s for s in songs if s.get('album') == album_name]
            if not album_songs:
                continue
            
            with open(album_playlist, 'w', encoding='utf-8') as f:
                f.write(f"#EXTM3U\n")
                f.write(f"#PLAYLIST: {album_name} by King Von\n")
                f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for song in album_songs:
                    clean_title = self.clean_filename(song['title'])
                    filename = f"{clean_title}.{self.config.format}"
                    
                    if (album_path / filename).exists():
                        f.write(f"#EXTINF:-1,{song['title']}\n")
                        f.write(f"{filename}\n")
        
        self.logger.drill(f"📝 Created organized playlists")
    
    def save_advanced_statistics(self):
        """Save comprehensive statistics"""
        stats_file = self.base_path / "king_von_download_stats.json"
        
        stats_data = {
            **self.stats,
            'config': {
                'artist': self.config.artist_name,
                'max_songs': self.config.max_songs,
                'quality': self.config.quality,
                'format': self.config.format,
                'bitrate': self.config.bitrate,
                'organize_by_album': self.config.organize_by_album
            },
            'discography_info': {
                'albums': len(self.discography.albums),
                'popular_singles': len(self.discography.popular_singles),
                'collaborations': len(self.discography.known_collaborations)
            },
            'success_rate': (self.stats['successful'] / max(self.stats['total_attempted'], 1)) * 100
        }
        
        if self.stats['start_time'] and self.stats['end_time']:
            stats_data['duration'] = str(self.stats['end_time'] - self.stats['start_time'])
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        
        self.logger.drill(f"📊 Saved advanced statistics")
    
    def print_drill_summary(self):
        """Print King Von themed summary"""
        duration = self.stats['end_time'] - self.stats['start_time'] if self.stats['end_time'] else None
        
        self.logger.drill("\n" + "="*60)
        self.logger.drill("🔫 KING VON DOWNLOAD COMPLETE 🔫")
        self.logger.drill("="*60)
        self.logger.drill(f"🎤 Artist: {self.config.artist_name}")
        self.logger.drill(f"📀 Total Attempted: {self.stats['total_attempted']}")
        self.logger.drill(f"✅ Successful: {self.stats['successful']}")
        self.logger.drill(f"❌ Failed: {self.stats['failed']}")
        self.logger.drill(f"⏭️  Skipped: {self.stats['skipped']}")
        
        if self.stats['total_attempted'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_attempted']) * 100
            self.logger.drill(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.stats['by_album']:
            self.logger.drill("\n📀 Downloads by Album:")
            for album, count in self.stats['by_album'].items():
                self.logger.drill(f"   • {album}: {count} tracks")
        
        if duration:
            self.logger.drill(f"⏱️  Duration: {duration}")
        
        self.logger.drill(f"📁 Download Directory: {self.base_path.absolute()}")
        self.logger.drill("="*60)
        self.logger.drill("🕊️ Rest in Peace King Von 🕊️")
        self.logger.drill("="*60)
    
    def run(self):
        """Main execution with drill music optimization"""
        self.logger.drill(f"🔫 Starting advanced King Von drill downloader...")
        self.stats['start_time'] = datetime.now()
        
        try:
            # Search for King Von songs
            songs = self.searcher.search_songs_advanced(self.config.artist_name, self.config.max_songs)
            
            if not songs:
                self.logger.error("No King Von tracks found!")
                return
            
            self.logger.drill(f"🎵 Found {len(songs)} King Von tracks to download")
            
            # Download songs
            for i, song in enumerate(songs, 1):
                self.stats['total_attempted'] += 1
                self.logger.drill(f"🎤 Processing {i}/{len(songs)}: {song['title']}")
                
                success = self.download_song(song)
                
                if success and i < len(songs):
                    time.sleep(self.config.delay_between_downloads)
            
            # Create organized playlists and save statistics
            self.create_advanced_playlist(songs)
            self.save_advanced_statistics()
            
        except KeyboardInterrupt:
            self.logger.drill("🛑 Download interrupted by user")
        except Exception as e:
            self.logger.error(f"💀 Unexpected error: {e}")
        finally:
            self.stats['end_time'] = datetime.now()
            self.print_drill_summary()

def main():
    """Main entry point for King Von downloader"""
    print("🔫 Advanced King Von YouTube Downloader")
    print("🎤 Drill Music Specialist")
    print("=" * 60)
    
    # Advanced configuration for King Von
    config = KingVonConfig(
        artist_name="King Von",
        download_dir="King_Von_Music",
        max_songs=100,
        quality="bestaudio/best",
        format="mp3",
        bitrate=320,
        embed_thumbnail=True,
        embed_metadata=True,
        skip_existing=True,
        max_retries=3,
        delay_between_downloads=2.0,
        organize_by_album=True,
        include_collaborations=True,
        prefer_official_videos=True
    )
    
    # Create and run advanced downloader
    downloader = AdvancedKingVonDownloader(config)
    downloader.run()

if __name__ == "__main__":
    main()
