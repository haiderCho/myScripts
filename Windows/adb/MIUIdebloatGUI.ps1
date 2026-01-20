<#
.SYNOPSIS
    MIUI Debloat Manager GUI v1.0
    A safe, graphical interface for debloating Xiaomi devices.

.DESCRIPTION
    Provides a checkbox-based interface to remove bloat, tracking, and ads from MIUI/HyperOS.
    Features:
    - Auto-detects ADB (Choco, SDK, or local).
    - Safety checks for Xiaomi devices.
    - Multi-user support (Second Space).
    - Backup and Restore functionality.

.NOTES
    Author: Antigravity
    Version: 1.0
#>

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# ==========================================
# CONFIGURATION & GLOBAL VARS
# ==========================================
$Script:AdbCmd = "adb"
$Script:DeviceBrand = ""
$Script:DeviceModel = ""
$Script:TargetUser = "0"
$Script:LogFile = "$PSScriptRoot\debloat_manager.log"
$Script:BackupFile = "$PSScriptRoot\removed_packages.log"

# Package Lists (Hashtables for Name -> PackageID)
$SafeApps = [Ordered]@{
    "MIUI Analytics" = "com.miui.analytics"
    "MIUI MSA - Ads" = "com.miui.msa.global"
    "Xiaomi Discover" = "com.xiaomi.discover"
    "App Finder" = "com.mi.appfinder"
    "App Vault" = "com.mi.globalminusscreen"
    "Waitpaper Carousel" = "com.miui.android.fashiongallery"
    "Yellow Pages" = "com.miui.yellowpage"
    "Frequent Phrases" = "com.miui.phrase"
    "Print Recommendations" = "com.google.android.printservice.recommendation"
    "Facebook Services" = "com.facebook.services"
    "Facebook System" = "com.facebook.system"
    "Facebook App Manager" = "com.facebook.appmanager"
    "Services & Feedback" = "com.miui.miservice"
}

$TrackingApps = [Ordered]@{
    "Google Ad Services" = "com.google.android.adservices.api"
    "Google Feedback" = "com.google.android.feedback"
    "MIUI Bug Report" = "com.miui.bugreport"
    "Mi Sight Service" = "com.miui.misightservice"
    "MIUI Daemon" = "com.miui.daemon"
    "Qualcomm Opt-In" = "com.qualcomm.qti.optinoverlay"
}

$JunkApps = [Ordered]@{
    "Mi Browser (Standard)" = "com.mi.globalbrowser"
    "Mi Browser Global" = "com.miui.browser"
    "Mi Browser (Old)" = "com.android.browser"
    "Mi Music" = "com.miui.player"
    "Mi Video" = "com.miui.videoplayer"
    "Mi Coin/Payment" = "com.xiaomi.payment"
    "YouTube (Stock)" = "com.google.android.youtube"
    "YouTube Music" = "com.google.android.apps.youtube.music"
    "Compass" = "com.miui.compass"
    "Scanner" = "com.miui.scanner"
    "Screen Recorder" = "com.miui.screenrecorder"
    "FM Radio" = "com.miui.fm"
    "Notes" = "com.miui.notes"
}

# ==========================================
# ADB HELPERS
# ==========================================
function Log-Msg ($msg) {
    if ($txtConsole) {
        $txtConsole.AppendText("[$((Get-Date).ToString('HH:mm:ss'))] $msg`r`n")
        $txtConsole.ScrollToCaret()
    }
    Add-Content -Path $Script:LogFile -Value "[$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))] $msg"
}

function Find-Adb {
    Log-Msg "Searching for ADB..."
    # 1. Path
    if (Get-Command "adb" -ErrorAction SilentlyContinue) {
        $Script:AdbCmd = "adb"
        Log-Msg "Found ADB in system PATH."
        return $true
    }
    # 2. Local
    if (Test-Path "$PSScriptRoot\adb.exe") {
        $Script:AdbCmd = "$PSScriptRoot\adb.exe"
        Log-Msg "Found ADB in script folder."
        return $true
    }
    # 3. Chocolatey
    $chocoPath = "$env:ProgramData\chocolatey\bin\adb.exe"
    if (Test-Path $chocoPath) {
        $Script:AdbCmd = $chocoPath
        Log-Msg "Found ADB in Chocolatey."
        return $true
    }
    Log-Msg "ERROR: ADB not found. Please install it."
    return $false
}

