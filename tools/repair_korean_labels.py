"""수동 위키 문서와 안내 문서의 깨진 한국어 라벨을 복구한다."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


FILES: dict[str, str] = {
    "wiki/index.md": """---
type: index
updated: 2026-06-17
---
# 목차

이 파일은 위키의 전체 목차다. 새 자료를 정리하거나 중요한 페이지를 만들 때마다 갱신한다.

## 전체 개요

- [[overview|전체 개요]] - 이 위키의 현재 목적, 범위, 핵심 질문.

## 원문 요약

- [[sample-source-summary|샘플 원문 요약]] - LLM Wiki 아이디어 문서에 대한 샘플 요약.
- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]] - `ASIS분석자료(FONE)` 폴더 자료에 대한 1차 통합 요약.

## 개념

- [[persistent-knowledge-wiki|지속형 지식 위키]] - 원문 자료를 LLM이 지속적으로 축적되는 위키로 변환하는 패턴.
- [[fone-as-is-analysis|FONE 현행 분석]] - FONE/FA-ONE 현행 분석에서 반복적으로 드러난 문제 구조.
- [[master-data-governance|기준정보 관리 체계]] - 브랜드, 칼라, 사이즈, 매장, 거래처 등 기준정보 표준화와 변경관리.
- [[plm-fone-integration|PLM-FONE 연계]] - 센트릭 PLM과 FONE/FA-ONE 상품기획 데이터 연계 방향.
- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]] - WMS와 FONE/FA-ONE 사이의 창고, 수불, 재고 정합성 이슈.
- [[sales-settlement-automation|영업관리 정산 자동화]] - 영업관리, 매출확정, 정산, EDI/VAN 대사 자동화 과제.

## 대상

- [[fa-one-fone|FA-ONE/FONE]] - 분석 대상 패션관리 시스템.
- [[centric-plm|센트릭 PLM]] - 상품기획/PLM 통합 후보 솔루션.
- [[wms|WMS]] - 창고관리 시스템.
- [[obsidian|옵시디언]] - Markdown 위키 탐색과 그래프 시각화를 위한 도구.

## 질문

- [[how-should-this-wiki-start|이 위키를 어떻게 시작할까?]] - 이 위키를 실제로 시작하기 위한 초기 판단 목록.
- [[fone-next-decisions|FONE 다음 의사결정]] - FONE/FA-ONE 분석을 다음 단계로 진행하기 위해 사용자가 정해야 할 항목.

## 자동화

- [[source-registry|원본 자료 목록]] - `raw/` 리소스 자동 등록 현황.
- [[pending-ingest|심층 정리 대기열]] - 새로 추가되거나 변경된 리소스의 심층 정리 대기열.
- [[obsidian-home|옵시디언 홈]] - Obsidian용 시작 페이지.

## 사용자 결정 필요

- TODO(user): `ASIS분석자료(FONE)` 중 파일별 심층 정리 우선순위를 정한다.
- TODO(user): FONE/FA-ONE, 센트릭 PLM, WMS의 공식 명칭과 범위를 확정한다.
- TODO(user): 웹 서비스 공개 범위와 인증 방식을 정한다.
""",
    "wiki/overview.md": """---
type: overview
updated: 2026-06-17
---
# 전체 개요

이 위키는 원본 자료를 단순 보관하는 공간이 아니라, LLM이 읽고 정리한 내용을 누적하는 지식 운영 공간이다. 현재는 FONE/FA-ONE 현행 분석 자료와 LLM Wiki 운영 방식이 주요 범위다.

## 현재 목적

- 원본 파일을 `raw/`에 보관하고, 자동 등록된 리소스 페이지를 만든다.
- 중요한 자료는 원문 요약, 개념 페이지, 대상 페이지, 질문 페이지로 나누어 재사용 가능한 지식으로 정리한다.
- Obsidian에서는 링크와 그래프를 중심으로 탐색하고, 웹 서비스에서는 검색과 현황 파악을 빠르게 한다.

## 현재 범위

- `ASIS분석자료(FONE)` 폴더의 1차 등록과 통합 요약.
- FONE/FA-ONE, 센트릭 PLM, WMS, 영업관리 정산, 기준정보 관리 등 핵심 개념 정리.
- 새 파일을 자동으로 등록하고 심층 정리 대기열에 올리는 자동화.

## 운영 원칙

