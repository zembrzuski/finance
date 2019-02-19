import requests
import service.file_io_service as file_io_service


def download_from_yahoo(company_code, cookie):
    # TODO - periodo 1 e periodo 2 estão chumbados no código. Tenho que fazer
    # TODO - um codigo que seja capaz de ser dinâmico para pegar a cotacao do dia.
    url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=950666400&period2=1550282400&interval=1d&events=history&crumb=fXcQRHMnGlU'.format(company_code)
    headers = {'cookie': cookie}
    response = requests.get(url, headers=headers).content.decode('utf-8')

    return response


def main():
    company_code = 'PETR4.SA'
    cookie = 'B=718jeftdruunv&b=3&s=ai; GUCS=AW-GqzEF; GUC=AQEBAQFcabldQUIesATu&s=AQAAAPu4-aZf&g=XGh1CA'

    cotacoes_csv = download_from_yahoo(company_code, cookie)
    file_io_service.persist_file(company_code, cotacoes_csv)

    return True


if __name__ == '__main__':
    """
    Script responsible for downloading and persisting prices from yahoo to local storage.
    """
    main()
    print('done')
