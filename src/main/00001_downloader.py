import requests
import src.service.file_io_service as file_io_service


def download_from_yahoo(company_code, cookie):
    # TODO - periodo 1 e periodo 2 estão chumbados no código. Tenho que fazer
    # TODO - um codigo que seja capaz de ser dinâmico para pegar a cotacao do dia.
    url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=946692000&period2=1550804400&interval=1d&events=history&crumb=U4e8eDQi/yI'.format(company_code)
    headers = {'cookie': cookie}
    response = requests.get(url, headers=headers).content.decode('utf-8')

    return response


def main():
    ativos = ["ABEV3.SA",
              "B3SA3.SA",
              "BBAS3.SA",
              "BBDC3.SA",
              "BBDC4.SA",
              "BBSE3.SA",
              "BRAP4.SA",
              "BRDT3.SA",
              "BRFS3.SA",
              "BRKM5.SA",
              "BRML3.SA",
              "BTOW3.SA",
              "CCRO3.SA",
              "CIEL3.SA",
              "CMIG4.SA",
              "CSAN3.SA",
              "CSNA3.SA",
              "CVCB3.SA",
              "CYRE3.SA",
              "ECOR3.SA",
              "EGIE3.SA",
              "ELET3.SA",
              "ELET6.SA",
              "EMBR3.SA",
              "ENBR3.SA",
              "EQTL3.SA",
              "ESTC3.SA",
              "FLRY3.SA",
              "GGBR4.SA",
              "GOAU4.SA",
              "GOLL4.SA",
              "HYPE3.SA",
              "IGTA3.SA",
              "ITSA4.SA",
              "ITUB4.SA",
              "JBSS3.SA",
              "KLBN11.SA",
              "KROT3.SA",
              "LAME4.SA",
              "LOGG3.SA",
              "LREN3.SA",
              "MGLU3.SA",
              "MRFG3.SA",
              "MRVE3.SA",
              "MULT3.SA",
              "NATU3.SA",
              "PCAR4.SA",
              "PETR3.SA",
              "PETR4.SA",
              "QUAL3.SA",
              "RADL3.SA",
              "RAIL3.SA",
              "RENT3.SA",
              "SANB11.SA",
              "SBSP3.SA",
              "SMLS3.SA",
              "SUZB3.SA",
              "TAEE11.SA",
              "TIMP3.SA",
              "UGPA3.SA",
              "USIM5.SA",
              "VALE3.SA",
              "VIVT4.SA",
              "VVAR3.SA",
              "WEGE3.SA"]

    for company_code in ativos:
        # cookie = 'B=718jeftdruunv&b=3&s=ai; GUCS=AW-GqzEF; GUC=AQEBAQFcabldQUIesATu&s=AQAAAPu4-aZf&g=XGh1CA'
        cookie = 'B=dm28aetdpvite&b=3&s=c2; GUCS=AZv5cK6w; GUC=AQEBAQFccXhdTkIhOAUC&s=AQAAALqIZ67s&g=XHAxPA; PRF=t%3DPETR4.SA'

        cotacoes_csv = download_from_yahoo(company_code, cookie)
        file_io_service.persist_file(company_code, cotacoes_csv)

    return True


if __name__ == '__main__':
    """
    Script responsible for downloading and persisting prices from yahoo to local storage.
    """
    main()
    print('done')