- 원본 파일명과 시스템 약어는 추적성을 위해 유지한다.
- 사용자의 판단이 필요한 항목은 `TODO(user)`로 남긴다.
- 자동 등록은 색인과 대기열 생성까지 담당하고, 해석과 종합은 별도 정리 작업으로 수행한다.

## 다음 작업

- TODO(user): PPT/PDF/Excel 자료를 어느 수준까지 파일별로 심층 정리할지 정한다.
- TODO(user): 웹 서비스를 개인용, 내부망용, 사내 공개용 중 어떤 방식으로 운영할지 정한다.
""",
    "wiki/concepts/README.md": """# 개념

이 폴더는 여러 원본 자료에서 반복적으로 등장하는 개념, 업무 과제, 분석 관점을 정리한다.
""",
    "wiki/entities/README.md": """# 대상

이 폴더는 시스템, 조직, 제품, 도구처럼 위키에서 반복적으로 언급되는 대상을 정리한다.
""",
    "wiki/questions/README.md": """# 질문

이 폴더는 사용자가 판단해야 할 항목, 아직 결론이 나지 않은 논점, 다음 분석 질문을 정리한다.
""",
    "wiki/sources/README.md": """# 원문 요약

이 폴더는 원본 자료나 원본 자료 묶음을 읽고 만든 요약 페이지를 보관한다.
""",
    "wiki/concepts/fone-as-is-analysis.md": """---
type: concept
title: FONE 현행 분석
aliases:
  - FONE AS-IS 분석
  - FA-ONE 현행 분석
tags:
  - FONE
  - 현행분석
  - 업무분석
updated: 2026-06-17
---
# FONE 현행 분석

## 정의

FONE 현행 분석은 FONE/FA-ONE 패션관리시스템의 현행 업무, 데이터, 시스템 연계, 현업 불편사항을 정리해 차세대 TO-BE 설계의 근거로 만드는 분석 작업이다.

## 현재 이해

- 분석 자료는 상품기획, 영업관리, 물류/WMS, POS, 기준정보, 데이터 이관, 정산 업무를 폭넓게 다룬다.
- 반복적으로 등장하는 핵심 문제는 기준정보 중복, 시스템 간 연계 부족, 수기 엑셀 보정, 코드/명칭 불일치, 예외 처리 방식의 비표준화다.
- FONE/FA-ONE은 여러 업무의 중심 시스템이지만 PLM, WMS, POS, AIS, VAN/EDI와의 역할 경계가 명확해야 한다.

## 반복되는 이슈 패턴

- 기준정보가 여러 시스템에서 중복 관리되어 정합성 문제가 생긴다.
- 영업/정산 업무에서 대사와 확정 절차가 수작업에 의존한다.
- 상품기획과 작업지시 데이터가 PLM과 FONE 사이에서 표준화되지 않았다.
- WMS와 FONE 간 입출고, 반품, 재고 조정의 기준 시점과 상태 값이 명확하지 않다.

## 근거

- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]
- [[fa-one-fone|FA-ONE/FONE]]

## 관련 페이지

- [[master-data-governance|기준정보 관리 체계]]
- [[plm-fone-integration|PLM-FONE 연계]]
- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]]
- [[sales-settlement-automation|영업관리 정산 자동화]]

## 열린 질문

- TODO(user): 현행 분석의 최종 산출물을 업무별 이슈 목록, TO-BE 요구사항, 전환 로드맵 중 어디에 맞출지 정한다.
- TODO(user): 파일별 심층 정리 우선순위를 정한다.
""",
    "wiki/concepts/master-data-governance.md": """---
type: concept
title: 기준정보 관리 체계
aliases:
  - 마스터 데이터 관리
  - Master Data Governance
tags:
  - FONE
  - 기준정보
  - 데이터관리
updated: 2026-06-17
---
# 기준정보 관리 체계

## 정의

기준정보 관리 체계는 브랜드, 서브브랜드, 칼라, 사이즈, 품종, 거래처, 매장 같은 기준정보를 표준화하고, 생성/변경/폐기/이력 관리를 통제하는 체계다.

## 현재 이해

- FONE/FA-ONE 분석 자료에서는 기준정보가 여러 업무 영역의 공통 병목으로 등장한다.
- 기준정보가 PLM, FONE, WMS, POS, AIS 등에서 서로 다르게 관리되면 연계 오류와 수기 보정이 증가한다.
- 코드 체계와 명칭 체계, 관리 주체, 승인 절차를 함께 정의해야 한다.

