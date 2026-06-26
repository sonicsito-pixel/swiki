---
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
