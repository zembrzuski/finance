import requests
import re

URL_MAGICA = "https://query1.finance.yahoo.com/v7/finance/quote?formatted=true&crumb=U4e8eDQi%2FyI&lang=en-US&region=US&symbols=GGBR4.SA&fields=messageBoardId%2ClongName%2CshortName%2CmarketCap%2CunderlyingSymbol%2CunderlyingExchangeSymbol%2CheadSymbolAsString%2CregularMarketPrice%2CregularMarketChange%2CregularMarketChangePercent%2CregularMarketVolume%2Cuuid%2CregularMarketOpen%2CfiftyTwoWeekLow%2CfiftyTwoWeekHigh&corsDomain=finance.yahoo.com"

def main():
    resp_content = requests.get('https://finance.yahoo.com/quote/PETR4.SA?p=PETR4.SA&.tsrc=fin-srch').content.decode('utf-8')
    match = re.match(r'.*26\.', resp_content)

    re.match(r'.*en-US', resp_content)

    re.match(r'.*26', 'gremio26tricolor26')

    resp_content

    if match:
        print('aer')

    print('oir')


if __name__ == '__main__':
    main()