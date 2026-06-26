# LLM 위키 웹 서비스

이 웹앱은 `wiki/` Markdown 파일을 읽어 검색, 대시보드, 자료 목록, 정리 대기열, 연결망, 업로드 화면을 제공한다.

## 실행

```powershell
cd C:\supersonic\llm_wiki
powershell -ExecutionPolicy Bypass -File tools/start_web_service.ps1
```

실행 포트는 `.wiki_state\web.port`에 기록된다.

## 중지

```powershell
powershell -ExecutionPolicy Bypass -File tools/stop_web_service.ps1
```

## 주요 기능

- 위키 페이지 검색과 본문 보기.
- 원본 자료 목록 보기.
- 심층 정리 대기열 보기.
- 위키 링크 기반 연결망 보기.
- 파일 업로드 후 자동 등록.

## 운영 메모

이 웹앱은 `wiki/` Markdown 파일을 기준 데이터로 유지한다. Obsidian과 함께 사용할 수 있고, 웹에서 업로드한 파일은 자동 등록 후 `wiki/pending-ingest.md`에 올라간다.
