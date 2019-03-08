import requests
import re

URL_MAGICA = "https://query1.finance.yahoo.com/v7/finance/quote?formatted=true&crumb=U4e8eDQi%2FyI&" \
             "lang=en-US&region=US&symbols=" \
             "{}" \
             "&fields=messageBoardId%2ClongName%2CshortName%2CmarketCap%2CunderlyingSymbol%2CunderlyingExchangeSymbol%2CheadSymbolAsString%2CregularMarketPrice%2CregularMarketChange%2CregularMarketChangePercent%2CregularMarketVolume%2Cuuid%2CregularMarketOpen%2CfiftyTwoWeekLow%2CfiftyTwoWeekHigh&corsDomain=finance.yahoo.com"

def main():
    resp = requests.get(URL_MAGICA.format('PETR4.SA,GGBR4.SA')).json()

    print('oir')


if __name__ == '__main__':
    main()