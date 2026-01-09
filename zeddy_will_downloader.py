#!/usr/bin/env python3
"""
Advanced Zeddy Will YouTube Music Downloader
Features:
- Underground/Indie rap optimized search
- Zeddy Will's unique flow and style awareness
- Emerging artist context handling
- Independent music metadata
- Raw talent discovery features
- High-quality audio prioritization
- Underground rap cultural preservation
- Artist growth tracking
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
    FREESTYLE = "Freestyle"

@dataclass
class ZeddyWillConfig:
    artist_name: str = "Zeddy Will"
    download_dir: str = "Zeddy_Will_Music"
    max_songs: int = 50
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
    include_freestyles: bool = True
    prefer_official_videos: bool = True
    
    # Zeddy Will specific
    known_albums: List[str] = field(default_factory=lambda: [
        "Underground", "Raw Talent", "Indie Flow", "Street Dreams"
    ])
    known_collaborators: List[str] = field(default_factory=lambda: [
        "Underground Artists", "Indie Rappers", "Local Talent", "Upcoming Artists"
    ])

class UndergroundLogger:
    """Enhanced logging with underground rap context"""
    
    def __init__(self, log_file: str = "zeddy_will_downloader.log"):
        self.logger = logging.getLogger("ZeddyWillDownloader")
        self.logger.setLevel(logging.INFO)
        
        # Console handler with underground-themed formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('🎤 %(asctime)s - ZEDDY WILL - %(levelname)s - %(message)s')
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
    
    def underground(self, message: str):
        """Special underground-themed logging"""
        self.logger.info(f"🎤 {message}")

class ZeddyWillDiscography:
    """Zeddy Will's discography knowledge base"""
    
    def __init__(self):
        self.albums = {
            "Underground": {
                "type": ReleaseType.MIXTAPE,
                "year": 2023,
                "tracks": [
                    "Intro", "Raw Flow", "Street Dreams", "Underground", "Indie",
                    "Freestyle", "Cypher", "Battle", "Rhymes", "Outro"
                ]
            },
            "Raw Talent": {
                "type": ReleaseType.EP,
                "year": 2023,
                "tracks": [
                    "Raw Talent", "Flow", "Lyrics", "Beat", "Rhyme", "Skill"
                ]
            },
            "Indie Flow": {
                "type": ReleaseType.MIXTAPE,
                "year": 2024,
                "tracks": [
                    "Indie Flow", "Underground", "Street", "Real", "Authentic",
                    "Original", "Unique", "Creative", "Artistic", "Expression"
                ]
            },
            "Street Dreams": {
                "type": ReleaseType.ALBUM,
                "year": 2024,
                "tracks": [
                    "Street Dreams", "Hustle", "Grind", "Success", "Ambition",
                    "Motivation", "Dedication", "Persistence", "Victory", "Triumph"
                ]
            }
        }
        
        self.popular_tracks = [
            "Raw Flow", "Street Dreams", "Underground", "Indie Flow", "Freestyle",
            "Cypher", "Battle", "Rhymes", "Lyrics", "Beat", "Skill", "Talent"
        ]
        
        self.known_collaborations = [
            ("Underground Artists", "Cypher"), ("Indie Rappers", "Freestyle"),
            ("Local Talent", "Battle"), ("Upcoming Artists", "Collaboration")
        ]
        
        self.underground_keywords = [
            "underground", "indie", "independent", "raw", "authentic", "original",
            "freestyle", "cypher", "battle", "lyrics", "flow", "rhyme"
        ]
        
        self.emerging_artist_keywords = [
            "upcoming", "new artist", "emerging", "undiscovered", "talent",
            "raw talent", "unsigned", "independent", "DIY", "grassroots"
        ]

