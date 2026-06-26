param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [int]$DebounceSeconds = 3
)

$ErrorActionPreference = "Stop"

$pythonCandidates = @(
    (Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"),
    "python"
)

$python = $null
foreach ($candidate in $pythonCandidates) {
    try {
        $cmd = Get-Command $candidate -ErrorAction Stop
        $python = $cmd.Source
        break
    } catch {
        continue
    }
}

if (-not $python) {
    throw "Python 실행 파일을 찾을 수 없습니다."
}

$script = Join-Path $RepoRoot "tools\wiki_auto_index.py"
$paths = @(
    (Join-Path $RepoRoot "raw\sources"),
    (Join-Path $RepoRoot "raw\assets")
) | Where-Object { Test-Path $_ }

if (-not $paths) {
    throw "원본 자료 경로를 찾을 수 없습니다."
}

Write-Host "원본 자료를 감시합니다. 중지하려면 Ctrl+C를 누르세요."
Write-Host "저장소: $RepoRoot"

$global:LastRun = Get-Date "2000-01-01"

function Invoke-WikiIndex {
    $now = Get-Date
    if (($now - $global:LastRun).TotalSeconds -lt $DebounceSeconds) {
        return
    }
    $global:LastRun = $now
    Write-Host "[$($now.ToString('yyyy-MM-dd HH:mm:ss'))] 위키 리소스 목록을 갱신합니다..."
    & $python $script --no-log
}

$watchers = @()
foreach ($path in $paths) {
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = $path
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents = $true
    $watcher.NotifyFilter = [System.IO.NotifyFilters]'FileName, DirectoryName, LastWrite, Size'

    Register-ObjectEvent $watcher Created -Action { Invoke-WikiIndex } | Out-Null
    Register-ObjectEvent $watcher Changed -Action { Invoke-WikiIndex } | Out-Null
    Register-ObjectEvent $watcher Renamed -Action { Invoke-WikiIndex } | Out-Null
    Register-ObjectEvent $watcher Deleted -Action { Invoke-WikiIndex } | Out-Null
    $watchers += $watcher
}

Invoke-WikiIndex

while ($true) {
    Start-Sleep -Seconds 1
}
