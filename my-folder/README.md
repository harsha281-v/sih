# SIH26153 ML module

Files:
- model.py: defines the multi-output LSTM.
- preprocessing.py: reproduces the notebook's flow -> minute-state -> target pipeline.
- train.py: trains and saves the model and scaler.
- predict.py: loads the saved artifacts and forecasts the latest window.
- explain.py: gradient-based feature importance for the future attack-ratio output.

Run:
    python train.py

This creates:
    scaler.pkl
    lstm_model.keras

Important:
The notebook uses TensorFlow/Keras, so the native model artifact is `.keras`, not `.pth`.
A `.pth` file is normally a PyTorch model checkpoint. Do not rename `.keras` to `.pth`.
