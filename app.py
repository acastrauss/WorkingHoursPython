from PyQt5.QtWidgets import (
    QCalendarWidget,
    QLabel,
    QLineEdit, 
    QMainWindow, 
    QPushButton
)

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from datetime import date
import db.DBAccess as db
import db.WorkingDay as wd

class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.db = db.DBWH()
        
        self.setWindowTitle("Working Hours")
        self.setGeometry(100, 100, 1000, 700)
        
        self.dateEdit = QCalendarWidget(self)
        self.dateEdit.setSelectedDate(date.today())
        self.dateEdit.setGeometry(10, 10, 350, 300)
        self.dateEdit.selectionChanged.connect(self.HandleDateChange)

        self.cdLabel = QLabel(self)
        self.cdLabel.setGeometry(400, 10, 150, 15)
        self.cdLabel.setText('Working hours for chosen day:')

        self.currentDay = QLineEdit(self)
        self.currentDay.setGeometry(400, 35, 70, 30)
        self.currentDay.setText(str(self.db.GetHoursForDay(date.today())))

        self.cdBtn = QPushButton(self)
        self.cdBtn.setGeometry(400, 80, 70, 30)
        self.cdBtn.setText('Save')
        self.cdBtn.clicked.connect(self.HandleHoursSave)

        self.cmLabel = QLabel(self)
        self.cmLabel.setGeometry(400, 200, 170, 15)
        self.cmLabel.setText('Working hours for chosen month:')

        self.currentMonth = QLineEdit(self)
        self.currentMonth.setGeometry(400, 225, 70, 30)
        
        color = "#087519"

        self.graphPen = pg.mkPen(
            color=(8, 117, 25),
            width=5
            )

        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(20, 350, 350, 200)
        self.graphWidget.setBackground('w')
        labelStyle = {
            'color': '#087519',
            'font-size': '10px'
        }
        self.graphWidget.setLabel(
            'left', 'Hours (h)', **labelStyle
        )
        self.graphWidget.setLabel(
            'bottom', 'Day', **labelStyle
        )

        self.graphWidget.setTitle(
            'Hours worked per day in current month', 
            color=color,
            size="7pt"
            )
        self.graphWidget.showGrid(
            x=True,
            y=True
        )

        self.SetMonthHours(date.today())
        
        self.show()
        
    def HandleDateChange(self):
        chosen = self.dateEdit.selectedDate().getDate()
        chosen = date(chosen[0], chosen[1], chosen[2])

        self.currentDay.setText(str(
            self.db.GetHoursForDay(chosen)
        ))        

        self.SetMonthHours(chosen)        

    def HandleHoursSave(self):
        h = float(self.currentDay.text())
        chosen = self.dateEdit.selectedDate().getDate()
        chosen = date(chosen[0], chosen[1], chosen[2])

        self.db.InsertWorkingDay(wd.WorkingDay(
            chosen, h
        ))

        self.SetMonthHours(chosen)

    def SetMonthHours(self, currDate:date):
        monthRange = wd.GetMonthRangeForDate(currDate)

        self.currentMonth.setText(str(
            self.db.GetHoursForMonth(monthRange[0], monthRange[1])
        ))

        monthHours = self.db.GetWholeMonth(monthRange[0], monthRange[1])
        daysList = list(monthHours.keys())
        daysList.sort()
        hoursList = list(monthHours.values())
        
        self.graphWidget.clear()
        
        if not(len(daysList) == 0 or len(hoursList) == 0):
            self.graphWidget.plot(daysList, hoursList, pen=self.graphPen)
            # tickstr = [[(d, str(d)) for d in daysList]]
            # print(tickstr)
            # self.graphWidget.setTicks(tickstr)
            