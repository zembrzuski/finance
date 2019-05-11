from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix as confusion
import src.service.file_io_service_for_machine_learning as ml_loader
import xgboost as xgb


def compute_accuracy(xg_reg, x, y):
    y_pred = xg_reg.predict(x)

    acertou = (y_pred > .5) == (y.as_matrix() > .5)
    numero_acertos = len(acertou[acertou])
    numero_erros = len(acertou) - numero_acertos

    return numero_acertos / (numero_acertos + numero_erros)


def main():
    # company_code = 'BBAS3.SA'
    company_code = 'PETR4.SA'

    historical_data = ml_loader.get_historical_data_for_ml(company_code)

    y = historical_data['label']
    x = historical_data.drop(columns=['label', 'Next_Day_Close', 'Date', 'Datee', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

    xg_reg = xgb.XGBRegressor(
        objective='reg:linear', colsample_bytree=0.3, learning_rate=0.1,
        max_depth=5, alpha=10, n_estimators=30)

    xg_reg.fit(x_train, y_train)

    print('train set accuracy: {}'.format(compute_accuracy(xg_reg, x_train, y_train)))
    print('test set accuracy: {}'.format(compute_accuracy(xg_reg, x_test, y_test)))

    print('finished')


if __name__ == '__main__':
    main()
