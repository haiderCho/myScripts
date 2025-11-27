@echo off
setlocal enabledelayedexpansion

REM === Define category folders ===
set categories=Brands Software Games Programming AndroidROMs Hardware System Media Folders Misc

for %%c in (%categories%) do (
    if not exist "%%c" mkdir "%%c"
)

REM === Brands ===
move "*Amazon.ico" "Brands" >nul
move "*Aorus*.ico" "Brands" >nul
move "*Asus*.ico" "Brands" >nul
move "Blizzard.ico" "Brands" >nul
move "Bethesda.ico" "Brands" >nul
move "Battlestate.ico" "Brands" >nul
move "bocbank.ico" "Brands" >nul
move "DeviantArt.ico" "Brands" >nul
move "Envato.ico" "Brands" >nul
move "Epic.ico" "Brands" >nul
move "EVGA.ico" "Brands" >nul
move "Gigabyte*.ico" "Brands" >nul
move "HiSpark.ico" "Brands" >nul
move "*Huggingface.ico" "Brands" >nul
move "*Logitech*.ico" "Brands" >nul
move "*Lenovo*.ico" "Brands" >nul
move "*mastodon.ico" "Brands" >nul
move "*miHoYo.ico" "Brands" >nul
move "*netease*.ico" "Brands" >nul
move "*Nexus*.ico" "Brands" >nul
move "NZXT.ico" "Brands" >nul
move "obsidian-3.ico" "Brands" >nul
move "OrangePi.ico" "Brands" >nul
move "Origin.ico" "Brands" >nul
move "Redbubble.ico" "Brands" >nul
move "Redhat.ico" "Brands" >nul
move "Riot.ico" "Brands" >nul
move "Rockstar.ico" "Brands" >nul
move "ROG.ico" "Brands" >nul
move "*Teamspeak.ico" "Brands" >nul
move "*tencent*.ico" "Brands" >nul
move "Tumblr.ico" "Brands" >nul
move "Ubisoft.ico" "Brands" >nul
move "Unsplash.ico" "Brands" >nul
move "*Wacom*.ico" "Brands" >nul
move "wikipedia.ico" "Brands" >nul
move "Xbox.ico" "Brands" >nul
move "Xiaomi*.ico" "Brands" >nul
move "Youtube.ico" "Brands" >nul

REM === Software ===
move "*Discord*.ico" "Software" >nul
move "Chrome.ico" "Software" >nul
move "cobalt.tools.ico" "Software" >nul
move "comfyui*.ico" "Software" >nul
move "Dism++.ico" "Software" >nul
move "dolby.ico" "Software" >nul
move "Drawing.ico" "Software" >nul
move "EASYEDA.ico" "Software" >nul
move "emby.ico" "Software" >nul
move "emule.ico" "Software" >nul
move "flux.ico" "Software" >nul
move "Grafana.ico" "Software" >nul
move "greenshot.ico" "Software" >nul
move "handshaker*.ico" "Software" >nul
move "Image Settings.ico" "Software" >nul
move "lmstudio.ico" "Software" >nul
move "marmoset_text.ico" "Software" >nul
move "mcreator.ico" "Software" >nul
move "notion.ico" "Software" >nul
move "Playnite.ico" "Software" >nul
move "popchat.ico" "Software" >nul
move "prometheus.ico" "Software" >nul
move "Quickshare.ico" "Software" >nul
move "scrcpy.ico" "Software" >nul
move "scummvm*.ico" "Software" >nul
move "Steam.ico" "Software" >nul
move "stex.ico" "Software" >nul

REM === Games ===
move "Battle.net.ico" "Games" >nul
move "dreamcast.ico" "Games" >nul
move "dosbox_new_01.ico" "Games" >nul
move "GOG*.ico" "Games" >nul
move "mame_arcade.ico" "Games" >nul
move "minecraft*.ico" "Games" >nul
move "MiniWorld_Main.ico" "Games" >nul
move "pc_engine*.ico" "Games" >nul
move "Playstation.ico" "Games" >nul
move "retroarch.ico" "Games" >nul
move "sega*.ico" "Games" >nul
move "snes.ico" "Games" >nul

REM === Programming ===
move "*chip*.ico" "Programming" >nul
move "concepts*.ico" "Programming" >nul
move "devto.ico" "Programming" >nul
move "elixir.ico" "Programming" >nul
move "gradle.ico" "Programming" >nul
move "gopher.ico" "Programming" >nul
move "haskell.ico" "Programming" >nul
move "ionic.ico" "Programming" >nul
move "ipsf.ico" "Programming" >nul
move "jest.ico" "Programming" >nul
move "langchain.ico" "Programming" >nul
move "less.ico" "Programming" >nul
move "lit.ico" "Programming" >nul
move "nim.ico" "Programming" >nul
move "nuke.ico" "Programming" >nul
move "pinia.ico" "Programming" >nul
move "pnpm.ico" "Programming" >nul
move "reactivex.ico" "Programming" >nul
move "svg.ico" "Programming" >nul
move "vala.ico" "Programming" >nul
move "zig.ico" "Programming" >nul

REM === Android ROMs ===
move "evolutionx*.ico" "AndroidROMs" >nul
move "evox.ico" "AndroidROMs" >nul
move "flamegapps.ico" "AndroidROMs" >nul
move "GSI.ico" "AndroidROMs" >nul
move "lineageos.ico" "AndroidROMs" >nul
move "miui.ico" "AndroidROMs" >nul
move "nikgapps.ico" "AndroidROMs" >nul
move "nusantara_project.ico" "AndroidROMs" >nul
move "opengapps.ico" "AndroidROMs" >nul
move "orangefox.ico" "AndroidROMs" >nul
move "paradox.ico" "AndroidROMs" >nul
move "paranoid.ico" "AndroidROMs" >nul
move "ricedroid.ico" "AndroidROMs" >nul
move "risingos.ico" "AndroidROMs" >nul
move "sparkos.ico" "AndroidROMs" >nul
move "statix.ico" "AndroidROMs" >nul
move "twrp.ico" "AndroidROMs" >nul
move "voltageos.ico" "AndroidROMs" >nul
move "yaap.ico" "AndroidROMs" >nul

REM === Hardware ===
move "cad.ico" "Hardware" >nul
move "desktop-computer.ico" "Hardware" >nul
move "keil4.ico" "Hardware" >nul
move "keil5.ico" "Hardware" >nul
move "luckfox.ico" "Hardware" >nul
move "rasberrypi.ico" "Hardware" >nul
move "rpi.ico" "Hardware" >nul
move "stm32.ico" "Hardware" >nul
move "vhd.ico" "Hardware" >nul

REM === System ===
move "Atention Folder.ico" "System" >nul
move "archive.ico" "System" >nul
move "cachefile.ico" "System" >nul
move "Close Folder.ico" "System" >nul
move "disabled.ico" "System" >nul
move "hibernate.ico" "System" >nul
move "lock.ico" "System" >nul
move "log.ico" "System" >nul
move "package.ico" "System" >nul
move "Search Folder.ico" "System" >nul
move "trash.ico" "System" >nul
move "Windows 11.ico" "System" >nul
move "Windows-updated-blocker.ico" "System" >nul
move "x64.ico" "System" >nul
move "x86.ico" "System" >nul

REM === Folders ===
move "*Folder*.ico" "Folders" >nul

REM === Misc ===
move "*.ico" "Misc" >nul

echo Sorting completed.
pause
