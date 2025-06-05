from market import LabourABM, plot_history


def main() -> None:
    configuration = {}

    abm = LabourABM(configuration, 365)
    abm.load(configuration)
    abm.run()
    market_data = abm.collect()
    plot_history(market_data)


if __name__ == "main":
    main()
