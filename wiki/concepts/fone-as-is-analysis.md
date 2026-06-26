---
type: concept
title: FONE 현행 분석
aliases:
  - FONE AS-IS 분석
  - FA-ONE 현행 분석
tags:
  - FONE
  - 현행분석
  - 업무분석
updated: 2026-06-19
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
- 현업인터뷰 기준으로 매장정보와 상품정보의 필드 사용 여부가 부서별로 크게 다르며, 단순 이관보다 필드 단위 재판정이 필요하다.

## 근거

- [[asis-fone-folder-ingest|FONE AS-IS 자료 묶음 정리]]
- [[field-interview-master-data-summary|현업인터뷰 기준정보 분석]]
- [[fa-one-fone|FA-ONE/FONE]]

## 관련 페이지

- [[master-data-governance|기준정보 관리 체계]]
- [[store-master-data-cleanup|매장 기준정보 정비]]
- [[product-master-data-cleanup|상품 기준정보 정비]]
- [[plm-fone-integration|PLM-FONE 연계]]
- [[wms-fone-inventory-integration|WMS-FONE 재고 연계]]
- [[sales-settlement-automation|영업관리 정산 자동화]]

## 열린 질문

- TODO(user): 현행 분석의 최종 산출물을 업무별 이슈 목록, TO-BE 요구사항, 전환 로드맵 중 어디에 맞출지 정한다.
- TODO(user): 파일별 심층 정리 우선순위를 정한다.
