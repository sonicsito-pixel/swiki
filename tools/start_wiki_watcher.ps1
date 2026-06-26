param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$stateDir = Join-Path $RepoRoot ".wiki_state"
$pidFile = Join-Path $stateDir "watcher.pid"
$watchScript = Join-Path $RepoRoot "tools\watch_sources.ps1"

New-Item -ItemType Directory -Force -Path $stateDir | Out-Null

if (Test-Path $pidFile) {
    $existingPid = (Get-Content -Raw -LiteralPath $pidFile).Trim()
    if ($existingPid -match '^\d+$') {
        $existing = Get-Process -Id ([int]$existingPid) -ErrorAction SilentlyContinue
        if ($existing) {
            Write-Host "위키 감시기가 이미 실행 중입니다. PID: $existingPid"
            exit 0
        }
    }
}

$args = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", $watchScript,
    "-RepoRoot", $RepoRoot
)

$process = Start-Process -FilePath "powershell.exe" `
    -ArgumentList $args `
    -WorkingDirectory $RepoRoot `
    -WindowStyle Hidden `
    -PassThru

Set-Content -LiteralPath $pidFile -Value $process.Id -Encoding ASCII
Write-Host "위키 감시기를 시작했습니다. PID: $($process.Id)"
