# 🌐 LLM Wiki 시스템 구축 및 운영 가이드라인 매뉴얼
> **신성통상 차세대 패션관리 시스템(FONE) PI 프로젝트 지식 관리 도구**

본 매뉴얼은 신성통상 IT기획팀 및 프로젝트 팀원들이 프로젝트 관련 원본 리소스(Excel, HTML, PDF 등)를 체계적으로 요약 및 자산화하고, 이를 유기적인 지식 구조망(Knowledge Graph)으로 탐색할 수 있는 **경량 LLM Wiki 포털 시스템**을 밑바닥부터 직접 구축하고 커스텀하는 방법론을 가이드합니다.

---

## 📌 1. 시스템 개념 및 아키텍처 개요

LLM Wiki 시스템은 **단절된 업무 자료를 상호 연결된 지식 자산으로 전환**하기 위해 설계되었습니다. 원본 자료(Raw Data)를 마크다운 기반의 요약 문서로 생성한 뒤, 문서 간의 양방향 연결 정보([[Link]])를 자동으로 추출해 시각적이고 인터랙티브한 그래프 및 통합 검색 포털을 제공합니다.

![LLM Wiki 시스템 아키텍처 개념도](C:/Users/user/.gemini/antigravity-cli/brain/9abfb6e7-2ddd-4f15-acee-3b7e5e3e4807/llm_wiki_architecture_1782439566689.jpg)

### ⚙️ 핵심 아키텍처 흐름 (Mermaid)

```mermaid
flowchart TD
    subgraph Raw Data Ingestion
        A[Excel / PPTX / PDF / HTML 원본] -->|텍스트/표 파싱 및 요약| B(Raw Sources)
    end

    subgraph Knowledge Base Repository
        B -->|PI 4단계 As-Is/To-Be 표준 변환| C[Obsidian 지식 카드 .md]
        C -->|개념 concept / 대상 entity / 질문 question| D{지식 축적 저장소 wiki/}
    end

    subgraph Auto Indexing Pipeline
        D -->|wiki_auto_index.py 실행| E[양방향 링크 [[Link]] 및 관계 추출]
        E -->|인덱싱 상태 갱신| F[(.wiki_state/metadata.json)]
    end

    subgraph Web Portal Service
        F -->|Node.js server.mjs API| G[HTML5 Single Page Application]
        G -->|Mermaid.js 엔진| H[동적 다이어그램 실시간 렌더링]
        G -->|HTML5 Canvas 포스 레이아웃| I[인터랙티브 인사이트 연결망]
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style F fill:#bfb,stroke:#333,stroke-width:2px
    style G fill:#fdd,stroke:#333,stroke-width:2px
```

---

## 📂 2. 디렉터리 구성 및 개발 환경 설정

시스템은 외부 무거운 라이브러리 프레임워크(React, Next.js 등)에 의존하지 않고, **Vanilla JS, HTML5, CSS3 및 경량 Node.js 내장 모듈**만으로 가볍고 빠르게 동작하도록 설계되어 로컬 PC에서도 제한 없이 구동 가능합니다.

### 📁 디렉터리 구조 트리

```text
llm_wiki/
├── raw/                         # [Raw] 분석 대상 원본 파일 보관소
│   ├── sources/                 # 엑셀, PPTX, PDF, HTML 원문 원본
│   └── assets/                  # 이미지, 참고 도표 등 리소스
├── wiki/                        # [Knowledge Base] Obsidian 호환 마크다운 지식 카드
│   ├── concepts/                # 주요 핵심 개념 카드 (예: plm-fone-integration.md)
│   ├── entities/                # 분석 대상 시스템/조직 카드 (예: store-master.md)
│   ├── sources/                 # 4단계 PI 표준 형식을 만족하는 원문 요약 카드
│   └── questions/               # 의사결정 및 현업 질문 카드
├── .wiki_state/                 # [System State] 자동 빌드된 인덱스 및 설정 저장소
│   ├── metadata.json            # 자동 인덱서가 생성하는 전체 문서 관계 DB (Git 추적 제외)
│   └── web.port                 # 웹 서비스 기동 포트 정보 기록 파일
├── tools/                       # [Scripts] 자동화 파이프라인 스크립트 폴더
│   ├── wiki_auto_index.py       # 지식 카드 파싱 및 링크 인덱스 생성 코어 스크립트
│   ├── start_web_service.ps1    # 웹 서비스 백그라운드 구동 파워쉘
│   └── watch_sources.ps1        # 마크다운 변경 실시간 감시 파워쉘
├── web/                         # [Web Application] 시각화 포털 소스코드
│   ├── server.mjs               # Node.js 내장 http 모듈 기반 초경량 API/정적 웹 서버
│   └── public/                  # 프론트엔드 정적 리소스 폴더
│       ├── index.html           # 메인 레이아웃 및 뷰
│       ├── app.js               # 마크다운 렌더러, Canvas 그래프, API 통신 엔진
│       └── styles.css           # 모던 테크 룩앤필 바닐라 CSS
└── start_wiki.bat               # [One-Click Launcher] 전체 시스템 기동 배치 파일
```

