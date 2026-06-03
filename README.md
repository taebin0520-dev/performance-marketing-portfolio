# 강태빈 퍼포먼스 마케팅 포트폴리오

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8+-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> **아토모스 주니어 퍼포먼스 마케터** 지원을 위해 제작한 데이터 분석 포트폴리오입니다.  
> 광고 성과 지표(CTR·CPC·CVR·CPA·ROAS) 분석부터 고객 이탈 예측(RFM), 키워드 전략까지 실무 중심으로 구성했습니다.

---

## 포트폴리오 구성

| # | 프로젝트 | 핵심 기술 | 파일 |
|---|---------|----------|------|
| 1 | 광고 성과 분석 | CTR, CPC, CVR, CPA, ROAS, Matplotlib | [scripts/ad_performance_analysis.py](scripts/ad_performance_analysis.py) |
| 2 | 고객 이탈 분석 | RFM 분석, 세그먼트, CRM 전략 | [scripts/customer_churn_analysis.py](scripts/customer_churn_analysis.py) |
| 3 | 검색광고 키워드 전략 | SKAG 구조, 품질지수, 입찰 전략 | [reports/keyword_strategy_report.md](reports/keyword_strategy_report.md) |

---

## 주요 분석 결과

### 1. 광고 성과 분석 (2024년 1~3월)

4개 채널 × 5개 캠페인 데이터 분석

| 채널 | ROAS | CPA | CVR |
|------|------|-----|-----|
| 카카오 디스플레이 | **451%** | 4,421원 | 4.52% |
| 구글 GDN | 440% | 4,535원 | 4.41% |
| 구글 검색 | 400% | 6,146원 | **4.88%** |
| 네이버 검색 | 396% | 6,200원 | 4.81% |

**인사이트:** 카카오 디스플레이 ROAS 451%로 최고 효율 → 예산 비중 확대 제안  
리마케팅 캠페인 ROAS 465%로 캠페인 중 1위 → 재노출 전략 유효성 검증

### 2. 고객 이탈 분석 (RFM 기반)

40명 고객 데이터 분석 (기준일: 2024-03-31)

| 세그먼트 | 고객 수 | 비율 | CRM 전략 |
|---------|--------|------|---------|
| 활성 고객 | 18명 | 45% | 재구매 유도 쿠폰 |
| 30일 비활성 | 7명 | 17.5% | 맞춤 추천 이메일 |
| 60일 비활성 | 5명 | 12.5% | 할인 리마케팅 광고 |
| 이탈 위험 | 10명 | 25% | 15% 할인쿠폰 + 카카오 메시지 |

### 3. 검색광고 키워드 전략

- SKAG 방식 캠페인 구조 설계
- 구매 의도별 4단계 키워드 분류 및 입찰 전략
- 품질지수 관리 체크리스트 제공
- 월간 키워드 관리 루틴 포함

---

## 빠른 시작

```bash
# 1. 저장소 클론
git clone https://github.com/taebin0520-dev/performance-marketing-portfolio.git
cd performance-marketing-portfolio

# 2. 패키지 설치
pip install pandas numpy matplotlib

# 3. 광고 성과 분석 실행
python scripts/ad_performance_analysis.py

# 4. 고객 이탈 분석 실행
python scripts/customer_churn_analysis.py
```

실행 후 `images/` 폴더에 차트 파일이 자동 저장됩니다.

---

## 디렉토리 구조

```
performance-marketing-portfolio/
├── data/
│   ├── ad_performance_data.csv      # 광고 성과 데이터 (캠페인×채널×일자)
│   └── customer_data.csv            # 고객 구매 이력 데이터
├── scripts/
│   ├── ad_performance_analysis.py   # 광고 성과 분석 (CTR/CPC/CVR/CPA/ROAS)
│   └── customer_churn_analysis.py   # 고객 이탈 분석 (RFM 세그먼트)
├── reports/
│   ├── ad_performance_report.md     # 광고 성과 분석 리포트
│   └── keyword_strategy_report.md   # 검색광고 키워드 전략 리포트
├── images/                          # 분석 차트 (스크립트 실행 시 자동 생성)
├── notebooks/                       # Jupyter 노트북 (추가 예정)
└── docs/                            # 추가 문서
```

---

## 핵심 마케팅 지표

```
CTR  (클릭률)    = 클릭수 / 노출수 × 100
CPC  (클릭당비용) = 비용 / 클릭수
CVR  (전환율)    = 전환수 / 클릭수 × 100
CPA  (전환당비용) = 비용 / 전환수
ROAS (광고수익률) = 수익 / 비용 × 100
```

---

## 기술 스택

- **언어:** Python 3.10+
- **라이브러리:** Pandas, NumPy, Matplotlib
- **분석 기법:** RFM 분석, 코호트 분석 (예정), SKAG 키워드 구조

---

## 관련 문서

- [광고 성과 분석 리포트](reports/ad_performance_report.md)
- [검색광고 키워드 전략 리포트](reports/keyword_strategy_report.md)

---

*강태빈 | taebin0520@gmail.com | 퍼포먼스 마케팅 포트폴리오*
