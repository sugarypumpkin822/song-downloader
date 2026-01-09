#!/usr/bin/env python3
"""
Advanced YNW Melly YouTube Music Downloader
Features:
- Melodic rap/Florida sound optimized search
- YNW Melly's unique melodic style awareness
- Legal case context handling (sensitive approach)
- Florida hip-hop metadata
- Emotional content preservation
- High-quality audio prioritization
- Florida rap cultural preservation
- Controversial content handling
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
    TRIBUTE = "Tribute"

@dataclass
class YNWMellyConfig:
    artist_name: str = "YNW Melly"
    download_dir: str = "YNW_Melly_Music"
    max_songs: int = 70
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
    include_tributes: bool = True
    prefer_official_videos: bool = True
    
    # YNW Melly specific
    known_albums: List[str] = field(default_factory=lambda: [
        "Melly vs. Melvin", "We All Shine", "Just a Matter of Slime", "I Am You"
    ])
    known_collaborators: List[str] = field(default_factory=lambda: [
        "YNW BSlime", "YNW Sakchaser", "Kanye West", "Lil Baby", "Young Thug",
        "Gunna", "Kodak Black", "Lil Durk", "Juice WRLD", "Trippie Redd"
    ])

class FloridaLogger:
    """Enhanced logging with Florida hip-hop context"""
    
    def __init__(self, log_file: str = "ynw_melly_downloader.log"):
        self.logger = logging.getLogger("YNWMellyDownloader")
        self.logger.setLevel(logging.INFO)
        
        # Console handler with Florida-themed formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('🎵 %(asctime)s - YNW MELLY - %(levelname)s - %(message)s')
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
    
    def florida(self, message: str):
        """Special Florida-themed logging"""
        self.logger.info(f"🌴 {message}")

class YNWMellyDiscography:
    """YNW Melly's discography knowledge base"""
    
    def __init__(self):
        self.albums = {
            "Melly vs. Melvin": {
                "type": ReleaseType.ALBUM,
                "year": 2019,
                "tracks": [
                    "Intro (Melly vs. Melvin)", "Murder on My Mind", "I Am You", "Virtual (Blue Balenciagas)",
                    "Suicidal", "772 Love", "Butter Pecan", "Medium Fries", "Street Gossip",
                    "Slang That Iron", "Hang Up On Me", "Freaky G", "The Recipe", "Melly vs. Melvin"
                ]
            },
            "We All Shine": {
                "type": ReleaseType.MIXTAPE,
                "year": 2018,
                "tracks": [
                    "Intro", "We All Shine", "Dangerously In Love", "Free Melly", "Moonwalkin'",
                    "Slime Talk", "F.N.F (Fuck Niggas Forever)", "Stand Up", "Real",
                    "No Heart", "Mama Cry", "Guardian Angel", "Outro"
                ]
            },
            "Just a Matter of Slime": {
                "type": ReleaseType.ALBUM,
                "year": 2021,
                "tracks": [
                    "Intro (Slime)", "223's", "Best Friends", "Slime Dreams", "Melly the Menace",
                    "Pieces", "Wonderful", "Bad Boy", "Tic Toc", "Water",
                    "Nobody", "Free YNW", "Melly vs. Melvin 2", "Outro"
                ]
            },
            "I Am You": {
                "type": ReleaseType.MIXTAPE,
                "year": 2018,
                "tracks": [
                    "I Am You", "Murder on My Mind", "Virtual (Blue Balenciagas)", "Suicidal",
                    "772 Love", "Butter Pecan", "Medium Fries", "Street Gossip",
                    "Slang That Iron", "Hang Up On Me", "Freaky G", "The Recipe"
                ]
            }
        }
        
        self.viral_hits = [
            "Murder on My Mind", "Suicidal", "Virtual (Blue Balenciagas)", "772 Love",
            "Butter Pecan", "I Am You", "F.N.F (Fuck Niggas Forever)", "223's"
        ]
        
        self.popular_singles = [
            "Murder on My Mind", "Suicidal", "Virtual (Blue Balenciagas)", "772 Love",
            "Butter Pecan", "I Am You", "F.N.F (Fuck Niggas Forever)", "223's",
            "Best Friends", "Slime Dreams", "Melly the Menace", "Pieces"
        ]
        
        self.known_collaborations = [
            ("YNW BSlime", "Dangerously In Love"), ("Kanye West", "Mixed Personalities"),
            ("Lil Baby", "Suicidal Remix"), ("Young Thug", "Just a Matter of Slime"),
            ("Gunna", "Slime Talk"), ("Kodak Black", "223's"), ("Lil Durk", "Melly vs. Melvin")
        ]
        
        self.florida_keywords = [
            "florida", "gifford", "772", "melodic rap", "emotional rap",
            "ynw", "young nigga world", "slime", "melly", "melvin"
        ]
        
        self.emotional_keywords = [
            "emotional", "melodic", "sad", "heartbreak", "love", "pain",
            "suicidal", "depression", "feelings", "vulnerable", "real"
        ]

