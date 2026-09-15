import pandas as pd


def detect_revenue_leakage(file_path):
    df = pd.read_csv(file_path)

    # Calculate revenue efficiency
    df["revenue_per_request"] = (
        df["revenue"] / df["ad_requests"]
    )

    # Calculate eCPM
    df["ecpm"] = (
        df["revenue"] / df["impressions"] * 1000
    )

    # Identify high-traffic, low-monetization inventory
    request_threshold = df["ad_requests"].quantile(0.75)
    revenue_threshold = df["revenue"].quantile(0.25)

    leakage = df[
        (df["ad_requests"] >= request_threshold)
        & (df["revenue"] <= revenue_threshold)
    ].copy()

    leakage["issue"] = "High traffic but low revenue"

    return leakage.sort_values(
        "ad_requests",
        ascending=False
    )
