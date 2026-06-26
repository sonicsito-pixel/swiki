param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$pidFile = Join-Path $RepoRoot ".wiki_state\web.pid"
$portFile = Join-Path $RepoRoot ".wiki_state\web.port"

if (-not (Test-Path $pidFile)) {
    Write-Host "웹 서비스 PID 파일을 찾을 수 없습니다."
    exit 0
}

$pidText = (Get-Content -Raw -LiteralPath $pidFile).Trim()
if ($pidText -notmatch '^\d+$') {
    Remove-Item -LiteralPath $pidFile -Force
    Remove-Item -LiteralPath $portFile -Force -ErrorAction SilentlyContinue
    Write-Host "잘못된 웹 서비스 PID 파일을 삭제했습니다."
    exit 0
}

$process = Get-Process -Id ([int]$pidText) -ErrorAction SilentlyContinue
if ($process) {
    Stop-Process -Id $process.Id -Force
    Write-Host "LLM 위키 웹 서비스를 중지했습니다. PID: $($process.Id)"
} else {
    Write-Host "웹 서비스 프로세스가 실행 중이 아니었습니다."
}

Remove-Item -LiteralPath $pidFile -Force
Remove-Item -LiteralPath $portFile -Force -ErrorAction SilentlyContinue
