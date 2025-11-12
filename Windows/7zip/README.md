These scripts Requires **7-Zip** (`7z.exe` in PATH or at `C:\Program Files\7-Zip\7z.exe`).

## 🔐MultiArchivePasswordTester.bat  
This batch script tests all passwords from `passwords.txt` on every archive in the folder.

### Features  
* Supports `.rar`, `.zip`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`, `.iso`
* Tries every password on every archive
* Logs all attempts to `attempts.log`
* Saves results to `attempts.csv` (`archive,password,success`)
* Extracts found archives to `extracted/`

### Usage  
1. Put this `script`, `passwords.txt`, and your `archives` in the same folder.
2. Run the `MultiArchivePasswordTester.bat` file.
3. Check:
   * `attempts.log` for details
   * `attempts.csv` for results
   * `extracted/` for extracted files

## ✂️SplitZIPArchiver.bat

### Usage:  
1. Run `SplitZIPArchiver.bat`.
2. Enter:
   * Source file/folder path
   * Archive name (no extension)
   * Split size (e.g., 100M, 700M, 1G)
   * Output folder path
3. The script creates a split `.7z` archive in the output folder.

#### Output Example:  
`archive.7z.001`, `archive.7z.002`, ...

## 💾ZipAllFolders.bat

This batch script compresses **each subfolder** in the current directory into its own `.zip` file.

### What It Does

For every folder (`X`) in the current directory, it creates a `X.zip` archive containing the contents of the folder `X`.

### Usage  
1. Place the `ZipAllFolders.bat` file in the parent directory containing your folders.
2. Run it — each folder will be zipped into a file with the same name.

### Notes  
* You can change compression level (`-mx=5`) or type (`-tzip`) as needed.
* Does not delete the original folders.