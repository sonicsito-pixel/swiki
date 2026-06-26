---
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
