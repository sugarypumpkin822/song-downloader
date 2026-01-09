#!/usr/bin/env python3
"""
Advanced Juice WRLD YouTube Music Downloader
Features:
- Emo rap/melodic trap optimized search
- Juice WRLD's unique style and legacy awareness
- "Lucid Dreams" viral hit prioritization
- Posthumous releases handling
- Emotional content preservation
- High-quality audio prioritization
- Chicago drill cultural context
- Tribute and memorial content
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
    POSTHUMOUS = "Posthumous"

@dataclass
class JuiceWRLDConfig:
    artist_name: str = "Juice WRLD"
    download_dir: str = "Juice_WRLD_Music"
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
    include_posthumous: bool = True
    prefer_official_videos: bool = True
    
    # Juice WRLD specific
    known_albums: List[str] = field(default_factory=lambda: [
        "Goodbye & Good Riddance", "Death Race for Love", "Legends Never Die",
        "Fighting Demons", "The Party Never Ends"
    ])
    known_collaborators: List[str] = field(default_factory=lambda: [
        "Lil Uzi Vert", "Brenda", "Trippie Redd", "Seezyn", "Clever",
        "The Weeknd", "Marshmello", "Halsey", "Elliot", "Yung Bans"
    ])

class EmoLogger:
    """Enhanced logging with emo rap context"""
    
    def __init__(self, log_file: str = "juice_wrld_downloader.log"):
        self.logger = logging.getLogger("JuiceWRLDDownloader")
        self.logger.setLevel(logging.INFO)
        
        # Console handler with emo-themed formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('💜 %(asctime)s - JUICE WRLD - %(levelname)s - %(message)s')
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
    
    def emo(self, message: str):
        """Special emo-themed logging"""
        self.logger.info(f"💜 {message}")

class JuiceWRLDDiscography:
    """Juice WRLD's discography knowledge base"""
    
    def __init__(self):
        self.albums = {
            "Goodbye & Good Riddance": {
                "type": ReleaseType.MIXTAPE,
                "year": 2018,
                "tracks": [
                    "Intro", "All Girls Are The Same", "Lucid Dreams", "Lean Wit Me",
                    "Make It Right", "Hate Me", "Black & White", "Used To",
                    "Candles", "Scared Of Love", "End Of The Road"
                ]
            },
            "Death Race for Love": {
                "type": ReleaseType.ALBUM,
                "year": 2019,
                "tracks": [
                    "Empty", "Fight For Your Love", "Lean Wit Me", "Mortal Man",
                    "Ring Ring", "Make Believe", "Hear Me Calling", "Wishing Well",
                    "Fighting Demons", "Righteous", "Empty", "Death Race"
                ]
            },
            "Legends Never Die": {
                "type": ReleaseType.ALBUM,
                "year": 2020,
                "tracks": [
                    "Bandit", "Life's A Mess", "Conversations", "Wishing Well",
                    "Bad Boy", "Righteous", "Hate Me", "Fighting Demons",
                    "Empty", "Get Through This", "Not Enough", "Legends Never Die"
                ]
            },
            "Fighting Demons": {
                "type": ReleaseType.ALBUM,
                "year": 2021,
                "tracks": [
                    "Burn", "Wishing Well", "Girl Of My Dreams", "Already Dead",
                    "Fighting Demons", "Righteous", "Hate Me", "Empty",
                    "Get Through This", "Not Enough", "Fighting Demons", "Outro"
                ]
            },
            "The Party Never Ends": {
                "type": ReleaseType.POSTHUMOUS,
                "year": 2024,
                "tracks": [
                    "The Party Never Ends", "Bandit", "Lucid Dreams", "All Girls Are The Same",
                    "Lean Wit Me", "Make It Right", "Hate Me", "Black & White",
                    "Used To", "Candles", "Scared Of Love", "End Of The Road"
                ]
            }
        }
        
        self.viral_hits = [
            "Lucid Dreams", "All Girls Are The Same", "Lean Wit Me", "Bandit",
            "Wishing Well", "Life's A Mess", "Conversations", "Righteous",
            "Fighting Demons", "Empty", "Burn", "Already Dead"
        ]
        
        self.popular_singles = [
            "Lucid Dreams", "All Girls Are The Same", "Lean Wit Me", "Bandit",
            "Wishing Well", "Life's A Mess", "Conversations", "Righteous",
            "Fighting Demons", "Empty", "Burn", "Already Dead", "Girl Of My Dreams"
        ]
        
        self.known_collaborations = [
            ("Lil Uzi Vert", "Wishing Well"), ("Brenda", "Juice WRLD & Brenda"),
            ("Trippie Redd", "Wit My Crew"), ("Seezyn", "Lean Wit Me"),
            ("Clever", "Life's A Mess"), ("The Weeknd", "Smile"),
            ("Marshmello", "Come & Go"), ("Halsey", "Life's A Mess")
        ]
        
        self.emo_keywords = [
            "emo", "emotional", "sad", "heartbreak", "love", "pain",
            "depression", "anxiety", "mental health", "feelings", "vulnerable"
        ]
        
        self.tribute_keywords = [
            "tribute", "rip", "rest in peace", "memorial", "legacy",
            "forever", "angel", "heaven", "gone but not forgotten"
        ]

