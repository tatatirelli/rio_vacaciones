from joblib import load

from src.model.model_factory import RioVacation

class RioVacationPredictor:
    def __init__(self, model_path):
        self.model = load(model_path)

    def predict(self, input_df) -> RioVacation:
        return self.model.predict(input_df)
