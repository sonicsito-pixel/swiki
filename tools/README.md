# 위키 자동화 도구

이 폴더는 원본 자료 등록, 감시기 실행, 웹 서비스 실행을 위한 스크립트를 담고 있다.

## 초기 등록

기존 원본 파일을 신규 대기 항목으로 보지 않고 기준선으로 등록할 때 사용한다.

```powershell
python tools/wiki_auto_index.py --baseline
```

## 수동 갱신

```powershell
python tools/wiki_auto_index.py --no-log
```

## 감시기 실행

```powershell
powershell -ExecutionPolicy Bypass -File tools/start_wiki_watcher.ps1
```

## 감시기 중지

```powershell
powershell -ExecutionPolicy Bypass -File tools/stop_wiki_watcher.ps1
```

## 웹 서비스 실행

```powershell
powershell -ExecutionPolicy Bypass -File tools/start_web_service.ps1
```

## 웹 서비스 중지

```powershell
powershell -ExecutionPolicy Bypass -File tools/stop_web_service.ps1
```

## 자동 갱신 대상

- `wiki/source-registry.md`
- `wiki/pending-ingest.md`
- `wiki/obsidian-home.md`
- `wiki/resources/auto/*.md`

자동화는 파일 등록과 변경 감지를 담당한다. 심층 요약, 개념 갱신, 모순 정리, 종합 판단은 LLM 정리 워크플로에서 수행한다.
