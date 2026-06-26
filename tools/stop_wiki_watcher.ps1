param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$pidFile = Join-Path $RepoRoot ".wiki_state\watcher.pid"

if (-not (Test-Path $pidFile)) {
    Write-Host "감시기 PID 파일을 찾을 수 없습니다."
    exit 0
}

$pidText = (Get-Content -Raw -LiteralPath $pidFile).Trim()
if ($pidText -notmatch '^\d+$') {
    Remove-Item -LiteralPath $pidFile -Force
    Write-Host "잘못된 감시기 PID 파일을 삭제했습니다."
    exit 0
}

$process = Get-Process -Id ([int]$pidText) -ErrorAction SilentlyContinue
if ($process) {
    Stop-Process -Id $process.Id -Force
    Write-Host "위키 감시기를 중지했습니다. PID: $($process.Id)"
} else {
    Write-Host "감시기 프로세스가 실행 중이 아니었습니다."
}

Remove-Item -LiteralPath $pidFile -Force
