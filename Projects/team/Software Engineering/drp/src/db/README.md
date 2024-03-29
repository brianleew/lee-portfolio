# Database

This directory will contain the files and schemas for the Web Portal database.
`import.py` takes `meter-data.csv` and creates a MySQL schema called `drp.sql`.
Once the schema is loaded, it creates tables with corresponding values from `meter-data.csv` file.
Next, use `mysql-to-flask.py` to query the tables created from `drp.sql` in `server.py` to display correpsonding visuals and datasets.

Libraries or module required for `import.py` to run:
'pip install mysql-connector-python'
'pip install python-dotenv'
(both commands only work when pip is installed on your machine)

Libraries or modules required for `mysql-to-flask.py` to run:
'pip install flask' (need to have pip installed beforehand)
'brew install mysql-client' (need to have homebrew installed beforehand)
then
may need to set export commands such as
'export MYSQLCLIENT_CFLAGS="-I/usr/local/opt/mysql-client/include/mysql"' (where mysql.h is located when you did "brew install mysql-client". Can find the path by doing "brew --prefix mysql-client" on terminal)
'export MYSQLCLIENT_LDFLAGS="-L/usr/local/opt/mysql-client/lib -lmysqlclient"' (this is where lmysqlclient.a is located)
finally, can do 'pip install Flask_MySQLdb'
or 
can experiment with 'pip install PyMySQL' which I have not tried yet to make 'pip install Flask_MySQLdb' work.

## About
This directory houses the schema and trigger sql files for the database as well as the script to import historical data. The import script will only work on the a file if it is in the same format as meter-data.csv.
- *Disabled import schema functionality as this should be ran after docker-compose initializes database*

## Running import script for historical data
- Install dependencies:
	- mysql-connector-python
	- python-dotenv
- Ensure .env has valid credentials
- Run using `python import.py [-f <file>] [-r <time>]`
	- [-f <file>]: Optional Specify specific csv file. DEFAULT: meter-data.csv
	- [-r <time>]: Optional Realtime Mode; Set interval time in seconds.
