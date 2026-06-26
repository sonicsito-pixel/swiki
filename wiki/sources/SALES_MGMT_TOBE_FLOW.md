# Sales Management (영업관리) TO-BE Process Flow

This document visualizes the optimized TO-BE processes for the Next-Gen ERP system, focusing on automation, real-time data sync, and efficiency.

---

## 1. Store & Master Data Management (매장 기준정보)
**Goal:** 매장 코드 중심의 통합 라이프사이클 관리 및 거점-종속(Hub-Spoke) 구조 체계화.

```mermaid
graph TD
    A["Brand/Business Strategy"] --> B{Store Open/Change?}
    B -->|Yes| C["F-ONE: Integrated Store Management UI"]
    
    subgraph "Master Data Definition"
        C --> D[매장 코드 및 속성 등록]
        D --> D1[거점-종속 매장 관계 정의]
        D1 --> D2[중간관리자 매핑 및 수수료율 설정]
    end

    D2 --> E[Real-time Sync to AIS]
    E --> F[Auto-assign Sub-store Info]
    F --> G[Ready for Sales/Inventory]
    
    %% Hub-Spoke Concept
    H["거점매장 (Anchor)"] --- I["종속매장 A"]
    H --- J["종속매장 B"]
    
    subgraph "Legacy (AS-IS) Pain Points"
        K["수기 엑셀로 거점 구조 관리"]
    end
    D1 -.->|시스템화| K
```

---

## 2. Sales & Settlement (매출 및 정산)
**Goal:** POS-ERP 실시간 매출 연동, 거점매장 매출 자동 배분, 결산 자동화.

```mermaid
graph TD
    subgraph "POS & Sales Event"
        A["매장/온라인 매출 발생"] --> B{프로모션 적용?}
        B -->|Yes| C[실시간 할인/쿠폰 배분 로직 적용]
        B -->|No| D[일반 매출 확정]
        C --> E[POS 매출 데이터 전송]
        D --> E
    end

    subgraph "F-ONE: Validation & Allocation"
        E --> F[POS vs ERP 매출 정합성 체크]
        F --> G{거점매장 해당?}
        G -->|Yes| G1["종속매장 매출 -> 거점매장 자동 배분/통합"]
        G -->|No| G2[단독 매장 매출 확정]
        G1 --> I[매출 확정 및 매출채권 인식]
        G2 --> I
    end

    subgraph "F-ONE: Settlement & Journaling"
        I --> J[수수료/판촉비/배송비 자동 계산]
        J --> K["정산 데이터 생성 (거점별 합산)"]
        K --> L[One-Click 회계 전표 생성 요청]
    end

    subgraph "AIS: Accounting"
        L --> M[AIS: 자동 전표 생성 및 인터페이스]
        M --> N["결산 완료 (D+1 목표)"]
    end

    %% Added Hub Logic
    O["AS-IS: 거점별 매출 수기 재배분"] -.->|자동화| G1
```

---

## 3. Commission Management (중간관리자)
**Goal:** Automated deduction calculation and seamless tax invoice (Trustbill) issuance.

```mermaid
graph TD
    A[Settled Sales Data] --> B["F-ONE: Apply Seasonal Commission Rates"]
    B --> C[Auto-Calculate Deductions]
    C --> D[Final Payment Amount Calculation]
    D --> E[System-generated Evidence]
    E --> F[One-click Trustbill Issuance]
    F --> G[Payment Authorization]
    
    subgraph "Security & Integrity"
        H[Rate History Tracking]
        I[Permission-based Access]
    end
    B --- H
    B --- I
```

---

## 4. A/R & Credit Management (미수금/채권)
**Goal:** Real-time credit monitoring and automated warning system for proactive collection.

```mermaid
graph TD
    A[Virtual Account Payment] --> B[Real-time F-ONE Sync]
    B --> C[Auto-Reconciliation with A/R]
    C --> D[Updated Credit Status]
    D --> E{"A/R > 1M KRW?"}
    E -->|Yes| F["Real-time Alert/Popup to Manager"]
    E -->|No| G[Normal Monitoring]
    F --> H[Prompt Collection Action]
    
    subgraph "Visibility"
        I[A/R Aging Dashboard]
        J[Long-term A/R Tracking]
    end
    D --- I
    D --- J
```

---

## 5. Inventory & Stock Management
**Goal:** Simplified self-consumption processing and expanded visibility across multiple years/seasons.

```mermaid
graph TD
    A[Store Inventory Need] --> B{Self-Consumption?}
    B -->|Yes| C[Direct Registration at Store App]
    B -->|No| D[Regular Sales/Transfer]
    C --> E[Real-time Stock Update]
    E --> F[Auto-Accounting for Cost]
    
    subgraph "Query Optimization"
        G["Multi-year/Season Integrated Search"]
        H[Warehouse Optimization History]
    end
    G --- D
    H --- D
```
