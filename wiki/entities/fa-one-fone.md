---
type: entity
title: FA-ONE/FONE
aliases:
  - FONE
  - FA-ONE
tags:
  - FONE
  - ERP
  - 패션관리
updated: 2026-06-19
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
- 현업인터뷰 자료에서는 매장정보와 상품정보가 FONE/FA-ONE의 핵심 기준정보 화면으로 드러나며, 필드별 사용 목적과 관리 주체가 부서마다 다르다.

## 관련 페이지

- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]
- [[fone-as-is-analysis|FONE 현행 분석]]
- [[master-data-governance|기준정보 관리 체계]]
- [[field-interview-master-data-summary|현업인터뷰 기준정보 분석]]
- [[store-master-data-cleanup|매장 기준정보 정비]]
- [[product-master-data-cleanup|상품 기준정보 정비]]
- [[plm-fone-integration|PLM-FONE 연계]]
- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]]
- [[sales-settlement-automation|영업관리 정산 자동화]]

## 사용자 결정 필요

- TODO(user): FONE과 FA-ONE의 공식 명칭과 범위를 확정한다.
- TODO(user): FONE을 ERP로 볼지, 패션 업무 플랫폼으로 볼지 표현 기준을 정한다.