## 주요 관리 대상

- 상품, 스타일, 품번, 컬러, 사이즈, 시즌, 브랜드, 품종.
- 매장, 창고, 거래처, 고객, 유통망.
- 수수료, 공제, 정산 기준, 회계 전표 기준.

## 필요 결정

- 기준정보별 기준 시스템을 정한다.
- 생성/변경 승인 권한과 이력 관리 방식을 정한다.
- 외부 시스템으로 배포되는 기준정보의 주기와 방식 API, 배치, 파일 연계를 정한다.

## 근거

- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]
- [[fone-as-is-analysis|FONE 현행 분석]]

## 관련 페이지

- [[plm-fone-integration|PLM-FONE 연계]]
- [[sales-settlement-automation|영업관리 정산 자동화]]

## 열린 질문

- TODO(user): 기준정보별 공식 기준 시스템을 확정한다.
- TODO(user): 코드 변경 시 과거 데이터 소급 반영 여부를 정한다.
""",
    "wiki/concepts/plm-fone-integration.md": """---
type: concept
title: PLM-FONE 연계
aliases:
  - 센트릭 PLM 연계
  - PLM FONE Integration
tags:
  - FONE
  - PLM
  - 상품기획
updated: 2026-06-17
---
# PLM-FONE 연계

## 정의

PLM-FONE 연계는 센트릭 PLM 같은 상품기획 시스템과 FONE/FA-ONE의 제품코드, 작업지시서, 스타일, 자재, 사이즈, 원가, 생산/소싱 데이터를 연결하는 과제다.

## 현재 이해

자료 기준으로 센트릭 PLM은 상품기획 데이터의 단일 기준 정보원 후보로 등장한다. 현재는 FONE의 작업지시서와 PLM 문서 또는 차트 간 항목 매핑 분석 수준이며, 단기적으로는 Excel Import/Export 기반 연계 검토, 장기적으로는 ERP/FONE 직접 연동이 언급된다.

## 반복되는 이슈

- 상품기획 데이터와 작업지시 데이터의 입력 위치가 명확하지 않다.
- PLM에서 관리할 항목과 FONE에서 관리할 항목의 경계가 필요하다.
- 센트릭 PLM 일부 기능은 검토/도입되었지만 FONE/FA-ONE과 유기적 연계가 부족한 상태로 보인다.

## 필요 결정

- 센트릭 PLM을 상품기획 데이터 기준 시스템으로 둘지 결정한다.
- FONE으로 전달할 데이터 범위와 전달 시점을 정한다.
- 엑셀 기반 임시 연계와 API/배치 기반 정식 연계의 단계별 계획을 정한다.

## 근거

- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]
- [[centric-plm|센트릭 PLM]]

## 관련 페이지

- [[fone-as-is-analysis|FONE 현행 분석]]
- [[master-data-governance|기준정보 관리 체계]]

## 열린 질문

- TODO(user): PLM에서 FONE으로 내려보낼 필수 항목 목록을 확정한다.
- TODO(user): 작업지시서 생성 주체를 PLM과 FONE 중 어디로 둘지 정한다.
""",
    "wiki/concepts/wms-fone-inventory-integration.md": """---
type: concept
title: WMS-FONE 재고 연계
aliases:
  - WMS FONE 재고 인터페이스
  - WMS-FONE Inventory Integration
tags:
  - FONE
  - WMS
  - 재고
updated: 2026-06-17
---
# WMS-FONE 재고 연계

## 정의

WMS-FONE 재고 연계는 WMS와 FONE/FA-ONE 사이의 입고, 출고, 반품, 센터간 이동, 매장 수불, 창고 수불, 재고 조정 데이터를 일관되게 연결하는 과제다.

## 반복되는 이슈

- 창고와 매장의 재고 기준 시점이 다를 수 있다.
- 입고, 출고, 반품, 이동, 조정의 상태 값과 확정 시점이 시스템별로 다르다.
- WMS 처리 결과가 FONE의 영업/정산 업무와 정확히 연결되어야 한다.
- 실물 물류 흐름과 장부 재고 흐름이 어긋날 때 예외 처리 기준이 필요하다.

## 필요 결정

- 재고 기준 시스템과 조회 기준 시점을 정한다.
- 인터페이스 실패 시 재처리 기준과 책임 주체를 정한다.
- 물류 이벤트가 매출, 정산, 회계로 이어지는 흐름을 정의한다.

