# iRoute proof of concept

## Overview
This repository contains the source code for a iRoute. The system aims to provide route planning, real-time tracking, and other useful features for users relying on public transportation. The project is built using Django, incorporating machine learning models for prediction and optimization.

## Getting Started

### Prerequisites
- Ensure you have Python installed on your system.
- Install required Python packages: `pip install -r requirements.txt`

### Running the Application
1. Navigate to the project directory.
2. Run the Django development server: `python manage.py runserver`
3. Access the application through the provided local address (usually `http://127.0.0.1:8000/`).

### Understanding manage.py
The `manage.py` script is a command-line utility provided by Django for various tasks, including running the development server, applying database migrations, and creating administrative users. For example, to start the development server, you can use the command: `python manage.py runserver`.

### Machine Learning Models
- `pred.ipynb`: This Jupyter Notebook contains the code for training the three different machine learning models used in the project. It covers the training process for prediction and optimization tasks.

### Dataset Generation
- `data_gen.py`: This Python script is responsible for generating datasets used during the training of the machine learning models. It ensures the availability of diverse and relevant data for effective model training.

### Additional Files
- The remaining files in the repository are test data files utilized during the development and testing phases of the project.

