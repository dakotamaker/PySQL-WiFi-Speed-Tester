from datetime import datetime

import mysql.connector
import speedtest
import argparse
import schedule
import time

class InternetTester:
  def __init__(self):
    self.parser = argparse.ArgumentParser(description='Pass in mysql connection details.')
    self.parser.add_argument("--t", help='Table in which you wish to write to. The table should exist already.', required=True)
    self.parser.add_argument("--h", help='The host name or IP of your mysql server.', required=True)
    self.parser.add_argument("--u", help='The user to log into your mysql server with.', required=True)
    self.parser.add_argument("--p", help="The password to login to your mysql server with.", required=True)
    self.parser.add_argument("--db", help="The database to use on your mysql server.", required=True)

    self.args = self.parser.parse_args()

    self.mydb = mysql.connector.connect(
      host=self.args.h,
      user=self.args.u,
      passwd=self.args.p,
      database=self.args.db
    )
    self.mysql = self.mydb.cursor()

  def __run_speed_test(self):
    servers = []
    threads = None
    speedTest = speedtest.Speedtest()
    speedTest.get_servers(servers)
    speedTest.get_best_server()
    speedTest.download(threads=threads)
    speedTest.upload(pre_allocate=False)
    speedTest.results.share()
    internet_results = speedTest.results.dict()
    return internet_results

  def __write_speed_data_to_db(self, internet_results):
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    downloadSpeed = round(internet_results['download'] / 1000000, 2)
    uploadSpeed = round(internet_results['upload'] / 1000000, 2)
    pingSpeed = round(internet_results['ping'], 2)

    queryString = f"INSERT INTO {self.args.t} (date, download, upload, ping) VALUES (\"{now}\", {downloadSpeed}, {uploadSpeed}, {pingSpeed})"

    self.mysql.execute(queryString)
    self.mydb.commit()

  def start(self):
    internet_results = self.__run_speed_test()
    self.__write_speed_data_to_db(internet_results)

def pysql_internet_test():
  internetTester = InternetTester()
  internetTester.start()

schedule.every(1).hour.do(pysql_internet_test)

while True:
  schedule.run_pending()
  time.sleep(1)