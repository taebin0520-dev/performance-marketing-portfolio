# 광고 성과 분석 스크립트
# 목적: 캠페인별/채널별 CTR, CPC, CVR, CPA, ROAS 계산 및 개선안 도출

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 한글 폰트 설정 (Windows: 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ── 데이터 로드 ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'ad_performance_data.csv'))
df['date'] = pd.to_datetime(df['date'])

print("=" * 60)
print("  광고 성과 분석 포트폴리오")
print("=" * 60)
print(f"\n분석 기간: {df['date'].min().date()} ~ {df['date'].max().date()}")
print(f"총 레코드 수: {len(df)}건\n")

# ── 핵심 마케팅 지표 계산 ────────────────────────────────────────────────────
df['CTR'] = df['clicks'] / df['impressions'] * 100          # 클릭률 (%)
df['CPC'] = df['cost'] / df['clicks']                        # 클릭당 비용 (원)
df['CVR'] = df['conversions'] / df['clicks'] * 100          # 전환율 (%)
df['CPA'] = df['cost'] / df['conversions']                   # 전환당 비용 (원)
df['ROAS'] = df['revenue'] / df['cost'] * 100                # 광고비 대비 수익률 (%)

print("── 지표 설명 ──────────────────────────────────────────────")
print("CTR  = 클릭 수 / 노출 수 × 100  → 광고가 얼마나 눈길을 끄는지")
print("CPC  = 비용 / 클릭 수            → 클릭 한 번에 드는 비용")
print("CVR  = 전환 수 / 클릭 수 × 100  → 클릭 후 실제 구매 비율")
print("CPA  = 비용 / 전환 수            → 고객 한 명 확보에 드는 비용")
print("ROAS = 수익 / 비용 × 100        → 투자한 광고비 대비 회수율")
print()

# ── 채널별 성과 요약 ──────────────────────────────────────────────────────────
channel_summary = df.groupby('channel').agg(
    총노출수=('impressions', 'sum'),
    총클릭수=('clicks', 'sum'),
    총비용=('cost', 'sum'),
    총전환수=('conversions', 'sum'),
    총수익=('revenue', 'sum')
).reset_index()

channel_summary['CTR(%)'] = (channel_summary['총클릭수'] / channel_summary['총노출수'] * 100).round(2)
channel_summary['CPC(원)'] = (channel_summary['총비용'] / channel_summary['총클릭수']).round(0).astype(int)
channel_summary['CVR(%)'] = (channel_summary['총전환수'] / channel_summary['총클릭수'] * 100).round(2)
channel_summary['CPA(원)'] = (channel_summary['총비용'] / channel_summary['총전환수']).round(0).astype(int)
channel_summary['ROAS(%)'] = (channel_summary['총수익'] / channel_summary['총비용'] * 100).round(1)

print("── 채널별 성과 요약 ─────────────────────────────────────────")
print(channel_summary[['channel', 'CTR(%)', 'CPC(원)', 'CVR(%)', 'CPA(원)', 'ROAS(%)']].to_string(index=False))
print()

# ── 캠페인별 성과 요약 ────────────────────────────────────────────────────────
campaign_summary = df.groupby('campaign').agg(
    총비용=('cost', 'sum'),
    총전환수=('conversions', 'sum'),
    총수익=('revenue', 'sum')
).reset_index()

campaign_summary['CPA(원)'] = (campaign_summary['총비용'] / campaign_summary['총전환수']).round(0).astype(int)
campaign_summary['ROAS(%)'] = (campaign_summary['총수익'] / campaign_summary['총비용'] * 100).round(1)
campaign_summary = campaign_summary.sort_values('ROAS(%)', ascending=False)

print("── 캠페인별 ROAS 순위 ───────────────────────────────────────")
print(campaign_summary[['campaign', '총비용', '총전환수', 'CPA(원)', 'ROAS(%)']].to_string(index=False))
print()

# ── 인사이트 및 개선안 ────────────────────────────────────────────────────────
best_roas = channel_summary.loc[channel_summary['ROAS(%)'].idxmax()]
worst_cpa = channel_summary.loc[channel_summary['CPA(원)'].idxmax()]
best_cvr = channel_summary.loc[channel_summary['CVR(%)'].idxmax()]

print("── 분석 인사이트 ────────────────────────────────────────────")
print(f"ROAS 최고 채널: {best_roas['channel']} ({best_roas['ROAS(%)']}%)")
print(f"   → 이 채널 예산을 우선 확대 검토")
print()
print(f"CPA 가장 높은 채널: {worst_cpa['channel']} (CPA {worst_cpa['CPA(원)']:,}원)")
print(f"   → 랜딩페이지 개선 또는 타겟 정교화 필요")
print()
print(f"전환율 최고 채널: {best_cvr['channel']} (CVR {best_cvr['CVR(%)']}%)")
print(f"   → 광고 소재·메시지가 타겟과 잘 맞음. 유사 타겟 확장 검토")
print()

# ── 시각화 저장 ───────────────────────────────────────────────────────────────
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('채널별 핵심 광고 성과 지표', fontsize=14, fontweight='bold')

channels = channel_summary['channel']
colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B2']

axes[0].bar(channels, channel_summary['ROAS(%)'], color=colors)
axes[0].set_title('ROAS (%) - 높을수록 좋음')
axes[0].set_ylabel('ROAS (%)')
axes[0].tick_params(axis='x', rotation=20)

axes[1].bar(channels, channel_summary['CPA(원)'], color=colors)
axes[1].set_title('CPA (원) - 낮을수록 효율적')
axes[1].set_ylabel('CPA (원)')
axes[1].tick_params(axis='x', rotation=20)

axes[2].bar(channels, channel_summary['CVR(%)'], color=colors)
axes[2].set_title('CVR (%) - 높을수록 좋음')
axes[2].set_ylabel('CVR (%)')
axes[2].tick_params(axis='x', rotation=20)

plt.tight_layout()
output_path = os.path.join(IMAGES_DIR, 'channel_performance.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"차트 저장 완료: {output_path}")
plt.close()

print("\n분석 완료.")
