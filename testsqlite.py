#-*-coding:utf-8-*- 


import sqlite3
import requests
import csv
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

class GetHS300():
    
    def __init__(self):
        self.conn = None

    def DownloadHS300(self, url):
        r = requests.get(url)
        self.xlspath = 'hs300.xls'
        with open(self.xlspath, "wb") as code:
            code.write(r.content)

    def ImportHS300(self):
        filename = 'hs300.csv'
        line = []
        self.result = []
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stkcode = row['成分券代码Constituent Code']
                stkname = row['成分券名称Constituent Name']
                market  = row['交易所Exchange']
                if market == 'SHH':
                    market = '1'
                elif market == 'SHZ':
                    market = '0'
                
                line = []
                line.append(market)
                line.append(stkcode)
                line.append(stkname)
               
                self.result.append(line)
        
        return self.result
        

    def DBDeal(self, dbname):
        self.conn = sqlite3.connect(dbname)
        cursor = self.conn.execute("select * from sqlite_master where type = 'table' and name = 'HSSTOCK'")
        query = """create table if not exists HSSTOCK(
                         market CHAR(1),
                         stkcode VARCHAR2(32),
                         stkname VARCHAR2(32)
                         );"""
        self.conn.execute(query)
        self.conn.commit() 
        self.conn.execute('delete from HSSTOCK')
        self.conn.commit()

    def InsertDB(self, result):
        sql = "insert into HSSTOCk values(?, ?, ?)"
        self.conn.executemany(sql, result)
        self.conn.commit()

        cursor = self.conn.execute("select * from HSSTOCK")
        self.conn.commit()
        raws = cursor.fetchall()
        self.conn.close()
        

if __name__ == '__main__':

    a = GetHS300()

    #a.DownloadHS300('http://www.csindex.com.cn/uploads/file/autofile/cons/000300cons.xls')
    
    result = a.ImportHS300()

    a.DBDeal('hs300.db')

    a.InsertDB(result)
    
