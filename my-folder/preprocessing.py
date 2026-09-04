from pathlib import Path
import pickle

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


LABEL_MAP = {
    "Benign": 0,
    "FTP-BruteForce": 1,
    "SSH-Bruteforce": 2,
}

STATE_FEATURES = [
    "flow_count",
    "total_packets",
    "total_bytes",
    "mean_duration",
    "median_duration",
    "std_duration",
    "mean_fwd_packets",
    "median_fwd_packets",
    "mean_bwd_packets",
    "median_bwd_packets",
    "mean_fwd_bytes",
    "median_fwd_bytes",
    "mean_bwd_bytes",
    "median_bwd_bytes",
    "mean_packets_per_sec",
    "median_packets_per_sec",
    "std_packets_per_sec",
    "mean_bytes_per_sec",
    "median_bytes_per_sec",
    "std_bytes_per_sec",
    "mean_packet_size",
    "median_packet_size",
    "std_packet_size",
    "mean_IAT",
    "median_IAT",
    "std_IAT",
    "unique_destination_ports",
    "syn_rate",
    "rst_rate",
    "ack_rate",
    "fin_rate",
    "tcp_flow_ratio",
    "udp_flow_ratio",
    "icmp_flow_ratio",
]

CONSTANT_COLS = [
    "Bwd PSH Flags",
    "Fwd URG Flags",
    "Bwd URG Flags",
    "CWE Flag Count",
    "Fwd Byts/b Avg",
    "Fwd Pkts/b Avg",
    "Fwd Blk Rate Avg",
    "Bwd Byts/b Avg",
    "Bwd Pkts/b Avg",
    "Bwd Blk Rate Avg",
    "Init Fwd Win Byts",
    "Init Bwd Win Byts",
]


def load_and_clean(csv_path):
    df = pd.read_csv(csv_path)

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce",
    )

    bad_timestamp_mask = df["Timestamp"].dt.year < 2018
    df = df.loc[~bad_timestamp_mask].copy()

    df = df.replace([np.inf, -np.inf], np.nan)

    # Keep the same label definitions used in the notebook.
    df = df[df["Label"].isin(LABEL_MAP)].copy()
    df["Label_ID"] = df["Label"].map(LABEL_MAP)

    existing_constant_cols = [
        c for c in CONSTANT_COLS if c in df.columns
    ]
    df = df.drop(columns=existing_constant_cols)

    df = df.sort_values("Timestamp").reset_index(drop=True)
    df["TimeWindow"] = df["Timestamp"].dt.floor("min")

    return df


