param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [int]$Port = 4173
)

$ErrorActionPreference = "Stop"

$stateDir = Join-Path $RepoRoot ".wiki_state"
$pidFile = Join-Path $stateDir "web.pid"
$portFile = Join-Path $stateDir "web.port"
$serverScript = Join-Path $RepoRoot "web\server.mjs"

New-Item -ItemType Directory -Force -Path $stateDir | Out-Null

if (Test-Path $pidFile) {
    $existingPid = (Get-Content -Raw -LiteralPath $pidFile).Trim()
    if ($existingPid -match '^\d+$') {
        $existing = Get-Process -Id ([int]$existingPid) -ErrorAction SilentlyContinue
        if ($existing) {
            $existingPort = (Get-Content -Raw -LiteralPath $portFile -ErrorAction SilentlyContinue).Trim()
            Write-Host "LLM 위키 웹 서비스가 이미 실행 중입니다. PID: $existingPid 포트: $existingPort"
            exit 0
        }
    }
}

$chosenPort = $Port
while (Get-NetTCPConnection -LocalPort $chosenPort -State Listen -ErrorAction SilentlyContinue) {
    $chosenPort += 1
}

$node = (Get-Command "node" -ErrorAction Stop).Source
$args = @($serverScript, "--port", "$chosenPort")

$process = Start-Process -FilePath $node `
    -ArgumentList $args `
    -WorkingDirectory $RepoRoot `
    -WindowStyle Hidden `
    -PassThru

Set-Content -LiteralPath $pidFile -Value $process.Id -Encoding ASCII
Set-Content -LiteralPath $portFile -Value $chosenPort -Encoding ASCII
Write-Host "LLM 위키 웹 서비스를 시작했습니다. PID: $($process.Id) URL: http://localhost:$chosenPort"
