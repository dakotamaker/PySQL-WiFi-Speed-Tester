# PySQL WiFi Speed Tester
A simple python script to run SpeedTests every hour and write the results to a MySQL database.

## Prerequisites
* A MySQL server
* Python 3
* A table in the MySQL server with the following columns:
    * `date`: A datetime column to track when the test was conducted
    * `download`: A float field for the download speeds in Mbps
    * `upload`: A float field for the upload speeds in Mbps
    * `ping`: A float field for the ping time in ms

## Usage
To download dependencies run: `pip3 install -r requirements.txt`

To execute the script run: 
`python pysql.py --h <your host> --u <your username> --p <your password> --t <your table name> --db <your database name>` (the options can be in any order).

You can always run `python pysql.py --help` to get more clarification on what each argument is for.
