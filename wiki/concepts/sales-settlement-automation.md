---
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
