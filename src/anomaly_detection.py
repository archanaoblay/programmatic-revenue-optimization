import pandas as pd


def detect_anomalies(file_path):
    df = pd.read_csv(file_path)

    # Calculate daily revenue
    daily_revenue = (
        df.groupby("date")["revenue"]
        .sum()
        .reset_index()
    )

    # Calculate baseline statistics
    mean_revenue = daily_revenue["revenue"].mean()
    std_revenue = daily_revenue["revenue"].std()

    # Define anomaly boundaries
    upper_limit = mean_revenue + (2 * std_revenue)
    lower_limit = mean_revenue - (2 * std_revenue)

    # Identify unusual revenue days
    anomalies = daily_revenue[
        (daily_revenue["revenue"] > upper_limit)
        | (daily_revenue["revenue"] < lower_limit)
    ].copy()

    anomalies["anomaly_type"] = anomalies["revenue"].apply(
        lambda x: "Unusually High Revenue"
        if x > upper_limit
        else "Unusually Low Revenue"
    )

    return anomalies.sort_values("revenue")
