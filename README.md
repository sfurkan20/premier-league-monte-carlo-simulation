## Used Technologies:
Python for back-end,

HTML, CSS, Javascript for front-end,

SQLite for database

### Usage:
First, execute the script in plmc_project/main.py
```
python plmc_project/main.py
```

Then, navigate to
```
127.0.0.1:8080
```
using your browser. 

### About SQL Queries:
This query is used to initiate the database:
```
CREATE TABLE "TeamModel" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"strength"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
);
```
All other necessary queries were generated automatically using 'SQLiteORM' class (written by me).
