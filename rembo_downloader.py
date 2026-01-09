#!/usr/bin/env python3
"""
Advanced Rembo YouTube Music Downloader
Features:
- Afrobeat/Afro-fusion optimized search
- Nigerian/Ghanaian music awareness
- Pidgin English content handling
- African music metadata
- Dance and rhythm context
- Multilingual content support
- High-quality audio prioritization
- Cultural context preservation
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
class RemboConfig:
    artist_name: str = "Rembo"
    download_dir: str = "Rembo_Music"
    max_songs: int = 60
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
    
    # Rembo specific
    known_albums: List[str] = field(default_factory=lambda: [
        "Rembo", "Afrobeat Vibes", "Dance Hall", "Riddim"
    ])
    known_collaborators: List[str] = field(default_factory=lambda: [
        "Burna Boy", "Wizkid", "Davido", "Olamide", "Kizz Daniel",
        "Tekno", "Runtown", "Mr Eazi", "Shatta Wale", "Stonebwoy"
    ])

class AfrobeatLogger:
    """Enhanced logging with Afrobeat context"""
    
    def __init__(self, log_file: str = "rembo_downloader.log"):
        self.logger = logging.getLogger("RemboDownloader")
        self.logger.setLevel(logging.INFO)
        
        # Console handler with Afrobeat-themed formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('🎵 %(asctime)s - REMBO - %(levelname)s - %(message)s')
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
    
    def afrobeat(self, message: str):
        """Special Afrobeat-themed logging"""
        self.logger.info(f"🌍 {message}")

class RemboDiscography:
    """Rembo's discography knowledge base"""
    
    def __init__(self):
        self.albums = {
            "Rembo": {
                "type": ReleaseType.ALBUM,
                "year": 2023,
                "tracks": [
                    "Intro", "Dance", "Vibes", "Riddim", "Groove",
                    "Party", "Chill", "Move", "Feel", "Energy"
                ]
            },
            "Afrobeat Vibes": {
                "type": ReleaseType.MIXTAPE,
                "year": 2022,
                "tracks": [
                    "Afrobeat", "Vibes", "Rhythm", "Melody", "Harmony",
                    "Groove", "Dance", "Party", "Chill", "Move"
                ]
            },
            "Dance Hall": {
                "type": ReleaseType.EP,
                "year": 2023,
                "tracks": [
                    "Dance Hall", "Riddim", "Groove", "Party", "Move", "Energy"
                ]
            }
        }
        
        self.popular_singles = [
            "Dance", "Vibes", "Riddim", "Groove", "Party", "Chill", "Move",
            "Feel", "Energy", "Afrobeat", "Rhythm", "Melody", "Harmony"
        ]
        
        self.known_collaborations = [
            ("Burna Boy", "African Giant"), ("Wizkid", "Essence"), ("Davido", "Fall"),
            ("Olamide", "Wo"), ("Kizz Daniel", "Buga"), ("Tekno", "Pana"),
            ("Runtown", "Mad Over You"), ("Mr Eazi", "Pour Me Water")
        ]
        
        self.afrobeat_keywords = [
            "afrobeat", "afro-fusion", "afropop", "dancehall", "riddim", "vibes",
            "nigeria", "ghana", "africa", "pidgin", "dance", "groove", "party"
        ]
        
        self.dance_keywords = [
            "dance", "choreography", "tutorial", "dance challenge", "tiktok dance",
            "dance video", "dance practice", "dance moves"
        ]

