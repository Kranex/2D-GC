
import os.path

from gc2d.MainWindow import MainWindow


def main():
    
    window = MainWindow()
    datafile = os.path.join(os.path.dirname(__file__), "MF_AE3.txt")
    window.load_chromatogram(datafile)
    window.select_integration()
    
    window.top.mainloop()
    

