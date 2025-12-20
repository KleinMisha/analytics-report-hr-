"""
Helper functions to create the figures to be displayed in the PDF
"""

import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path
import calendar


TASK_CATEGORIES = ("coaching", "lecture", "exam review")
COLORS = ["#46dabf", "#9f7ae7", "#da3e94"]
COLORS = ["#46dabf", "#00a9ff", "#9f7ae7"]
sns.set_palette(COLORS)


def prepare_data(path: Path) -> pd.DataFrame:
    """load the data, do some needed cleaning steps"""
    # load the data:
    df = pd.read_excel(path)  # type: ignore

    # convert column to datetime objects
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    dates = list(df["date"])

    # add the name of the day and month
    month_names, month_abbrevs = get_month_names(dates)
    day_names, day_abbrevs = get_day_names(dates)
    df["month_name"] = month_names
    df["month_abbrev"] = month_abbrevs
    df["day_name"] = day_names
    df["day_abbrev"] = day_abbrevs

    # simplify task categories
    df["task"] = clean_task_names(list(df["task"]))
    return df


def clean_task_names(tasks: list[str]) -> list[str]:
    """Simplify the task string to create a category out of it"""
    return [categorize_task(task) for task in tasks]


def categorize_task(task: str) -> str:
    """Simplify the task string to create a category out of it"""
    for category in TASK_CATEGORIES:
        if has_matching_word(task, category):
            return category
    return "other"


def is_known_category(task: str) -> bool:
    """Checks if any of the words in the task description match any of the words in the possible categories"""
    return any(
        has_matching_word(task, known_category) for known_category in TASK_CATEGORIES
    )


def has_matching_word(string_1: str, string_2: str) -> bool:
    """Checks if the two strings have (at least) a word in common"""
    words = string_1.split(" ")
    words_to_match = string_2.split(" ")
    return any(word in words_to_match for word in words)


def get_month_names(dates: list[datetime]) -> tuple[list[str], list[str]]:
    """determine the name of the month (and it's abbreviation)"""
    month_names = [calendar.month_name[date.month] for date in dates]
    month_abbrevs = [calendar.month_abbr[date.month] for date in dates]
    return month_names, month_abbrevs


def get_day_names(dates: list[datetime]) -> tuple[list[str], list[str]]:
    """determine the name of the day (and it's abbreviation)"""
    day_names = [calendar.day_name[date.weekday()] for date in dates]
    day_abbrevs = [calendar.day_abbr[date.weekday()] for date in dates]
    return day_names, day_abbrevs


def plot_pie_chart_activities(data: pd.DataFrame) -> None:
    """A pie chart showing the percentage of time spend on different activities"""

    # calculate totals per category
    totals = data.groupby("task")["hours"].sum()

    # ensure the same ordering in the colors/categories with other figures
    totals.sort_index(
        key=lambda x: pd.Index(TASK_CATEGORIES).get_indexer(x),
        inplace=True,
    )

    # Create plot
    plt.pie(
        totals,
        labels=totals.index,
        autopct="%1.1f%%",
        shadow=True,
        explode=[0.0, 0.0, 0.4],
        startangle=90,
        radius=1.8,
        textprops={"size": 11, "color": "white", "weight": "bold"},
    )
    plt.legend(loc="center", bbox_to_anchor=(0.5, -0.4), fontsize=12, ncols=3)
    plt.show()


def plot_monthly_hours_breakdown(data: pd.DataFrame) -> None:
    """A stacked bar chart showing per month the number of hours spent and the fraction of them spent on a certain activity"""

    # Calculate total hours for every task and month
    by_month_and_task = data.groupby(["month_name", "task"])["hours"]
    totals = by_month_and_task.sum()

    # create a pivot-table
    df_totals = totals.unstack()

    # some cleaning: If task not occuring in a month, means zero hours spent on it
    df_totals.fillna(0.0, inplace=True)

    # place months in chronological order
    months_in_order = list(calendar.month_name)[1:]
    df_totals = df_totals.sort_index(
        key=lambda x: pd.Index(months_in_order).get_indexer(x)
    )

    # make the plot
    _, ax = plt.subplots()
    previous_category = None
    for category in TASK_CATEGORIES:
        start_bar_from = df_totals[previous_category] if previous_category else None
        ax.bar(
            df_totals.index, df_totals[category], bottom=start_bar_from, label=category
        )
        previous_category = category

    plt.legend()
    plt.xlabel("Month", fontsize=14)
    plt.ylabel("# hours", fontsize=14)
    plt.yticks([i * 5 for i in range(9)], fontsize=14)
    plt.xticks(fontsize=14)
    sns.despine()


def plot_daily_hours(data: pd.DataFrame) -> None:
    """A simple chart showing number of hours spent VS date"""


def display_monthly_income(data: pd.DataFrame) -> None:
    """Show name of the moth and the amount claimed at Hogeschool Rotterdam"""


def calculate_income(hourly_rate: float, hours_worked: int) -> float:
    return hourly_rate * hours_worked


def determine_project_duration(data: pd.DataFrame) -> tuple[datetime, datetime]:
    """Find earliest and latest entry dates"""
    ...