## 근거

- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]
- [[wms|WMS]]

## 관련 페이지

- [[fone-as-is-analysis|FONE 현행 분석]]
- [[sales-settlement-automation|영업관리 정산 자동화]]

## 열린 질문

- TODO(user): FONE과 WMS 중 재고 조회의 공식 기준 시스템을 정한다.
- TODO(user): 반품과 재고 조정의 승인 흐름을 확정한다.
""",
    "wiki/concepts/sales-settlement-automation.md": """---
type: concept
title: 영업관리 정산 자동화
aliases:
  - 매출 정산 자동화
  - Sales Settlement Automation
tags:
  - FONE
  - 영업관리
  - 정산
updated: 2026-06-17
---
# 영업관리 정산 자동화

## 정의

영업관리 정산 자동화는 영업관리 영역의 매출 확정, 유통망 정산, VAN/POS/EDI 대사, 수수료/공제/채권 관리, AIS 전표 전송을 수기 중심에서 자동 연계와 예외 관리 중심으로 전환하는 과제다.

## 반복되는 이슈

- POS, VAN, EDI, FONE 사이의 매출 데이터 대사가 수작업에 의존한다.
- 정산 기준과 수수료, 공제 항목이 복잡해 예외 처리가 많다.
- 확정된 매출과 회계 전표 전송 시점의 정합성이 중요하다.
- 유통망별 특수 조건이 표준 프로세스와 충돌할 수 있다.

## 필요 결정

- 매출 확정의 기준 데이터와 확정 시점을 정한다.
- 자동 대사 실패 시 예외 큐와 승인 절차를 정한다.
- AIS 전표 전송 범위와 재처리 기준을 정한다.

## 근거

- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]
- [[fa-one-fone|FA-ONE/FONE]]

## 관련 페이지

- [[fone-as-is-analysis|FONE 현행 분석]]
- [[master-data-governance|기준정보 관리 체계]]
- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]]

## 열린 질문

- TODO(user): 정산 자동화에서 우선 개선할 유통 채널을 정한다.
- TODO(user): 자동 대사 허용 오차와 수기 승인 기준을 정한다.
""",
    "wiki/concepts/persistent-knowledge-wiki.md": """---
type: concept
title: 지속형 지식 위키
aliases:
  - LLM Wiki
  - Persistent Knowledge Wiki
tags:
  - 지식관리
  - LLM
  - Obsidian
updated: 2026-06-17
---
# 지속형 지식 위키

## 정의

지속형 지식 위키는 LLM이 원문 자료를 읽고, 그 내용을 Markdown 위키로 계속 축적하고 갱신하는 지식관리 패턴이다.

## 현재 이해

일반적인 파일 업로드나 RAG 시스템은 질문 시점에 관련 조각을 검색하고 답을 만든다. 반면 지속형 지식 위키는 이전에 읽은 자료의 요약, 연결, 모순, 질문을 위키에 남겨 다음 작업의 출발점으로 삼는다.

## 핵심 구성

- 원본 보관소: `raw/`에 파일을 원형 그대로 보관한다.
- 원문 요약: 자료 단위의 핵심 내용과 근거를 정리한다.
- 개념/대상/질문 페이지: 반복되는 지식 단위를 분리해 연결한다.
- 작업 기록: 어떤 자료를 언제 어떻게 반영했는지 남긴다.

## 관련 페이지

- [[sample-source-summary|샘플 원문 요약]]
- [[how-should-this-wiki-start|이 위키를 어떻게 시작할까?]]
- [[obsidian|옵시디언]]

## 열린 질문

- TODO(user): 자동 정리의 승인 단계를 어느 수준으로 둘지 정한다.
- TODO(user): 개인용 위키와 공유용 웹 서비스의 공개 범위를 구분한다.
""",
    "wiki/entities/centric-plm.md": """---
type: entity
title: 센트릭 PLM
aliases:
  - Centric PLM
  - Centric Software PLM
tags:
  - PLM
  - 상품기획
updated: 2026-06-17
---
# 센트릭 PLM

## 정의

센트릭 PLM은 상품기획, 디자인, 샘플, 자재, 사이즈, 작업지시, 제품 개발 데이터를 관리하는 PLM 솔루션으로 자료에 등장한다.

## FONE과의 관계

