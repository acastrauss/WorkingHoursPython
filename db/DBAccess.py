from datetime import date
import sqlite3
import os
from .WorkingDay import (
    AddZeroToDate,
    WorkingDay, 
    GetMonthNumber, 
    GetDayStartStr,
    GetDayEndStr
)
from sqlite3.dbapi2 import Connection, Error


class DBWH():
    def __init__(self) -> None:
        dbFile = os.path.join(os.curdir, "db", "WorkingHours.db")
        dbExists = True
        if not os.path.exists(dbFile):
            f = open(dbFile, "x")
            f.close()
            print("DB file created.")
            dbExists = False

        self.dbPath = dbFile
        self.conn = sqlite3.connect(self.dbPath)
        
        if not dbExists:
            self.CreateTableWorkingHours()

    def __del__(self):
        if(self.conn):
            self.conn.close()

    def CreateTableWorkingHours(self):
        sql = """
            CREATE TABLE IF NOT EXISTS workingHours (
                id INTEGER PRIMARY KEY,
                day DATE NOT NULL,
                hours REAL
            );
        """

        curs = self.conn.cursor()

        curs.execute(sql)
        curs.close()

    def GetNextId(self)->int:
        sql = """
            SELECT MAX(id) FROM workingHours
        """

        curs = self.conn.cursor()
        curs.execute(sql)
        id = curs.fetchone()[0]
        
        if(id is None):
            id = 1
        else:
            id += 1

        curs.close()
        return id

    def DayId(self, date:date)->int:
        sql = """
            SELECT id
            FROM workingHours
            WHERE day = date(?)
        """
        
        curs = self.conn.cursor()

        curs.execute(sql, [
            str(date)
        ])

        id = curs.fetchone()

        if(id is None):
            id = -1
        else:
            id = id[0]

        curs.close()

        return id

    def InsertWorkingDay(self, day:WorkingDay):
        dayId = self.DayId(day.Date)
        
        sql = """"""

        curs = self.conn.cursor()

        if(dayId == -1):
            sql = """
                INSERT INTO workingHours (
                    id, day, hours
                )
                VALUES (
                    ?, ?, ?
                )
            """
            curs.execute(sql, [
                self.GetNextId(), day.Date, day.Hours
            ])

        else:
            sql = """
                UPDATE workingHours
                SET hours = ?
                WHERE id = ?
            """
            curs.execute(sql, [
                day.Hours, dayId
            ])

        self.conn.commit()
        curs.close()

    def GetHoursForMonth(self, monthStart:date, monthEnd:date)->float:
        sql = """
            SELECT sum(hours)
            FROM workingHours
            WHERE day BETWEEN 
            date(?) and date(?)
        """

        curs = self.conn.cursor()

        curs.execute(sql, [
            monthStart, monthEnd
        ])

        sum = curs.fetchone()
        
        if(sum[0] is None):
            sum = 0
        else:
            sum = sum[0]

        curs.close()

        return sum

    def GetHoursForDay(self, day:date)->float:
        
        sql = """
            SELECT hours
            FROM workingHours
            WHERE day = date(?)
        """

        curs = self.conn.cursor()

        curs.execute(sql, [
            day
        ])

        sum = curs.fetchone()

        if(sum is None):
            sum = 0
        else:
            sum = sum[0]

        curs.close()

        return sum
        
    def GetWholeMonth(self, monthStart:date, monthEnd:date)->dict[int, float]:
        sql = """
            SELECT hours
            FROM workingHours
            WHERE day BETWEEN 
            date(?) and date(?)
        """

        curs = self.conn.cursor()

        curs.execute(sql, [
            monthStart, monthEnd
        ])
        month = curs.fetchall()

        ret = {}

        for i in range(len(month)):
            ret[i + 1] = month[i][0]

        curs.close()

        return ret