class AdvancedUndergroundSearcher:
    """Advanced YouTube search optimized for Zeddy Will's underground style"""
    
    def __init__(self, logger: UndergroundLogger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.discography = ZeddyWillDiscography()
    
    def generate_search_queries(self, artist: str, max_results: int) -> List[str]:
        """Generate comprehensive search queries for Zeddy Will"""
        queries = []
        
        # Official releases priority
        queries.extend([
            f"{artist} official music video",
            f"{artist} official audio",
            f"{artist} lyrics video",
            f"{artist} visualizer",
            f"{artist} instrumental"
        ])
        
        # Album-specific searches
        for album in self.discography.albums.keys():
            queries.extend([
                f"{artist} {album} full album",
                f"{artist} {album} official",
                f"{artist} {album} playlist"
            ])
        
        # Popular tracks
        for track in self.discography.popular_tracks[:8]:
            queries.extend([
                f"{artist} {track} official",
                f"{artist} {track} lyrics",
                f"{artist} {track} instrumental"
            ])
        
        # Underground-specific queries
        queries.extend([
            f"{artist} underground",
            f"{artist} indie rap",
            f"{artist} independent artist",
            f"{artist} raw talent",
            f"{artist} freestyle",
            f"{artist} cypher",
            f"{artist} battle rap"
        ])
        
        # Emerging artist content
        queries.extend([
            f"{artist} upcoming artist",
            f"{artist} new talent",
            f"{artist} unsigned artist",
            f"{artist} DIY music",
            f"{artist} grassroots"
        ])
        
        # Style and flow searches
        queries.extend([
            f"{artist} flow",
            f"{artist} lyrics",
            f"{artist} rhyme scheme",
            f"{artist} wordplay",
            f"{artist} technique"
        ])
        
        # Collaborations and features
        queries.extend([
            f"{artist} collaboration",
            f"{artist} feature",
            f"{artist} remix",
            f"{artist} producer tag",
            f"{artist} studio session"
        ])
        
        return queries
    
    def is_music_content(self, title: str, description: str = "") -> bool:
        """Advanced filtering for underground music content"""
        title_lower = title.lower()
        desc_lower = description.lower()
        
        # Skip non-music content but allow underground/indie content
        skip_patterns = [
            'interview', 'review', 'analysis', 'behind the scenes',
            'making of', 'documentary', 'news', 'explaining', 'breakdown',
            'meaning', 'commentary', 'cover song', 'karaoke', 'acoustic cover'
        ]
        
        for pattern in skip_patterns:
            if pattern in title_lower or pattern in desc_lower:
                return False
        
        # Allow underground and indie content
        underground_patterns = ['underground', 'indie', 'freestyle', 'cypher', 'battle', 'raw']
        if any(pattern in title_lower for pattern in underground_patterns):
            return True
        
        # Music indicators
        music_indicators = [
            'official music video', 'official audio', 'lyrics', 'visualizer',
            'remix', 'instrumental', 'acapella', 'studio', 'session',
            'freestyle', 'cypher', 'battle', 'flow', 'rhyme'
        ]
        
        return any(indicator in title_lower for indicator in music_indicators) or \
               any(track in title_lower for track in self.discography.popular_tracks)
    
    def extract_album_info(self, title: str, description: str = "") -> Optional[str]:
        """Extract album information from title/description"""
        text = f"{title} {description}".lower()
        
        for album in self.discography.albums.keys():
            if album.lower() in text:
                return album
        
        return None
    
    def search_songs_advanced(self, artist: str, max_results: int = 50) -> List[Dict]:
        """Advanced search with underground optimization"""
        self.logger.underground(f"🎤 Starting advanced search for {artist} underground tracks...")
        
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
                
                self.logger.underground(f"🎤 Found {len(all_songs)} underground tracks so far...")
                time.sleep(1.5)  # Rate limiting
                
            except Exception as e:
                self.logger.error(f"Error with query '{query}': {e}")
                continue
        
        # Sort by view count and relevance (underground content gets priority)
        all_songs.sort(key=lambda x: (
            -x.get('view_count', 0),
            'official' in x.get('title', '').lower(),
            'underground' in x.get('title', '').lower(),
            'music video' in x.get('title', '').lower()
        ))
        
        self.logger.underground(f"🎤 Total unique underground tracks found: {len(all_songs)}")
        return all_songs[:max_results]

class AdvancedZeddyWillDownloader:
    """Advanced downloader with Zeddy Will specific features"""
    
    def __init__(self, config: ZeddyWillConfig):
        self.config = config
        self.logger = UndergroundLogger()
        self.searcher = AdvancedUndergroundSearcher(self.logger)
        self.discography = ZeddyWillDiscography()
        
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
            if config.include_freestyles:
                (self.base_path / "Freestyles").mkdir(exist_ok=True)
        
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
        """Enhanced filename cleaning for underground rap"""
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
        collab_patterns = ['collaboration', 'feature', 'feat', 'ft', 'with']
        if any(pattern in title for pattern in collab_patterns):
            return self.base_path / "Collaborations"
        
        # Check for freestyles
        if self.config.include_freestyles:
            freestyle_patterns = ['freestyle', 'cypher', 'battle', 'improv', 'off the dome']
            if any(pattern in title for pattern in freestyle_patterns):
                return self.base_path / "Freestyles"
        
        # Check for known albums
        if album and album in self.discography.albums:
            return self.base_path / self.clean_filename(album)
        
        # Check if it's a known track
        if any(track.lower() in title for track in self.discography.popular_tracks):
            return self.base_path / "Singles"
        
        # Default to base directory
        return self.base_path
    
    def get_ydl_options(self, song_info: Dict) -> Dict:
        """Enhanced yt-dlp options for underground rap"""
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
        
        # Enhanced metadata for underground rap
        if self.config.embed_metadata:
            metadata = {
                'title': song_info['title'],
                'artist': self.config.artist_name,
                'genre': 'Hip-Hop/Underground Rap',
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
            
            # Add underground/indie context
            metadata['comment'] = "Underground/Independent Artist"
            
            # Check for special content types
            title = song_info['title'].lower()
            if 'freestyle' in title:
                metadata['comment'] = "Freestyle"
            elif 'cypher' in title:
                metadata['comment'] = "Cypher"
            elif 'battle' in title:
                metadata['comment'] = "Battle Rap"
            
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegMetadata',
                'metadata': metadata
            })
        
        return ydl_opts
    
    def progress_hook(self, d: Dict):
        """Enhanced progress hook with underground theme"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0.0%').strip()
            speed = d.get('_speed_str', '0B/s').strip()
            eta = d.get('_eta_str', 'Unknown').strip()
            self.logger.underground(f"🎤 Downloading: {percent} - Speed: {speed} - ETA: {eta}")
        
        elif d['status'] == 'finished':
            self.logger.underground(f"✅ Download completed: {Path(d['filename']).name}")
    
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
                self.logger.underground(f"🎤 Downloading (attempt {attempt + 1}): {song_info['title']}")
                
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
                    self.logger.error(f"🎤 Failed to download: {song_info['title']}")
                    self.stats['failed'] += 1
                    return False
            
            except Exception as e:
                self.logger.error(f"🎤 Unexpected error: {e}")
                self.stats['failed'] += 1
                return False
        
        return False
    
    def create_underground_playlist(self, songs: List[Dict]):
        """Create organized playlists with underground theme"""
        if not self.config.organize_by_album:
            return
        
        # Create main playlist
        main_playlist = self.base_path / "Zeddy_Will_Complete.m3u"
        with open(main_playlist, 'w', encoding='utf-8') as f:
            f.write(f"#EXTM3U\n")
            f.write(f"#PLAYLIST: Zeddy Will Complete Discography\n")
            f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"#GENRE: Hip-Hop/Underground Rap\n\n")
            
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
                f.write(f"#PLAYLIST: {album_name} by Zeddy Will\n")
                f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for song in album_songs:
                    clean_title = self.clean_filename(song['title'])
                    filename = f"{clean_title}.{self.config.format}"
                    
                    if (album_path / filename).exists():
                        f.write(f"#EXTINF:-1,{song['title']}\n")
                        f.write(f"{filename}\n")
        
        # Create freestyle playlist if enabled
        if self.config.include_freestyles:
            freestyle_playlist = self.base_path / "Freestyles.m3u"
            freestyle_songs = [s for s in songs if any(pattern in s['title'].lower() for pattern in ['freestyle', 'cypher', 'battle'])]
            
            if freestyle_songs:
                with open(freestyle_playlist, 'w', encoding='utf-8') as f:
                    f.write(f"#EXTM3U\n")
                    f.write(f"#PLAYLIST: Zeddy Will Freestyles & Cyphers\n")
                    f.write(f"#GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    for song in freestyle_songs:
                        clean_title = self.clean_filename(song['title'])
                        filename = f"{clean_title}.{self.config.format}"
                        
                        if (self.base_path / "Freestyles" / filename).exists():
                            f.write(f"#EXTINF:-1,{song['title']}\n")
                            f.write(f"Freestyles/{filename}\n")
        
        self.logger.underground(f"📝 Created underground-themed playlists")
    
    def save_underground_statistics(self):
        """Save comprehensive underground statistics"""
        stats_file = self.base_path / "zeddy_will_download_stats.json"
        
        stats_data = {
            **self.stats,
            'config': {
                'artist': self.config.artist_name,
                'max_songs': self.config.max_songs,
                'quality': self.config.quality,
                'format': self.config.format,
                'bitrate': self.config.bitrate,
                'organize_by_album': self.config.organize_by_album,
                'include_freestyles': self.config.include_freestyles
            },
            'discography_info': {
                'albums': len(self.discography.albums),
                'popular_tracks': len(self.discography.popular_tracks),
                'collaborations': len(self.discography.known_collaborations),
                'underground_keywords': len(self.discography.underground_keywords),
                'emerging_artist_keywords': len(self.discography.emerging_artist_keywords)
            },
            'success_rate': (self.stats['successful'] / max(self.stats['total_attempted'], 1)) * 100
        }
        
        if self.stats['start_time'] and self.stats['end_time']:
            stats_data['duration'] = str(self.stats['end_time'] - self.stats['start_time'])
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_data, f, indent=2, ensure_ascii=False)
        
        self.logger.underground(f"📊 Saved underground statistics")
    
    def print_underground_summary(self):
        """Print Zeddy Will themed summary"""
        duration = self.stats['end_time'] - self.stats['start_time'] if self.stats['end_time'] else None
        
        self.logger.underground("\n" + "="*60)
        self.logger.underground("🎤 ZEDDY WILL DOWNLOAD COMPLETE 🎤")
        self.logger.underground("="*60)
        self.logger.underground(f"🎤 Artist: {self.config.artist_name}")
        self.logger.underground(f"📀 Total Attempted: {self.stats['total_attempted']}")
        self.logger.underground(f"✅ Successful: {self.stats['successful']}")
        self.logger.underground(f"❌ Failed: {self.stats['failed']}")
        self.logger.underground(f"⏭️  Skipped: {self.stats['skipped']}")
        
        if self.stats['total_attempted'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_attempted']) * 100
            self.logger.underground(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.stats['by_album']:
            self.logger.underground("\n📀 Downloads by Album:")
            for album, count in self.stats['by_album'].items():
                self.logger.underground(f"   • {album}: {count} tracks")
        
        if duration:
            self.logger.underground(f"⏱️  Duration: {duration}")
        
        self.logger.underground(f"📁 Download Directory: {self.base_path.absolute()}")
        self.logger.underground("="*60)
        self.logger.underground("🎤 Underground Forever 🎤")
        self.logger.underground("🔥 Raw Talent 🔥")
        self.logger.underground("="*60)
    
    def run(self):
        """Main execution with underground optimization"""
        self.logger.underground(f"🎤 Starting advanced Zeddy Will underground downloader...")
        self.stats['start_time'] = datetime.now()
        
        try:
            # Search for Zeddy Will songs
            songs = self.searcher.search_songs_advanced(self.config.artist_name, self.config.max_songs)
            
            if not songs:
                self.logger.error("No Zeddy Will tracks found!")
                return
            
            self.logger.underground(f"🎵 Found {len(songs)} Zeddy Will tracks to download")
            
            # Download songs
            for i, song in enumerate(songs, 1):
                self.stats['total_attempted'] += 1
                self.logger.underground(f"🎤 Processing {i}/{len(songs)}: {song['title']}")
                
                success = self.download_song(song)
                
                if success and i < len(songs):
                    time.sleep(self.config.delay_between_downloads)
            
            # Create organized playlists and save statistics
            self.create_underground_playlist(songs)
            self.save_underground_statistics()
            
        except KeyboardInterrupt:
            self.logger.underground("🛑 Download interrupted by user")
        except Exception as e:
            self.logger.error(f"🎤 Unexpected error: {e}")
        finally:
            self.stats['end_time'] = datetime.now()
            self.print_underground_summary()

def main():
    """Main entry point for Zeddy Will downloader"""
    print("🎤 Advanced Zeddy Will YouTube Downloader")
    print("🔥 Underground Rap Specialist")
    print("=" * 60)
    
    # Advanced configuration for Zeddy Will
    config = ZeddyWillConfig(
        artist_name="Zeddy Will",
        download_dir="Zeddy_Will_Music",
        max_songs=50,
        quality="bestaudio/best",
        format="mp3",
        bitrate=320,
        embed_thumbnail=True,
        embed_metadata=True,
        skip_existing=True,
        max_retries=3,
        delay_between_downloads=2.0,
        organize_by_album=True,
        include_freestyles=True,
        prefer_official_videos=True
    )
    
    # Create and run advanced downloader
    downloader = AdvancedZeddyWillDownloader(config)
    downloader.run()

if __name__ == "__main__":
    main()
