import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class LGDValidator:

    def basic_metrics(self, y_true, y_pred):
        mae = np.mean(np.abs(y_true - y_pred))
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))

        return {
            "MAE": mae,
            "RMSE": rmse,
            "Mean Actual": np.mean(y_true),
            "Mean Predicted": np.mean(y_pred)
        }

    def distribution_comparison(self, y_true, y_pred, bins=50):

        plt.figure(figsize=(10,5))
        plt.hist(y_true, bins=bins, alpha=0.5, label="Actual")
        plt.hist(y_pred, bins=bins, alpha=0.5, label="Predicted")
        plt.title("LGD Distribution Comparison")
        plt.legend()
        plt.show()

    def segment_analysis(self, df, y_true, y_pred, segment_col):

        df_temp = df.copy()
        df_temp['actual'] = y_true
        df_temp['predicted'] = y_pred

        result = df_temp.groupby(segment_col)[['actual','predicted']].mean()

        return result

    def stability_check(self, y_train_true, y_train_pred, y_test_true, y_test_pred):

        train_mean = np.mean(y_train_pred)
        test_mean = np.mean(y_test_pred)

        return {
            "Train Mean LGD": train_mean,
            "Test Mean LGD": test_mean,
            "Drift": abs(train_mean - test_mean)
        }