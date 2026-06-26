# LLM 위키

`C:\supersonic\llm_wiki`는 원본 자료를 LLM이 읽고, 해석된 내용을 Markdown 위키와 웹 서비스로 누적하기 위한 작업 공간이다.

## 기본 구조

- `raw/` - 원본 자료 보관소. 원본 파일명은 추적성을 위해 유지한다.
- `wiki/` - 사람이 읽고 연결할 수 있는 Markdown 지식 위키.
- `wiki/resources/auto/` - 자동 등록된 리소스 페이지.
- `tools/` - 자동 등록, 감시, 웹 서비스 실행 스크립트.
- `web/` - 로컬 웹 서비스.
- `.obsidian/` - Obsidian Vault 설정.

## 빠른 시작

```powershell
cd C:\supersonic\llm_wiki
python tools/wiki_auto_index.py --no-log
powershell -ExecutionPolicy Bypass -File tools/start_wiki_watcher.ps1
powershell -ExecutionPolicy Bypass -File tools/start_web_service.ps1
```

웹 서비스가 실행되면 `.wiki_state\web.port`에 기록된 포트로 접속한다. 현재 기본 포트는 `http://localhost:4174`다.

## 새 자료 추가

1. 원본 파일을 `raw/sources/` 또는 `raw/attachments/`에 넣는다.
2. 감시기가 켜져 있으면 자동으로 `wiki/resources/auto/`에 리소스 페이지가 생긴다.
3. 변경된 리소스는 [[pending-ingest|심층 정리 대기열]]에 올라간다.
4. 중요한 자료는 LLM에게 원문 요약과 관련 페이지 갱신을 요청한다.

## 추천 요청문

```text
wiki/pending-ingest.md의 대기열을 보고 우선순위가 높은 리소스를 정리해줘.
원문 요약을 만들고, 관련 개념/대상 페이지를 갱신하고,
index.md와 log.md도 업데이트해줘.
판단이 필요한 항목은 TODO(user)로 남겨줘.
```

## 사용자가 판단해야 할 항목

- TODO(user): 웹 서비스를 개인 PC 전용, 내부망 공유, 사내 공개 중 어디까지 열지 정한다.
- TODO(user): 민감 자료의 업로드와 공개 기준을 정한다.
- TODO(user): 파일별 심층 정리 우선순위를 정한다.
