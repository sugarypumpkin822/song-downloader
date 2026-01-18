# Advanced YouTube Music Downloaders Collection

A comprehensive collection of powerful, feature-rich Python applications to download songs from various artists from YouTube with enhanced metadata, high-quality audio, and intelligent organization.

## 🎵 Available Downloaders

### 🎤 Eminem Downloader
**File**: `eminem_downloader.py`
- **Genre**: Hip-Hop/Rap
- **Specialty**: Multi-era discography, Spotify integration
- **Run**: `python eminem_downloader.py`

### 🔫 King Von Downloader
**File**: `king_von_downloader.py`
- **Genre**: Drill/Trap
- **Specialty**: Chicago drill, posthumous releases, O'Block context
- **Run**: `python king_von_downloader.py`

### 🤠 Lil Loaded Downloader
**File**: `lil_loaded_downloader.py`
- **Genre**: Texas Rap/Drill
- **Specialty**: Dallas rap scene, posthumous content, Texas cultural context
- **Run**: `python lil_loaded_downloader.py`

### 🌍 Rembo Downloader
**File**: `rembo_downloader.py`
- **Genre**: Afrobeat/Afro-fusion
- **Specialty**: African music, dance content, cultural preservation
- **Run**: `python rembo_downloader.py`

### 💰 Blueface Downloader
**File**: `blueface_downloader.py`
- **Genre**: West Coast Hip-Hop
- **Specialty**: California rap, viral hits, Crip context
- **Run**: `python blueface_downloader.py`

### 🔥 NLE Choppa Downloader
**File**: `nle_choppa_downloader.py`
- **Genre**: Memphis Drill
- **Specialty**: Shotta Flow series, spiritual content, Memphis rap
- **Run**: `python nle_choppa_downloader.py`

### 🎤 Zeddy Will Downloader
**File**: `zeddy_will_downloader.py`
- **Genre**: Underground Rap
- **Specialty**: Indie/underground scene, freestyles, emerging artists
- **Run**: `python zeddy_will_downloader.py`

### 🌴 YNW Melly Downloader
**File**: `ynw_melly_downloader.py`
- **Genre**: Melodic Rap/Florida Hip-Hop
- **Specialty**: Emotional content, Florida rap, tribute content
- **Run**: `python ynw_melly_downloader.py`

### 🎵 Lil Tecca Downloader
**File**: `lil_tecca_downloader.py`
- **Genre**: Melodic SoundCloud Rap
- **Specialty**: Viral hits, teen rap, TikTok trends
- **Run**: `python lil_tecca_downloader.py`

### 💜 Juice WRLD Downloader
**File**: `juice_wrld_downloader.py`
- **Genre**: Emo Rap/Melodic Trap
- **Specialty**: Emotional content, posthumous releases, 999 legacy
- **Run**: `python juice_wrld_downloader.py`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Choose Your Downloader

```bash
# Example: Download Juice WRLD songs
python juice_wrld_downloader.py

# Example: Download King Von songs
python king_von_downloader.py

# Example: Download Lil Tecca songs
python lil_tecca_downloader.py
```

### 3. Configure (Optional)

Each downloader has a `Config` class you can customize:

```python
config = ArtistConfig(
    artist_name="Artist Name",
    download_dir="Artist_Music",
    max_songs=50,
    quality="bestaudio/best",
    format="mp3",
    bitrate=320,
    embed_thumbnail=True,
    embed_metadata=True,
    skip_existing=True,
    max_retries=3,
    delay_between_downloads=2.0
)
```

### Special Folder Examples

