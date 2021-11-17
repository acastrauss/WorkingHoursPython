import datetime
import calendar

class WorkingDay():
    def __init__(self, date:datetime.date, hours:float) -> None:
        self.date = date
        self.hours = hours

    @property
    def Date(self):
        return self.date

    @property
    def Hours(self):
        return self.hours


def GetMonthNumber(month:str)->int:
    choices = {
        'january' : 1,
        'february' : 2,
        'march' : 3,
        'april' : 4,
        'may' : 5,
        'june' : 6,
        'july' : 7,
        'august' : 8,
        'september' : 9,
        'october' : 10,
        'november' : 11,
        'december' : 12
    }

    return choices.get(month.lower(), -1)


def GetMonthRangeForDate(date:datetime.date)->tuple[datetime.date]:
    range = calendar.monthrange(date.year, date.month)
    start = datetime.date(date.year, date.month, 1)
    end = datetime.date(date.year, date.month, range[1])
    return (
        start, end
    )

def AddZeroToDate(date:str)->str:
    spl = date.split(' ')[0]
    parts = spl.split('-')
    
    y = str(parts[0])
    m = str(parts[1])
    d = str(parts[2])

    if(int(y) < 10):
        y = f"000{y}"
    elif(int(y) < 100):
        y = f"00{y}"
    elif(int(y) < 1000):
        y = f"0{y}"

    if(int(m) < 10):
        m = f"0{m}"
    
    if(int(d) < 10):
        d = f"0{d}"

    return f"{y}-{m}-{d} {date.split(' ')[1]}"

def GetDayStartStr(date:datetime.date)->str:
    return f"{date.year}-{date.month}-{date.day} 00:00:00"

def GetDayEndStr(date:datetime.date)->str:
    return f"{date.year}-{date.month}-{date.day} 23:59:59"


# now = datetime.date.fromisoformat('2021-07-03')

# print(datetime.date.today())
# print(str(now))