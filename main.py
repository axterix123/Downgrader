from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
import warnings
from convert import convert_vissim_23, convert_vissim_24
import os
from downgrader_ui import Ui_MainWindow

warnings.filterwarnings("ignore", category=DeprecationWarning)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.open_file)
        self.ui.pushButton_2.clicked.connect(self.convert_23to10)
        self.ui.pushButton_3.clicked.connect(self.convert_24to10)

    def open_file(self):
        self.path_files = QFileDialog.getOpenFileNames(self,"Seleccionar Archivo .inpx",directory="c:\\", filter="*.inpx")[0]
        if isinstance(self.path_files,list):
            if len(self.path_files)==1:
                self.ui.lineEdit.setText(self.path_files[0])
            elif len(self.path_files) == 0 or self.path_files == "No se ha seleccionado ningún archivo":
                self.ui.lineEdit.setText("No se ha seleccionado ningún archivo")
            else:
                self.ui.lineEdit.setText("Múltiples archivos escogidos")

    def convert_23to10(self):
        for i,file in enumerate(self.path_files):
            route,name = os.path.split(file)
            name = name[:-5]+'_v10.inpx'
            final_file = os.path.join(route,name)
            try:
                convert_vissim_23(file,final_file)
                self.ui.textEdit.setText(f"Archivo procesado:\n{name}\nSe recomienda utilizar los .sig")
            except:
                return self.ui.textEdit.setText(f"Error al procesar el archivo:\n->{name}\nPosiblemente este en v10")
    
    def convert_24to10(self):
        for file in self.path_files:
            route, name = os.path.split(file)
            name = name[:-5]+'v_10.inpx'
            final_file = os.path.join(route,name)
            try:
                convert_vissim_24(file,final_file)
                self.ui.textEdit.setText(f"Archivo procesado:\n{name}\nSe recomienda utilizar los .sig")
            except Exception as e:
                return self.ui.textEdit.setText(e)

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()