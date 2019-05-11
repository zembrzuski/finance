from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix as confusion
import src.service.file_io_service_for_machine_learning as ml_loader
import xgboost as xgb
import sklearn.metrics as metrics


def compute_accuracy(xg_reg, x, y):
    y_pred = xg_reg.predict(x)

    acertou = (y_pred > .5) == (y.as_matrix() > .5)
    numero_acertos = len(acertou[acertou])
    numero_erros = len(acertou) - numero_acertos

    return numero_acertos / (numero_acertos + numero_erros)


def my_split(x, y, test_size):
    index = int(len(x) * (1-test_size))
    return x[0:index], x[index:-1], y[0:index], y[index:-1]


def do_lots_of_tests(x_train, x_test, y_train, y_test):
    results = open('results.txt', 'a')

    best_auc = -1

    for colsample in [0.1, 0.2, 0.3, 0.4, 0.5]:
        for depth in [2, 3, 4, 5, 6, 7, 8]:
            for alpha in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
                for estim in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
                    xg_reg = xgb.XGBRegressor(
                        objective='reg:linear', colsample_bytree=colsample, learning_rate=0.1,
                        max_depth=depth, alpha=alpha, n_estimators=estim)

                    xg_reg.fit(x_train, y_train)

                    auc = metrics.roc_auc_score(y_test, xg_reg.predict(x_test))

                    results.writelines([
                        'colsample {}'.format(colsample),
                        'depth {}'.format(depth),
                        'alpha {}'.format(alpha),
                        'estimators {}'.format(estim),
                        'auc {}'.format(auc),
                        '----------------',
                        ''
                    ])

                    if auc > best_auc:
                        best_auc = auc

                    print('actual auc: {}'.format(auc))
                    print('best auc: {}'.format(best_auc))
                    print('-----------------')

    results.close()


def do_simple_xgboost_regression(x_train, y_train, x_test, y_test):
    xg_reg = xgb.XGBRegressor(objective='reg:linear', colsample_bytree=0.3, learning_rate=0.1,
                              max_depth=5, alpha=10, n_estimators=10)

    xg_reg.fit(x_train, y_train)

    train_accuracy = compute_accuracy(xg_reg, x_train, y_train)
    test_accuracy = compute_accuracy(xg_reg, x_test, y_test)

    print('train set accuracy: {}'.format(train_accuracy))
    print('test set accuracy: {}'.format(test_accuracy))

    y_score = xg_reg.predict(x_test)

    score = metrics.roc_auc_score(y_test, y_score)
    print('score {}'.format(score))


def main():
    # company_code = 'BBAS3.SA'
    company_code = 'PETR4.SA'

    historical_data = ml_loader.get_historical_data_for_ml(company_code)

    y = historical_data['label']
    x = historical_data.drop(columns=[
        'label', 'Next_Day_Close', 'Date', 'Datee', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
    x_train, x_test, y_train, y_test = my_split(x, y, test_size=0.3)

    do_lots_of_tests(x_train, x_test, y_train, y_test)
    # do_simple_xgboost_regression(x_train, y_train, x_test, y_test)

    print('finished')


if __name__ == '__main__':
    main()
