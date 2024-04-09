# Storompt Server

## Installation Guide

### Prerequisites
- Python (version 3.6 or higher) installed on your system.
- PostgreSQL (version 9.5 or higher) installed and running.
- pip package manager installed.

### Setup

1. Clone the repository:
   ```shell
   git clone https://github.com/TaylonChan/storompt_server.git
   cd storompt_server
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```shell
   python3 -m venv env
   source env/bin/activate
   ```

3. Install project dependencies:
   ```shell
   pip install -r requirements.txt
   ```

4. Create a PostgreSQL database for the project:
   - Open the PostgreSQL shell:
     ```shell
     psql
     ```

   - Create the database:
     ```sql
     CREATE DATABASE storompt;
     ```

   - Create a database user and grant permissions:
     ```sql
     CREATE USER storompt_user WITH PASSWORD 'your_password';
     GRANT ALL PRIVILEGES ON DATABASE storompt TO storompt_user;
     ```

   - Exit the PostgreSQL shell:
     ```sql
     \q
     ```

5. Configure the database settings:
   - Open the `.env` file and update the following settings:
     ```shell
     DB_NAME=storompt
     DB_USER=storompt_user
     DB_PASS=your_password
     DB_PORT=5432
     REPLICATE_API_TOKEN=your_replicate_token
     ```

6. Apply database migrations:
   ```shell
   python manage.py migrate
   ```

7. Create a superuser (admin) account:
   ```shell
   python manage.py createsuperuser
   ```

8. Start the development server:
   ```shell
   python manage.py runserver
   ```

9. Access the application in your web browser:
   ```
   http://localhost:8000/
   ```

### Additional Configuration

- To use a different port for the development server, specify it in the `runserver` command:
  ```shell
  python manage.py runserver 8080
  ```

- For production deployment, make sure to update the `DEBUG` setting to `False` in the `.env` file and configure a web server (e.g., Nginx) and a WSGI server (e.g., Gunicorn).

### Troubleshooting

- If you encounter any issues during the installation or setup process, please refer to the official Django documentation or open an issue in the project's GitHub repository for assistance.