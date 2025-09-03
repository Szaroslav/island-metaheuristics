import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

RESULTS_PATH = os.path.join("..", "results")


def plot_scalefree_fitness(df: pd.DataFrame) -> None:
    """
    Plots the fitness of the scale-free topology model.
    """
    df = df[(df["number_of_islands"] == 500) & (df["topology"] == "scale_free")]

    group_cols = [
        "topology",
        "number_of_islands",
        "number_of_migrants",
        "migration_interval",
        "m0",
        "m",
    ]
    df_grouped = df.groupby(group_cols, as_index=False)["best"].mean()

    m_order = sorted(df_grouped["m"].unique())

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=df_grouped,
        x="m0",
        y="best",
        hue="m",
        hue_order=m_order,
        palette="viridis",
    )

    plt.title(
        "Jakość modelu topologii bezskalowej pogrupowana według m0\n"
            "(liczba wysp = 500)",
        fontsize=18,
        fontweight="bold",
    )
    plt.xlabel("m0", fontsize=15)
    plt.ylabel("Uśredniony najlepszy wynik [fitness]", fontsize=15)
    plt.legend(title="m")

    plt.tight_layout()

    plt.savefig(
        os.path.join(RESULTS_PATH, "plots", "scalefree_fitness_500.png"),
        dpi=200,
    )


def plot_complete_fitness(df: pd.DataFrame) -> None:
    """
    Plots the fitness of the complete topology model.
    """
    df = df[df["topology"] == "complete"]

    group_cols = [
        "topology",
        "number_of_islands",
        "number_of_migrants",
        "migration_interval",
    ]
    df_grouped = df.groupby(group_cols, as_index=False)["best"].mean()

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=df_grouped,
        x="number_of_islands",
        y="best",
        palette="viridis",
    )

    plt.title(
        "Jakość modelu topologii pełnej w zależności od liczby wysp",
        fontsize=18,
        fontweight="bold",
    )
    plt.xlabel("Liczba wysp", fontsize=15)
    plt.ylabel("Uśredniony najlepszy wynik [fitness]", fontsize=15)

    plt.tight_layout()

    plt.savefig(
        os.path.join(RESULTS_PATH, "plots", "complete_fitness.png"),
        dpi=200,
    )


def plot_scalefree_vs_complete_fitness_comparision(df: pd.DataFrame) -> None:
    """
    Plots the comparison of fitness between scale-free and complete topology
    models.
    """
    group_cols = [
        "topology",
        "number_of_islands",
        "number_of_migrants",
        "migration_interval",
        "m0",
        "m",
    ]
    df_grouped = df.groupby(group_cols, as_index=False)["best"].mean()

    group_cols = [
        "topology",
        "number_of_islands",
        "number_of_migrants",
        "migration_interval",
    ]
    indicies = df_grouped.groupby(group_cols)["best"].idxmin()
    df = df_grouped.loc[indicies] \
        .replace({"topology": {
            "scale_free": "Bezskalowa",
            "complete": "Pełna",
        }})

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=df,
        x="number_of_islands",
        y="best",
        hue="topology",
        palette="viridis",
    )

    plt.title(
        "Porównanie jakości topologii w zależności od liczby wysp",
        fontsize=18,
        fontweight="bold",
    )
    plt.xlabel("Liczba wysp", fontsize=15)
    plt.ylabel("Uśredniony najlepszy wynik [fitness]", fontsize=15)
    plt.legend(title="Topologia")

    plt.tight_layout()

    plt.savefig(
        os.path.join(RESULTS_PATH, "plots", "scalefree_vs_complete_fitness_comparison.png"),
        dpi=200,
    )


def plot_scalefree_vs_complete_time_comparison(df: pd.DataFrame) -> None:
    """
    Plots the comparison of execution time between scale-free and complete
    topology models.
    """
    df.replace({
        "topology": {
            "scale_free": "Bezskalowa",
            "complete": "Pełna",
        }}, inplace=True)

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=df,
        x="number_of_islands",
        y="execution_time",
        hue="topology",
        palette="viridis",
    )

    plt.title(
        "Porównanie wydajności topologii w zależności od liczby wysp",
        fontsize=18,
        fontweight="bold",
    )
    plt.xlabel("Liczba wysp", fontsize=15)
    plt.ylabel("Czas wykonywania najlepszej konfiguracji [s]", fontsize=15)
    plt.legend(title="Topologia")

    plt.tight_layout()

    plt.savefig(
        os.path.join(RESULTS_PATH, "plots", "scalefree_vs_complete_time_comparison.png"),
        dpi=200,
    )


if __name__ == "__main__":
    # Load CSVs
    df_fitn = pd.read_csv(os.path.join(RESULTS_PATH, "csv", "fitness.csv"))
    df_time = pd.read_csv(
        os.path.join(RESULTS_PATH, "csv", "execution_time.csv")
    )

    os.makedirs(os.path.join(RESULTS_PATH, "plots"), exist_ok=True)

    sns.set_theme(style="darkgrid")

    plot_scalefree_fitness(df_fitn)
    plot_complete_fitness(df_fitn)
    plot_scalefree_vs_complete_fitness_comparision(df_fitn)
    plot_scalefree_vs_complete_time_comparison(df_time)