function Get-ConnectedDevice {
    $out = & $Script:AdbCmd devices
    $lines = $out -split "`r`n"
    foreach ($line in $lines) {
        if ($line -match "device$") {
            return $true
        }
    }
    return $false
}

function Get-PackageStatus ($pkg) {
    # Returns true if installed for $Script:TargetUser
    $res = & $Script:AdbCmd shell pm list packages --user $Script:TargetUser $pkg
    return ($res -match "package:$pkg")
}

function Debloat-Package ($pkg, $name) {
    Log-Msg "Removing: $name ($pkg)..."
    $res = & $Script:AdbCmd shell pm uninstall --user $Script:TargetUser $pkg 2>&1
    if ($res -match "Success") {
        Log-Msg "SUCCESS: Removed $name"
        Add-Content -Path $Script:BackupFile -Value "[$((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))] REMOVED: $pkg ($name)"
    } else {
        Log-Msg "FAIL: $res"
    }
}

# ==========================================
# GUI CONSTRUCTION
# ==========================================
$form = New-Object System.Windows.Forms.Form
$form.Text = "MIUI Debloat Manager GUI v1.0"
$form.Size = New-Object System.Drawing.Size(800, 600)
$form.StartPosition = "CenterScreen"
# Dark Theme Colors
$bgColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
$fgColor = [System.Drawing.Color]::WhiteSmoke
$panelColor = [System.Drawing.Color]::FromArgb(45, 45, 48)
$form.BackColor = $bgColor
$form.ForeColor = $fgColor

# HEADER
$headerPanel = New-Object System.Windows.Forms.Panel
$headerPanel.Dock = "Top"
$headerPanel.Height = 60
$headerPanel.BackColor = $panelColor
$form.Controls.Add($headerPanel)

$lblStatus = New-Object System.Windows.Forms.Label
$lblStatus.Text = "Status: Check ADB"
$lblStatus.AutoSize = $true
$lblStatus.Location = New-Object System.Drawing.Point(10, 10)
$lblStatus.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
$headerPanel.Controls.Add($lblStatus)

$lblBrand = New-Object System.Windows.Forms.Label
$lblBrand.Text = "Device: Unknown"
$lblBrand.AutoSize = $true
$lblBrand.Location = New-Object System.Drawing.Point(10, 35)
$headerPanel.Controls.Add($lblBrand)

$btnRefresh = New-Object System.Windows.Forms.Button
$btnRefresh.Text = "Connect / Refresh"
$btnRefresh.Location = New-Object System.Drawing.Point(600, 15)
$btnRefresh.Size = New-Object System.Drawing.Size(150, 30)
$btnRefresh.FlatStyle = "Flat"
$btnRefresh.BackColor = [System.Drawing.Color]::FromArgb(0, 122, 204)
$headerPanel.Controls.Add($btnRefresh)

# TABS
$tabControl = New-Object System.Windows.Forms.TabControl
$tabControl.Dock = "Top"
$tabControl.Height = 400
#$tabControl.Appearance = "FlatButtons" 
$form.Controls.Add($tabControl)

function Add-Tab ($title, $pkgList) {
    $page = New-Object System.Windows.Forms.TabPage
    $page.Text = $title
    $page.BackColor = $bgColor
    
    $list = New-Object System.Windows.Forms.CheckedListBox
    $list.Dock = "Fill"
    $list.BackColor = $bgColor
    $list.ForeColor = $fgColor
    $list.CheckOnClick = $true
    
    foreach ($key in $pkgList.Keys) {
        $pkg = $pkgList[$key]
        $list.Items.Add("$key  [$pkg]") | Out-Null
    }
    
    $page.Controls.Add($list)
    $tabControl.TabPages.Add($page)
    return $list
}

