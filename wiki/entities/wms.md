---
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