자료에서는 센트릭 PLM을 상품기획 데이터의 기준 시스템 후보로 보고, FONE/FA-ONE의 작업지시서와 제품/스타일 데이터를 PLM과 연결하는 방안을 검토한다.

## 주요 논점

- PLM과 FONE 중 어느 시스템이 상품기획 데이터의 기준이 되는가.
- 작업지시서, 자재, 사이즈, 원가, 코멘트 시트를 어떤 방식으로 연계하는가.
- 엑셀 기반 연계와 정식 인터페이스 중 어느 단계를 먼저 적용하는가.

## 관련 페이지

- [[plm-fone-integration|PLM-FONE 연계]]
- [[fone-as-is-analysis|FONE 현행 분석]]
- [[master-data-governance|기준정보 관리 체계]]

## 사용자 결정 필요

- TODO(user): 센트릭 PLM 도입 범위와 FONE/FA-ONE 연계 범위를 확정한다.
""",
    "wiki/entities/fa-one-fone.md": """---
type: entity
title: FA-ONE/FONE
aliases:
  - FONE
  - FA-ONE
tags:
  - FONE
  - ERP
  - 패션관리
updated: 2026-06-17
---
# FA-ONE/FONE

## 정의

FA-ONE/FONE은 분석 자료의 중심이 되는 패션관리 시스템이다. 상품기획, 영업관리, 물류, 정산, 기준정보, 외부 시스템 연계와 폭넓게 연결된다.

## 주요 업무 범위

- 상품과 스타일, 작업지시, 제품 정보 관리.
- 영업관리, 매출 확정, 정산, 채권/공제 관리.
- WMS, POS, VAN/EDI, AIS, PLM 등 외부 시스템과의 연계.
- 기준정보와 코드 관리.

## 현재 관찰

- 여러 업무의 중심 허브 역할을 하지만 시스템 간 역할 경계가 불명확한 부분이 있다.
- 엑셀 기반 보정과 수작업 대사가 여전히 많이 등장한다.
- TO-BE 설계에서는 기준정보, 인터페이스, 예외 처리, 권한/승인 체계 정리가 중요하다.

## 관련 페이지

- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]
- [[fone-as-is-analysis|FONE 현행 분석]]
- [[master-data-governance|기준정보 관리 체계]]
- [[plm-fone-integration|PLM-FONE 연계]]
- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]]
- [[sales-settlement-automation|영업관리 정산 자동화]]

## 사용자 결정 필요

- TODO(user): FONE과 FA-ONE의 공식 명칭과 범위를 확정한다.
- TODO(user): FONE을 ERP로 볼지, 패션 업무 플랫폼으로 볼지 표현 기준을 정한다.
""",
    "wiki/entities/obsidian.md": """---
type: entity
title: 옵시디언
aliases:
  - Obsidian
tags:
  - Obsidian
  - Markdown
updated: 2026-06-17
---
# 옵시디언

## 정의

옵시디언은 Markdown 파일을 로컬 Vault로 열고, 양방향 링크와 그래프를 통해 지식 구조를 탐색하는 도구다.

## 이 위키에서의 역할

`C:\\supersonic\\llm_wiki` 폴더 전체를 Vault로 열면 `wiki/`의 문서와 `raw/`의 원본 자료를 같은 작업 공간에서 확인할 수 있다. 위키 링크는 옵시디언과 웹 서비스에서 모두 탐색 가능하도록 유지한다.

## 관련 페이지

- [[persistent-knowledge-wiki|지속형 지식 위키]]
- [[obsidian-home|옵시디언 홈]]
- [[sample-source-summary|샘플 원문 요약]]

## 사용자 결정 필요

- TODO(user): 옵시디언에서 사용할 추가 플러그인과 태그 규칙을 정한다.
""",
    "wiki/entities/wms.md": """---
type: entity
title: WMS
aliases:
  - Warehouse Management System
  - 창고관리시스템
tags:
  - WMS
  - 물류
updated: 2026-06-17
---
# WMS

## 정의

WMS는 창고의 입고, 출고, 반품, 재고 이동, 재고 조정, 피킹/패킹 등 물류 실행을 관리하는 시스템이다.

## FONE과의 관계

FONE/FA-ONE은 영업, 정산, 기준정보와 연결되어 있고 WMS는 실물 물류와 재고 실행을 담당한다. 두 시스템 사이의 재고 기준과 확정 시점이 맞아야 영업/정산 데이터의 신뢰성이 유지된다.

