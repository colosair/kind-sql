# 친절한 SQL 튜닝 — 학습 정리

> 교재 **『친절한 SQL 튜닝』**(조시형 저, Oracle 중심)을 절(節) 단위로 정리·심화한 학습 노트입니다.  
> 단순 요약이 아니라 **개념 간 연결 · 실행계획 해독 · 튜닝 포인트 진단**까지 담았으며, 모든 개념을 통일 원리 **`reduce I/O`** 로 귀결시킵니다.

---

## 📚 장별 바로가기

| 장  | 제목                                                     | 핵심                                                |
| :-: | -------------------------------------------------------- | --------------------------------------------------- |
| 💾  | [**1장. SQL 처리 과정과 I/O**](#1장-sql-처리-과정과-io)  | SQL 실행 원리와 I/O 메커니즘 — 책 전체의 기초       |
| 🌲  | [**2장. 인덱스 기본**](#2장-인덱스-기본)                 | B\*Tree 인덱스 구조와 수직·수평 탐색                |
| 🎯  | [**3장. 인덱스 튜닝**](#3장-인덱스-튜닝)                 | 랜덤 액세스 최소화 — "SQL 튜닝은 랜덤 I/O와의 전쟁" |
| 🔗  | [**4장. 조인 튜닝**](#4장-조인-튜닝)                     | NL · 소트 머지 · 해시 조인과 서브쿼리 변환          |
| 📊  | [**5장. 소트 튜닝**](#5장-소트-튜닝)                     | 소트 부하 제거 · 생략 · 경감                        |
| ✏️  | [**6장. DML 튜닝**](#6장-dml-튜닝)                       | 쓰기 작업의 부가 비용 줄이기                        |
| 🧠  | [**7장. SQL 옵티마이저**](#7장-sql-옵티마이저)           | 옵티마이저의 비용 추정과 개발자의 역할              |
| 📎  | [**부록. 실행계획 분석 도구**](#부록-실행계획-분석-도구) | 실행계획 확인 도구 모음                             |

---

## 1장. SQL 처리 과정과 I/O

> 🗺️ **[1장 전체 흐름 한눈에 보기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1%EC%9E%A5_%EC%A0%84%EC%B2%B4_%ED%9D%90%EB%A6%84.md)**

- [1.1.1 구조적 집합적 선언적 질의 언어](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.1.1_%EA%B5%AC%EC%A1%B0%EC%A0%81_%EC%A7%91%ED%95%A9%EC%A0%81_%EC%84%A0%EC%96%B8%EC%A0%81_%EC%A7%88%EC%9D%98_%EC%96%B8%EC%96%B4.md)
- [1.1.2 SQL 최적화](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.1.2_SQL_%EC%B5%9C%EC%A0%81%ED%99%94.md)
- [1.1.3 SQL 옵티마이저](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.1.3_SQL_%EC%98%B5%ED%8B%B0%EB%A7%88%EC%9D%B4%EC%A0%80.md)
- [1.1.4 실행계획과 비용](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.1.4_%EC%8B%A4%ED%96%89%EA%B3%84%ED%9A%8D%EA%B3%BC_%EB%B9%84%EC%9A%A9.md)
- [1.1.5 옵티마이저 힌트](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.1.5_%EC%98%B5%ED%8B%B0%EB%A7%88%EC%9D%B4%EC%A0%80_%ED%9E%8C%ED%8A%B8.md)
- [1.2.1 소프트 파싱 vs 하드 파싱](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.2.1_%EC%86%8C%ED%94%84%ED%8A%B8_%ED%8C%8C%EC%8B%B1_vs_%ED%95%98%EB%93%9C_%ED%8C%8C%EC%8B%B1.md)
- [1.2.2 바인드 변수의 중요성](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.2.2_%EB%B0%94%EC%9D%B8%EB%93%9C_%EB%B3%80%EC%88%98%EC%9D%98_%EC%A4%91%EC%9A%94%EC%84%B1.md)
- [1.3.1 SQL이 느린 이유](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.3.1_SQL%EC%9D%B4_%EB%8A%90%EB%A6%B0_%EC%9D%B4%EC%9C%A0.md)
- [1.3.2 데이터베이스 저장 구조](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.3.2_%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4_%EC%A0%80%EC%9E%A5_%EA%B5%AC%EC%A1%B0.md)
- [1.3.3 블록 단위 IO](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.3.3_%EB%B8%94%EB%A1%9D_%EB%8B%A8%EC%9C%84_IO.md)
- [1.3.4 시퀀셜 액세스 vs 랜덤 액세스](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.3.4_%EC%8B%9C%ED%80%80%EC%85%9C_%EC%95%A1%EC%84%B8%EC%8A%A4_vs_%EB%9E%9C%EB%8D%A4_%EC%95%A1%EC%84%B8%EC%8A%A4.md)
- [1.3.5 논리적 IO vs 물리적 IO](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.3.5_%EB%85%BC%EB%A6%AC%EC%A0%81_IO_vs_%EB%AC%BC%EB%A6%AC%EC%A0%81_IO.md)
- [1.3.6 Single Block IO vs Multiblock IO](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.3.6_Single_Block_IO_vs_Multiblock_IO.md)
- [1.3.7 Table Full Scan vs Index Range Scan](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.3.7_Table_Full_Scan_vs_Index_Range_Scan.md)
- [1.3.8 캐시 탐색 메커니즘](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/01%EC%9E%A5/1.3.8_%EC%BA%90%EC%8B%9C_%ED%83%90%EC%83%89_%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md)

<div align="right">

[🔝 장별 바로가기](#-장별-바로가기) &nbsp;|&nbsp; [2장. 인덱스 기본](#2장-인덱스-기본) ➡️

</div>

---

## 2장. 인덱스 기본

> 🗺️ **[2장 전체 흐름 한눈에 보기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2%EC%9E%A5_%EC%A0%84%EC%B2%B4_%ED%9D%90%EB%A6%84.md)**

- [2.1.1 미리 보는 인덱스 튜닝](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.1.1_%EB%AF%B8%EB%A6%AC_%EB%B3%B4%EB%8A%94_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%ED%8A%9C%EB%8B%9D.md)
- [2.1.2 인덱스 구조](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.1.2_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EA%B5%AC%EC%A1%B0.md)
- [2.1.3 인덱스 수직적 탐색](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.1.3_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%88%98%EC%A7%81%EC%A0%81_%ED%83%90%EC%83%89.md)
- [2.1.4 인덱스 수평적 탐색](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.1.4_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%88%98%ED%8F%89%EC%A0%81_%ED%83%90%EC%83%89.md)
- [2.1.5 결합 인덱스 구조와 탐색](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.1.5_%EA%B2%B0%ED%95%A9_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EA%B5%AC%EC%A1%B0%EC%99%80_%ED%83%90%EC%83%89.md)
- [2.2.1 인덱스를 사용한다는 것](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.2.1_%EC%9D%B8%EB%8D%B1%EC%8A%A4%EB%A5%BC_%EC%82%AC%EC%9A%A9%ED%95%9C%EB%8B%A4%EB%8A%94_%EA%B2%83.md)
- [2.2.2 인덱스를 Range Scan 할 수 없는 이유](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.2.2_%EC%9D%B8%EB%8D%B1%EC%8A%A4%EB%A5%BC_Range_Scan_%ED%95%A0_%EC%88%98_%EC%97%86%EB%8A%94_%EC%9D%B4%EC%9C%A0.md)
- [2.2.3 더 중요한 인덱스 사용 조건](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.2.3_%EB%8D%94_%EC%A4%91%EC%9A%94%ED%95%9C_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%82%AC%EC%9A%A9_%EC%A1%B0%EA%B1%B4.md)
- [2.2.4 인덱스를 이용한 소트 연산 생략](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.2.4_%EC%9D%B8%EB%8D%B1%EC%8A%A4%EB%A5%BC_%EC%9D%B4%EC%9A%A9%ED%95%9C_%EC%86%8C%ED%8A%B8_%EC%97%B0%EC%82%B0_%EC%83%9D%EB%9E%B5.md)
- [2.2.5 ORDER BY 절에서 컬럼 가공](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.2.5_ORDER_BY_%EC%A0%88%EC%97%90%EC%84%9C_%EC%BB%AC%EB%9F%BC_%EA%B0%80%EA%B3%B5.md)
- [2.2.6 SELECT LIST에서 컬럼 가공](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.2.6_SELECT_LIST%EC%97%90%EC%84%9C_%EC%BB%AC%EB%9F%BC_%EA%B0%80%EA%B3%B5.md)
- [2.2.7 자동 형변환](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.2.7_%EC%9E%90%EB%8F%99_%ED%98%95%EB%B3%80%ED%99%98.md)
- [2.3.1 Index Range Scan](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.3.1_Index_Range_Scan.md)
- [2.3.2 Index Full Scan](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.3.2_Index_Full_Scan.md)
- [2.3.3 Index Unique Scan](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.3.3_Index_Unique_Scan.md)
- [2.3.4 Index Skip Scan](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.3.4_Index_Skip_Scan.md)
- [2.3.5 Index Fast Full Scan](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.3.5_Index_Fast_Full_Scan.md)
- [2.3.6 Index Range Scan Descending](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/02%EC%9E%A5/2.3.6_Index_Range_Scan_Descending.md)

<div align="right">

⬅️ [1장. SQL 처리 과정과 I/O](#1장-sql-처리-과정과-io) &nbsp;|&nbsp; [🔝 장별 바로가기](#-장별-바로가기) &nbsp;|&nbsp; [3장. 인덱스 튜닝](#3장-인덱스-튜닝) ➡️

</div>

---

## 3장. 인덱스 튜닝

> 🗺️ **[3장 전체 흐름 한눈에 보기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3%EC%9E%A5_%EC%A0%84%EC%B2%B4_%ED%9D%90%EB%A6%84.md)**

- [3.1.1 테이블 랜덤 액세스](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.1.1_%ED%85%8C%EC%9D%B4%EB%B8%94_%EB%9E%9C%EB%8D%A4_%EC%95%A1%EC%84%B8%EC%8A%A4.md)
- [3.1.2 인덱스 클러스터링 팩터](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.1.2_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%A7%81_%ED%8C%A9%ED%84%B0.md)
- [3.1.3 인덱스 손익분기점](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.1.3_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%86%90%EC%9D%B5%EB%B6%84%EA%B8%B0%EC%A0%90.md)
- [3.1.4 인덱스 컬럼 추가](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.1.4_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%BB%AC%EB%9F%BC_%EC%B6%94%EA%B0%80.md)
- [3.1.5 인덱스만 읽고 처리](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.1.5_%EC%9D%B8%EB%8D%B1%EC%8A%A4%EB%A7%8C_%EC%9D%BD%EA%B3%A0_%EC%B2%98%EB%A6%AC.md)
- [3.1.6 인덱스 구조 테이블](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.1.6_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EA%B5%AC%EC%A1%B0_%ED%85%8C%EC%9D%B4%EB%B8%94.md)
- [3.1.7 클러스터 테이블](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.1.7_%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0_%ED%85%8C%EC%9D%B4%EB%B8%94.md)
- [3.2.1 부분범위 처리](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.2.1_%EB%B6%80%EB%B6%84%EB%B2%94%EC%9C%84_%EC%B2%98%EB%A6%AC.md)
- [3.2.2 부분범위 처리 구현](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.2.2_%EB%B6%80%EB%B6%84%EB%B2%94%EC%9C%84_%EC%B2%98%EB%A6%AC_%EA%B5%AC%ED%98%84.md)
- [3.2.3 OLTP 환경에서 부분범위 처리를 활용한 성능개선 원리](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.2.3_OLTP_%ED%99%98%EA%B2%BD%EC%97%90%EC%84%9C_%EB%B6%80%EB%B6%84%EB%B2%94%EC%9C%84_%EC%B2%98%EB%A6%AC%EB%A5%BC_%ED%99%9C%EC%9A%A9%ED%95%9C_%EC%84%B1%EB%8A%A5%EA%B0%9C%EC%84%A0_%EC%9B%90%EB%A6%AC.md)
- [3.3.10 범위검색 조건을 남용할 때 생기는 비효율](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.10_%EB%B2%94%EC%9C%84%EA%B2%80%EC%83%89_%EC%A1%B0%EA%B1%B4%EC%9D%84_%EB%82%A8%EC%9A%A9%ED%95%A0_%EB%95%8C_%EC%83%9D%EA%B8%B0%EB%8A%94_%EB%B9%84%ED%9A%A8%EC%9C%A8.md)
- [3.3.11 다양한 옵션 조건 처리 방식의 장단점 비교](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.11_%EB%8B%A4%EC%96%91%ED%95%9C_%EC%98%B5%EC%85%98_%EC%A1%B0%EA%B1%B4_%EC%B2%98%EB%A6%AC_%EB%B0%A9%EC%8B%9D%EC%9D%98_%EC%9E%A5%EB%8B%A8%EC%A0%90_%EB%B9%84%EA%B5%90.md)
- [3.3.12 함수호출부하 해소를 위한 인덱스 구성](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.12_%ED%95%A8%EC%88%98%ED%98%B8%EC%B6%9C%EB%B6%80%ED%95%98_%ED%95%B4%EC%86%8C%EB%A5%BC_%EC%9C%84%ED%95%9C_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EA%B5%AC%EC%84%B1.md)
- [3.3.1 인덱스 탐색](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.1_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%ED%83%90%EC%83%89.md)
- [3.3.2 인덱스 스캔 효율성](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.2_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%8A%A4%EC%BA%94_%ED%9A%A8%EC%9C%A8%EC%84%B1.md)
- [3.3.3 액세스 조건과 필터 조건](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.3_%EC%95%A1%EC%84%B8%EC%8A%A4_%EC%A1%B0%EA%B1%B4%EA%B3%BC_%ED%95%84%ED%84%B0_%EC%A1%B0%EA%B1%B4.md)
- [3.3.4 비교 연산자 종류와 컬럼 순서에 따른 군집성](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.4_%EB%B9%84%EA%B5%90_%EC%97%B0%EC%82%B0%EC%9E%90_%EC%A2%85%EB%A5%98%EC%99%80_%EC%BB%AC%EB%9F%BC_%EC%88%9C%EC%84%9C%EC%97%90_%EB%94%B0%EB%A5%B8_%EA%B5%B0%EC%A7%91%EC%84%B1.md)
- [3.3.5 인덱스 선행 컬럼이 등치 조건이 아닐 때 생기는 비효율](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.5_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%84%A0%ED%96%89_%EC%BB%AC%EB%9F%BC%EC%9D%B4_%EB%93%B1%EC%B9%98_%EC%A1%B0%EA%B1%B4%EC%9D%B4_%EC%95%84%EB%8B%90_%EB%95%8C_%EC%83%9D%EA%B8%B0%EB%8A%94_%EB%B9%84%ED%9A%A8%EC%9C%A8.md)
- [3.3.6 BETWEEN을 IN List로 전환](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.6_BETWEEN%EC%9D%84_IN_List%EB%A1%9C_%EC%A0%84%ED%99%98.md)
- [3.3.7 Index Skip Scan 활용](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.7_Index_Skip_Scan_%ED%99%9C%EC%9A%A9.md)
- [3.3.8 IN 조건은 등치인가](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.8_IN_%EC%A1%B0%EA%B1%B4%EC%9D%80_%EB%93%B1%EC%B9%98%EC%9D%B8%EA%B0%80.md)
- [3.3.9 BETWEEN과 LIKE 스캔 범위 비교](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.3.9_BETWEEN%EA%B3%BC_LIKE_%EC%8A%A4%EC%BA%94_%EB%B2%94%EC%9C%84_%EB%B9%84%EA%B5%90.md)
- [3.4.1 인덱스 설계가 어려운 이유](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.4.1_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%84%A4%EA%B3%84%EA%B0%80_%EC%96%B4%EB%A0%A4%EC%9A%B4_%EC%9D%B4%EC%9C%A0.md)
- [3.4.2 가장 중요한 두 가지 선택 기준](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.4.2_%EA%B0%80%EC%9E%A5_%EC%A4%91%EC%9A%94%ED%95%9C_%EB%91%90_%EA%B0%80%EC%A7%80_%EC%84%A0%ED%83%9D_%EA%B8%B0%EC%A4%80.md)
- [3.4.3 스캔 효율성 이외의 판단 기준](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.4.3_%EC%8A%A4%EC%BA%94_%ED%9A%A8%EC%9C%A8%EC%84%B1_%EC%9D%B4%EC%99%B8%EC%9D%98_%ED%8C%90%EB%8B%A8_%EA%B8%B0%EC%A4%80.md)
- [3.4.4 공식을 초월한 전략적 설계](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.4.4_%EA%B3%B5%EC%8B%9D%EC%9D%84_%EC%B4%88%EC%9B%94%ED%95%9C_%EC%A0%84%EB%9E%B5%EC%A0%81_%EC%84%A4%EA%B3%84.md)
- [3.4.5 소트 연산을 생략하기 위한 컬럼 추가](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.4.5_%EC%86%8C%ED%8A%B8_%EC%97%B0%EC%82%B0%EC%9D%84_%EC%83%9D%EB%9E%B5%ED%95%98%EA%B8%B0_%EC%9C%84%ED%95%9C_%EC%BB%AC%EB%9F%BC_%EC%B6%94%EA%B0%80.md)
- [3.4.6 결합 인덱스 선택도](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.4.6_%EA%B2%B0%ED%95%A9_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%84%A0%ED%83%9D%EB%8F%84.md)
- [3.4.7 중복 인덱스 제거](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.4.7_%EC%A4%91%EB%B3%B5_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%A0%9C%EA%B1%B0.md)
- [3.4.8 인덱스 설계도 작성](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/03%EC%9E%A5/3.4.8_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EC%84%A4%EA%B3%84%EB%8F%84_%EC%9E%91%EC%84%B1.md)

<div align="right">

⬅️ [2장. 인덱스 기본](#2장-인덱스-기본) &nbsp;|&nbsp; [🔝 장별 바로가기](#-장별-바로가기) &nbsp;|&nbsp; [4장. 조인 튜닝](#4장-조인-튜닝) ➡️

</div>

---

## 4장. 조인 튜닝

> 🗺️ **[4장 전체 흐름 한눈에 보기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4%EC%9E%A5_%EC%A0%84%EC%B2%B4_%ED%9D%90%EB%A6%84.md)**

- [4.1.1 NL 조인 기본 메커니즘](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.1.1_NL_%EC%A1%B0%EC%9D%B8_%EA%B8%B0%EB%B3%B8_%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md)
- [4.1.2 NL 조인 실행계획 제어](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.1.2_NL_%EC%A1%B0%EC%9D%B8_%EC%8B%A4%ED%96%89%EA%B3%84%ED%9A%8D_%EC%A0%9C%EC%96%B4.md)
- [4.1.3 NL 조인 수행 과정 분석](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.1.3_NL_%EC%A1%B0%EC%9D%B8_%EC%88%98%ED%96%89_%EA%B3%BC%EC%A0%95_%EB%B6%84%EC%84%9D.md)
- [4.1.4 NL 조인 튜닝 포인트](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.1.4_NL_%EC%A1%B0%EC%9D%B8_%ED%8A%9C%EB%8B%9D_%ED%8F%AC%EC%9D%B8%ED%8A%B8.md)
- [4.1.5 NL 조인 특징 요약](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.1.5_NL_%EC%A1%B0%EC%9D%B8_%ED%8A%B9%EC%A7%95_%EC%9A%94%EC%95%BD.md)
- [4.1.6 NL 조인 튜닝 실습](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.1.6_NL_%EC%A1%B0%EC%9D%B8_%ED%8A%9C%EB%8B%9D_%EC%8B%A4%EC%8A%B5.md)
- [4.1.7 NL 조인 확장 메커니즘](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.1.7_NL_%EC%A1%B0%EC%9D%B8_%ED%99%95%EC%9E%A5_%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md)
- [4.2.1 SGA vs PGA](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.2.1_SGA_vs_PGA.md)
- [4.2.2 소트 머지 조인 기본 메커니즘](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.2.2_%EC%86%8C%ED%8A%B8_%EB%A8%B8%EC%A7%80_%EC%A1%B0%EC%9D%B8_%EA%B8%B0%EB%B3%B8_%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md)
- [4.2.3 소트 머지 조인이 빠른 이유](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.2.3_%EC%86%8C%ED%8A%B8_%EB%A8%B8%EC%A7%80_%EC%A1%B0%EC%9D%B8%EC%9D%B4_%EB%B9%A0%EB%A5%B8_%EC%9D%B4%EC%9C%A0.md)
- [4.2.4 소트 머지 조인의 주용도](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.2.4_%EC%86%8C%ED%8A%B8_%EB%A8%B8%EC%A7%80_%EC%A1%B0%EC%9D%B8%EC%9D%98_%EC%A3%BC%EC%9A%A9%EB%8F%84.md)
- [4.2.5 소트 머지 조인 제어하기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.2.5_%EC%86%8C%ED%8A%B8_%EB%A8%B8%EC%A7%80_%EC%A1%B0%EC%9D%B8_%EC%A0%9C%EC%96%B4%ED%95%98%EA%B8%B0.md)
- [4.2.6 소트 머지 조인 특징 요약](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.2.6_%EC%86%8C%ED%8A%B8_%EB%A8%B8%EC%A7%80_%EC%A1%B0%EC%9D%B8_%ED%8A%B9%EC%A7%95_%EC%9A%94%EC%95%BD.md)
- [4.3.1 해시 조인 기본 메커니즘](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.3.1_%ED%95%B4%EC%8B%9C_%EC%A1%B0%EC%9D%B8_%EA%B8%B0%EB%B3%B8_%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md)
- [4.3.2 해시 조인이 빠른 이유](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.3.2_%ED%95%B4%EC%8B%9C_%EC%A1%B0%EC%9D%B8%EC%9D%B4_%EB%B9%A0%EB%A5%B8_%EC%9D%B4%EC%9C%A0.md)
- [4.3.3 대용량 Build Input 처리](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.3.3_%EB%8C%80%EC%9A%A9%EB%9F%89_Build_Input_%EC%B2%98%EB%A6%AC.md)
- [4.3.4 해시 조인 실행계획 제어](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.3.4_%ED%95%B4%EC%8B%9C_%EC%A1%B0%EC%9D%B8_%EC%8B%A4%ED%96%89%EA%B3%84%ED%9A%8D_%EC%A0%9C%EC%96%B4.md)
- [4.3.5 조인 메소드 선택 기준](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.3.5_%EC%A1%B0%EC%9D%B8_%EB%A9%94%EC%86%8C%EB%93%9C_%EC%84%A0%ED%83%9D_%EA%B8%B0%EC%A4%80.md)
- [4.4.1 서브쿼리 변환이 필요한 이유](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.4.1_%EC%84%9C%EB%B8%8C%EC%BF%BC%EB%A6%AC_%EB%B3%80%ED%99%98%EC%9D%B4_%ED%95%84%EC%9A%94%ED%95%9C_%EC%9D%B4%EC%9C%A0.md)
- [4.4.2 서브쿼리와 조인](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.4.2_%EC%84%9C%EB%B8%8C%EC%BF%BC%EB%A6%AC%EC%99%80_%EC%A1%B0%EC%9D%B8.md)
- [4.4.3 뷰와 조인](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.4.3_%EB%B7%B0%EC%99%80_%EC%A1%B0%EC%9D%B8.md)
- [4.4.4 스칼라 서브쿼리 조인](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/04%EC%9E%A5/4.4.4_%EC%8A%A4%EC%B9%BC%EB%9D%BC_%EC%84%9C%EB%B8%8C%EC%BF%BC%EB%A6%AC_%EC%A1%B0%EC%9D%B8.md)

<div align="right">

⬅️ [3장. 인덱스 튜닝](#3장-인덱스-튜닝) &nbsp;|&nbsp; [🔝 장별 바로가기](#-장별-바로가기) &nbsp;|&nbsp; [5장. 소트 튜닝](#5장-소트-튜닝) ➡️

</div>

---

## 5장. 소트 튜닝

> 🗺️ **[5장 전체 흐름 한눈에 보기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5%EC%9E%A5_%EC%A0%84%EC%B2%B4_%ED%9D%90%EB%A6%84.md)**

- [5.1.1 소트 수행 과정](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.1.1_%EC%86%8C%ED%8A%B8_%EC%88%98%ED%96%89_%EA%B3%BC%EC%A0%95.md)
- [5.1.2 소트 오퍼레이션](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.1.2_%EC%86%8C%ED%8A%B8_%EC%98%A4%ED%8D%BC%EB%A0%88%EC%9D%B4%EC%85%98.md)
- [5.2.1 Union vs Union All](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.2.1_Union_vs_Union_All.md)
- [5.2.2 Exists 활용](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.2.2_Exists_%ED%99%9C%EC%9A%A9.md)
- [5.2.3 조인 방식 변경](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.2.3_%EC%A1%B0%EC%9D%B8_%EB%B0%A9%EC%8B%9D_%EB%B3%80%EA%B2%BD.md)
- [5.3.1 Sort Order By 생략](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.3.1_Sort_Order_By_%EC%83%9D%EB%9E%B5.md)
- [5.3.2 Top N 쿼리](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.3.2_Top_N_%EC%BF%BC%EB%A6%AC.md)
- [5.3.3 최소값 최대값 구하기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.3.3_%EC%B5%9C%EC%86%8C%EA%B0%92_%EC%B5%9C%EB%8C%80%EA%B0%92_%EA%B5%AC%ED%95%98%EA%B8%B0.md)
- [5.3.4 이력 조회](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.3.4_%EC%9D%B4%EB%A0%A5_%EC%A1%B0%ED%9A%8C.md)
- [5.3.5 Sort Group By 생략](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.3.5_Sort_Group_By_%EC%83%9D%EB%9E%B5.md)
- [5.4.1 소트 데이터 줄이기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.4.1_%EC%86%8C%ED%8A%B8_%EB%8D%B0%EC%9D%B4%ED%84%B0_%EC%A4%84%EC%9D%B4%EA%B8%B0.md)
- [5.4.2 Top N 쿼리의 소트 부하 경감 원리](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.4.2_Top_N_%EC%BF%BC%EB%A6%AC%EC%9D%98_%EC%86%8C%ED%8A%B8_%EB%B6%80%ED%95%98_%EA%B2%BD%EA%B0%90_%EC%9B%90%EB%A6%AC.md)
- [5.4.3 Top N 쿼리가 아닐 때 발생하는 소트 부하](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.4.3_Top_N_%EC%BF%BC%EB%A6%AC%EA%B0%80_%EC%95%84%EB%8B%90_%EB%95%8C_%EB%B0%9C%EC%83%9D%ED%95%98%EB%8A%94_%EC%86%8C%ED%8A%B8_%EB%B6%80%ED%95%98.md)
- [5.4.4 분석함수에서의 Top N 소트](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/05%EC%9E%A5/5.4.4_%EB%B6%84%EC%84%9D%ED%95%A8%EC%88%98%EC%97%90%EC%84%9C%EC%9D%98_Top_N_%EC%86%8C%ED%8A%B8.md)

<div align="right">

⬅️ [4장. 조인 튜닝](#4장-조인-튜닝) &nbsp;|&nbsp; [🔝 장별 바로가기](#-장별-바로가기) &nbsp;|&nbsp; [6장. DML 튜닝](#6장-dml-튜닝) ➡️

</div>

---

## 6장. DML 튜닝

> 🗺️ **[6장 전체 흐름 한눈에 보기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6%EC%9E%A5_%EC%A0%84%EC%B2%B4_%ED%9D%90%EB%A6%84.md)**

- [6.1.1 DML 성능에 영향을 미치는 요소](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.1.1_DML_%EC%84%B1%EB%8A%A5%EC%97%90_%EC%98%81%ED%96%A5%EC%9D%84_%EB%AF%B8%EC%B9%98%EB%8A%94_%EC%9A%94%EC%86%8C.md)
- [6.1.2 데이터베이스 Call과 성능](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.1.2_%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4_Call%EA%B3%BC_%EC%84%B1%EB%8A%A5.md)
- [6.1.3 Array Processing 활용](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.1.3_Array_Processing_%ED%99%9C%EC%9A%A9.md)
- [6.1.4 인덱스 및 제약 해제를 통한 대량 DML 튜닝](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.1.4_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EB%B0%8F_%EC%A0%9C%EC%95%BD_%ED%95%B4%EC%A0%9C%EB%A5%BC_%ED%86%B5%ED%95%9C_%EB%8C%80%EB%9F%89_DML_%ED%8A%9C%EB%8B%9D.md)
- [6.1.5 수정가능 조인 뷰](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.1.5_%EC%88%98%EC%A0%95%EA%B0%80%EB%8A%A5_%EC%A1%B0%EC%9D%B8_%EB%B7%B0.md)
- [6.1.6 MERGE 문 활용](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.1.6_MERGE_%EB%AC%B8_%ED%99%9C%EC%9A%A9.md)
- [6.2.1 Direct Path IO](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.2.1_Direct_Path_IO.md)
- [6.2.2 Direct Path Insert](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.2.2_Direct_Path_Insert.md)
- [6.2.3 병렬 DML](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.2.3_%EB%B3%91%EB%A0%AC_DML.md)
- [6.3.1 테이블 파티션](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.3.1_%ED%85%8C%EC%9D%B4%EB%B8%94_%ED%8C%8C%ED%8B%B0%EC%85%98.md)
- [6.3.2 인덱스 파티션](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.3.2_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%ED%8C%8C%ED%8B%B0%EC%85%98.md)
- [6.3.3 파티션을 활용한 대량 UPDATE 튜닝](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.3.3_%ED%8C%8C%ED%8B%B0%EC%85%98%EC%9D%84_%ED%99%9C%EC%9A%A9%ED%95%9C_%EB%8C%80%EB%9F%89_UPDATE_%ED%8A%9C%EB%8B%9D.md)
- [6.3.4 파티션을 활용한 대량 DELETE 튜닝](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.3.4_%ED%8C%8C%ED%8B%B0%EC%85%98%EC%9D%84_%ED%99%9C%EC%9A%A9%ED%95%9C_%EB%8C%80%EB%9F%89_DELETE_%ED%8A%9C%EB%8B%9D.md)
- [6.3.5 파티션을 활용한 대량 INSERT 튜닝](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.3.5_%ED%8C%8C%ED%8B%B0%EC%85%98%EC%9D%84_%ED%99%9C%EC%9A%A9%ED%95%9C_%EB%8C%80%EB%9F%89_INSERT_%ED%8A%9C%EB%8B%9D.md)
- [6.4.1 오라클 Lock](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.4.1_%EC%98%A4%EB%9D%BC%ED%81%B4_Lock.md)
- [6.4.2 트랜잭션 동시성 제어](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.4.2_%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98_%EB%8F%99%EC%8B%9C%EC%84%B1_%EC%A0%9C%EC%96%B4.md)
- [6.4.3 채번 방식에 따른 INSERT 성능 비교](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/06%EC%9E%A5/6.4.3_%EC%B1%84%EB%B2%88_%EB%B0%A9%EC%8B%9D%EC%97%90_%EB%94%B0%EB%A5%B8_INSERT_%EC%84%B1%EB%8A%A5_%EB%B9%84%EA%B5%90.md)

<div align="right">

⬅️ [5장. 소트 튜닝](#5장-소트-튜닝) &nbsp;|&nbsp; [🔝 장별 바로가기](#-장별-바로가기) &nbsp;|&nbsp; [7장. SQL 옵티마이저](#7장-sql-옵티마이저) ➡️

</div>

---

## 7장. SQL 옵티마이저

> 🗺️ **[7장 전체 흐름 한눈에 보기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7%EC%9E%A5_%EC%A0%84%EC%B2%B4_%ED%9D%90%EB%A6%84.md)**

- [7.1.1 선택도와 카디널리티](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7.1.1_%EC%84%A0%ED%83%9D%EB%8F%84%EC%99%80_%EC%B9%B4%EB%94%94%EB%84%90%EB%A6%AC%ED%8B%B0.md)
- [7.1.2 통계정보](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7.1.2_%ED%86%B5%EA%B3%84%EC%A0%95%EB%B3%B4.md)
- [7.1.3 비용 계산 원리](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7.1.3_%EB%B9%84%EC%9A%A9_%EA%B3%84%EC%82%B0_%EC%9B%90%EB%A6%AC.md)
- [7.2.1 옵티마이저 종류](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7.2.1_%EC%98%B5%ED%8B%B0%EB%A7%88%EC%9D%B4%EC%A0%80_%EC%A2%85%EB%A5%98.md)
- [7.2.2 옵티마이저 모드](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7.2.2_%EC%98%B5%ED%8B%B0%EB%A7%88%EC%9D%B4%EC%A0%80_%EB%AA%A8%EB%93%9C.md)
- [7.2.3 옵티마이저에 영향을 미치는 요소](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7.2.3_%EC%98%B5%ED%8B%B0%EB%A7%88%EC%9D%B4%EC%A0%80%EC%97%90_%EC%98%81%ED%96%A5%EC%9D%84_%EB%AF%B8%EC%B9%98%EB%8A%94_%EC%9A%94%EC%86%8C.md)
- [7.2.4 옵티마이저의 한계](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7.2.4_%EC%98%B5%ED%8B%B0%EB%A7%88%EC%9D%B4%EC%A0%80%EC%9D%98_%ED%95%9C%EA%B3%84.md)
- [7.2.5 개발자의 역할](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7.2.5_%EA%B0%9C%EB%B0%9C%EC%9E%90%EC%9D%98_%EC%97%AD%ED%95%A0.md)
- [7.2.6 튜닝 전문가 되는 공부방법](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/07%EC%9E%A5/7.2.6_%ED%8A%9C%EB%8B%9D_%EC%A0%84%EB%AC%B8%EA%B0%80_%EB%90%98%EB%8A%94_%EA%B3%B5%EB%B6%80%EB%B0%A9%EB%B2%95.md)

<div align="right">

⬅️ [6장. DML 튜닝](#6장-dml-튜닝) &nbsp;|&nbsp; [🔝 장별 바로가기](#-장별-바로가기) &nbsp;|&nbsp; [부록. 실행계획 분석 도구](#부록-실행계획-분석-도구) ➡️

</div>

---

## 부록. 실행계획 분석 도구

> 🗺️ **[부록 전체 흐름 한눈에 보기](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/%EB%B6%80%EB%A1%9D/%EB%B6%80%EB%A1%9D_%EC%A0%84%EC%B2%B4_%ED%9D%90%EB%A6%84.md)**

- [부록.1 실행계획 확인](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/%EB%B6%80%EB%A1%9D/%EB%B6%80%EB%A1%9D.1_%EC%8B%A4%ED%96%89%EA%B3%84%ED%9A%8D_%ED%99%95%EC%9D%B8.md)
- [부록.2 AutoTrace](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/%EB%B6%80%EB%A1%9D/%EB%B6%80%EB%A1%9D.2_AutoTrace.md)
- [부록.3 SQL 트레이스](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/%EB%B6%80%EB%A1%9D/%EB%B6%80%EB%A1%9D.3_SQL_%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%8A%A4.md)
- [부록.4 DBMS XPLAN 패키지](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/%EB%B6%80%EB%A1%9D/%EB%B6%80%EB%A1%9D.4_DBMS_XPLAN_%ED%8C%A8%ED%82%A4%EC%A7%80.md)
- [부록.5 실시간 SQL 모니터링](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/%EB%B6%80%EB%A1%9D/%EB%B6%80%EB%A1%9D.5_%EC%8B%A4%EC%8B%9C%EA%B0%84_SQL_%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81.md)
- [부록.6 VSQL](%EB%82%B4%EC%9A%A9%EC%A0%95%EB%A6%AC/%EB%B6%80%EB%A1%9D/%EB%B6%80%EB%A1%9D.6_VSQL.md)

<div align="right">

⬅️ [7장. SQL 옵티마이저](#7장-sql-옵티마이저) &nbsp;|&nbsp; [🔝 장별 바로가기](#-장별-바로가기)

</div>

---

## 🧭 그 밖의 자료

- [📖 전체 목차 — 전 챕터 계층 구조](%EC%B9%9C%EC%A0%88%ED%95%9C%20SQL%20%ED%8A%9C%EB%8B%9D%20%E2%80%94%20%EC%A0%84%EC%B2%B4%20%EB%AA%A9%EC%B0%A8.md)
- [🔎 절·페이지 인덱스](%EC%9D%B8%EB%8D%B1%EC%8A%A4/%EC%A0%88_%ED%8E%98%EC%9D%B4%EC%A7%80_%EC%9D%B8%EB%8D%B1%EC%8A%A4.md)
- [📝 전범위 연습문제 25문항](%EC%97%B0%EC%8A%B5%EB%AC%B8%EC%A0%9C/%EC%B9%9C%EC%A0%88%ED%95%9C%20SQL%20%ED%8A%9C%EB%8B%9D_%EC%A0%84%EB%B2%94%EC%9C%84_25%EB%AC%B8%ED%95%AD.md)
- [📚 연습문제 합본 (PDF)](%EC%97%B0%EC%8A%B5%EB%AC%B8%EC%A0%9C/%EC%97%B0%EC%8A%B5%EB%AC%B8%EC%A0%9C%20%ED%95%A9%EB%B3%B8.pdf)
- [🤖 학습 어시스턴트 지침](AGENTS.md)
