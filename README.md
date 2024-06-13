# Login/Signup With FastAPI & Postgres

## Setup

This project requires a PostgreSQL database. The connection to the database is established through a URL stored in an environment variable. Follow these steps to set it up:

1. Create a new file in the project root directory and name it `.env`.

2. Open the `.env` file and add the following line:

    ```env
    URL=your_database_url
    ```

    Replace `your_database_url` with the actual URL of your PostgreSQL database.

3. Save and close the `.env` file.

Now, your application will be able to access the PostgreSQL database using the URL stored in the `URL` environment variable.
