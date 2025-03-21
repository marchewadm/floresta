# Floresta - Django E-commerce Website

This project was developed as part of an assignment for the *Advanced Python Programming Techniques* course at my university. It is one of the tasks required for the course, where the goal was to create a simple e-commerce website using Django, allowing users to browse products, add them to their cart, and place orders.

## Table of Contents

- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Running the Project without Docker](#running-the-project-without-docker)
  - [Running the Project via Docker](#running-the-project-via-docker)
- [Contributions and Feedback](#contributions-and-feedback)

## Demo

In a hurry? Watch a quick demo of the project below:

[Floresta Demo](https://github.com/marchewadev/floresta/assets/23455210/4f278c7a-afc4-4289-bb36-763863afdfa6)

## Prerequisites

- **Python 3.10** - required if running the project locally **without** Docker. If you don't have Python installed, you can download it from [here](https://www.python.org/downloads/). If you already have a different version of Python installed, and you encounter issues, try using [pyenv](https://github.com/pyenv/pyenv) (for macOS/Linux) or [pyenv-win](https://github.com/pyenv-win/pyenv-win) (for Windows) to install Python 3.10.
- **Docker** - optional, if you prefer running the project via Docker instead of manually setting up a local environment. You can download Docker from [here](https://docs.docker.com/get-started/get-docker/).

## Installation

Clone the repository:

```bash
git clone https://github.com/marchewadev/floresta.git
cd floresta
```
### Running the Project without Docker

#### Setup Virtual Environment (optional, but recommended)

If you want to run the project locally using a virtual environment, follow these steps:

1. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment:**

   - For **Windows**:

    ```bash
    .\venv\Scripts\activate
    ```

   - For **Linux/macOS**:

    ```bash
    source ./venv/bin/activate
    ```

#### Installing Dependencies

1. To install the required dependencies, run:

    ```bash
    pip install -r ./requirements.txt
    ```

#### Running the Django Development Server

1. **Run migrations** to set up the database:

    ```bash
    python floresta/manage.py makemigrations
    python floresta/manage.py migrate
    ```

2. **Create a superuser account** to access the Django admin panel:

    ```bash
    python floresta/manage.py createsuperuser
    ```

    (You'll be prompted to enter an email and password)

3. **Start the Django development server**:

    ```bash
    python floresta/manage.py runserver
    ```

    The development server should now be running at `http://127.0.0.1:8000/`.

### Running the Project via Docker

Alternatively, you can run the project using **Docker**. Follow the steps below to build and run the Docker container.

1. **Build the Docker image**:

    ```bash
    docker build -t django-app .
    ```

2. **Run the Docker container**:

    To run the container in the foreground (**default behavior**):

    ```bash
    docker run -p 8000:8000 django-app
    ```

    To run the container in the background (**detached mode**):

    ```bash
    docker run -d -p 8000:8000 django-app
    ```

    Running the container in detached mode allows you to close your terminal session while the app continues to run in the background. To stop the container when you're done, run:

    ```bash
    docker stop <container_id>
    ```

    You can find the container ID by running:

    ```bash
    docker ps
    ```

    This will list all running containers along with their IDs.


3. Open your browser and go to `http://127.0.0.1:8000/` to see the application in action.

4. The Docker container will automatically run migrations and create a superuser account (if not already created). The default admin credentials are:
    - **Email**: `admin@floresta.com`
    - **Password**: `admin`

## Contributions and feedback

Feel free to explore the project and make any modifications as needed. If you encounter any issues or have suggestions for improvements, please don't hesitate to open an issue or submit a pull request!