### 🛠️ 개발 환경 요구사항
* **Python 3.8 이상**: 문서 파싱 및 링크 관계 분석 인덱서 구동용
* **Node.js 16.x 이상**: 로컬 웹 포털 및 API 서버 구동용
* **Obsidian (권장)**: 마크다운 편집 및 로컬 양방향 링크 관리 인터페이스용

---

## ⚙️ 3. 핵심 모듈별 구축 가이드

### 1단계: Python 기반 양방향 링크 인덱서 (`tools/wiki_auto_index.py`)
이 모듈은 Obsidian의 양방향 링크 문법인 `[[문서명]]` 패턴을 정규식으로 탐색하여 지식 노드(Node)와 연결 엣지(Edge) 정보를 정밀 추출하고, 이를 프론트엔드가 즉시 렌더링할 수 있는 JSON 구조로 병합하여 `.wiki_state/metadata.json`에 저장합니다.

> [!TIP]
> **인덱서의 핵심 메커니즘**
> 1. `wiki/` 폴더 내의 모든 `.md` 파일을 순회하며 프론트메터(Frontmatter) 정보 추출.
> 2. 정규식 `\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]`을 이용해 본문 내 연결된 지식 링크를 모두 수집.
> 3. 이를 노드 리스트와 엣지 리스트로 구조화하여 JSON 파일로 저장.

```python
# tools/wiki_auto_index.py 핵심 요약 예시
import os
import re
import json

WIKI_DIR = "./wiki"
OUTPUT_FILE = "./.wiki_state/metadata.json"
LINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")

def build_index():
    nodes = []
    edges = []
    
    # 1. wiki/ 하위 폴더 순회하며 markdown 파일 스캔
    for root, dirs, files in os.walk(WIKI_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, WIKI_DIR).replace("\\", "/")
                
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 정규식 패턴으로 양방향 링크 추출
                matches = LINK_PATTERN.findall(content)
                for match in matches:
                    target_link = match[0].strip()
                    edges.append({
                        "source": rel_path,
                        "target": target_link
                    })
                    
                nodes.append({
                    "path": rel_path,
                    "title": file.replace(".md", ""),
                    "type": root.split(os.sep)[-1]  # 폴더명을 타입으로 지정 (concepts, entities 등)
                })
                
    # 2. 메타데이터 파일 쓰기
    state = {"nodes": nodes, "edges": edges}
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    build_index()
```

---

### 2단계: Node.js 초경량 API 및 파일 서버 (`web/server.mjs`)
외부 Express 라이브러리를 배제하고 Node.js 내장 `node:http`와 `node:fs/promises`를 사용하여 배포 및 기동 오버헤드를 제로화했습니다.

> [!IMPORTANT]
> **로컬 원본 파일 직접 열기 기능 (Security & OS Bridge)**
> 웹 브라우저 샌드박스의 한계를 넘어서기 위해, 사용자가 웹 화면에서 "로컬 파일 열기" 버튼을 누르면 Node.js 백엔드가 OS의 기본 열기 어플리케이션(Excel, Acrobat, Web Browser 등)으로 로컬 raw 파일을 직접 띄워주는 API(`openLocalFile`)를 구현했습니다.

```javascript
// web/server.mjs 내의 로컬 파일 브릿지 API 핵심 로직
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";

async function openLocalFile(req, res) {
  const payload = await parseJsonBody(req);
  const sourcePath = String(payload.sourcePath || "");
  
  if (!sourcePath.startsWith("raw/")) {
    throw new Error("raw 폴더 안의 파일만 열 수 있습니다.");
  }
  
  const fullPath = resolve(repoRoot, sourcePath);
  if (!existsSync(fullPath)) {
    throw new Error("로컬 파일을 찾을 수 없습니다.");
  }

  // OS별 기본 프로그램 기동 커맨드 분기
  const openers = {
    win32: ["rundll32.exe", ["url.dll,FileProtocolHandler", fullPath]],
    darwin: ["open", [fullPath]],
    linux: ["xdg-open", [fullPath]],
  };
  const [command, args] = openers[process.platform] || openers.win32;
  
  const child = spawn(command, args, {
    detached: true,
    stdio: "ignore",
    windowsHide: true,
  });
  child.unref();
  
  return { opened: true, sourcePath };
}
```

---

