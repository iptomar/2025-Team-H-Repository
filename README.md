# 2025-Team-H-Repository

## Setup

> [!IMPORTANT]
> You need both [bun](https://bun.sh/) and [uv](https://docs.astral.sh/uv/getting-started/installation/) to run the `frontend/` and `backend` projects respecitvely.
> You also need either [MariaDB](https://mariadb.org/) or [MySQL](https://dev.mysql.com/downloads/installer/) services running.

### Backend
Install the python libraries.
```sh
$ uv sync
```

Create a database and a user with permissions on it.

Example:
```sh
$ sudo mariadb
MariaDB [(none)]> create database horarios;
MariaDB [(none)]> create user 'username'@'localhost' identified by 'password';
MariaDB [(none)]> grant all privileges on horarios.* to 'username'@'localhost';
MariaDB [(none)]> flush privileges;
MariaDB [(none)]> exit;
```

Create a `.env` file with the database url and credentials.

Example:
```env
DATABASE_URL=mariadb+pymysql://username:password@localhost:3306/horarios
SECRET_KEY=your-secret-key-here  # for jwt tokens. not used yet, you can skip this
```
Activate virtual environment:
```sh
$ .venv\Scripts\activate
```
Run the server:
```sh
$ uvicorn app.main:app --reload

```
The `--reload` flag is optional, it will just make it so that when you update a file, the server will automatically update,

### Frontend

Install the dependencies.
```sh
bun install
```

Run the project in development mode, and open it in the browser.
```sh
$ bun dev

  VITE v6.2.2  ready in 1068 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```
