import sys
from PyQt5.QtWidgets import QApplication
from app import App



def Run():
    qapp = QApplication(sys.argv)

    a = App()
    
    qapp.exec()




if __name__  == '__main__':
    Run()