### 3단계: 프론트엔드 다이어그램 엔진 이식 (Mermaid.js)
마크다운 내에 포함된 구조적 순서도 및 비즈니스 프로세스 다이어그램(` ```mermaid `)을 웹 브라우저에서 그래픽 형태로 정상 렌더링하기 위해 프론트엔드를 확장 연동합니다.

#### ① [index.html](file:///C:/supersonic/llm_wiki/web/public/index.html) 설정
HTML `<head>` 영역에 Mermaid CDN을 포함시킵니다.
```html
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
```

#### ② [app.js](file:///C:/supersonic/llm_wiki/web/public/app.js) 마크다운 파서 업데이트
기존 커스텀 `renderMarkdown` 내의 코드 블록 검출 루프를 개선하여 `mermaid` 타입 검출 시 `<div class="mermaid">` 노드로 변환하게 만듭니다.
```javascript
// app.js - renderMarkdown 내 분기 로직
if (line.startsWith("```")) {
  flushList();
  flushTable();
  if (code) {
    if (code === "mermaid") {
      // Mermaid 용 전용 렌더 컨테이너로 래핑
      html.push(`<div class="mermaid">${escapeHtml(codeLines.join("\n"))}</div>`);
    } else {
      html.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
    }
    codeLines = [];
    code = false;
  } else {
    const type = line.slice(3).trim().toLowerCase();
    code = type === "mermaid" ? "mermaid" : "normal";
  }
  continue;
}
```

#### ③ [app.js](file:///C:/supersonic/llm_wiki/web/public/app.js) 로딩 완료 라이프사이클에 렌더 트리거 추가
마크다운이 화면의 `#docBody` 영역에 로드 및 바인딩 완료된 직후, 실시간 컴파일러를 실행하여 SVG 그래픽으로 동적 변환합니다.
```javascript
// app.js - loadPage 함수의 본문 삽입부 하단
$("docBody").innerHTML = renderMarkdown(page.markdown);

if (typeof mermaid !== 'undefined') {
  try {
    // 렌더러가 DOM을 탐색해 .mermaid 클래스 요소를 그래픽 SVG로 변환
    if (typeof mermaid.run === 'function') {
      await mermaid.run({ nodes: document.querySelectorAll('.mermaid') });
    } else if (typeof mermaid.init === 'function') {
      mermaid.init(undefined, document.querySelectorAll('.mermaid'));
    }
  } catch (error) {
    console.error("Mermaid 렌더링 실패:", error);
  }
}
```

---

### 4단계: HTML5 Canvas 기반 인터랙티브 연결망 시각화 (`app.js`)
문서 간 유기적 연결 강도를 2D 물리 포스 레이아웃 알고리즘으로 모델링하여 시각적으로 구현하고 마우스 이벤트를 접목해 고도의 세련된 UI를 달성했습니다.

> [!NOTE]
> **인터랙티브 기능의 특장점**
> * **Hover Action**: 특정 지식 노드에 마우스 커서를 올리면 연관된 이웃 노드들과 연결 경로선만 강조 표시(`Highlighted`)되고, 상관없는 나머지 문서 노드들은 반투명화(`Dimmed`) 처리되어 시각적 복잡도를 완전히 낮춥니다.
> * **Click Action**: 캔버스 내부의 특정 노드 구체를 마우스 클릭 시, 해당 문서로 즉시 이동 및 로드(`Wiki View`)하여 지식 탐색 효율성을 극대화합니다.
> * **Grid & Shadow**: 격자 그리드 배경 렌더링과 노드의 3D 부드러운 그림자 효과로 모던한 대시보드 그래픽 디자인을 연출합니다.

```javascript
// app.js - HTML5 Canvas 마우스 오버 감지 및 하이라이트 구현 로직
let hoveredNode = null;
let canvasNodes = []; // buildGraphLayout 연산 후 좌표가 할당된 노드 배열

function handleGraphMouseMove(event) {
  const canvas = $("graphCanvas");
  if (!canvas || !canvasNodes.length) return;
  const rect = canvas.getBoundingClientRect();
  
  // 마우스의 캔버스 상대 좌표 계산
  const mx = event.clientX - rect.left;
  const my = event.clientY - rect.top;
  
  let found = null;
  // 클릭 범위 판정을 위해 충돌체 반경(radius)에 보정치 5px 추가 적용
  for (let i = canvasNodes.length - 1; i >= 0; i--) {
    const node = canvasNodes[i];
    const dx = mx - node.x;
    const dy = my - node.y;
    const dist = Math.hypot(dx, dy);
    if (dist <= (node.radius || 10) + 5) {
      found = node;
      break;
    }
  }
  
  if (found !== hoveredNode) {
    hoveredNode = found;
    canvas.style.cursor = hoveredNode ? "pointer" : "default";
    drawGraph(); // 오버 상태가 변하면 하이라이트 상태를 반영하여 재도화
  }
}
```

---

## 🚀 4. 원클릭 시스템 기동 및 운영 가이드

팀원들이 복잡한 콘솔 명령어나 프로세스 종료 과정을 의식하지 않고 원클릭으로 구동할 수 있도록 실행 자동화 환경을 함께 구성합니다.

### 1) 통합 실행 배치 스크립트 (`start_wiki.bat`)
```bat
@echo off
title LLM Wiki Launcher
cd /d "%~dp0"

echo [1/3] Running wiki auto indexing...
python tools\wiki_auto_index.py --no-log

echo.
echo [2/3] Starting wiki watcher (background)...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\start_wiki_watcher.ps1

echo.
echo [3/3] Starting LLM wiki web service (background)...
powershell -NoProfile -ExecutionPolicy Bypass -File tools\start_web_service.ps1

echo.
echo ====================================================
echo  기동 완료! 브라우저에서 아래 포트로 접속하세요.
echo  - Port Check: .wiki_state\web.port 파일을 확인하세요
echo ====================================================
echo.
pause
```

### 2) 백그라운드 구동 파워쉘 (`tools/start_web_service.ps1`)
이 스크립트는 이미 실행 중인 프로세스가 있으면 알리고 없으면 사용 가능한 임의 포트(기본 4173)를 찾아 Node 프로세스를 윈도우 뒤편으로 숨겨(`-WindowStyle Hidden`) 안전히 구동합니다.

```powershell
param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [int]$Port = 4173
)

$ErrorActionPreference = "Stop"
$stateDir = Join-Path $RepoRoot ".wiki_state"
$pidFile = Join-Path $stateDir "web.pid"
$portFile = Join-Path $stateDir "web.port"
$serverScript = Join-Path $RepoRoot "web\server.mjs"

# 포트 중복 충돌 방지 탐색 루프
$chosenPort = $Port
while (Get-NetTCPConnection -LocalPort $chosenPort -State Listen -ErrorAction SilentlyContinue) {
    $chosenPort += 1
}

$node = (Get-Command "node" -ErrorAction Stop).Source
$args = @($serverScript, "--port", "$chosenPort")

# 백그라운드로 Node 프로세스 기동
$process = Start-Process -FilePath $node `
    -ArgumentList $args `
    -WorkingDirectory $RepoRoot `
    -WindowStyle Hidden `
    -PassThru

Set-Content -LiteralPath $pidFile -Value $process.Id -Encoding ASCII
Set-Content -LiteralPath $portFile -Value $chosenPort -Encoding ASCII
Write-Host "LLM 위키 서버 기동 완료. PID: $($process.Id) Port: $chosenPort"
```

---

## 📝 5. 지식 자산 등록 및 관리 규칙 (Rules)

팀원들과 지식 위키를 협업 및 증설해 갈 때 다음의 표준 프로세스 규칙을 준수해야 지식 그래프와 다이어그램이 망가지지 않고 유지됩니다.

1. **4단계 PI 표준 프레임워크 준수 (지식 카드 포맷)**
   모든 원문 요약 문서는 다음 형식을 갖춰 생성되어야 합니다.
   * **As-Is (현행)**: 수기 작업 및 레거시 시스템 제약 실태.
   * **To-Be (목표)**: 디지털 전환 후의 고효율 업무 시나리오.
   * **Gap (격차)**: 데이터의 단절 및 한계점 상세 원인 분석.
   * **해결방안 (RFP)**: 제안요청서에 직접 반영할 수 있는 시스템 요건.
2. **이름 규칙 및 폴더 분류**
   * 개념 정의 -> `wiki/concepts/` (예: `master-data-governance.md`)
   * 시스템/대상 -> `wiki/entities/` (예: `centric-plm.md`)
   * 문서 원본 요약 -> `wiki/sources/` (예: `sales-mgmt-asis.md`)
3. **양방향 링크 활성화**
   * 지식 카드 본문 작성 시 타 문서의 핵심 개념이나 시스템을 언급할 때는 반드시 `[[개념파일명]]` 혹은 `[[centric-plm|PLM 연동]]` 형식을 활용하여 양방향 링크를 형성해야 합니다. 인덱서가 이를 추적해 지식 지도(인사이트 연결망)에 노드를 자동 연결합니다.
4. **다이어그램 삽입**
   * 업무 프로세스 맵이나 인터랙션 시퀀스는 마크다운 코드 블록 ` ```mermaid ` 를 사용해 텍스트 다이어그램으로 작성하면, 포털 웹에서 자동으로 실시간 그래픽 렌더링을 처리합니다.

---
> **IT기획팀 연락망 및 기술 지원**: IT기획팀 (내선 1024) / 프로젝트 매니저 김남형 과장
