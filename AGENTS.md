# LLM 위키 작업 지침

이 저장소는 원본 자료를 Markdown 위키와 웹 서비스로 정리하는 지식 운영 공간이다.

## 작업 원칙

- 원본 파일은 `raw/`에 그대로 보관한다.
- 해석된 지식은 `wiki/`의 원문 요약, 개념, 대상, 질문, 목차, 작업 기록에 반영한다.
- 원본 파일명과 FONE/PLM/WMS/POS 같은 시스템 약어는 추적성을 위해 유지한다.
- 사용자의 판단이 필요한 항목은 반드시 `TODO(user)`로 남긴다.

## 자동 등록 워크플로

```powershell
python tools/wiki_auto_index.py --no-log
powershell -ExecutionPolicy Bypass -File tools/start_wiki_watcher.ps1
```

자동 등록은 다음 파일을 갱신한다.

- `wiki/source-registry.md`: 원본 자료 목록.
- `wiki/pending-ingest.md`: 새로 추가되거나 변경된 리소스의 심층 정리 대기열.
- `wiki/obsidian-home.md`: Obsidian 시작 페이지.
- `wiki/resources/auto/*.md`: 리소스별 자동 페이지.

자동 등록은 심층 요약을 대체하지 않는다. `pending-ingest.md`에 올라온 항목은 이후 LLM 정리 워크플로를 통해 원문 요약, 개념/대상 페이지, index, log에 반영한다.

## 심층 정리 워크플로

1. 원본 파일과 자동 리소스 페이지를 확인한다.
2. `wiki/sources/`에 원문 요약을 만든다.
3. 관련 `wiki/concepts/`, `wiki/entities/`, `wiki/questions/` 페이지를 만들거나 갱신한다.
4. `wiki/index.md`와 `wiki/log.md`를 갱신한다.
5. 판단이 필요한 항목은 `TODO(user)`로 남긴다.

## 웹 서비스

```powershell
powershell -ExecutionPolicy Bypass -File tools/start_web_service.ps1
```

웹 서비스는 `wiki/` Markdown 파일을 기준 데이터로 읽는다. 웹에서 업로드한 파일도 `raw/uploads/`에 저장되고 자동 등록된다.

## 점검 기준

- 깨진 위키 링크가 없는지 확인한다.
- 깨진 물음표 표기처럼 인코딩이 손상된 문구가 없는지 확인한다.
- 자동 생성 파일과 수동 문서가 같은 한국어 라벨을 사용하는지 확인한다.
- 충돌 내용은 `모순/주의` 섹션에 기록한다.