class AdvancedFloridaSearcher:
    """Advanced YouTube search optimized for YNW Melly's melodic style"""
    
    def __init__(self, logger: FloridaLogger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.discography = YNWMellyDiscography()
    
    def generate_search_queries(self, artist: str, max_results: int) -> List[str]:
        """Generate comprehensive search queries for YNW Melly"""
        queries = []
        
        # Official releases priority
        queries.extend([
            f"{artist} official music video",
            f"{artist} official audio",
            f"{artist} clean version",
            f"{artist} explicit version",
            f"{artist} lyrics video"
        ])
        
        # Album-specific searches
        for album in self.discography.albums.keys():
            queries.extend([
                f"{artist} {album} full album",
                f"{artist} {album} official",
                f"{artist} {album} playlist"
            ])
        
        # Viral hits priority
        for hit in self.discography.viral_hits[:5]:
            queries.extend([
                f"{artist} {hit} official",
                f"{artist} {hit} remix",
                f"{artist} {hit} lyrics",
                f"{artist} {hit} instrumental"
            ])
        
        # Popular songs
        for song in self.discography.popular_singles[:8]:
            queries.append(f"{artist} {song} official")
        
        # Florida-specific queries
        queries.extend([
            f"{artist} florida rap",
            f"{artist} gifford",
            f"{artist} 772",
            f"{artist} melodic rap",
            f"{artist} emotional rap",
            f"{artist} ynw"
        ])
        
        # Emotional and melodic content
        queries.extend([
            f"{artist} emotional songs",
            f"{artist} melodic rap",
            f"{artist} sad songs",
            f"{artist) love songs",
            f"{artist} heartbreak",
            f"{artist} pain"
        ])
        
        # Tribute and support content
        if self.include_tributes:
            queries.extend([
                f"{artist} tribute",
                f"{artist} free melly",
                f"{artist} support",
                f"{artist} fan made",
                f"{artist} memorial"
            ])
        
        # Collaborations
        for collaborator, _ in self.discography.known_collaborations[:5]:
            queries.append(f"{artist} {collaborator}")
        
        return queries
    
    def is_music_content(self, title: str, description: str = "") -> bool:
        """Advanced filtering for melodic rap music content"""
        title_lower = title.lower()
        desc_lower = description.lower()
        
        # Skip non-music content but allow tribute/support content
        skip_patterns = [
            'interview', 'review', 'analysis', 'behind the scenes',
            'making of', 'documentary', 'news', 'explaining', 'breakdown',
            'meaning', 'commentary', 'cover song', 'karaoke', 'acoustic cover'
        ]
        
        for pattern in skip_patterns:
            if pattern in title_lower or pattern in desc_lower:
                return False
        
        # Allow tribute and support content for YNW Melly
        tribute_patterns = ['tribute', 'free melly', 'support', 'fan made', 'memorial']
        if any(pattern in title_lower for pattern in tribute_patterns):
            return True
        
        # Music indicators
        music_indicators = [
            'official music video', 'official audio', 'lyrics', 'visualizer',
            'remix', 'clean version', 'explicit', 'radio edit', 'instrumental',
            'bass boosted', 'slowed', 'reverb', 'acoustic', 'live'
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
    
    def search_songs_advanced(self, artist: str, max_results: int = 70) -> List[Dict]:
        """Advanced search with Florida melodic rap optimization"""
        self.logger.florida(f"🌴 Starting advanced search for {artist} Florida melodic tracks...")
        
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
                
                self.logger.florida(f"🌴 Found {len(all_songs)} Florida melodic tracks so far...")
                time.sleep(1.5)  # Rate limiting
                
            except Exception as e:
                self.logger.error(f"Error with query '{query}': {e}")
                continue
        
        # Sort by view count and relevance (viral hits get priority)
        all_songs.sort(key=lambda x: (
            -x.get('view_count', 0),
            'murder on my mind' in x.get('title', '').lower(),
            'official' in x.get('title', '').lower(),
            'music video' in x.get('title', '').lower()
        ))
        
        self.logger.florida(f"🌴 Total unique Florida melodic tracks found: {len(all_songs)}")
        return all_songs[:max_results]

class AdvancedYNWMellyDownloader:
    """Advanced downloader with YNW Melly specific features"""
    
    def __init__(self, config: YNWMellyConfig):
        self.config = config
        self.logger = FloridaLogger()
        self.searcher = AdvancedFloridaSearcher(self.logger)
        self.searcher.include_tributes = config.include_tributes
        self.discography = YNWMellyDiscography()
        
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
            if config.include_tributes:
                (self.base_path / "Tributes").mkdir(exist_ok=True)
        
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
        """Enhanced filename cleaning for melodic rap"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'\s+', ' ', filename).strip()
        
        # Remove common YouTube artifacts
        filename = re.sub(r'\[.*?\]', '', filename)  # Remove brackets
        filename = re.sub(r'\(.*?official.*?\)', '', filename, flags=re.IGNORECASE)
        filename = re.sub(r'\(.*?music.*?video.*?\)', '', filename, flags=re.IGNORECASE)
        filename = re.sub(r'\(.*?audio.*?\)', '', filename, flags=re.IGNORECASE)
        filename = re.sub(r'\(.*?remix.*?\)', '', filename, flags=re.IGNORECASE)
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
        collab_patterns = ['feat', 'ft', 'featuring', 'with', 'and']
        if any(pattern in title for pattern in collab_patterns):
            return self.base_path / "Collaborations"
        
        # Check for tribute content
        if self.config.include_tributes:
            tribute_patterns = ['tribute', 'free melly', 'support', 'fan made', 'memorial']
            if any(pattern in title for pattern in tribute_patterns):
                return self.base_path / "Tributes"
        
        # Check for known albums
        if album and album in self.discography.albums:
            return self.base_path / self.clean_filename(album)
        
        # Check if it's a known single
        if any(single.lower() in title for single in self.discography.popular_singles):
            return self.base_path / "Singles"
        
        # Default to base directory
        return self.base_path
    
    def get_ydl_options(self, song_info: Dict) -> Dict:
        """Enhanced yt-dlp options for melodic rap"""
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
        
        # Enhanced metadata for melodic rap
        if self.config.embed_metadata:
            metadata = {
                'title': song_info['title'],
                'artist': self.config.artist_name,
                'genre': 'Hip-Hop/Melodic Rap',
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
            
            # Add Florida location info
            metadata['location'] = "Gifford, Florida"
            
            # Check for emotional content
            title = song_info['title'].lower()
            emotional_patterns = ['suicidal', 'emotional', 'sad', 'love', 'pain', 'heartbreak']
            if any(pattern in title for pattern in emotional_patterns):
                metadata['comment'] = "Emotional/Melodic Content"
            
            # Check for viral hits
            if any(hit.lower() in title for hit in self.discography.viral_hits):
                metadata['comment'] = "Viral Hit"
            
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegMetadata',
                'metadata': metadata
            })
        
        return ydl_opts
    
    def progress_hook(self, d: Dict):
        """Enhanced progress hook with Florida theme"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%').strip()
            speed = d.get('_speed_str', '0B/s').strip()
            eta = d.get('_eta_str', 'Unknown').strip()
            self.logger.florida(f"🌴 Downloading: {percent} - Speed: {speed} - ETA: {eta}")
        
        elif d['status'] == 'finished':
            self.logger.florida(f"✅ Download completed: {Path(d['filename']).name}")
    
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
                self.logger.florida(f"🎤 Downloading (attempt {attempt + 1}): {song_info['title']}")
                
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
                    self.logger.error(f"🌴 Failed to download: {song_info['title']}")
                    self.stats['failed'] += 1
                    return False
            
            except Exception as e:
                self.logger.error(f"🌴 Unexpected error: {e}")
                self.stats['failed'] += 1
                return False
        
        return False
    
    def create_florida_playlist(self, songs: List[Dict]):
        """Create organized playlists with Florida theme"""
        if not self.config.organize_by_album:
            return
        
        # Create main playlist
        main_playlist = self.base_path / "YNW_Melly_Complete.m3u"
        with open(main_playlist, 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n")
            f.write(f"#PLAYLIST: YNW Melly Complete Discography\n")
            f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"#GENRE: Hip-Hop/Melodic Rap\n\n")
            
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
                f.write(f"#PLAYLIST: {album_name} by YNW Melly\n")
                f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for song in album_songs:
                    clean_title = self.clean_filename(song['title'])
                    filename = f"{clean_title}.{self.config.format}"
                    
                    if (album_path / filename).exists():
                        f.write(f"#EXTINF:-1,{song['title']}\n")
                        f.write(f"{filename}\n")
        
        # Create emotional/melodic playlist
        emotional_playlist = self.base_path / "Emotional_Hits.m3u"
        emotional_songs = [s for s in songs if any(pattern in s['title'].lower() for pattern in ['suicidal', 'emotional', 'sad', 'love', 'pain', 'heartbreak'])]
        
        if emotional_songs:
            with open(emotional_playlist, 'w', encoding='utf-8') as f:
                f.write(f"#EXTM3U\n")
                f.write(f"#PLAYLIST: YNW Melly Emotional & Melodic Hits\n")
                f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for song in emotional_songs:
                    clean_title = self.clean_filename(song['title'])
                    filename = f"{clean_title}.{self.config.format}"
                    
                    # Find the file location
                    for root_dir in [self.base_path] + [d for d in self.base_path.iterdir() if d.is_dir()]:
                        file_path = root_dir / filename
                        if file_path.exists():
                            relative_path = file_path.relative_to(self.base_path)
                            f.write(f"#EXTINF:-1,{song['title']}\n")
                            f.write(f"{relative_path}\n")
                            break
        
        self.logger.florida(f"📝 Created Florida-themed playlists")
    
    def save_florida_statistics(self):
        """Save comprehensive Florida statistics"""
        stats_file = self.base_path / "ynw_melly_download_stats.json"
        
        stats_data = {
            **self.stats,
            'config': {
                'artist': self.config.artist_name,
                'max_songs': self.config.max_songs,
                'quality': self.config.quality,
                'format': self.config.format,
                'bitrate': self.config.bitrate,
                'organize_by_album': self.config.organize_by_album,
                'include_tributes': self.config.include_tributes
            },
            'discography_info': {
                'albums': len(self.discography.albums),
                'viral_hits': len(self.discography.viral_hits),
                'popular_singles': len(self.discography.popular_singles),
                'collaborations': len(self.discography.known_collaborations),
                'florida_keywords': len(self.discography.florida_keywords),
                'emotional_keywords': len(self.discography.emotional_keywords)
            },
            'success_rate': (self.stats['successful'] / max(self.stats['total_attempted'], 1)) * 100
        }
        
        if self.stats['start_time'] and self.stats['end_time']:
            stats_data['duration'] = str(self.stats['end_time'] - self.stats['start_time'])
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        
        self.logger.florida(f"📊 Saved Florida statistics")
    
    def print_florida_summary(self):
        """Print YNW Melly themed summary"""
        duration = self.stats['end_time'] - self.stats['start_time'] if self.stats['end_time'] else None
        
        self.logger.florida("\n" + "="*60)
        self.logger.florida("🌴 YNW MELLY DOWNLOAD COMPLETE 🌴")
        self.logger.florida("="*60)
        self.logger.florida(f"🎤 Artist: {self.config.artist_name}")
        self.logger.florida(f"📀 Total Attempted: {self.stats['total_attempted']}")
        self.logger.florida(f"✅ Successful: {self.stats['successful']}")
        self.logger.florida(f"❌ Failed: {self.stats['failed']}")
        self.logger.florida(f"⏭️  Skipped: {self.stats['skipped']}")
        
        if self.stats['total_attempted'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_attempted']) * 100
            self.logger.florida(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.stats['by_album']:
            self.logger.florida("\n📀 Downloads by Album:")
            for album, count in self.stats['by_album'].items():
                self.logger.florida(f"   • {album}: {count} tracks")
        
        if duration:
            self.logger.florida(f"⏱️  Duration: {duration}")
        
        self.logger.florida(f"📁 Download Directory: {self.base_path.absolute()}")
        self.logger.florida("="*60)
        self.logger.florida("🌴 Florida Forever 🌴")
        self.logger.florida("🎵 Melodic Vibes 🎵")
        self.logger.florida("="*60)
    
    def run(self):
        """Main execution with Florida melodic rap optimization"""
        self.logger.florida(f"🌴 Starting advanced YNW Melly Florida melodic downloader...")
        self.stats['start_time'] = datetime.now()
        
        try:
            # Search for YNW Melly songs
            songs = self.searcher.search_songs_advanced(self.config.artist_name, self.config.max_songs)
            
            if not songs:
                self.logger.error("No YNW Melly tracks found!")
                return
            
            self.logger.florida(f"🎵 Found {len(songs)} YNW Melly tracks to download")
            
            # Download songs
            for i, song in enumerate(songs, 1):
                self.stats['total_attempted'] += 1
                self.logger.florida(f"🎤 Processing {i}/{len(songs)}: {song['title']}")
                
                success = self.download_song(song)
                
                if success and i < len(songs):
                    time.sleep(self.config.delay_between_downloads)
            
            # Create organized playlists and save statistics
            self.create_florida_playlist(songs)
            self.save_florida_statistics()
            
        except KeyboardInterrupt:
            self.logger.florida("🛑 Download interrupted by user")
        except Exception as e:
            self.logger.error(f"🌴 Unexpected error: {e}")
        finally:
            self.stats['end_time'] = datetime.now()
            self.print_florida_summary()

def main():
    """Main entry point for YNW Melly downloader"""
    print("🌴 Advanced YNW Melly YouTube Downloader")
    print("🎵 Florida Melodic Rap Specialist")
    print("=" * 60)
    
    # Advanced configuration for YNW Melly
    config = YNWMellyConfig(
        artist_name="YNW Melly",
        download_dir="YNW_Melly_Music",
        max_songs=70,
        quality="bestaudio/best",
        format="mp3",
        bitrate=320,
        embed_thumbnail=True,
        embed_metadata=True,
        skip_existing=True,
        max_retries=3,
        delay_between_downloads=2.0,
        organize_by_album=True,
        include_tributes=True,
        prefer_official_videos=True
    )
    
    # Create and run advanced downloader
    downloader = AdvancedYNWMellyDownloader(config)
    downloader.run()

if __name__ == "__main__":
    main()
