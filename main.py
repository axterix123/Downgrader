from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
import warnings
from convert import convert_vissim
import os
from downgrader_ui import Ui_MainWindow

warnings.filterwarnings("ignore", category=DeprecationWarning)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.open_file)
        self.ui.pushButton_2.clicked.connect(self.convert)


    def open_file(self):
        self.path_files = QFileDialog.getOpenFileNames(self,"Seleccionar Archivo .inpx",directory="c:\\", filter="*.inpx")[0]
        if isinstance(self.path_files,list):
            if len(self.path_files)==1:
                self.ui.lineEdit.setText(self.path_files[0])
            else:
                self.ui.lineEdit.setText("Múltiples archivos escogidos")

    def convert(self):
        for i,file in enumerate(self.path_files):
            route,name = os.path.split(file)
            name = name[:-5]+'_v10.inpx'
            final_file = os.path.join(route,name)
            try:
                convert_vissim(file,final_file)
                self.ui.textEdit.setText(f"Archivo procesado:\n{name}")
            except:
                return self.ui.textEdit.setText(f"Error al procesar el archivo:\n->{name}\nPosiblemente este en v10")

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()