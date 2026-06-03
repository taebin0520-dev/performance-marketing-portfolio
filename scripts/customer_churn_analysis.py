# 고객 이탈 분석 스크립트 (RFM 기반)
# 목적: 마지막 구매일·구매 빈도·구매 금액으로 이탈 위험 고객 분류 및 CRM 전략 제안

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ── 데이터 로드 ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'customer_data.csv'))
df['signup_date'] = pd.to_datetime(df['signup_date'])
df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'])

# 분석 기준일 (데이터 최신 날짜 기준)
REFERENCE_DATE = pd.Timestamp('2024-03-31')

print("=" * 60)
print("  고객 이탈 분석 포트폴리오 (RFM 분석)")
print("=" * 60)
print(f"\n기준일: {REFERENCE_DATE.date()}")
print(f"총 고객 수: {len(df)}명\n")

# ── RFM 계산 ──────────────────────────────────────────────────────────────────
# R (Recency): 마지막 구매 이후 경과 일수 → 낮을수록 최근 고객
# F (Frequency): 총 구매 횟수 → 높을수록 충성 고객
# M (Monetary): 총 구매 금액 → 높을수록 고가치 고객
df['Recency'] = (REFERENCE_DATE - df['last_purchase_date']).dt.days
df['Frequency'] = df['purchase_count']
df['Monetary'] = df['total_amount']

print("── RFM 지표 설명 ────────────────────────────────────────────")
print("R (Recency)   : 마지막 구매 후 며칠이 지났는지 (적을수록 활성)")
print("F (Frequency) : 총 구매 횟수 (많을수록 충성)")
print("M (Monetary)  : 총 구매 금액 (클수록 고가치)")
print()

# ── 30/60/90일 기준 이탈 위험 분류 ────────────────────────────────────────────
def classify_churn_risk(days):
    if days <= 30:
        return '활성 고객'
    elif days <= 60:
        return '30일 비활성'
    elif days <= 90:
        return '60일 비활성'
    else:
        return '이탈 위험'

df['churn_risk'] = df['Recency'].apply(classify_churn_risk)

churn_counts = df['churn_risk'].value_counts()
print("── 이탈 위험 고객 분류 결과 ─────────────────────────────────")
for category, count in churn_counts.items():
    pct = count / len(df) * 100
    print(f"  {category:15s}: {count}명 ({pct:.1f}%)")
print()

# 이탈 위험 고객 상세
at_risk = df[df['churn_risk'] == '이탈 위험'][['customer_id', 'name', 'Recency', 'Frequency', 'Monetary', 'product_category']]
at_risk = at_risk.sort_values('Monetary', ascending=False)
print("── 이탈 위험 고객 상세 (구매 금액 상위순) ──────────────────")
print(at_risk.to_string(index=False))
print()

# ── RFM 점수 산정 (1~3점, 간단 버전) ──────────────────────────────────────────
df['R_score'] = pd.cut(df['Recency'], bins=[0, 30, 90, 999], labels=[3, 2, 1])
df['F_score'] = pd.cut(df['Frequency'], bins=[0, 4, 9, 999], labels=[1, 2, 3])
df['M_score'] = pd.cut(df['Monetary'], bins=[0, 299999, 699999, 9999999], labels=[1, 2, 3])
df['RFM_score'] = df['R_score'].astype(int) + df['F_score'].astype(int) + df['M_score'].astype(int)

# ── 고객 세그먼트 분류 ────────────────────────────────────────────────────────
def segment(row):
    if row['RFM_score'] >= 8:
        return 'VIP 고객'
    elif row['RFM_score'] >= 6:
        return '우수 고객'
    elif row['R_score'] == 1:
        return '이탈 위험'
    else:
        return '일반 고객'

df['segment'] = df.apply(segment, axis=1)

seg_summary = df.groupby('segment').agg(
    고객수=('customer_id', 'count'),
    평균구매금액=('Monetary', 'mean'),
    평균구매횟수=('Frequency', 'mean'),
    평균Recency=('Recency', 'mean')
).round(1)

print("── 고객 세그먼트 분석 ───────────────────────────────────────")
print(seg_summary.to_string())
print()

# ── CRM 캠페인 제안 ───────────────────────────────────────────────────────────
print("── CRM 캠페인 제안 ──────────────────────────────────────────")
print("VIP 고객     → 프리미엄 멤버십 초대, 신제품 선공개, 전용 할인")
print("우수 고객    → 재구매 쿠폰, 리뷰 이벤트, 포인트 적립 강조")
print("이탈 위험    → 15% 할인 쿠폰 + '보고 싶어요' 이메일/카카오 발송")
print("일반 고객    → 카테고리별 맞춤 추천 + 신규 프로모션 안내")
print()

# ── 시각화 저장 ───────────────────────────────────────────────────────────────
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('고객 이탈 분석 (RFM 기반)', fontsize=13, fontweight='bold')

# 이탈 위험 분류 파이차트
colors_pie = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
axes[0].pie(churn_counts.values, labels=churn_counts.index,
            autopct='%1.1f%%', colors=colors_pie, startangle=90)
axes[0].set_title('이탈 위험 단계별 고객 비율')

# 세그먼트별 평균 구매 금액
seg_plot = df.groupby('segment')['Monetary'].mean().sort_values(ascending=False)
axes[1].bar(seg_plot.index, seg_plot.values, color=['#3498db', '#2ecc71', '#e74c3c', '#95a5a6'])
axes[1].set_title('세그먼트별 평균 구매 금액 (원)')
axes[1].set_ylabel('평균 구매 금액 (원)')
axes[1].tick_params(axis='x', rotation=15)

plt.tight_layout()
output_path = os.path.join(IMAGES_DIR, 'customer_churn_analysis.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"차트 저장 완료: {output_path}")
plt.close()

print("\n분석 완료.")
