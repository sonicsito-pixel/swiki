# Gemini CLI to Antigravity CLI Migration Guide

Gemini CLI가 Antigravity CLI로 전환됨에 따라, 기존의 프로젝트 컨텍스트와 메모리를 안전하게 이전하기 위한 가이드를 작성합니다.

## 1. 주요 변경 사항 (예상)
*   **루트 디렉토리:** `~/.gemini` → `~/.antigravitycli`
*   **컨텍스트 파일 명칭:** `GEMINI.md` → `ANTIGRAVITY.md`
*   **환경 변수 및 설정:** `.gemini` 폴더 내 설정들이 `.antigravitycli`로 이전되어야 함.

## 2. 이전 단계 (Manual Steps)

### 단계 1: 프로젝트 지시서(Instructions) 이전
현재 프로젝트 루트(`C:\supersonic`)에 있는 `GEMINI.md` 파일을 `ANTIGRAVITY.md`로 이름을 바꾸거나 복사합니다.
```bash
cp C:\supersonic\GEMINI.md C:\supersonic\ANTIGRAVITY.md
```

### 단계 2: 프로젝트 메모리(Memories) 이전
Gemini CLI가 저장한 '기억'들을 새로운 CLI 환경으로 복사합니다.
*   **원본:** `C:\Users\user\.gemini\tmp\supersonic\memory\`
*   **대상:** `C:\Users\user\.antigravitycli\tmp\supersonic\memory\` (디렉토리가 없으면 생성 필요)

### 단계 3: 글로벌 설정 및 메모리 이전
사용자 전역 설정(`~/.gemini/GEMINI.md`)을 새로운 위치로 이동합니다.
*   **원본:** `C:\Users\user\.gemini\GEMINI.md`
*   **대상:** `C:\Users\user\.antigravitycli\ANTIGRAVITY.md` (또는 해당 CLI의 글로벌 설정 파일)

## 3. 자동화 스크립트 (PowerShell)
다음 스크립트를 사용하여 간단하게 이전할 수 있습니다. (사용자 승인 후 실행 권장)

```powershell
# 1. 프로젝트 파일 복사
Copy-Item "C:\supersonic\GEMINI.md" "C:\supersonic\ANTIGRAVITY.md" -Force

# 2. 메모리 디렉토리 생성 및 복사
$newMemPath = "C:\Users\user\.antigravitycli\tmp\supersonic\memory"
if (!(Test-Path $newMemPath)) { New-Item -ItemType Directory -Path $newMemPath -Force }
Copy-Item "C:\Users\user\.gemini\tmp\supersonic\memory\*" $newMemPath -Recurse -Force

Write-Host "Migration to Antigravity CLI completed successfully."
```

## 4. 주의 사항
*   커스텀 스킬(`.skill`) 파일이 있다면 해당 파일들도 `~/.antigravitycli/skills` 폴더로 이동해야 합니다.
*   Antigravity CLI를 처음 실행할 때 새로운 세션 ID가 생성될 수 있으므로, 기존 작업 내역(History)은 파일 기반 산출물을 통해 확인해야 합니다.
