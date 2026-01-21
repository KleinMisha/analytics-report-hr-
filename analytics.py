"""
Helper functions to create the figures to be displayed in the PDF
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path
from typing import Any
import calendar
import webcolors  # type: ignore
from matplotlib.axes import Axes


TASK_CATEGORIES = ("coaching", "project lesson", "lecture (incl. prep)", "exam review")
COLORS = ["#46dabf", "#009ac9", "#ff6384", "#58508d", "#ffa600"]
sns.set_palette(COLORS)


# Functions called from Quarto document
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


def plot_pie_chart_activities(data: pd.DataFrame) -> None:
    """A pie chart showing the percentage of time spend on different activities"""

    # calculate totals per category
    hours_per_task = data.groupby("task")["hours"].sum()
    hours_per_task.sort_index(
        key=lambda x: pd.Index(TASK_CATEGORIES).get_indexer(x),
        inplace=True,
    )

    # data for in the pie chart
    tot_hours = sum(list(hours_per_task))
    percentages = [hrs / tot_hours * 100.0 for hrs in hours_per_task]
    tasks = list(hours_per_task.index)

    # build pie chart
    _, ax = plt.subplots(figsize=(8, 5))
    pie_chart_with_formatting(
        ax, percentages, tasks, threshold=10.0, text_pos=2.0, line_start_pos=1.0
    )

    plt.show()


def plot_pie_chart_days(data: pd.DataFrame) -> None:
    """A pie chart showing the percentage of time spend per weekday"""
    # calculate totals per weekday
    hours_per_day = data.groupby("day_abbrev")["hours"].sum()
    hours_per_day.sort_index(
        key=lambda x: pd.Index(list(calendar.day_abbr)).get_indexer(x), inplace=True
    )

    # data for in the pie chart
    tot_hours = sum(list(hours_per_day))
    percentages = [hrs / tot_hours * 100.0 for hrs in hours_per_day]
    weekdays = list(hours_per_day.index)

    # build pie chart
    _, ax = plt.subplots()
    pie_chart_with_formatting(
        ax, percentages, weekdays, threshold=10.0, text_pos=2.0, line_start_pos=1.0
    )

    plt.show()


def plot_monthly_hours_breakdown(data: pd.DataFrame) -> None:
    """A stacked bar chart showing per month the number of hours spent and the fraction of them spent on a certain activity"""

    # Calculate total hours for every task and month
    by_month_and_task = data.groupby(["month_abbrev", "task"])["hours"]
    totals = by_month_and_task.sum()

    # create a pivot-table
    df_totals = totals.unstack()

    # some cleaning: If task not occuring in a month, means zero hours spent on it
    df_totals.fillna(0.0, inplace=True)

    # place months in chronological order
    months_in_order = list(calendar.month_abbr)[1:]
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

    plt.xlabel("Month", fontsize=14)
    plt.ylabel("# hours", fontsize=14)
    plt.yticks([i * 5 for i in range(9)], fontsize=14)
    plt.xticks(fontsize=14)
    sns.despine()


def plot_daily_hours(data: pd.DataFrame) -> None:
    """A simple chart showing number of hours spent VS date"""
    # sum all tasks
    hours_per_day = data.groupby("date")["hours"].sum()
    date = pd.to_datetime(hours_per_day.index)

    # create the plot
    plt.stem(date, hours_per_day, basefmt="none")
    plt.xticks(fontsize=14, rotation=40)
    plt.yticks(fontsize=14)
    plt.ylabel("# hours", fontsize=14)
    plt.ylim(0, None)
    sns.despine()
    plt.show()


def bar_chart_monthly_incomes(data: pd.DataFrame, hourly_rate: int) -> None:
    """A horizontal bar chart showing the income, with the last month highlighted (and on top)"""

    hours_per_month = data.groupby(["month_abbrev"])["hours"].sum()
    hours_per_month.sort_index(
        key=lambda x: pd.Index(list(calendar.month_abbr)).get_indexer(x), inplace=True
    )
    months = list(hours_per_month.index)
    hours = list(hours_per_month.values)
    for n, hrs in enumerate(hours):
        income = calculate_income(hourly_rate, hrs)
        # the last month: fill the bar. Others leave showing only the outline.
        if n == len(hours) - 1:
            facecolor = COLORS[1]
        else:
            facecolor = "none"
        # simply add one bar at the time
        plt.barh(n, income, facecolor=facecolor, edgecolor="black", linewidth=2)
    plt.yticks(range(len(months)), months, fontsize=14)
    plt.xticks(fontsize=14)
    plt.xlabel("Earnings (€)", fontsize=14)
    sns.despine()


def create_html_monthly_incomes(
    data: pd.DataFrame, hourly_rate: int, text_format: dict[str, Any]
) -> str:
    """Show name of the month and the amount claimed at Hogeschool Rotterdam
    #! for this simple script: Just assume I do not forget to enter the dictionary properly. Would've used some dataclass or typed dictionary if this would be 'production' code.
    """
    hours_per_month = data.groupby(["month_abbrev"])["hours"].sum()
    hours_per_month.sort_index(
        key=lambda x: pd.Index(list(calendar.month_abbr)).get_indexer(x), inplace=True
    )
    months: list[str] = list(hours_per_month.index)
    hours: list[float] = list(hours_per_month.values)
    rows = []
    for i, (month, hrs) in enumerate(zip(months, hours)):
        if i == len(months) - 1:
            text_format.update({"color": COLORS[1]})
        else:
            text_format.update({"color": "black"})

        income = calculate_income(hourly_rate, hrs)
        rows.append(create_html_text(f"{month} \t €{income}", **text_format))
    html_table = "<br>".join(reversed(rows))
    return f"<div> {html_table}</div>"


def determine_project_period(data: pd.DataFrame) -> tuple[str, str]:
    """Finds and formats start-/end- dates of the project based on entered dates in dataset."""
    first_day: datetime = data["date"].min()
    last_day: datetime = data["date"].max()
    return first_day.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d")


def calculate_total_hours(data: pd.DataFrame) -> float:
    """Simply add together all hours spend"""
    return float(data["hours"].sum())


# Helper functions
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


def calculate_income(hourly_rate: int, hours_worked: float) -> float:
    return hourly_rate * hours_worked


def create_html_text(
    text: str,
    color: str = "#000000",
    size: int = 10,
    bold: bool = False,
    italic: bool = False,
) -> str:
    """Generate HTML for formatted text with some basic (not extensive) options"""

    # validate color:
    if not is_valid_html_color(color):
        raise ValueError(
            f"Unkown color: {color}. \n Enter either a HEX code [ex. #009ac9, #000000, etc.] \n or a known name from {webcolors.names()}"
        )

    # set options:
    weight = "bold" if bold else "normal"
    style = "italic" if italic else "normal"

    # build the HTML string
    adjust_color = f"color: {color}"
    adjust_size = f"font-size: {size}px"
    adjust_weight = f"font-weight: {weight}"
    adjust_style = f"font-style: {style};"
    formatting = (
        ";".join([adjust_color, adjust_size, adjust_weight, adjust_style])
        + "white-space: pre;"  # Apparently the thing that tells it to interpret the \t and \n as I'd like it.
    )
    return f'<div style="{formatting}">{text}</div>'


def is_valid_html_color(color: str) -> bool:
    """Check if entered color is a correct HEX code or a known name for a HTML/CSS color."""
    is_known_name = color in webcolors.names()
    is_hex = color.startswith("#") and len(color[1:]) == 6
    return is_known_name or is_hex


def pie_chart_with_formatting(
    ax: Axes,
    percentages: list[float],
    labels: list[str],
    threshold: float = 10.0,
    text_pos: float = 2.0,
    line_start_pos: float = 1.0,
) -> None:
    """
    A custom formatted pie chart
    ---
    * Display `percentages` of every slice in their wedge, if the wedge is large enough
    * For smaller wedges (percentage of total below given `threshold`), draw a indicator line and place text outside of wedge
    * Applies some additional styling for placing the labels with `text_pos` and `line_start_pos` both given as a fraction of the total figure
    """

    # ensure the same ordering in the colors/categories with other figures

    # Create plot
    wedges, *_ = ax.pie(
        percentages,
        labels=labels,
        autopct=lambda pct: custom_pct_formatting_rule(pct, threshold),
        shadow=True,
        startangle=90.0,
        radius=1.5,
        textprops={"size": 16, "color": "white", "weight": "bold"},
    )
    for wedge, pct in zip(wedges, percentages):
        if not is_large_slice(pct, threshold):
            # Get the angle at the middle of the wedge
            angle = (wedge.theta2 + wedge.theta1) / 2
            angle_rad = np.radians(angle)
            # center coordinate of the wedge (x,y), using polar coordinates
            x = np.cos(angle_rad)
            y = np.sin(angle_rad)

            # Add text annotation with a line
            ax.annotate(
                f"{pct:.1f}%",
                xy=(x * line_start_pos, y * line_start_pos),
                xytext=(x * text_pos, y * text_pos),
                fontsize=16,
                fontweight="bold",
                color="black",
                ha="left" if x > 0 else "right",
                va="center",
                arrowprops=dict(
                    arrowstyle="-", color="black", lw=1, connectionstyle="arc3,rad=0"
                ),
            )

    plt.legend(
        loc="center", bbox_to_anchor=(1.5, 1.0), fontsize=20, ncols=1, frameon=False
    )


def is_large_slice(percentage: float, threshold: float) -> bool:
    return percentage > threshold


def custom_pct_formatting_rule(percentage: float, threshold: float) -> str:
    """Only display the percentage the wedge represents if it exceeds a threshold value."""
    if is_large_slice(percentage, threshold):
        return f"{percentage:.1f}%"
    return ""
