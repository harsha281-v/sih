import tensorflow as tf

NUM_CLASSES = 3


def build_model(seq_len: int, n_features: int) -> tf.keras.Model:
    inputs = tf.keras.Input(
        shape=(seq_len, n_features),
        name="network_sequence",
    )

    x = tf.keras.layers.LSTM(64, name="lstm")(inputs)
    x = tf.keras.layers.Dropout(0.2, name="dropout")(x)

    current_type = tf.keras.layers.Dense(
        NUM_CLASSES, activation="softmax", name="current_type"
    )(x)

    current_ratio = tf.keras.layers.Dense(
        1, activation="sigmoid", name="current_ratio"
    )(x)

    future_type = tf.keras.layers.Dense(
        NUM_CLASSES, activation="softmax", name="future_type"
    )(x)

    future_ratio = tf.keras.layers.Dense(
        1, activation="sigmoid", name="future_ratio"
    )(x)

    model = tf.keras.Model(
        inputs=inputs,
        outputs=[
            current_type,
            current_ratio,
            future_type,
            future_ratio,
        ],
    )

    model.compile(
        optimizer="adam",
        loss={
            "current_type": "sparse_categorical_crossentropy",
            "current_ratio": "mse",
            "future_type": "sparse_categorical_crossentropy",
            "future_ratio": "mse",
        },
        metrics={
            "current_type": "accuracy",
            "current_ratio": "mae",
            "future_type": "accuracy",
            "future_ratio": "mae",
        },
    )

    return model
