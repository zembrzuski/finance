from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix as confusion
import src.service.file_io_service_for_machine_learning as ml_loader
import xgboost as xgb


def main():
    # company_code = 'BBAS3.SA'
    company_code = 'PETR4.SA'

    historical_data = ml_loader.get_historical_data_for_ml(company_code)

    y = historical_data['label']
    X = historical_data.drop(columns=['label', 'Next_Day_Close', 'Date', 'Datee', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    xg_reg = xgb.XGBRegressor(objective='reg:linear', colsample_bytree=0.3, learning_rate=0.1,
                              max_depth=5, alpha=6, n_estimators=10)

    xg_reg.fit(X_train, y_train)

    y_pred = xg_reg.predict(X_test)

    acertou = (y_pred > .5) == (y_test.as_matrix() > .5)
    numero_acertos = len(acertou[acertou])
    numero_erros = len(acertou) - numero_acertos

    print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(numero_acertos/(numero_acertos+numero_erros)))
    # print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(xg_reg.score(X_test, y_test)))

    # confusion_matrix = confusion(y_test, y_pred)
    # print(confusion_matrix)

    print('finished')


if __name__ == '__main__':
    main()
