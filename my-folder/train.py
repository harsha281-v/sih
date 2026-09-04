from pathlib import Path

import numpy as np
import tensorflow as tf

from model import build_model
from preprocessing import (
    STATE_FEATURES,
    create_sequences,
    build_state_dataset,
    fit_scaler,
    load_and_clean,
    save_scaler,
)

SEQ_LEN = 10
CSV_PATH = Path("14-02-2018.csv")
MODEL_PATH = Path("lstm_model.keras")
SCALER_PATH = Path("scaler.pkl")


def main():
    print("Loading data...")
    df = load_and_clean(CSV_PATH)

    print("Building minute-level network states...")
    dataset = build_state_dataset(df)

    # For the prototype, keep the two continuous segments from
    # the notebook and fit ONE scaler on all training states.
    X_all = dataset[STATE_FEATURES].to_numpy(dtype=np.float32)

    X_scaled, scaler = fit_scaler(X_all)
    save_scaler(scaler, SCALER_PATH)

    X_seq, y_current_type, y_current_ratio, y_future_type, y_future_ratio = (
        create_sequences(X_scaled, dataset, SEQ_LEN)
    )

    if len(X_seq) == 0:
        raise ValueError("No sequences were created. Check the dataset.")

    print("X:", X_seq.shape)
    print("Current type:", y_current_type.shape)
    print("Current ratio:", y_current_ratio.shape)
    print("Future type:", y_future_type.shape)
    print("Future ratio:", y_future_ratio.shape)

    model = build_model(
        seq_len=SEQ_LEN,
        n_features=len(STATE_FEATURES),
    )

    model.summary()

    history = model.fit(
        X_seq,
        {
            "current_type": y_current_type,
            "current_ratio": y_current_ratio,
            "future_type": y_future_type,
            "future_ratio": y_future_ratio,
        },
        epochs=30,
        batch_size=32,
        shuffle=False,
    )

    model.save(MODEL_PATH)

    print(f"\nSaved model: {MODEL_PATH}")
    print(f"Saved scaler: {SCALER_PATH}")

    return history


if __name__ == "__main__":
    main()