def build_state_dataset(df):
    df_state = df.copy()

    df_state["Total_Packets"] = (
        df_state["Tot Fwd Pkts"] + df_state["Tot Bwd Pkts"]
    )
    df_state["Total_Bytes"] = (
        df_state["TotLen Fwd Pkts"] + df_state["TotLen Bwd Pkts"]
    )

    state = df_state.groupby("TimeWindow").agg(
        flow_count=("TimeWindow", "size"),
        total_packets=("Total_Packets", "sum"),
        total_bytes=("Total_Bytes", "sum"),
        mean_duration=("Flow Duration", "mean"),
        median_duration=("Flow Duration", "median"),
        std_duration=("Flow Duration", "std"),
        mean_fwd_packets=("Tot Fwd Pkts", "mean"),
        median_fwd_packets=("Tot Fwd Pkts", "median"),
        mean_bwd_packets=("Tot Bwd Pkts", "mean"),
        median_bwd_packets=("Tot Bwd Pkts", "median"),
        mean_fwd_bytes=("TotLen Fwd Pkts", "mean"),
        median_fwd_bytes=("TotLen Fwd Pkts", "median"),
        mean_bwd_bytes=("TotLen Bwd Pkts", "mean"),
        median_bwd_bytes=("TotLen Bwd Pkts", "median"),
        mean_packets_per_sec=("Flow Pkts/s", "mean"),
        median_packets_per_sec=("Flow Pkts/s", "median"),
        std_packets_per_sec=("Flow Pkts/s", "std"),
        mean_bytes_per_sec=("Flow Byts/s", "mean"),
        median_bytes_per_sec=("Flow Byts/s", "median"),
        std_bytes_per_sec=("Flow Byts/s", "std"),
        mean_packet_size=("Pkt Len Mean", "mean"),
        median_packet_size=("Pkt Len Mean", "median"),
        std_packet_size=("Pkt Len Mean", "std"),
        mean_IAT=("Flow IAT Mean", "mean"),
        median_IAT=("Flow IAT Mean", "median"),
        std_IAT=("Flow IAT Mean", "std"),
        unique_destination_ports=("Dst Port", "nunique"),
    )

    flags = df_state.groupby("TimeWindow").agg(
        syn_rate=("SYN Flag Cnt", lambda x: (x > 0).mean()),
        rst_rate=("RST Flag Cnt", lambda x: (x > 0).mean()),
        ack_rate=("ACK Flag Cnt", lambda x: (x > 0).mean()),
        fin_rate=("FIN Flag Cnt", lambda x: (x > 0).mean()),
    )

    protocols = df_state.groupby("TimeWindow").agg(
        tcp_flow_ratio=("Protocol", lambda x: (x == 6).mean()),
        udp_flow_ratio=("Protocol", lambda x: (x == 17).mean()),
        icmp_flow_ratio=("Protocol", lambda x: (x == 1).mean()),
    )

    state = state.join(flags).join(protocols)

    label_counts = (
        df_state.groupby("TimeWindow")["Label"]
        .value_counts()
        .unstack(fill_value=0)
    )

    for label in LABEL_MAP:
        if label not in label_counts.columns:
            label_counts[label] = 0

    label_counts["Attack_Count"] = (
        label_counts["FTP-BruteForce"]
        + label_counts["SSH-Bruteforce"]
    )

    label_counts["Total_Flows"] = label_counts[
        ["Benign", "FTP-BruteForce", "SSH-Bruteforce"]
    ].sum(axis=1)

    label_counts["Current_Attack_Type"] = "Benign"
    attack_mask = label_counts["Attack_Count"] > 0

    label_counts.loc[attack_mask, "Current_Attack_Type"] = (
        label_counts.loc[
            attack_mask,
            ["FTP-BruteForce", "SSH-Bruteforce"],
        ].idxmax(axis=1)
    )

    label_counts["Attack_Ratio"] = (
        label_counts["Attack_Count"] / label_counts["Total_Flows"]
    )

    dataset = state.join(
        label_counts[
            ["Attack_Ratio", "Current_Attack_Type"]
        ]
    )

    # Prevent a future target from crossing a time gap.
    dataset["Segment"] = (
        dataset.index.to_series()
        .diff()
        .gt(pd.Timedelta(minutes=1))
        .cumsum()
    )

    dataset["Future_Attack_Ratio"] = (
        dataset.groupby("Segment")["Attack_Ratio"].shift(-1)
    )
    dataset["Future_Attack_Type"] = (
        dataset.groupby("Segment")["Current_Attack_Type"].shift(-1)
    )

    dataset = dataset.dropna(
        subset=["Future_Attack_Ratio", "Future_Attack_Type"]
    )

    return dataset


def create_sequences(X, df, seq_len=10):
    X_seq = []
    y_current_type = []
    y_current_ratio = []
    y_future_type = []
    y_future_ratio = []

    # Sequence construction is performed inside each segment so
    # no sequence can cross a timestamp gap.
    for _, group in df.groupby("Segment", sort=False):
        indices = group.index
        if len(indices) <= seq_len:
            continue

        X_group = X[df.index.get_indexer(indices)]

        for i in range(seq_len, len(group)):
            X_seq.append(X_group[i-seq_len:i])

            row = group.iloc[i]
            y_current_type.append(LABEL_MAP[row["Current_Attack_Type"]])
            y_current_ratio.append(row["Attack_Ratio"])
            y_future_type.append(LABEL_MAP[row["Future_Attack_Type"]])
            y_future_ratio.append(row["Future_Attack_Ratio"])

    return (
        np.asarray(X_seq, dtype=np.float32),
        np.asarray(y_current_type, dtype=np.int64),
        np.asarray(y_current_ratio, dtype=np.float32),
        np.asarray(y_future_type, dtype=np.int64),
        np.asarray(y_future_ratio, dtype=np.float32),
    )


def fit_scaler(X):
    scaler = StandardScaler()
    return scaler.fit_transform(X), scaler


def save_scaler(scaler, path="scaler.pkl"):
    with open(path, "wb") as f:
        pickle.dump(scaler, f)


def load_scaler(path="scaler.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)