## 주요 논점

- 입고, 출고, 반품, 이동, 조정의 확정 기준.
- FONE과 WMS 간 인터페이스 실패 시 재처리 방식.
- 장부 재고와 실물 재고 차이에 대한 승인/조정 절차.

## 관련 페이지

- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]]
- [[fone-as-is-analysis|FONE 현행 분석]]

## 사용자 결정 필요

- TODO(user): WMS와 FONE 사이의 재고 기준 시스템을 확정한다.
""",
    "wiki/questions/fone-next-decisions.md": """---
type: question
title: FONE 다음 의사결정
aliases:
  - FONE 다음 단계
tags:
  - FONE
  - TODO
updated: 2026-06-17
---
# FONE 다음 의사결정

## 질문

`ASIS분석자료(FONE)` 정리 이후 무엇을 사용자가 판단해야 하는가?

## 짧은 답

현재는 1차 폴더 정리가 끝난 상태다. 다음 단계에서는 분석 범위, 우선순위 파일, 명칭 통일, 업무영역별 중요도, TO-BE 산출물 형식을 정해야 한다.

## 판단 필요 항목

- TODO(user): 상세 정리할 파일 Top 10을 고른다.
- TODO(user): FONE/FA-ONE, 센트릭 PLM, WMS의 공식 명칭을 정한다.
- TODO(user): TO-BE 산출물을 요구사항 목록, 업무 프로세스, 데이터 모델, 실행 로드맵 중 어디에 맞출지 정한다.
- TODO(user): 영업관리, 물류, 상품기획, 기준정보 중 우선 분석 영역을 정한다.

## 바로 할 수 있는 요청 예시

```text
pending-ingest.md의 대기열을 보고 우선순위가 높은 리소스를 정리해줘.
원문 요약을 만들고, 관련 개념/대상 페이지를 갱신하고,
index.md와 log.md도 업데이트해줘.
판단이 필요한 항목은 TODO(user)로 남겨줘.
```

## 관련 페이지

- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]
- [[fone-as-is-analysis|FONE 현행 분석]]
- [[master-data-governance|기준정보 관리 체계]]
- [[plm-fone-integration|PLM-FONE 연계]]
- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]]
- [[sales-settlement-automation|영업관리 정산 자동화]]
""",
    "wiki/questions/how-should-this-wiki-start.md": """---
type: question
title: 이 위키를 어떻게 시작할까?
tags:
  - 지식관리
  - 운영
updated: 2026-06-17
---
# 이 위키를 어떻게 시작할까?

## 질문

LLM이 원본 자료를 읽고 위키로 계속 축적하려면 어떤 구조와 규칙부터 갖춰야 하는가?

## 짧은 답

원본 보관소, 원문 요약, 개념 페이지, 대상 페이지, 질문 페이지, 목차, 작업 기록을 먼저 만든다. 이후 새 자료가 들어올 때마다 원문 요약을 만들고 관련 페이지를 갱신한다.

## 판단 필요 항목

- TODO(user): 모든 변경을 사용자 검토 후 반영할지, LLM이 바로 반영할지 정한다.
- TODO(user): 원본 자료 공개 범위와 민감정보 처리 기준을 정한다.
- TODO(user): 웹 서비스와 옵시디언 중 어떤 화면을 주 사용 화면으로 둘지 정한다.

## 요청 예시

```text
raw/sources/<파일명>을 정리해줘.
원문 요약을 만들고, 관련 개념/대상 페이지를 갱신하고,
index.md와 log.md도 업데이트해줘.
판단이 필요한 항목은 TODO(user)로 남겨줘.
```

## 관련 페이지

- [[persistent-knowledge-wiki|지속형 지식 위키]]
- [[sample-source-summary|샘플 원문 요약]]
- [[obsidian|옵시디언]]
""",
    "wiki/sources/sample-source-summary.md": """---
type: source-summary
title: 샘플 원문 요약
source: ../../llm-wiki.md
tags:
  - 샘플
  - LLM
updated: 2026-06-17
---
# 샘플 원문 요약

## 원본 정보

- 원본 파일: [llm-wiki.md](../../llm-wiki.md)
- 상태: 샘플 요약

## 요약

LLM Wiki 아이디어는 원본 자료를 매번 새로 읽는 방식이 아니라, LLM이 읽은 내용을 Markdown 위키에 누적해 다음 작업의 맥락으로 재사용하는 방식이다.

