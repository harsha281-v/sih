from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf

from preprocessing import (
    STATE_FEATURES,
    build_state_dataset,
    load_and_clean,
    load_scaler,
)

SEQ_LEN = 10
MODEL_PATH = Path("lstm_model.keras")
SCALER_PATH = Path("scaler.pkl")

ID_TO_LABEL = {
    0: "Benign",
    1: "FTP-BruteForce",
    2: "SSH-Bruteforce",
}


def load_artifacts():
    model = tf.keras.models.load_model(MODEL_PATH)
    scaler = load_scaler(SCALER_PATH)
    return model, scaler


def predict_from_csv(csv_path):
    model, scaler = load_artifacts()

    df = load_and_clean(csv_path)
    dataset = build_state_dataset(df)

    if len(dataset) < SEQ_LEN:
        raise ValueError(
            f"Need at least {SEQ_LEN} minute states for prediction."
        )

    X = dataset[STATE_FEATURES].to_numpy(dtype=np.float32)
    X_scaled = scaler.transform(X)

    # Use the latest continuous segment only.
    latest_segment = dataset["Segment"].iloc[-1]
    mask = dataset["Segment"].to_numpy() == latest_segment

    X_latest = X_scaled[mask]

    if len(X_latest) < SEQ_LEN:
        raise ValueError(
            "The latest continuous segment is shorter than SEQ_LEN."
        )

    X_input = X_latest[-SEQ_LEN:].reshape(
        1, SEQ_LEN, len(STATE_FEATURES)
    )

    outputs = model.predict(X_input, verbose=0)

    current_type_probs = outputs[0][0]
    current_ratio = float(outputs[1][0, 0])
    future_type_probs = outputs[2][0]
    future_ratio = float(outputs[3][0, 0])

    current_type_id = int(np.argmax(current_type_probs))
    future_type_id = int(np.argmax(future_type_probs))

    return {
        "current_attack_type": ID_TO_LABEL[current_type_id],
        "current_attack_probability": float(
            current_type_probs[current_type_id]
        ),
        "current_attack_ratio": current_ratio,
        "future_attack_type": ID_TO_LABEL[future_type_id],
        "future_attack_probability": float(
            future_type_probs[future_type_id]
        ),
        "future_attack_ratio": future_ratio,
    }


if __name__ == "__main__":
    result = predict_from_csv("14-02-2018.csv")
    for key, value in result.items():
        print(f"{key}: {value}")
