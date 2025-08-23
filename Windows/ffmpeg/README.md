## 🔹 1. Basic Info

* **Check version**

  ```bash
  ffmpeg -version
  ```
* **Check supported formats & codecs**

  ```bash
  ffmpeg -formats
  ffmpeg -codecs
  ```

---

## 🔹 2. Input & Output

* **Convert a video** (e.g., MP4 → MKV)

  ```bash
  ffmpeg -i input.mp4 output.mkv
  ```
* **Convert audio** (e.g., WAV → MP3)

  ```bash
  ffmpeg -i input.wav output.mp3
  ```

---

## 🔹 3. Extracting

* **Extract audio from video**

  ```bash
  ffmpeg -i video.mp4 -vn -acodec copy audio.aac
  ```
* **Extract video without audio**

  ```bash
  ffmpeg -i video.mp4 -an output.mp4
  ```
* **Take a screenshot at 1 minute**

  ```bash
  ffmpeg -ss 00:01:00 -i video.mp4 -frames:v 1 screenshot.png
  ```

---

## 🔹 4. Compression & Re-encoding

* **Compress video with H.264**

  ```bash
  ffmpeg -i input.mp4 -vcodec libx264 -crf 23 output.mp4
  ```

  (lower `-crf` = better quality, 18–28 is typical)
* **Compress audio**

  ```bash
  ffmpeg -i input.wav -b:a 192k output.mp3
  ```

---

## 🔹 5. Trimming & Cutting

* **Cut a clip (without re-encoding, fast)**

  ```bash
  ffmpeg -ss 00:01:00 -to 00:02:00 -i input.mp4 -c copy clip.mp4
  ```
* **Cut with re-encoding (accurate cuts)**

  ```bash
  ffmpeg -ss 00:01:00 -to 00:02:00 -i input.mp4 -c:v libx264 -c:a aac clip.mp4
  ```

---

## 🔹 6. Merging & Concatenation

* **Merge multiple files (same codec/format)**
  Create `file_list.txt`:

  ```
  file 'file1.mp4'
  file 'file2.mp4'
  ```

  Then run:

  ```bash
  ffmpeg -f concat -safe 0 -i file_list.txt -c copy output.mp4
  ```

* **Merge audio + video**

  ```bash
  ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4
  ```

---

## 🔹 7. Subtitles

* **Add subtitles (soft subs)**

  ```bash
  ffmpeg -i video.mp4 -i subs.srt -c copy -c:s mov_text output.mp4
  ```
* **Burn subtitles into video (hard subs)**

  ```bash
  ffmpeg -i video.mp4 -vf subtitles=subs.srt output.mp4
  ```

---

## 🔹 8. Screen & Webcam Recording

* **Record screen (Linux X11 example)**

  ```bash
  ffmpeg -video_size 1920x1080 -framerate 30 -f x11grab -i :0.0 output.mkv
  ```
* **Record webcam**

  ```bash
  ffmpeg -f v4l2 -i /dev/video0 output.mkv
  ```
* **Record screen + audio (Windows example)**

  ```bash
  ffmpeg -f dshow -i video="screen-capture-recorder" -f dshow -i audio="virtual-audio-capturer" output.mkv
  ```

---

## 🔹 9. Streaming

* **Stream to RTMP server (e.g., YouTube Live)**

  ```bash
  ffmpeg -re -i input.mp4 -c:v libx264 -b:v 3000k -c:a aac -f flv rtmp://a.rtmp.youtube.com/live2/STREAM_KEY
  ```

---

## 🔹 10. Useful Tricks

* **Show media info**

  ```bash
  ffmpeg -i input.mp4
  ```
* **Change playback speed**

  * Faster (2×):

    ```bash
    ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output.mp4
    ```
  * Slower (0.5×):

    ```bash
    ffmpeg -i input.mp4 -filter:v "setpts=2.0*PTS" output.mp4
    ```
* **Convert image sequence to video**

  ```bash
  ffmpeg -framerate 24 -i img%03d.png output.mp4
  ```