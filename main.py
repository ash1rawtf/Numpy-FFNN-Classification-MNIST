from typing import Any

import numpy as np
import pandas as pd

import plots
from model import Model, ModelData

TEST_DATA_SPLIT = 2000
VAL_DATA_SPLIT = 6000


def one_hot_encoding(y: np.ndarray) -> np.ndarray:
    one_hot_y = np.zeros((y.size, np.max(y) + 1))
    one_hot_y[np.arange(y.size), y] = 1
    return one_hot_y


def get_data() -> tuple[np.ndarray, ...]:
    data = pd.read_csv("data/train.csv").to_numpy()

    test_data = data[:TEST_DATA_SPLIT]
    val_data = data[TEST_DATA_SPLIT : TEST_DATA_SPLIT + VAL_DATA_SPLIT]
    train_data = data[TEST_DATA_SPLIT + VAL_DATA_SPLIT :]

    x_train, y_train = train_data[:, 1:] / 255, train_data[:, 0]
    x_val, y_val = val_data[:, 1:] / 255, val_data[:, 0]
    x_test, y_test = test_data[:, 1:] / 255, test_data[:, 0]

    y_train = one_hot_encoding(y_train)
    y_val = one_hot_encoding(y_val)
    y_test = one_hot_encoding(y_test)

    return x_train, y_train, x_val, y_val, x_test, y_test


def test_models(
    data: tuple[np.ndarray, ...],
    comparable_attr_name: str,
    comparable_attr_list: list[Any],
    model_params: dict[str, str | int],
) -> list[ModelData]:
    models_data = []
    for comparable_attr in comparable_attr_list:
        model_params[comparable_attr_name] = comparable_attr

        model = Model(
            hidden_neurons_count=model_params["hidden_neurons_count"],
            hidden_activation_func=model_params["hidden_activation_func"],
            optimizer=model_params["optimizer"],
            learning_rate=model_params["learning_rate"],
            epochs=model_params["epochs"],
            batch_size=model_params["batch_size"],
        )

        model.calc_avarage(*data)
        models_data.append(model.model_data)
        del model

    return models_data


def main() -> None:
    x_train, y_train, x_val, y_val, x_test, y_test = get_data()

    model_w_nesterov = Model(
        hidden_neurons_count=25,
        hidden_activation_func="elu",
        optimizer="nesterov",
        learning_rate=0.05,
        epochs=250,
        batch_size=250,
    )
    model_w_nesterov.calc_avarage(x_train, y_train, x_val, y_val, x_test, y_test, 10)

    plots.plot_predictions(model_w_nesterov, x_test, y_test, np.random.randint(0, x_test.shape[-1], 10))

    # model_w_adam = Model(
    #     hidden_neurons_count=50,
    #     hidden_activation_func="elu",
    #     optimizer="adam",
    #     learning_rate=0.01,
    #     epochs=250,
    #     batch_size=100,
    # )
    # model_w_adam.calc_avarage(x_train, y_train, x_val, y_val, x_test, y_test, 10)
    #
    # plots.plot_predictions(model_w_adam, x_test, y_test, np.random.randint(0, x_test.shape[-1], 10))

    # models_data = test_models(
    #     (x_train, y_train, x_val, y_val, x_test, y_test, 10),
    #     comparable_attr_name="hidden_activation_func",
    #     comparable_attr_list=["sigmoid", "tanh", "relu", "leaky_relu", "elu"],
    #     model_params={
    #         "hidden_neurons_count": 10,
    #         "optimizer": "nesterov",
    #         "learning_rate": 0.05,
    #         "epochs": 250,
    #         "batch_size": 250,
    #     },
    # )
    #
    # plots.plot_train_and_val_loss_and_accuracy(models_data, "hidden_activation_func")
    # plots.plot_test_loss_and_accuracy(models_data, "hidden_activation_func")


if __name__ == "__main__":
    main()
