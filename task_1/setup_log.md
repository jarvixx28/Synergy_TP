# Setup Log

## Repository Setup

```bash
mkdir Synergy_TP
cd Synergy_TP
git init
```

## Folder Creation

```bash
mkdir task_1
mkdir task_2

mkdir task_1\src
mkdir task_1\data

mkdir task_2\src
mkdir task_2\data
mkdir task_2\output
```

## Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

## Package Installation

```bash
pip install requests
```

## Generate Requirements

```bash
pip freeze > task_1\requirements.txt
```

## Git Commands

```bash
git add .
git commit -m "Completed Task 1 setup"
git push
```