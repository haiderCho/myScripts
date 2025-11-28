@echo off
setlocal enabledelayedexpansion

:: ================================================
:: File Sorter
:: Sorts files into folders based on keywords
:: Author: haiderCho
:: ================================================

:: Safety Check: Don't run in system folders
if /i "%CD%"=="C:\Windows" goto :unsafe
if /i "%CD%"=="C:\Windows\System32" goto :unsafe
if /i "%CD%"=="C:\" goto :unsafe

echo Sorting files in: "%CD%"
echo.

:: Define category folders
set categories=Brands Software Games Programming AndroidROMs Hardware System Media Folders Misc

for %%c in (%categories%) do (
    if not exist "%%c" mkdir "%%c"
)

:: Logging function
set "LOGFILE=sort_log.txt"
echo [%DATE% %TIME%] Sorting started > "%LOGFILE%"

:: === Brands ===
call :MoveFiles "*Amazon.ico" "Brands"
call :MoveFiles "*Aorus*.ico" "Brands"
call :MoveFiles "*Asus*.ico" "Brands"
call :MoveFiles "Blizzard.ico" "Brands"
call :MoveFiles "Bethesda.ico" "Brands"
call :MoveFiles "Battlestate.ico" "Brands"
call :MoveFiles "bocbank.ico" "Brands"
call :MoveFiles "DeviantArt.ico" "Brands"
call :MoveFiles "Envato.ico" "Brands"
call :MoveFiles "Epic.ico" "Brands"
call :MoveFiles "EVGA.ico" "Brands"
call :MoveFiles "Gigabyte*.ico" "Brands"
call :MoveFiles "HiSpark.ico" "Brands"
call :MoveFiles "*Huggingface.ico" "Brands"
call :MoveFiles "*Logitech*.ico" "Brands"
call :MoveFiles "*Lenovo*.ico" "Brands"
call :MoveFiles "*mastodon.ico" "Brands"
call :MoveFiles "*miHoYo.ico" "Brands"
call :MoveFiles "*netease*.ico" "Brands"
call :MoveFiles "*Nexus*.ico" "Brands"
call :MoveFiles "NZXT.ico" "Brands"
call :MoveFiles "obsidian-3.ico" "Brands"
call :MoveFiles "OrangePi.ico" "Brands"
call :MoveFiles "Origin.ico" "Brands"
call :MoveFiles "Redbubble.ico" "Brands"
call :MoveFiles "Redhat.ico" "Brands"
call :MoveFiles "Riot.ico" "Brands"
call :MoveFiles "Rockstar.ico" "Brands"
call :MoveFiles "ROG.ico" "Brands"
call :MoveFiles "*Teamspeak.ico" "Brands"
call :MoveFiles "*tencent*.ico" "Brands"
call :MoveFiles "Tumblr.ico" "Brands"
call :MoveFiles "Ubisoft.ico" "Brands"
call :MoveFiles "Unsplash.ico" "Brands"
call :MoveFiles "*Wacom*.ico" "Brands"
call :MoveFiles "wikipedia.ico" "Brands"
call :MoveFiles "Xbox.ico" "Brands"
call :MoveFiles "Xiaomi*.ico" "Brands"
call :MoveFiles "Youtube.ico" "Brands"

:: === Software ===
call :MoveFiles "*Discord*.ico" "Software"
call :MoveFiles "Chrome.ico" "Software"
call :MoveFiles "cobalt.tools.ico" "Software"
call :MoveFiles "comfyui*.ico" "Software"
call :MoveFiles "Dism++.ico" "Software"
call :MoveFiles "dolby.ico" "Software"
call :MoveFiles "Drawing.ico" "Software"
call :MoveFiles "EASYEDA.ico" "Software"
call :MoveFiles "emby.ico" "Software"
call :MoveFiles "emule.ico" "Software"
call :MoveFiles "flux.ico" "Software"
call :MoveFiles "Grafana.ico" "Software"
call :MoveFiles "greenshot.ico" "Software"
call :MoveFiles "handshaker*.ico" "Software"
call :MoveFiles "Image Settings.ico" "Software"
call :MoveFiles "lmstudio.ico" "Software"
call :MoveFiles "marmoset_text.ico" "Software"
call :MoveFiles "mcreator.ico" "Software"
call :MoveFiles "notion.ico" "Software"
call :MoveFiles "Playnite.ico" "Software"
call :MoveFiles "popchat.ico" "Software"
call :MoveFiles "prometheus.ico" "Software"
call :MoveFiles "Quickshare.ico" "Software"
call :MoveFiles "scrcpy.ico" "Software"
call :MoveFiles "scummvm*.ico" "Software"
call :MoveFiles "Steam.ico" "Software"
call :MoveFiles "stex.ico" "Software"

