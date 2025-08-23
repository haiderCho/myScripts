## 🧰 1. **Installation**

### ✅ Using `pip` (Recommended):

```bash
pip install -U gallery-dl
```

Or, if you want to install it only for your user:

```bash
pip install --user -U gallery-dl
```

---

## 🛠️ 2. **Basic Usage**

### 📥 Download from a URL:

```bash
gallery-dl <URL>
```

**Example:**

```bash
gallery-dl https://www.deviantart.com/artistname/gallery
```

This downloads all the images from that artist’s gallery.

---

## ⚙️ 3. **Configuration File**

Create a config file for authentication, output paths, format settings, and more.

### 📁 Default location:

* **Linux/Mac**: `~/.config/gallery-dl/config.json`
* **Windows**: `%APPDATA%\gallery-dl\config.json`

You can create it manually.

### 🧾 Example `config.json`:

```json
{
    "extractor": {
        "base-directory": "~/Downloads/gallery-dl",
        "postprocessors": [{
            "name": "metadata"
        }],
        "twitter": {
            "username": "your_username",
            "password": "your_password"
        }
    },
    "downloader": {
        "part": true,
        "rate": null,
        "timeout": 30
    }
}
```

---

## 🔐 4. **Authentication (Login for private content)**

For some sites (like Instagram, Twitter, Pixiv, etc.), you need to log in.

There are 3 common ways:

### a. **Username & password** (some sites)

```json
"twitter": {
    "username": "your_username",
    "password": "your_password"
}
```

### b. **Cookies (recommended)**

Use browser cookies for logged-in access.

Use a browser extension like:

* **Get cookies.txt**
* Export cookies for the site, and save them as `cookies.txt`.

Then run:

```bash
gallery-dl --cookies cookies.txt <URL>
```

---

## 📁 5. **Change Output Directory or Filename Format**

You can customize where and how files are saved.

### In config file:

```json
"extractor": {
    "base-directory": "~/Downloads/gallery-dl",
    "filename": "{title}_{id}.{extension}"
}
```

### Or via CLI:

```bash
gallery-dl -D ./downloads --filename "{author}_{title}" <URL>
```

---

## 🌐 6. **Supported Sites**

Run this to list all supported sites:

```bash
gallery-dl --list-extractors
```

Or visit: [https://github.com/mikf/gallery-dl/blob/master/docs/supportedsites.md](https://github.com/mikf/gallery-dl/blob/master/docs/supportedsites.md)

---

## 🧪 7. **Dry Run (Preview Only)**

To check what would be downloaded, but not actually download:

```bash
gallery-dl --simulate <URL>
```

---

## 💡 8. **Useful Tips**

* **Update regularly**: Some site layouts change frequently. Update with:

  ```bash
  pip install -U gallery-dl
  ```

* **Use `--range` or `--limit`** to restrict the number of items:

  ```bash
  gallery-dl --range 1-5 <URL>
  gallery-dl --limit 10 <URL>
  ```

* **Use with `aria2c` or `wget`** if you want to accelerate downloading using external tools.

---

## 🔄 9. **Downloading from a list of URLs**

Create a `.txt` file (e.g., `urls.txt`) with one URL per line:

```txt
https://www.reddit.com/r/pics/
https://twitter.com/username/media
```

Then run:

```bash
gallery-dl -i urls.txt
```

---

## 🧹 10. **Postprocessors (e.g., save metadata)**

In `config.json`:

```json
"postprocessors": [{
    "name": "metadata"
}]
```