## 1. **Basic Download**

```bash
yt-dlp URL
```

Downloads the best available video+audio.

---

## 2. **Download Audio Only**

```bash
yt-dlp -x --audio-format mp3 URL
```

* `-x` → extract audio
* `--audio-format mp3` → convert to mp3 (can also be `opus`, `wav`, `m4a`, etc.)

---

## 3. **Choose Quality**

```bash
yt-dlp -f bestvideo+bestaudio URL
yt-dlp -f "bv*+ba/b" URL
yt-dlp -f "137+140" URL
```

* `bestvideo+bestaudio` → best separate streams
* `"137+140"` → manually choose formats by ID (check with `-F`)

List available formats first:

```bash
yt-dlp -F URL
```

---

## 4. **Download Playlist**

```bash
yt-dlp URL
```

By default, yt-dlp downloads entire playlists.
For a single video from a playlist:

```bash
yt-dlp --no-playlist URL
```

---

## 5. **Download Subtitles**

```bash
yt-dlp --write-subs --sub-lang en --convert-subs srt URL
```

* Downloads English subs and converts them to `.srt`.

For auto-generated subs:

```bash
yt-dlp --write-auto-subs --sub-lang en URL
```

---

## 6. **File Naming & Output Template**

```bash
yt-dlp -o "%(title)s.%(ext)s" URL
yt-dlp -o "%(playlist_index)s - %(title)s.%(ext)s" URL
```

* `%()` variables let you control filenames (title, uploader, resolution, etc.).
  👉 Full template list: `yt-dlp --help | grep -A50 "OUTPUT TEMPLATE"`

---

## 7. **Download with Cookies (e.g., private videos)**

```bash
yt-dlp --cookies-from-browser chrome URL
```

(or `firefox`, `edge`, etc.)

Or use an exported cookies.txt:

```bash
yt-dlp --cookies cookies.txt URL
```

---

## 8. **Throttling / Speed**

```bash
yt-dlp -r 500K URL
```

* `-r` → limit download rate (e.g., `500K`, `2M`)

Resume interrupted download:

```bash
yt-dlp -c URL
```

---

## 9. **Merge into MKV/MP4**

By default, yt-dlp merges separate video/audio using ffmpeg.
To force format:

```bash
yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 URL
```

---

## 10. **Advanced Tricks**

* Download first N videos from a playlist:

  ```bash
  yt-dlp --playlist-items 1-10 URL
  ```
* Download only audio with thumbnail embedded:

  ```bash
  yt-dlp -x --audio-format mp3 --embed-thumbnail URL
  ```
* Avoid overwriting existing files:

  ```bash
  yt-dlp -w URL
  ```

---

⚡ **Pro Tip:** You can make a `config.txt` file in your yt-dlp directory (or `~/.config/yt-dlp/config`) with your favorite options (like `-f bestvideo+bestaudio -o "%(title)s.%(ext)s"`) so you don’t have to type them every time.

---

### Common Options:

| Option                      | Description                               |
| --------------------------- | ----------------------------------------- |
| `-f best`                   | Download best quality format available.   |
| `-o "%(title)s.%(ext)s"`    | Set output filename to video title.       |
| `--audio-format mp3`        | Convert audio to MP3 (requires ffmpeg).   |
| `--extract-audio`           | Extract audio only.                       |
| `--playlist-items 1,3,5`    | Download specific videos from a playlist. |
| `--merge-output-format mp4` | Merge formats into MP4 (for DASH videos). |