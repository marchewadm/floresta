# Floresta - Django E-commerce Website

This project was developed as part of an assignment for the "Advanced Python Programming Techniques" course at my university. It was created from scratch by myself.

## Prerequisites

- Python 3.10 or higher

## Installation

```bash
git clone https://github.com/marchewadev/floresta.git
cd floresta
python -m venv venv
```

### Activate the virtual environment

- For Windows:

```bash
./venv/Scripts/Activate.ps1
```

- For Linux:

```bash
source /venv/Scripts/activate
```

### Install dependencies

```bash
pip install -r ./requirements.txt
```

## Usage

To run the Django development server, use the following command:

```bash
python floresta/manage.py runserver
```

On your first usage, you will also need to run migrations before running development server:

```bash
python floresta/manage.py makemigrations
python floresta/manage.py migrate
```

## Contributions and feedback

Feel free to explore the project and make any modifications as needed. If you encounter any issues or have suggestions for improvements, please don't hesitate to open an issue or submit a pull request. Happy coding!
