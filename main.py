import numpy as np
import pandas as pd
from model import Model
from plots import plot_train_loss_and_accuracy

TEST_DATA_SPLIT = 2000


def one_hot_encoding(y: np.ndarray) -> np.ndarray:
    one_hot_y = np.zeros((y.size, np.max(y) + 1))
    one_hot_y[np.arange(y.size), y] = 1
    return one_hot_y


def get_data() -> tuple[np.ndarray, ...]:
    data = pd.read_csv("data/train.csv").to_numpy()

    train_data = data[TEST_DATA_SPLIT:]
    test_data = data[:TEST_DATA_SPLIT]

    x_train, y_train = train_data[:, 1:] / 255, train_data[:, 0]
    x_test, y_test = test_data[:, 1:] / 255, test_data[:, 0]

    y_train = one_hot_encoding(y_train)
    y_test = one_hot_encoding(y_test)

    return x_train, y_train, x_test, y_test


def main() -> None:
    x_train, y_train, x_test, y_test = get_data()

    model1 = Model(
        hidden_neurons_count=10, learning_rate=0.0001, epochs=100, batch_size=250
    )
    # model1.train_model(x_train, y_train)
    # model1.test_model(x_test, y_test)

    model1.calc_avarage(x_train, y_train, x_test, y_test, 5) 

    plot_train_loss_and_accuracy(
        (model1.model_data,),
        "learning_rate",
    )


if __name__ == "__main__":
    main()
