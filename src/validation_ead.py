import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class EADValidator:

    def basic_metrics(self, y_true, y_pred):
        mae = np.mean(np.abs(y_true - y_pred))
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
        bias = np.mean(y_true - y_pred)

        return {
            "MAE": mae,
            "RMSE": rmse,
            "Bias": bias,
            "Mean Actual": np.mean(y_true),
            "Mean Predicted": np.mean(y_pred)
        }

    def distribution_comparison(self, y_true, y_pred, bins=50):

        plt.figure(figsize=(10,5))
        plt.hist(y_true, bins=bins, alpha=0.5, label="Actual")
        plt.hist(y_pred, bins=bins, alpha=0.5, label="Predicted")
        plt.title("EAD Distribution Comparison")
        plt.legend()
        plt.show()

    def utilization_behavior(self, funded_amount, y_pred):

        ccf_pred = y_pred / funded_amount

        return {
            "Mean Predicted CCF": np.mean(ccf_pred),
            "Max Predicted CCF": np.max(ccf_pred),
            "Min Predicted CCF": np.min(ccf_pred)
        }

    def stability_check(self, y_train_pred, y_test_pred):

        train_mean = np.mean(y_train_pred)
        test_mean = np.mean(y_test_pred)

        return {
            "Train Mean EAD": train_mean,
            "Test Mean EAD": test_mean,
            "Drift": abs(train_mean - test_mean)
        }