## 핵심 포인트

- 원본 자료는 `raw/`에 보관하고, 해석된 지식은 `wiki/`에 남긴다.
- 새 자료가 들어오면 원문 요약, 개념 페이지, 대상 페이지, 질문 페이지, 목차와 작업 기록을 갱신한다.
- Obsidian은 로컬 지식 탐색에 적합하고, 웹 서비스는 검색과 공유에 적합하다.

## 관련 페이지

- [[persistent-knowledge-wiki|지속형 지식 위키]]
- [[how-should-this-wiki-start|이 위키를 어떻게 시작할까?]]

## 열린 질문

- TODO(user): 샘플 문서를 실제 운영 규칙으로 어느 정도까지 확장할지 정한다.
""",
    "wiki/sources/asis-fone-folder-ingest.md": """---
type: source-summary
title: FONE AS-IS 자료 묶음 정리
source: ../../raw/sources/ASIS분석자료(FONE)
tags:
  - FONE
  - ASIS
  - 현행분석
updated: 2026-06-17
---
# FONE AS-IS 자료 묶음 정리

## 원본 정보

- 원본 폴더: `raw/sources/ASIS분석자료(FONE)`
- 자료 성격: FONE/FA-ONE 차세대 및 현행 분석 관련 문서 묶음.
- 정리 상태: 1차 폴더 정리.

## 요약

`ASIS분석자료(FONE)` 폴더는 FONE/FA-ONE 시스템의 현행 업무, 프로세스, 데이터, 인터페이스, 차세대 검토 자료를 폭넓게 담고 있다. 1차 정리 기준으로 가장 중요한 흐름은 기준정보 표준화, PLM-FONE 연계, WMS-FONE 재고 연계, 영업관리 정산 자동화다.

## 핵심 결론

- FONE/FA-ONE은 상품기획, 영업관리, 물류, 정산, 기준정보를 연결하는 핵심 업무 시스템이다.
- 여러 자료에서 수작업 엑셀 보정, 시스템 간 코드 불일치, 인터페이스 실패 처리, 기준정보 중복 관리가 반복된다.
- 상품기획 데이터는 센트릭 PLM 중심의 표준화와 FONE/FA-ONE 연계가 필요하다.
- WMS와 FONE 사이의 재고 기준, 물류 이벤트 확정 시점, 예외 처리가 TO-BE 설계의 핵심이다.
- 영업관리 영역은 POS/VAN/EDI 대사, 매출 확정, 정산, AIS 전표 전송의 자동화 필요성이 크다.

## 주요 자료 범주

### 1. 업무 프로세스와 기능 분석

FONE 프로세스, FA-ONE 프로세스 로직, 현행 업무 흐름, TO-BE 비교 자료가 포함되어 있다. 업무 흐름과 화면/기능의 현행 구조를 파악하는 데 중요하다.

### 2. 기준정보와 데이터 구조

DB 테이블, ERD, 데이터 이관, 기준정보 관련 문서가 포함되어 있다. 브랜드, 상품, 스타일, 칼라, 사이즈, 매장, 거래처 등 공통 기준정보가 여러 시스템에 영향을 준다.

### 3. PLM은 상품기획 데이터의 단일 기준 정보원 후보로 등장한다

센트릭 PLM은 제품코드, 작업지시서, 스타일/속성, 자재, 사이즈 스펙, 코멘트 시트, 샘플 추적 등 상품기획 데이터의 기준 시스템 후보로 제시된다. 단기적으로는 엑셀 업로드/다운로드 기반의 연계 검토, 장기적으로는 ERP/FONE 연동이 언급된다.

### 4. WMS와 물류 연계

WMS, 물류 마스터플랜, 재고/수불/출고/반품 관련 자료가 포함되어 있다. WMS와 FONE 사이의 데이터 기준 시점과 상태 값 정의가 필요하다.

### 5. 영업관리, POS, 정산

POS, VAN/EDI, 매출 확정, 정산, 수수료, 공제, 채권, AIS 전표 전송 관련 자료가 포함되어 있다. 자동 대사와 예외 관리가 핵심 개선 방향이다.

## 근거와 연결

