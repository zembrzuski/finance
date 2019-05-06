from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix as confusion
import src.service.file_io_service_for_machine_learning as ml_loader


def main():
    company_code = 'BBAS3.SA'
    # company_code = 'PETR4.SA'

    historical_data = ml_loader.get_historical_data_for_ml(company_code)

    # print(historical_data['label'].value_counts())
    # sns.countplot(x='label', data=historical_data, palette='hls')
    # plt.show()
    # historical_data.groupby('label').mean()

    y = historical_data['label']
    X = historical_data.drop(columns=['label', 'Next_Day_Close', 'Date', 'Datee', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    # X = historical_data.drop(columns=['label', 'Next_Day_Close', 'Date', 'Datee', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)

    y_pred = logreg.predict(X_test)

    print('Accuracy of logistic regression classifier on train set: {:.2f}'.format(logreg.score(X_train, y_train)))
    print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

    confusion_matrix = confusion(y_test, y_pred)
    print(confusion_matrix)

    print('finished')


if __name__ == '__main__':
    main()