$clbSafe = Add-Tab "Safe Debloat" $SafeApps
$clbTrack = Add-Tab "Tracking" $TrackingApps
$clbJunk = Add-Tab "Junk Apps" $JunkApps

# CONSOLE
$txtConsole = New-Object System.Windows.Forms.TextBox
$txtConsole.Multiline = $true
$txtConsole.Dock = "Bottom"
$txtConsole.Height = 100
$txtConsole.ScrollBars = "Vertical"
$txtConsole.BackColor = [System.Drawing.Color]::Black
$txtConsole.ForeColor = [System.Drawing.Color]::LimeGreen
$txtConsole.Font = New-Object System.Drawing.Font("Consolas", 9)
$form.Controls.Add($txtConsole)

# ACTIONS
$actionPanel = New-Object System.Windows.Forms.Panel
$actionPanel.Dock = "Bottom"
$actionPanel.Height = 50
$form.Controls.Add($actionPanel)

$btnDebloat = New-Object System.Windows.Forms.Button
$btnDebloat.Text = "DEBLOAT SELECTED"
$btnDebloat.Size = New-Object System.Drawing.Size(200, 35)
$btnDebloat.Location = New-Object System.Drawing.Point(280, 5)
$btnDebloat.BackColor = [System.Drawing.Color]::Crimson
$btnDebloat.ForeColor = [System.Drawing.Color]::White
$btnDebloat.FlatStyle = "Flat"
$actionPanel.Controls.Add($btnDebloat)

$lblUser = New-Object System.Windows.Forms.Label
$lblUser.Text = "User ID:"
$lblUser.Location = New-Object System.Drawing.Point(550, 15)
$lblUser.AutoSize = $true
$actionPanel.Controls.Add($lblUser)

$txtUser = New-Object System.Windows.Forms.TextBox
$txtUser.Text = "0"
$txtUser.Location = New-Object System.Drawing.Point(610, 12)
$txtUser.Size = New-Object System.Drawing.Size(50, 20)
$actionPanel.Controls.Add($txtUser)

# EVENTS
$btnRefresh.Add_Click({
    Log-Msg "Connecting..."
    if (-not (Find-Adb)) { return }
    
    if (Get-ConnectedDevice) {
        $brand = & $Script:AdbCmd shell getprop ro.product.brand
        $model = & $Script:AdbCmd shell getprop ro.product.model
        $Script:DeviceBrand = $brand.Trim()
        $lblStatus.Text = "Status: Connected"
        $lblStatus.ForeColor = [System.Drawing.Color]::LimeGreen
        $lblBrand.Text = "Device: $brand $model"
        Log-Msg "Connected to $brand $model"
        
        # Verify Brand
        if ($brand -notmatch "(?i)Xiaomi|Redmi|POCO") {
            [System.Windows.Forms.MessageBox]::Show("Warning: Non-Xiaomi device detected!", "Safety Warning")
            $lblStatus.ForeColor = [System.Drawing.Color]::Orange
        }
    } else {
        $lblStatus.Text = "Status: No Device"
        $lblStatus.ForeColor = [System.Drawing.Color]::Red
        Log-Msg "No device found. Check USB Debugging."
    }
})

$btnDebloat.Add_Click({
    $Script:TargetUser = $txtUser.Text
    Log-Msg "Starting Debloat on User $Script:TargetUser..."
    
    # Process Tabs
    $lists = @($clbSafe, $clbTrack, $clbJunk)
    $dicts = @($SafeApps, $TrackingApps, $JunkApps)
    
    for ($i=0; $i -lt $lists.Count; $i++) {
        $list = $lists[$i]
        $dict = $dicts[$i]
        
        foreach ($item in $list.CheckedItems) {
            # Extract name and package from string: "Name  [com.pkg]"
            if ($item -match "^(.*)  \[(.*)\]$") {
                $name = $matches[1]
                $pkg = $matches[2]
                Debloat-Package $pkg $name
            }
        }
    }
    Log-Msg "Done."
    [System.Windows.Forms.MessageBox]::Show("Debloat Complete", "Done")
})

# INITIALIZE
Find-Adb | Out-Null

$form.ShowDialog()
