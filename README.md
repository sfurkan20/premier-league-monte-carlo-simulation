## Used Technologies:
Python for back-end,

HTML, CSS, Javascript for front-end,

SQLite for database

### Usage:
```
python plmc_project/main.py
```

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