- **Posthumous/** - For deceased artists (Juice WRLD, King Von, etc.)
- **Tributes/** - Fan-made tributes and memorials
- **Viral_Hits/** - Popular viral songs
- **Freestyles/** - Freestyle sessions and cyphers
- **Dance_Videos/** - Dance challenges and choreography
- **Shotta_Flow_Series/** - Specific series (NLE Choppa)
- **Trending/** - TikTok and social media trends

## 🎵 Genre-Specific Features

### **Drill/Melodic Rap Artists**
- Chicago drill context (King Von, Juice WRLD)
- Memphis drill optimization (NLE Choppa)
- Texas drill scene (Lil Loaded)
- Cultural preservation and location metadata

### **West Coast/Regional Artists**
- California rap context (Blueface)
- Texas rap scene (Lil Loaded)
- Florida hip-hop (YNW Melly)
- Regional cultural keywords

### **Melodic/SoundCloud Artists**
- Teen rap optimization (Lil Tecca)
- SoundCloud aesthetic preservation
- TikTok trend inclusion
- Viral hit prioritization

### **International Artists**
- Afrobeat specialization (Rembo)
- Cultural context preservation
- Dance content inclusion
- Multilingual support

### **Underground/Indie Artists**
- Emerging artist support (Zeddy Will)
- Freestyle and cypher content
- DIY music scene preservation
- Raw talent discovery

## ⚙️ Configuration Options

### **Basic Settings**
- `artist_name`: Artist to search for
- `download_dir`: Download directory
- `max_songs`: Maximum songs to download
- `quality`: Audio quality preference
- `format`: Audio format (MP3, FLAC, etc.)

### **Advanced Settings**
- `embed_thumbnail`: Embed album art
- `embed_metadata`: Add metadata tags
- `skip_existing`: Skip already downloaded files
- `max_retries`: Retry attempts for failed downloads
- `delay_between_downloads`: Delay between downloads

### **Artist-Specific Settings**
- `include_posthumous`: Include posthumous releases
- `include_viral_hits`: Separate viral hit folder
- `include_freestyles`: Download freestyle content
- `include_trending`: Include TikTok trends
- `organize_by_album`: Create album folders

## 🎭 Artist-Specific Highlights

### **Juice WRLD** 💜
- 999 legacy preservation
- Emotional content categorization
- Posthumous release handling
- Chicago drill context

### **King Von** 🔫
- O'Block cultural context
- Drill music optimization
- Posthumous tribute content
- Chicago scene preservation

### **Lil Tecca** 🎵
- Viral hit prioritization
- Teen rap optimization
- TikTok trend inclusion
- SoundCloud aesthetic

### **NLE Choppa** 🔥
- Shotta Flow series
- Memphis drill scene
- Spiritual content inclusion
- High-energy rap

### **Blueface** 💰
- West Coast rap context
- "Thotiana" viral hits
- California cultural preservation
- Crip gang context

### **YNW Melly** 🌴
- Florida melodic rap
- Emotional content handling
- Tribute and support content
- Gifford location metadata

### **Lil Loaded** 🤠
- Texas drill scene
- Posthumous releases
- Dallas cultural context
- "6locc 6a6y" series

### **Rembo** 🌍
- Afrobeat specialization
- African music preservation
- Dance content inclusion
- Cultural context

### **Lil Tecca** 🎵
- Melodic SoundCloud rap
- Viral hit optimization
- Teen cultural context
- TikTok trend support

### **Zeddy Will** 🎤
- Underground rap support
- Emerging artist focus
- Freestyle content
- DIY music scene

### **Eminem** 🎤
- Multi-era discography
- Spotify integration
- Hip-hop legend status
- Comprehensive metadata

## � Future Enhancements

Planned features for upcoming versions:
- [ ] GUI interface for easier use
- [ ] Batch downloading multiple artists
- [ ] Automatic updates for new releases
- [ ] Integration with streaming platforms
- [ ] Mobile app version
- [ ] Cloud storage integration
- [ ] Social media sharing features

## 🎯 Usage Tips

### **First Time Setup**
1. Start with small `max_songs` value (10-20)
2. Test different quality settings
3. Verify FFmpeg installation
4. Check available disk space

### **Performance Optimization**
1. Increase `max_retries` for unstable connections
2. Adjust `delay_between_downloads` to avoid rate limiting
3. Use SSD storage for faster processing
4. Close other bandwidth-intensive applications

### **Legal & Ethical**
1. Only download content you have rights to
2. Respect artist copyrights
3. Support artists through official channels
4. Follow YouTube's Terms of Service

## Legal Notice

This tool is for educational and personal use only. Please respect copyright laws and only download content you have the right to access. The authors are not responsible for any misuse of this software.

## System Requirements

- **Python**: 3.7 or higher
- **FFmpeg**: Required for audio processing
- **Memory**: 4GB+ RAM recommended
- **Storage**: 5GB+ for full discographies
- **Network**: Stable internet connection

### Installing FFmpeg

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to folder (e.g., `C:\ffmpeg`)
3. Add to PATH: `set PATH=%PATH%;C:\ffmpeg\bin`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## Logging & Statistics

Each downloader generates comprehensive reports:

### **Log Files**
- Real-time console output
- Detailed log files (`artist_downloader.log`)
- Error tracking and debugging info

### **Statistics**
- Total songs attempted/successful/failed
- Success rate percentage
- Download duration
- Configuration summary
- Discography breakdown

### **Playlists**
- M3U format for universal compatibility
- Album-specific playlists
- Special category playlists (Viral Hits, Emotional, etc.)
- Complete discography playlist

## Troubleshooting

### **Common Issues**

**FFmpeg Errors**
- Install FFmpeg and add to system PATH
- Verify installation with `ffmpeg -version`
- Restart terminal after PATH changes

**Network Issues**
- Check internet connection stability
- Increase `max_retries` value
- Try different quality settings
- Use VPN for geo-restricted content

**Permission Errors**
- Run as administrator (Windows)
- Change download directory permissions
- Ensure write access to target folder

**Quality Issues**
- Change `quality` parameter to `"bestaudio/best"`
- Check source video quality
- Verify bitrate settings

### **Debug Mode**
For detailed troubleshooting, modify logger level:
```python
self.logger.setLevel(logging.DEBUG)
```

## Contributing

Feel free to submit issues and enhancement requests!

### **How to Contribute**
1. Report bugs with detailed descriptions
2. Suggest new artist-specific features
3. Share configuration improvements
4. Help with documentation
5. Test new releases

## License

This project is for educational purposes. Use responsibly and in accordance with YouTube's Terms of Service and applicable copyright laws.

---

**🎵 Happy Downloading! Support Your Favorite Artists! 🎵**

