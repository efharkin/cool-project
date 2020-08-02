import matplotlib.pyplot as plt

from fetch_data import DataFetcher

SPREADSHEET_ID = 'secret'

def main():
    fetcher = DataFetcher(SPREADSHEET_ID, 'token.pickle', 'credentials.json')
    temperatures = fetcher.get_temperatures()

    ax = plt.subplot(111)
    for location in temperatures.iloc[:, 1].unique():
        subset = temperatures.loc[temperatures['Location'] == location, :]
        plt.plot(subset['Date'], subset['Temperature'], '.-', label=location)

    plt.ylim(15, 35)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Temperature (C)')
    plt.xlabel('Time')
    plt.legend()
    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    main()