:: === Games ===
call :MoveFiles "Battle.net.ico" "Games"
call :MoveFiles "dreamcast.ico" "Games"
call :MoveFiles "dosbox_new_01.ico" "Games"
call :MoveFiles "GOG*.ico" "Games"
call :MoveFiles "mame_arcade.ico" "Games"
call :MoveFiles "minecraft*.ico" "Games"
call :MoveFiles "MiniWorld_Main.ico" "Games"
call :MoveFiles "pc_engine*.ico" "Games"
call :MoveFiles "Playstation.ico" "Games"
call :MoveFiles "retroarch.ico" "Games"
call :MoveFiles "sega*.ico" "Games"
call :MoveFiles "snes.ico" "Games"

:: === Programming ===
call :MoveFiles "*chip*.ico" "Programming"
call :MoveFiles "concepts*.ico" "Programming"
call :MoveFiles "devto.ico" "Programming"
call :MoveFiles "elixir.ico" "Programming"
call :MoveFiles "gradle.ico" "Programming"
call :MoveFiles "gopher.ico" "Programming"
call :MoveFiles "haskell.ico" "Programming"
call :MoveFiles "ionic.ico" "Programming"
call :MoveFiles "ipsf.ico" "Programming"
call :MoveFiles "jest.ico" "Programming"
call :MoveFiles "langchain.ico" "Programming"
call :MoveFiles "less.ico" "Programming"
call :MoveFiles "lit.ico" "Programming"
call :MoveFiles "nim.ico" "Programming"
call :MoveFiles "nuke.ico" "Programming"
call :MoveFiles "pinia.ico" "Programming"
call :MoveFiles "pnpm.ico" "Programming"
call :MoveFiles "reactivex.ico" "Programming"
call :MoveFiles "svg.ico" "Programming"
call :MoveFiles "vala.ico" "Programming"
call :MoveFiles "zig.ico" "Programming"

:: === Android ROMs ===
call :MoveFiles "evolutionx*.ico" "AndroidROMs"
call :MoveFiles "evox.ico" "AndroidROMs"
call :MoveFiles "flamegapps.ico" "AndroidROMs"
call :MoveFiles "GSI.ico" "AndroidROMs"
call :MoveFiles "lineageos.ico" "AndroidROMs"
call :MoveFiles "miui.ico" "AndroidROMs"
call :MoveFiles "nikgapps.ico" "AndroidROMs"
call :MoveFiles "nusantara_project.ico" "AndroidROMs"
call :MoveFiles "opengapps.ico" "AndroidROMs"
call :MoveFiles "orangefox.ico" "AndroidROMs"
call :MoveFiles "paradox.ico" "AndroidROMs"
call :MoveFiles "paranoid.ico" "AndroidROMs"
call :MoveFiles "ricedroid.ico" "AndroidROMs"
call :MoveFiles "risingos.ico" "AndroidROMs"
call :MoveFiles "sparkos.ico" "AndroidROMs"
call :MoveFiles "statix.ico" "AndroidROMs"
call :MoveFiles "twrp.ico" "AndroidROMs"
call :MoveFiles "voltageos.ico" "AndroidROMs"
call :MoveFiles "yaap.ico" "AndroidROMs"

:: === Hardware ===
call :MoveFiles "cad.ico" "Hardware"
call :MoveFiles "desktop-computer.ico" "Hardware"
call :MoveFiles "keil4.ico" "Hardware"
call :MoveFiles "keil5.ico" "Hardware"
call :MoveFiles "luckfox.ico" "Hardware"
call :MoveFiles "rasberrypi.ico" "Hardware"
call :MoveFiles "rpi.ico" "Hardware"
call :MoveFiles "stm32.ico" "Hardware"
call :MoveFiles "vhd.ico" "Hardware"

:: === System ===
call :MoveFiles "Atention Folder.ico" "System"
call :MoveFiles "archive.ico" "System"
call :MoveFiles "cachefile.ico" "System"
call :MoveFiles "Close Folder.ico" "System"
call :MoveFiles "disabled.ico" "System"
call :MoveFiles "hibernate.ico" "System"
call :MoveFiles "lock.ico" "System"
call :MoveFiles "log.ico" "System"
call :MoveFiles "package.ico" "System"
call :MoveFiles "Search Folder.ico" "System"
call :MoveFiles "trash.ico" "System"
call :MoveFiles "Windows 11.ico" "System"
call :MoveFiles "Windows-updated-blocker.ico" "System"
call :MoveFiles "x64.ico" "System"
call :MoveFiles "x86.ico" "System"

:: === Folders ===
call :MoveFiles "*Folder*.ico" "Folders"

:: === Misc ===
call :MoveFiles "*.ico" "Misc"

echo Sorting completed.
pause
exit /b

:MoveFiles
if exist "%~1" (
    move "%~1" "%~2" >nul
    echo Moved "%~1" to "%~2"
    echo Moved "%~1" to "%~2" >> "%LOGFILE%"
)
exit /b

:unsafe
echo [ERROR] Unsafe directory! Do not run this script in system folders.
pause