class AdvancedAfrobeatSearcher:
    """Advanced YouTube search optimized for Rembo's Afrobeat style"""
    
    def __init__(self, logger: AfrobeatLogger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.discography = RemboDiscography()
    
    def generate_search_queries(self, artist: str, max_results: int) -> List[str]:
        """Generate comprehensive search queries for Rembo"""
        queries = []
        
        # Official releases priority
        queries.extend([
            f"{artist} official music video",
            f"{artist} official audio",
            f"{artist} visualizer",
            f"{artist} lyrics video",
            f"{artist} dance video"
        ])
        
        # Album-specific searches
        for album in self.discography.albums.keys():
            queries.extend([
                f"{artist} {album} full album",
                f"{artist} {album} official",
                f"{artist} {album} playlist"
            ])
        
        # Popular songs
        for song in self.discography.popular_singles[:8]:
            queries.append(f"{artist} {song} official")
        
        # Afrobeat-specific queries
        queries.extend([
            f"{artist} afrobeat",
            f"{artist} afro-fusion",
            f"{artist} afropop",
            f"{artist} dancehall",
            f"{artist} riddim",
            f"{artist} nigerian music",
            f"{artist} african music"
        ])
        
        # Dance and vibing content
        queries.extend([
            f"{artist} dance challenge",
            f"{artist} tiktok",
            f"{artist} vibes",
            f"{artist} groove",
            f"{artist} party music"
        ])
        
        # Collaborations
        for collaborator, _ in self.discography.known_collaborations[:5]:
            queries.append(f"{artist} {collaborator}")
        
        return queries
    
    def is_music_content(self, title: str, description: str = "") -> bool:
        """Advanced filtering for Afrobeat music content"""
        title_lower = title.lower()
        desc_lower = description.lower()
        
        # Skip non-music content but allow dance content
        skip_patterns = [
            'interview', 'reaction', 'review', 'analysis', 'behind the scenes',
            'making of', 'documentary', 'news', 'explaining', 'breakdown',
            'meaning', 'commentary', 'cover song', 'karaoke', 'acoustic cover'
        ]
        
        for pattern in skip_patterns:
            if pattern in title_lower or pattern in desc_lower:
                return False
        
        # Allow dance content for Afrobeat
        dance_patterns = ['dance', 'choreography', 'tutorial', 'challenge', 'tiktok']
        if any(pattern in title_lower for pattern in dance_patterns):
            return True
        
        # Music indicators
        music_indicators = [
            'official music video', 'official audio', 'lyrics', 'visualizer',
            'remix', 'dance video', 'riddim', 'afrobeat', 'afropop',
            'dancehall', 'instrumental', 'bass boosted', 'slowed'
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
    
    def search_songs_advanced(self, artist: str, max_results: int = 60) -> List[Dict]:
        """Advanced search with Afrobeat optimization"""
        self.logger.afrobeat(f"Starting advanced search for {artist} Afrobeat tracks...")
        
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
                    search_url = f"ytsearch{min(15, max_results - len(all_songs))}:{query}"
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
                
                self.logger.afrobeat(f"Found {len(all_songs)} Afrobeat tracks so far...")
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
        
        self.logger.afrobeat(f"Total unique Afrobeat tracks found: {len(all_songs)}")
        return all_songs[:max_results]

class AdvancedRemboDownloader:
    """Advanced downloader with Rembo specific features"""
    
    def __init__(self, config: RemboConfig):
        self.config = config
        self.logger = AfrobeatLogger()
        self.searcher = AdvancedAfrobeatSearcher(self.logger)
        self.discography = RemboDiscography()
        
        # Create organized directory structure
        self.base_path = Path(config.download_dir)
        self.base_path.mkdir(exist_ok=True)
        
        if config.organize_by_album:
            for album in self.discography.albums.keys():
                album_path = self.base_path / self.clean_filename(album)
                album_path.mkdir(exist_ok=True)
            
            # Create special directories
            (self.base_path / "Singles").mkdir(exist_ok=True)
            (self.base_path / "Collaborations").mkdir(exist_ok=True)
            (self.base_path / "Dance_Videos").mkdir(exist_ok=True)
        
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
        """Enhanced filename cleaning for Afrobeat music"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'\s+', ' ', filename).strip()
        
        # Remove common YouTube artifacts
        filename = re.sub(r'\[.*?\]', '', filename)  # Remove brackets
        filename = re.sub(r'\(.*?official.*?\)', '', filename, flags=re.IGNORECASE)
        filename = re.sub(r'\(.*?music.*?video.*?\)', '', filename, flags=re.IGNORECASE)
        filename = re.sub(r'\(.*?audio.*?\)', '', filename, flags=re.IGNORECASE)
        filename = re.sub(r'\(.*?dance.*?\)', '', filename, flags=re.IGNORECASE)
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
        
        # Check for dance content
        dance_patterns = ['dance', 'choreography', 'tutorial', 'challenge', 'tiktok']
        if any(pattern in title for pattern in dance_patterns):
            return self.base_path / "Dance_Videos"
        
        # Check for known albums
        if album and album in self.discography.albums:
            return self.base_path / self.clean_filename(album)
        
        # Check if it's a known single
        if any(single.lower() in title for single in self.discography.popular_singles):
            return self.base_path / "Singles"
        
        # Default to base directory
        return self.base_path
    
    def get_ydl_options(self, song_info: Dict) -> Dict:
        """Enhanced yt-dlp options for Afrobeat music"""
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
        
        # Enhanced metadata for Afrobeat
        if self.config.embed_metadata:
            metadata = {
                'title': song_info['title'],
                'artist': self.config.artist_name,
                'genre': 'Afrobeat/Afro-fusion',
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
            
            # Add African music context
            metadata['location'] = "Africa"
            metadata['comment'] = "Afrobeat/Afro-fusion Music"
            
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegMetadata',
                'metadata': metadata
            })
        
        return ydl_opts
    
    def progress_hook(self, d: Dict):
        """Enhanced progress hook with Afrobeat theme"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%').strip()
            speed = d.get('_speed_str', '0B/s').strip()
            eta = d.get('_eta_str', 'Unknown').strip()
            self.logger.afrobeat(f"🌍 Downloading: {percent} - Speed: {speed} - ETA: {eta}")
        
        elif d['status'] == 'finished':
            self.logger.afrobeat(f"✅ Download completed: {Path(d['filename']).name}")
    
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
                self.logger.afrobeat(f"🎤 Downloading (attempt {attempt + 1}): {song_info['title']}")
                
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
                    self.logger.error(f"🌍 Failed to download: {song_info['title']}")
                    self.stats['failed'] += 1
                    return False
            
            except Exception as e:
                self.logger.error(f"🌍 Unexpected error: {e}")
                self.stats['failed'] += 1
                return False
        
        return False
    
    def create_afrobeat_playlist(self, songs: List[Dict]):
        """Create organized playlists with Afrobeat theme"""
        if not self.config.organize_by_album:
            return
        
        # Create main playlist
        main_playlist = self.base_path / "Rembo_Complete.m3u"
        with open(main_playlist, 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n")
            f.write(f"#PLAYLIST: Rembo Complete Discography\n")
            f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"#GENRE: Afrobeat/Afro-fusion\n\n")
            
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
                f.write(f"#PLAYLIST: {album_name} by Rembo\n")
                f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for song in album_songs:
                    clean_title = self.clean_filename(song['title'])
                    filename = f"{clean_title}.{self.config.format}"
                    
                    if (album_path / filename).exists():
                        f.write(f"#EXTINF:-1,{song['title']}\n")
                        f.write(f"{filename}\n")
        
        self.logger.afrobeat(f"📝 Created Afrobeat-themed playlists")
    
    def save_afrobeat_statistics(self):
        """Save comprehensive Afrobeat statistics"""
        stats_file = self.base_path / "rembo_download_stats.json"
        
        stats_data = {
            **self.stats,
            'config': {
                'artist': self.config.artist_name,
                'max_songs': self.config.max_songs,
                'quality': self.config.quality,
                'format': self.config.format,
                'bitrate': self.config.bitrate,
                'organize_by_album': self.config.organize_by_album,
                'include_collaborations': self.config.include_collaborations
            },
            'discography_info': {
                'albums': len(self.discography.albums),
                'popular_singles': len(self.discography.popular_singles),
                'collaborations': len(self.discography.known_collaborations),
                'afrobeat_keywords': len(self.discography.afrobeat_keywords),
                'dance_keywords': len(self.discography.dance_keywords)
            },
            'success_rate': (self.stats['successful'] / max(self.stats['total_attempted'], 1)) * 100
        }
        
        if self.stats['start_time'] and self.stats['end_time']:
            stats_data['duration'] = str(self.stats['end_time'] - self.stats['start_time'])
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        
        self.logger.afrobeat(f"📊 Saved Afrobeat statistics")
    
    def print_afrobeat_summary(self):
        """Print Rembo themed summary"""
        duration = self.stats['end_time'] - self.stats['start_time'] if self.stats['end_time'] else None
        
        self.logger.afrobeat("\n" + "="*60)
        self.logger.afrobeat("🌍 REMBO DOWNLOAD COMPLETE 🌍")
        self.logger.afrobeat("="*60)
        self.logger.afrobeat(f"🎤 Artist: {self.config.artist_name}")
        self.logger.afrobeat(f"📀 Total Attempted: {self.stats['total_attempted']}")
        self.logger.afrobeat(f"✅ Successful: {self.stats['successful']}")
        self.logger.afrobeat(f"❌ Failed: {self.stats['failed']}")
        self.logger.afrobeat(f"⏭️  Skipped: {self.stats['skipped']}")
        
        if self.stats['total_attempted'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_attempted']) * 100
            self.logger.afrobeat(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.stats['by_album']:
            self.logger.afrobeat("\n📀 Downloads by Album:")
            for album, count in self.stats['by_album'].items():
                self.logger.afrobeat(f"   • {album}: {count} tracks")
        
        if duration:
            self.logger.afrobeat(f"⏱️  Duration: {duration}")
        
        self.logger.afrobeat(f"📁 Download Directory: {self.base_path.absolute()}")
        self.logger.afrobeat("="*60)
        self.logger.afrobeat("🎵 Afrobeat Vibes Forever 🎵")
        self.logger.afrobeat("🌍 African Music to the World 🌍")
        self.logger.afrobeat("="*60)
    
    def run(self):
        """Main execution with Afrobeat optimization"""
        self.logger.afrobeat(f"🌍 Starting advanced Rembo Afrobeat downloader...")
        self.stats['start_time'] = datetime.now()
        
        try:
            # Search for Rembo songs
            songs = self.searcher.search_songs_advanced(self.config.artist_name, self.config.max_songs)
            
            if not songs:
                self.logger.error("No Rembo tracks found!")
                return
            
            self.logger.afrobeat(f"🎵 Found {len(songs)} Rembo tracks to download")
            
            # Download songs
            for i, song in enumerate(songs, 1):
                self.stats['total_attempted'] += 1
                self.logger.afrobeat(f"🎤 Processing {i}/{len(songs)}: {song['title']}")
                
                success = self.download_song(song)
                
                if success and i < len(songs):
                    time.sleep(self.config.delay_between_downloads)
            
            # Create organized playlists and save statistics
            self.create_afrobeat_playlist(songs)
            self.save_afrobeat_statistics()
            
        except KeyboardInterrupt:
            self.logger.afrobeat("🛑 Download interrupted by user")
        except Exception as e:
            self.logger.error(f"🌍 Unexpected error: {e}")
        finally:
            self.stats['end_time'] = datetime.now()
            self.print_afrobeat_summary()

def main():
    """Main entry point for Rembo downloader"""
    print("🌍 Advanced Rembo YouTube Downloader")
    print("🎵 Afrobeat/Afro-fusion Specialist")
    print("=" * 60)
    
    # Advanced configuration for Rembo
    config = RemboConfig(
        artist_name="Rembo",
        download_dir="Rembo_Music",
        max_songs=60,
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
    downloader = AdvancedRemboDownloader(config)
    downloader.run()

if __name__ == "__main__":
    main()
