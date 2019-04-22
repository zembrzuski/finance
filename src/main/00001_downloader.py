import src.config.basic_config as config
import src.service.yahoo_historical_importer as historical_importer


def main():
    companies_chunks = [
        config.companies[x:x + config.chunk_size]
        for x in range(0, len(config.companies), config.chunk_size)]

    historical_importer.import_historical_data(companies_chunks)


if __name__ == '__main__':
    # TODO COMECAR A TESTAR ESSA BAGAÇA.
    main()
