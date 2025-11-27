import os
import shutil

# Path to the folder containing all your icons
source_folder = r"C:\Users\NOBEL\GitHub\Folder-Icons\Windows 11 Style\ZFolder 11"  # <-- change this

# Destination folders
dev_folder = os.path.join(source_folder, "Development")
prod_folder = os.path.join(source_folder, "Productivity")

# Create folders if they don't exist
os.makedirs(dev_folder, exist_ok=True)
os.makedirs(prod_folder, exist_ok=True)

# Lists of icons for each folder
development_icons = [
    "3D_Printer.ico", "adb.ico", "ae.ico", "ahk.ico", "ahk (2).ico", "ai_script.ico",
    "AltiumDesigner.ico", "appwrite-1.ico", "application-1.ico", "application-2.ico",
    "application-3.ico", "Autohotkey.ico", "avalonia.ico", "avalonia_border.ico",
    "CCS.ico", "cubeIDE.ico", "cubeMX.ico", "cypress.ico", "ddev.ico", "flask.ico",
    "flstudio-1.ico", "flstudio.ico", "graphql.ico", "gulp.ico", "haxe.ico",
    "haxe_flixel.ico", "hbuilderx.ico", "hbuilderx_text.ico", "idea.ico", "java-1.ico",
    "javascript-js.ico", "jenkins.ico", "julia.ico", "kotlin-2.ico", "ktor.ico",
    "kubernetes.ico", "lua.ico", "marmoset.ico", "materialui.ico", "matlab.ico",
    "musescore_studio.ico", "mysql-1.ico", "nodejs-2.ico", "npm.ico", "nuget.ico",
    "nuxtjs.ico", "obs-studio.ico", "octave.ico", "ollama.ico", "openscad.ico",
    "openshift.ico", "openstack.ico", "oracle-1.ico", "oracle.ico", "peazip.ico",
    "prisma.ico", "processing.ico", "pug.ico", "Qualcomm.ico", "qwik-1.ico", "qwik.ico",
    "r.ico", "rabbitmq.ico", "rails.ico", "redis.ico", "redux.ico", "remix.ico",
    "replit.ico", "rollupjs.ico", "ros.ico", "RTthread-1.ico", "RTthread.ico", "sass.ico",
    "sass (2).ico", "selenium.ico", "sentry.ico", "sequelize.ico", "sharex.ico",
    "sharex (2).ico", "solidity.ico", "solidjs.ico", "styled-components.ico", "supabase.ico",
    "svelte.ico", "swift.ico", "swift-1.ico", "swift (2).ico", "symfony-2.ico",
    "syncthing.ico", "syncthing-1.ico", "tauri.ico", "threejs.ico", "todesk.ico",
    "typora.ico", "typora-1.ico", "uipath.ico", "uipath-1.ico", "Vagrant.ico", "vite.ico",
    "Vivado.ico", "vnote.ico", "VOFA.ico", "webflow.ico", "web_assembly.ico",
    "xamarin.ico", "Xilinx.ico", "yarn.ico", "yew.ico", "yii2.ico", "zotero.ico"
]

productivity_icons = [
    "archive.ico", "autoruns.ico", "baidu_netdisk.ico", "backups.ico", "canMV.ico",
    "civitai.ico", "courseforge.ico", "creative-cloud.ico", "crewai.ico", "cupcut.ico",
    "davinci.ico", "Design-1.ico", "desktop-computer.ico", "devto.ico", "Dism++.ico",
    "dolby.ico", "dts.ico", "emacs.ico", "emule.ico", "enpass.ico", "Envato.ico",
    "ESPIDF-1.ico", "ESPIDF.ico", "everything.ico", "excel.ico", "fiverr.ico",
    "flamegapps.ico", "Font-2.ico", "fonts.ico", "foobar2000.ico", "GoWin.ico", "grafana.ico",
    "greenshot.ico", "GSI.ico", "gtk.ico", "handshaker.ico", "handshaker-1.ico", "HiSpark.ico",
    "Home_Assisant.ico", "Huggingface.ico", "Hwinfo.ico", "KeePassXC.ico", "KeePassXC-1.ico",
    "keyshot.ico", "kicad.ico", "Kicad_GERBER.ico", "Kicad_PCB.ico", "Kicad_SCH.ico",
    "lens.ico", "LocalSend-1.ico", "LocalSend-2.ico", "LocalSend-3.ico", "LocalSend-5.ico",
    "LocalSend-6.ico", "log.ico", "Logitech_Options.ico", "Logitech_Options-1.ico",
    "Logitech_Options+.ico", "Logitech_control.ico", "lr.ico", "lumion (2).ico",
    "macrium_reflect.ico", "markdown-1.ico", "miui.ico", "moonrepo-moon.ico", "moonrepo-proto.ico",
    "ms365.ico", "nameless.ico", "netease.ico", "netease_cloud_music-1.ico",
    "netease_cloud_music.ico", "netease_cloud_music_white.ico", "netease_mumu_player_12.ico",
    "nikgapps.ico", "nusantara_project.ico", "orangefox.ico", "osu!.ico", "oven.ico",
    "package.ico", "paradox.ico", "paranoid.ico", "photoscape.ico", "pico8_reworked_02.ico",
    "pixelify.ico", "pixelated.ico", "pixel-experience.ico", "pixelbuilds.ico",
    "pixel-builds.ico", "plan9.ico", "planet_scale.ico", "png.ico", "popchat.ico",
    "popmods.ico", "powerpoint.ico", "pr.ico", "Quickshare.ico", "Readyfor-Motorola.ico",
    "Revo-uninstaller.ico", "rexus.ico", "ricdroid.ico", "risingos.ico", "rocket.ico",
    "root.ico", "rpcs3.ico", "ryujinx-emu.ico", "Scoop.ico", "scrcpy.ico", "Shortcuts.ico",
    "simplenote.ico", "taaghche.ico", "Tailscale.ico", "teamfiles.ico", "ticktick.ico",
    "tidwib.ico", "tim.ico", "trash.ico", "Ubisoft_connect.ico", "ubuntu-studio.ico",
    "user.ico", "user2.ico", "v2ray.ico", "viz.ico", "Wacom (2).ico", "wallpapers.ico",
    "wechat-1.ico", "wikipedia.ico", "Windows-updated-blocker.ico", "wiztree.ico", "word.ico",
    "workers.ico", "xbox_original.ico", "xiaomi-1.ico", "Xmind.ico", "yaap.ico",
    "youtube-black.ico"
]

# Move icons
for icon in development_icons:
    src = os.path.join(source_folder, icon)
    if os.path.exists(src):
        shutil.move(src, dev_folder)

for icon in productivity_icons:
    src = os.path.join(source_folder, icon)
    if os.path.exists(src):
        shutil.move(src, prod_folder)

print("Icons moved successfully!")
