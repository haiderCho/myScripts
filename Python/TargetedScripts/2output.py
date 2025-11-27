import os
import shutil

# Set this to the folder where all your .ico files are currently located
SOURCE_FOLDER = r"C:\Users\NOBEL\GitHub\Folder-Icons\Windows 11 Style\ZFolder 11\Productivity"
DEST_FOLDER = r"C:\Users\NOBEL\GitHub\Folder-Icons\Windows 11 Style\ZFolder 11\Productivity"

# Category mapping
categories = {
    "Backup_System": [
        "archive.ico", "autoruns.ico", "backups.ico", "Dism++.ico", "everything.ico",
        "log.ico", "macrium_reflect.ico", "Revo-uninstaller.ico", "wiztree.ico", "root.ico"
    ],
    "Cloud_FileSync": [
        "baidu_netdisk.ico", "LocalSend-1.ico", "LocalSend-2.ico", "LocalSend-3.ico",
        "LocalSend-5.ico", "LocalSend-6.ico"
    ],
    "Productivity_Office": [
        "excel.ico", "ms365.ico", "powerpoint.ico", "word.ico", "ticktick.ico",
        "taaghche.ico", "simplenote.ico", "teamfiles.ico", "pr.ico"
    ],
    "Multimedia_Design": [
        "canMV.ico", "civitai.ico", "courseforge.ico", "creative-cloud.ico", "crewai.ico",
        "cupcut.ico", "davinci.ico", "Design-1.ico", "Font-2.ico", "fonts.ico", "foobar2000.ico",
        "keyshot.ico", "kicad.ico", "Kicad_GERBER.ico", "Kicad_PCB.ico", "Kicad_SCH.ico",
        "lens.ico", "lumion (2).ico", "markdown-1.ico", "photoscape.ico", "pico8_reworked_02.ico",
        "pixel-builds.ico", "pixel-experience.ico", "pixelated.ico", "pixelbuilds.ico",
        "pixelify.ico", "plan9.ico", "planet_scale.ico", "png.ico", "popmods.ico"
    ],
    "Development_Programming": [
        "devto.ico", "ESPIDF-1.ico", "ESPIDF.ico", "flask.ico", "Grafana.ico", "GSI.ico", "gtk.ico",
        "handshaker-1.ico", "handshaker.ico", "Huggingface.ico", "javascript-js.ico", "npm.ico",
        "nuget.ico", "prisma.ico", "Qwik-1.ico", "qwik.ico", "rails.ico", "redis.ico", "redux.ico",
        "remix.ico", "replit.ico", "rollupjs.ico", "ros.ico", "RTthread-1.ico", "RTthread.ico",
        "sass (2).ico", "sass.ico", "selenium.ico", "sentry.ico", "sequelize.ico", "sharex (2).ico",
        "sharex.ico", "solidity.ico", "solidjs.ico", "styled-components.ico", "supabase.ico",
        "svelte.ico", "swift (2).ico", "swift-1.ico", "swift.ico", "symfony-2.ico", "syncthing-1.ico",
        "syncthing.ico", "tauri.ico", "todesk.ico", "uipath-1.ico", "uipath.ico", "Vagrant.ico",
        "vite.ico", "Vivado.ico", "vnote.ico", "VOFA.ico", "webflow.ico", "web_assembly.ico",
        "xamarin.ico", "Xilinx.ico", "yarn.ico", "yew.ico", "yii2.ico", "zotero.ico"
    ],
    "Security_Passwords": [
        "enpass.ico", "KeePassXC-1.ico", "KeePassXC.ico", "Tailscale.ico"
    ],
    "Gaming_Emulator": [
        "osu!.ico", "Readyfor-Motorola.ico", "rpcs3.ico", "ryujinx-emu.ico",
        "Ubisoft_connect.ico", "xbox_original.ico"
    ],
    "Misc_System_Accessory": [
        "desktop-computer.ico", "dolby.ico", "dts.ico", "GoWin.ico", "HiSpark.ico",
        "Home_Assisant.ico", "Hwinfo.ico", "nameless.ico", "miui.ico", "moonrepo-moon.ico",
        "moonrepo-proto.ico", "netease.ico", "netease_cloud_music-1.ico", "netease_cloud_music.ico",
        "netease_cloud_music_white.ico", "netease_mumu_player_12.ico", "nikgapps.ico",
        "nusantara_project.ico", "orangefox.ico", "oven.ico", "package.ico", "paradox.ico",
        "paranoid.ico", "Quickshare.ico", "rexus.ico", "risingos.ico", "rocket.ico", "scrcpy.ico",
        "Shortcuts.ico", "user.ico", "user2.ico", "v2ray.ico", "viz.ico", "Wacom (2).ico",
        "wallpapers.ico", "wechat-1.ico", "wikipedia.ico", "Windows-updated-blocker.ico",
        "workers.ico", "xiaomi-1.ico", "Xmind.ico", "yaap.ico", "youtube-black.ico"
    ]
}

# Create destination folders if they don't exist
for category in categories:
    os.makedirs(os.path.join(DEST_FOLDER, category), exist_ok=True)

# Move files into their respective folders
for category, files in categories.items():
    for file_name in files:
        src_path = os.path.join(SOURCE_FOLDER, file_name)
        dest_path = os.path.join(DEST_FOLDER, category, file_name)
        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            print(f"Moved {file_name} to {category}")
        else:
            print(f"File not found: {file_name}")

print("Sorting completed.")
