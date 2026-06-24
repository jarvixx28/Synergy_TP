# Task 1: GitHub, Virtual Environment, and Linux Basics

## Description
This task demonstrates Git repository setup, Python virtual environments, package management, and basic Linux command usage.

## Project Structure

task_1/
├── README.md
├── requirements.txt
├── setup_log.md
├── linux_commands.md
├── src/
│   └── hello.py
└── data/
    └── sample.txt

## Setup Instructions

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r task_1/requirements.txt
```

## Run Program

From the repository root:

```bash
python task_1/src/hello.py
```