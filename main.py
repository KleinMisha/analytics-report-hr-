"""
Use the quarto CLI to render a PDF report
"""

from pathlib import Path
import subprocess
from dotenv import load_dotenv
import os
from datetime import datetime

# load environment variables
load_dotenv(".env")


# settings:
INPUT_FILE = "working_hours_report.qmd"
REPORTS_DIR = Path("./reports/")
BASE_FILE_NAME = "working_hours_report"

# parameters inside the markdown
HOURLY_RATE: int = int(os.getenv("HOURLY_RATE", 0.0))
DATA_PATH = (
    "/Users/misha/Documents/work/HSR_Rotterdam_minor_data_science/hours_worked.xlsx"
)


def main():
    today = datetime.today()
    filename = f"{today:%Y%m%d}_{BASE_FILE_NAME}.pdf"
    output = ["--output-dir", f"{REPORTS_DIR}", "--output", f"{filename}"]
    parameters = [
        "-P",
        f"hourly_rate:{HOURLY_RATE}",
        "-P",
        f"data_path:{DATA_PATH}",
    ]
    dont_clear_dir = ["--no-clean"]
    quarto_render = ["quarto", "render", INPUT_FILE]

    command = quarto_render + parameters + output + dont_clear_dir
    print(f"Running {' '.join(command)} ")
    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        print(
            f"\N{CHECK MARK} Successfully compiled {INPUT_FILE} \N{RIGHTWARDS ARROW} {REPORTS_DIR}/{filename}"
        )
    except subprocess.CalledProcessError as e:
        print(f"\N{CROSS MARK} Failed to compile {INPUT_FILE}")
        print(f"    Error message: {e.stderr}")


if __name__ == "__main__":
    main()
