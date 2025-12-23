#  📝 PDF Analytics report.
Create a PDF report summarizing my activities for the Hogeschool Rotterdam.

![Example](example_output.png "Rendered output (with income/earnings omitted from this image)")


# 💡 What I learned. 
Main purpose is to document my activities and the amount I should claim per month. Especially since I might declare my working hours some time after the project. Having this document serves as a little backup, just in case there is ever some doubt on what activities I performed (do not expect this to ever occur). 

Mostly, I wanted to learn how to generate PDF documents with values/graphs computed using Python. 
Making this report might not have been strictly necessary, but it taught me some valuable tooling. 

---
![skyblue](https://img.shields.io/badge/Note-skyblue?style=flat&logo=appveyor&logoColor=white)

Given this is an extremely simple project, I did not include any tests and placed almost everything in the project's root directory. I simply do not expect this project to every grow. If it does, then I'd reorganize some files and such. 



# 🛠️ Tools 
💻 **Programming Language:** `Python`, `Typst` (see below). <br>
📦 **Dependency Management:** `uv`. <br>
📝 **Document Creation:** `Quarto`, `Typst`. <br>
🔒 **Secrets:** Hourly rate / Income (using Python's  `dotenv` package)<br>


# Installation & Usage 
1. Clone this repository 

2. Install the [VSCode quarto extension](https://quarto.org/docs/get-started/hello/vscode.html)
3. Install the [quarto CLI](). (`main.py` calls the `quarto render` command)
    On macOS, simple installation via Homebrew
    ```{bash}
    brew install quarto
    ```
4. Install `uv` (see [documentation](https://docs.astral.sh/uv/#installation))
5. Install dependencies
    
    ```{bash}
    uv run python main.py
    ```

    This will automatically take care of building the virtual environment using the specifications in the `pyproject.toml` file.
6. Output is written into `reports/` (under `.gitignore`).

---

![skyblue](https://img.shields.io/badge/Note-skyblue?style=flat&logo=appveyor&logoColor=white)

⚠️ Quarto will ask you to first install some `LaTex` engine and `papermill`. Simply follow the instructions shown on screen.

```{bash}
quarto install tinytex
```
and 
```{bash}
quarto install papermill
```


Then run the python code again 
```
uv run python main.py
```

or, after activating the environment manually (shown here for MacOS)
```
source .venv/bin/activate
python main.py
```