class AdvancedEmoSearcher:
    """Advanced YouTube search optimized for Juice WRLD's emo rap style"""
    
    def __init__(self, logger: EmoLogger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.discography = JuiceWRLDDiscography()
    
    def generate_search_queries(self, artist: str, max_results: int) -> List[str]:
        """Generate comprehensive search queries for Juice WRLD"""
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
        for hit in self.discography.viral_hits[:6]:
            queries.extend([
                f"{artist} {hit} official",
                f"{artist} {hit} remix",
                f"{artist} {hit} lyrics",
                f"{artist} {hit} instrumental",
                f"{artist} {hit} sped up"
            ])
        
        # Popular songs
        for song in self.discography.popular_singles[:10]:
            queries.append(f"{artist} {song} official")
        
        # Emo rap-specific queries
        queries.extend([
            f"{artist} emo rap",
            f"{artist} emotional rap",
            f"{artist} sad songs",
            f"{artist} heartbreak",
            f"{artist} mental health",
            f"{artist} anxiety"
        ])
        
        # Tribute and memorial content
        if self.include_posthumous:
            queries.extend([
                f"{artist} tribute",
                f"{artist} rip",
                f"{artist} memorial",
                f"{artist} legacy",
                f"{artist} forever",
                f"{artist} angel"
            ])
        
        # Chicago drill context
        queries.extend([
            f"{artist} chicago",
            f"{artist} drill",
            f"{artist) 999",
            f"{artist) lucid dreams",
            f"{artist) all girls are the same"
        ])
        
        # Collaborations
        for collaborator, _ in self.discography.known_collaborations[:6]:
            queries.append(f"{artist} {collaborator}")
        
        return queries
    
    def is_music_content(self, title: str, description: str = "") -> bool:
        """Advanced filtering for emo rap music content"""
        title_lower = title.lower()
        desc_lower = description.lower()
        
        # Skip non-music content but allow tribute/emo content
        skip_patterns = [
            'interview', 'review', 'analysis', 'behind the scenes',
            'making of', 'documentary', 'news', 'explaining', 'breakdown',
            'meaning', 'commentary', 'cover song', 'karaoke', 'acoustic cover'
        ]
        
        for pattern in skip_patterns:
            if pattern in title_lower or pattern in desc_lower:
                return False
        
        # Allow tribute and emo content for Juice WRLD
        tribute_patterns = ['tribute', 'rip', 'memorial', 'legacy', 'forever', 'angel']
        emo_patterns = ['emo', 'emotional', 'sad', 'heartbreak', 'sped up', 'slowed']
        
        if any(pattern in title_lower for pattern in tribute_patterns + emo_patterns):
            return True
        
        # Music indicators
        music_indicators = [
            'official music video', 'official audio', 'lyrics', 'visualizer',
            'remix', 'clean version', 'explicit', 'radio edit', 'instrumental',
            'bass boosted', 'slowed', 'reverb', 'sped up', 'live'
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
        """Advanced search with emo rap optimization"""
        self.logger.emo(f"💜 Starting advanced search for {artist} emo rap tracks...")
        
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
                    search_url = f"ytsearch{min(25, max_results - len(all_songs))}:{query}"
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
                
                self.logger.emo(f"💜 Found {len(all_songs)} emo rap tracks so far...")
                time.sleep(1.5)  # Rate limiting
                
            except Exception as e:
                self.logger.error(f"Error with query '{query}': {e}")
                continue
        
        # Sort by view count and relevance (Lucid Dreams gets priority)
        all_songs.sort(key=lambda x: (
            -x.get('view_count', 0),
            'lucid dreams' in x.get('title', '').lower(),
            'official' in x.get('title', '').lower(),
            'music video' in x.get('title', '').lower()
        ))
        
        self.logger.emo(f"💜 Total unique emo rap tracks found: {len(all_songs)}")
        return all_songs[:max_results]

class AdvancedJuiceWRLDDownloader:
    """Advanced downloader with Juice WRLD specific features"""
    
    def __init__(self, config: JuiceWRLDConfig):
        self.config = config
        self.logger = EmoLogger()
        self.searcher = AdvancedEmoSearcher(self.logger)
        self.searcher.include_posthumous = config.include_posthumous
        self.discography = JuiceWRLDDiscography()
        
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
            if config.include_posthumous:
                (self.base_path / "Posthumous").mkdir(exist_ok=True)
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
        """Enhanced filename cleaning for emo rap"""
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
        if self.config.include_posthumous:
            tribute_patterns = ['tribute', 'rip', 'memorial', 'legacy', 'forever', 'angel']
            if any(pattern in title for pattern in tribute_patterns):
                return self.base_path / "Tributes"
        
        # Check for posthumous content
        if self.config.include_posthumous:
            posthumous_patterns = ['posthumous', 'unreleased', 'leaked', 'after death']
            if any(pattern in title for pattern in posthumous_patterns):
                return self.base_path / "Posthumous"
        
        # Check for known albums
        if album and album in self.discography.albums:
            return self.base_path / self.clean_filename(album)
        
        # Check if it's a known single
        if any(single.lower() in title for single in self.discography.popular_singles):
            return self.base_path / "Singles"
        
        # Default to base directory
        return self.base_path
    
    def get_ydl_options(self, song_info: Dict) -> Dict:
        """Enhanced yt-dlp options for emo rap"""
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
        
        # Enhanced metadata for emo rap
        if self.config.embed_metadata:
            metadata = {
                'title': song_info['title'],
                'artist': self.config.artist_name,
                'genre': 'Hip-Hop/Emo Rap',
                'description': song_info.get('description', ''),
            }
            
            # Add album info if available
            if song_info.get('album'):
                metadata['album'] = song_info['album']
                album_info = self.discography.albums.get(song_info['album'])
                if album_info:
                    metadata['date'] = str(album_info['year'])
                    metadata['albumartist'] = self.config.artist_name
                    
                    # Mark posthumous releases
                    if album_info['type'] == ReleaseType.POSTHUMOUS:
                        metadata['comment'] = "Posthumous Release"
            
            # Add release date if available
            if song_info.get('upload_date'):
                if not metadata.get('date'):
                    metadata['date'] = song_info['upload_date'][:4]
            
            # Add Chicago location info
            metadata['location'] = "Chicago, Illinois"
            
            # Check for emotional content
            title = song_info['title'].lower()
            emotional_patterns = ['lucid dreams', 'sad', 'heartbreak', 'emo', 'emotional']
            if any(pattern in title for pattern in emotional_patterns):
                metadata['comment'] = "Emotional Content"
            
            # Check for viral hits
            if any(hit.lower() in title for hit in self.discography.viral_hits):
                metadata['comment'] = "Viral Hit"
            
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegMetadata',
                'metadata': metadata
            })
        
        return ydl_opts
    
    def progress_hook(self, d: Dict):
        """Enhanced progress hook with emo theme"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%').strip()
            speed = d.get('_speed_str', '0B/s').strip()
            eta = d.get('_eta_str', 'Unknown').strip()
            self.logger.emo(f"💜 Downloading: {percent} - Speed: {speed} - ETA: {eta}")
        
        elif d['status'] == 'finished':
            self.logger.emo(f"✅ Download completed: {Path(d['filename']).name}")
    
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
                self.logger.emo(f"🎤 Downloading (attempt {attempt + 1}): {song_info['title']}")
                
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
                    self.logger.error(f"💜 Failed to download: {song_info['title']}")
                    self.stats['failed'] += 1
                    return False
            
            except Exception as e:
                self.logger.error(f"💜 Unexpected error: {e}")
                self.stats['failed'] += 1
                return False
        
        return False
    
    def create_emo_playlist(self, songs: List[Dict]):
        """Create organized playlists with emo theme"""
        if not self.config.organize_by_album:
            return
        
        # Create main playlist
        main_playlist = self.base_path / "Juice_WRLD_Complete.m3u"
        with open(main_playlist, 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n")
            f.write(f"#PLAYLIST: Juice WRLD Complete Discography\n")
            f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"#GENRE: Hip-Hop/Emo Rap\n\n")
            
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
                f.write(f"#PLAYLIST: {album_name} by Juice WRLD\n")
                f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for song in album_songs:
                    clean_title = self.clean_filename(song['title'])
                    filename = f"{clean_title}.{self.config.format}"
                    
                    if (album_path / filename).exists():
                        f.write(f"#EXTINF:-1,{song['title']}\n")
                        f.write(f"{filename}\n")
        
        # Create emotional hits playlist
        emotional_playlist = self.base_path / "Emotional_Hits.m3u"
        emotional_songs = [s for s in songs if any(pattern in s['title'].lower() for pattern in ['lucid dreams', 'sad', 'heartbreak', 'emo', 'emotional'])]
        
        if emotional_songs:
            with open(emotional_playlist, 'w', encoding='utf-8') as f:
                f.write(f"#EXTM3U\n")
                f.write(f"#PLAYLIST: Juice WRLD Emotional Hits\n")
                f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for song in emotional_songs:
                    clean_title = self.clean_filename(song['title'])
                    filename = f"{clean_title}.{self.config.format}"
                    
                    # Find file location
                    for root_dir in [self.base_path] + [d for d in self.base_path.iterdir() if d.is_dir()]:
                        file_path = root_dir / filename
                        if file_path.exists():
                            relative_path = file_path.relative_to(self.base_path)
                            f.write(f"#EXTINF:-1,{song['title']}\n")
                            f.write(f"{relative_path}\n")
                            break
        
        self.logger.emo(f"📝 Created emo-themed playlists")
    
    def save_emo_statistics(self):
        """Save comprehensive emo statistics"""
        stats_file = self.base_path / "juice_wrld_download_stats.json"
        
        stats_data = {
            **self.stats,
            'config': {
                'artist': self.config.artist_name,
                'max_songs': self.config.max_songs,
                'quality': self.config.quality,
                'format': self.config.format,
                'bitrate': self.config.bitrate,
                'organize_by_album': self.config.organize_by_album,
                'include_posthumous': self.config.include_posthumous
            },
            'discography_info': {
                'albums': len(self.discography.albums),
                'viral_hits': len(self.discography.viral_hits),
                'popular_singles': len(self.discography.popular_singles),
                'collaborations': len(self.discography.known_collaborations),
                'emo_keywords': len(self.discography.emo_keywords),
                'tribute_keywords': len(self.discography.tribute_keywords)
            },
            'success_rate': (self.stats['successful'] / max(self.stats['total_attempted'], 1)) * 100
        }
        
        if self.stats['start_time'] and self.stats['end_time']:
            stats_data['duration'] = str(self.stats['end_time'] - self.stats['start_time'])
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        
        self.logger.emo(f"📊 Saved emo statistics")
    
    def print_emo_summary(self):
        """Print Juice WRLD themed summary"""
        duration = self.stats['end_time'] - self.stats['start_time'] if self.stats['end_time'] else None
        
        self.logger.emo("\n" + "="*60)
        self.logger.emo("💜 JUICE WRLD DOWNLOAD COMPLETE 💜")
        self.logger.emo("="*60)
        self.logger.emo(f"🎤 Artist: {self.config.artist_name}")
        self.logger.emo(f"📀 Total Attempted: {self.stats['total_attempted']}")
        self.logger.emo(f"✅ Successful: {self.stats['successful']}")
        self.logger.emo(f"❌ Failed: {self.stats['failed']}")
        self.logger.emo(f"⏭️  Skipped: {self.stats['skipped']}")
        
        if self.stats['total_attempted'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_attempted']) * 100
            self.logger.emo(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.stats['by_album']:
            self.logger.emo("\n📀 Downloads by Album:")
            for album, count in self.stats['by_album'].items():
                self.logger.emo(f"   • {album}: {count} tracks")
        
        if duration:
            self.logger.emo(f"⏱️  Duration: {duration}")
        
        self.logger.emo(f"📁 Download Directory: {self.base_path.absolute()}")
        self.logger.emo("="*60)
        self.logger.emo("💜 999 Forever 💜")
        self.logger.emo("🎤 Lucid Dreams Forever 🎤")
        self.logger.emo("🕊️ Rest in Peace Juice WRLD 🕊️")
        self.logger.emo("="*60)
    
    def run(self):
        """Main execution with emo rap optimization"""
        self.logger.emo(f"💜 Starting advanced Juice WRLD emo rap downloader...")
        self.stats['start_time'] = datetime.now()
        
        try:
            # Search for Juice WRLD songs
            songs = self.searcher.search_songs_advanced(self.config.artist_name, self.config.max_songs)
            
            if not songs:
                self.logger.error("No Juice WRLD tracks found!")
                return
            
            self.logger.emo(f"🎵 Found {len(songs)} Juice WRLD tracks to download")
            
            # Download songs
            for i, song in enumerate(songs, 1):
                self.stats['total_attempted'] += 1
                self.logger.emo(f"🎤 Processing {i}/{len(songs)}: {song['title']}")
                
                success = self.download_song(song)
                
                if success and i < len(songs):
                    time.sleep(self.config.delay_between_downloads)
            
            # Create organized playlists and save statistics
            self.create_emo_playlist(songs)
            self.save_emo_statistics()
            
        except KeyboardInterrupt:
            self.logger.emo("🛑 Download interrupted by user")
        except Exception as e:
            self.logger.error(f"💜 Unexpected error: {e}")
        finally:
            self.stats['end_time'] = datetime.now()
            self.print_emo_summary()

def main():
    """Main entry point for Juice WRLD downloader"""
    print("💜 Advanced Juice WRLD YouTube Downloader")
    print("🎤 Emo Rap Specialist")
    print("=" * 60)
    
    # Advanced configuration for Juice WRLD
    config = JuiceWRLDConfig(
        artist_name="Juice WRLD",
        download_dir="Juice_WRLD_Music",
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
        include_posthumous=True,
        prefer_official_videos=True
    )
    
    # Create and run advanced downloader
    downloader = AdvancedJuiceWRLDDownloader(config)
    downloader.run()

if __name__ == "__main__":
    main()
