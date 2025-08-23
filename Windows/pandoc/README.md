Pandoc is a powerful command-line tool for converting between document formats (Markdown, Word, PDF, HTML, LaTeX, etc.).

---

## 🔧 Installation

* **Windows/macOS/Linux**: [Download Pandoc](https://pandoc.org/installing.html) and install.
* Check installation:

  ```bash
  pandoc --version
  ```

---

## 📂 Basic Usage

The general structure:

```bash
pandoc input.ext -o output.ext
```

* `input.ext` → source file (e.g., `.md`, `.docx`, `.html`)
* `output.ext` → target file (e.g., `.pdf`, `.docx`, `.html`)

---

## 📖 Common Conversions

### 1. Markdown → PDF

```bash
pandoc file.md -o file.pdf
```

👉 Needs **LaTeX** installed (like [TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/)).

### 2. Markdown → Word

```bash
pandoc file.md -o file.docx
```

### 3. Word → Markdown

```bash
pandoc file.docx -o file.md
```

### 4. Markdown → HTML

```bash
pandoc file.md -o file.html
```

---

## 🎨 Options & Styling

### Add Table of Contents

```bash
pandoc file.md -o file.pdf --toc
```

### Set Metadata (title, author, date)

```bash
pandoc file.md -o file.pdf -V title="My Report" -V author="John Doe" -V date="2025-08-22"
```

### Use Custom Template

```bash
pandoc file.md -o file.pdf --template=mytemplate.tex
```

### Apply CSS (for HTML output)

```bash
pandoc file.md -o file.html --css=style.css
```

---

## 📑 Multiple Input Files

```bash
pandoc chap1.md chap2.md chap3.md -o book.pdf
```

---

## ⚡ Extra Tips

* **Preview before converting** (to HTML):

  ```bash
  pandoc file.md -o file.html && open file.html
  ```
* **Extract text from PDFs** (requires `pdftotext`):

  ```bash
  pdftotext file.pdf output.txt
  ```
* **List supported formats**:

  ```bash
  pandoc --list-output-formats
  ```
