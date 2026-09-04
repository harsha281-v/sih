import numpy as np
import tensorflow as tf

from model import build_model
from preprocessing import STATE_FEATURES


def gradient_feature_importance(model, X):
    """
    Simple model-agnostic-in-spirit gradient saliency for the
    future attack-ratio output.

    X shape: (batch, seq_len, n_features)
    Returns mean absolute gradient per feature.
    """
    X_tensor = tf.convert_to_tensor(X, dtype=tf.float32)

    with tf.GradientTape() as tape:
        tape.watch(X_tensor)
        outputs = model(X_tensor, training=False)
        future_ratio = outputs[3]

    gradients = tape.gradient(future_ratio, X_tensor)
    importance = tf.reduce_mean(tf.abs(gradients), axis=[0, 1])

    scores = importance.numpy()

    return sorted(
        zip(STATE_FEATURES, scores),
        key=lambda x: x[1],
        reverse=True,
    )


if __name__ == "__main__":
    print(
        "Use gradient_feature_importance(model, X) after loading "
        "your trained model and a scaled sequence batch."
    )
