import pandas as pd


def calculate_kpis(file_path):
    df = pd.read_csv(file_path)

    # Calculate key programmatic advertising KPIs
    total_requests = df["ad_requests"].sum()
    total_responses = df["responses"].sum()
    total_wins = df["wins"].sum()
    total_impressions = df["impressions"].sum()
    total_revenue = df["revenue"].sum()

    fill_rate = (total_responses / total_requests) * 100
    win_rate = (total_wins / total_responses) * 100
    ctr = (df["clicks"].sum() / total_impressions) * 100
    ecpm = (total_revenue / total_impressions) * 1000
    revenue_per_request = total_revenue / total_requests

    return {
        "Total Ad Requests": total_requests,
        "Total Responses": total_responses,
        "Fill Rate (%)": round(fill_rate, 2),
        "Total Wins": total_wins,
        "Win Rate (%)": round(win_rate, 2),
        "Total Impressions": total_impressions,
        "CTR (%)": round(ctr, 2),
        "eCPM": round(ecpm, 2),
        "Revenue": round(total_revenue, 2),
        "Revenue per Request": round(revenue_per_request, 6)
    }