- [[fa-one-fone|FA-ONE/FONE]]
- [[fone-as-is-analysis|FONE 현행 분석]]
- [[master-data-governance|기준정보 관리 체계]]
- [[plm-fone-integration|PLM-FONE 연계]]
- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]]
- [[sales-settlement-automation|영업관리 정산 자동화]]
- [[fone-next-decisions|FONE 다음 의사결정]]

## 한계와 주의

- 이번 정리는 폴더 전체를 대상으로 한 1차 통합 요약이다.
- 이미지, 압축파일, 일부 바이너리 자료는 심층 분석하지 않았다.
- 원본 파일명과 시스템 약어는 추적성을 위해 그대로 유지했다.

## 사용자 결정 필요

- TODO(user): 우선순위가 높은 파일을 지정하면 개별 파일 단위로 심층 정리한다.
- TODO(user): FONE/FA-ONE의 공식 명칭과 범위를 확정한다.
- TODO(user): 업무 영역별 TO-BE 산출물 형식을 정한다.
""",
    "wiki/_templates/concept-page.md": """---
type: concept
title:
aliases: []
tags: []
updated:
---
# 개념명

## 정의

## 현재 이해

## 근거

## 관련 원문

## 관련 개념

## 모순/주의

## 열린 질문

## 사용자 결정 필요
""",
    "wiki/_templates/entity-page.md": """---
type: entity
title:
aliases: []
tags: []
updated:
---
# 대상명

## 정의

## 역할

## 주요 관계

## 관련 근거

## 관련 페이지

## 열린 질문

## 사용자 결정 필요
""",
    "wiki/_templates/question-page.md": """---
type: question
title:
tags: []
updated:
---
# 질문명

## 질문

## 답변

## 근거

## 판단 필요 항목

## 후속 작업

## 답변 후 갱신할 페이지

## 사용자 결정 필요
""",
    "wiki/_templates/source-summary.md": """---
type: source-summary
title:
source:
tags: []
updated:
---
# 원문 요약

## 원본 정보

- 원본 파일:
- 작성일:
- 상태:

## 요약

## 핵심 포인트

## 주요 근거

## 관련 개념

## 관련 대상

## 모순/주의

## 열린 질문

## 사용자 결정 필요
""",
    "wiki/_templates/lint-report.md": """---
type: lint-report
title:
updated:
---
# 위키 점검 보고서

## 요약

## 깨진 링크

## 중복 가능 페이지

## 제목 형식 문제

## 모순/주의

## 정리 필요 항목

## 다음 점검 전 확인 사항

## 사용자 결정 필요
""",
    "README.md": """# LLM 위키

`C:\\supersonic\\llm_wiki`는 원본 자료를 LLM이 읽고, 해석된 내용을 Markdown 위키와 웹 서비스로 누적하기 위한 작업 공간이다.

## 기본 구조

- `raw/` - 원본 자료 보관소. 원본 파일명은 추적성을 위해 유지한다.
- `wiki/` - 사람이 읽고 연결할 수 있는 Markdown 지식 위키.
- `wiki/resources/auto/` - 자동 등록된 리소스 페이지.
- `tools/` - 자동 등록, 감시, 웹 서비스 실행 스크립트.
- `web/` - 로컬 웹 서비스.
- `.obsidian/` - Obsidian Vault 설정.

## 빠른 시작

```powershell
cd C:\\supersonic\\llm_wiki
python tools/wiki_auto_index.py --no-log
powershell -ExecutionPolicy Bypass -File tools/start_wiki_watcher.ps1
powershell -ExecutionPolicy Bypass -File tools/start_web_service.ps1
```

웹 서비스가 실행되면 `.wiki_state\\web.port`에 기록된 포트로 접속한다. 현재 기본 포트는 `http://localhost:4174`다.

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
""",
    "AGENTS.md": """# LLM 위키 작업 지침

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
""",
    "tools/README.md": """# 위키 자동화 도구

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
""",
    "web/README.md": """# LLM 위키 웹 서비스

이 웹앱은 `wiki/` Markdown 파일을 읽어 검색, 대시보드, 자료 목록, 정리 대기열, 연결망, 업로드 화면을 제공한다.

## 실행

```powershell
cd C:\\supersonic\\llm_wiki
powershell -ExecutionPolicy Bypass -File tools/start_web_service.ps1
```

실행 포트는 `.wiki_state\\web.port`에 기록된다.

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
""",
}


def main() -> None:
    for relative, content in FILES.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        print(f"repaired {relative}")


if __name__ == "__main__":
    main()
