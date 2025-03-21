# 2025-Team-H-Repository

## Setup

> [!IMPORTANT]
> You need both [bun](https://bun.sh/) and [uv](https://docs.astral.sh/uv/getting-started/installation/) to run the `frontend/` and `backend` projects respecitvely.
> You also need either [MariaDB](https://mariadb.org/) or [MySQL](https://dev.mysql.com/downloads/installer/) services running.

### Backend
Install the python libraries.
```sh
uv sync
```

Create a database and a user with permissions on it.

Example:
```sh
$ sudo mariadb
MariaDB [(none)]> create database horarios;
MariaDB [(none)]> create user 'username'@'localhost' identified by 'password';
MariaDB [(none)]> grant all privileges on horarios.* to 'admin'@'localhost';
MariaDB [(none)]> flush privileges;
MariaDB [(none)]> exit;
```

Create a `.env` file with the database url and credentials.

Example:
```env
DATABASE_URL=mariadb+pymysql://username:password@localhost:3306/horarios
SECRET_KEY=your-secret-key-here  # for jwt tokens. not used yet, you can skip this
```
