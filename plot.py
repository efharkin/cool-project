import matplotlib.pyplot as plt
import seaborn as sns

from fetch_data import DataFetcher


def main():
    with open('secrets/spreadsheet_id.txt', 'r') as f:
        SPREADSHEET_ID = f.readline().strip()
        f.close()

    fetcher = DataFetcher(
        SPREADSHEET_ID, 'secrets/token.pickle', 'secrets/credentials.json'
    )
    temperatures = fetcher.get_temperatures()
    events = fetcher.get_events()

    ax = plt.subplot(111)
    BORDER_HEIGHT = 0.01
    BAR_HEIGHT = 0.04
    for i, eventtype in enumerate(events['Event'].unique()):
        for j, (_, event) in enumerate(
            events.loc[events['Event'] == eventtype, :].iterrows()
        ):
            if j == 0:
                ax.axvspan(
                    event['StartDate'],
                    event['EndDate'],
                    ymin=1 - BAR_HEIGHT * (i + 1) + BORDER_HEIGHT,
                    ymax=1 - BAR_HEIGHT * i - BORDER_HEIGHT,
                    color=sns.color_palette()[i],
                    label=eventtype,
                )
            else:
                ax.axvspan(
                    event['StartDate'],
                    event['EndDate'],
                    ymin=1 - BAR_HEIGHT * (i + 1) + BORDER_HEIGHT,
                    ymax=1 - BAR_HEIGHT * i - BORDER_HEIGHT,
                    color=sns.color_palette()[i],
                )

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
