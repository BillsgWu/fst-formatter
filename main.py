from PyQt5.QtCore import pyqtSlot,QRect
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox,QFileDialog,QLabel
from widget import Ui_Form
from settings import *
from lib import *
from os import listdir,path
from time import sleep
import sys
class Window(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("FST处理工具-版本：" + VERSION)
        self.ui.log.setFontFamily("Ubuntu Mono")
    @pyqtSlot()
    def on_bselectfolder_clicked(self):
        directory = QFileDialog.getExistingDirectory(self,"选择文件夹")
        logger.info(f"Select directory \"{directory}\".")
        self.ui.eselectfolder.setText(directory)
        logger.info(f"Cleaning old table item.")
        logger.info(f"There were {self.ui.fileprogresstable.rowCount()} rows in the table.")
        for i in range(self.ui.fileprogresstable.rowCount()):
            self.ui.fileprogresstable.removeRow(0)
        hasfile = False
        processls = []
        for file in listdir(directory):
            filename = path.join(directory,file)
            if path.isfile(filename) and file.lower().endswith(".fst"):
                logger.info(f"Scanning file {filename}")
                errcnt = 0
                hasfile = True
                nrow = self.ui.fileprogresstable.rowCount()
                self.ui.fileprogresstable.insertRow(nrow)
                try:
                    self.ui.fileprogresstable.setCellWidget(nrow,0,QLabel(str(nrow + 1)))
                    self.ui.fileprogresstable.setCellWidget(nrow,1,QLabel(filename))
                    self.ui.fileprogresstable.setCellWidget(nrow,3,QLabel("Waiting"))
                    detail = scan_type(filename)[1]
                    self.ui.fileprogresstable.setCellWidget(nrow,2,QLabel(detail["MachineType"]))
                    logger.info(f"Maching:{detail['MachineType']} Version:{detail['Version']} Setup:{detail["SetupType"]}")
                    processls.append([nrow,filename])
                except Exception as e:
                    logger.error(f"Exception occors while scanning file {filename}")
                    logger.error(str(e))
                    QMessageBox.critical(self,"错误",f"文件{filename}中出现了未知错误，程序将不会对其操作。")
                    errcnt += 1
                self.ui.fileprogresstable.setCellWidget(nrow,4,QLabel(f"0W/{errcnt}E"))
        if not hasfile:
            logger.critical("There are no .fst files in the selected directory.")
            QMessageBox.critical(self,"致命错误","选定文件夹没有fst文件",QMessageBox.Ok)
            return
        logger.info("Prepareing to process file.")
        ret = QMessageBox.question(self,"扫描完成","扫描完成，立刻进行处理？",QMessageBox.Ok,QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            for task in processls:
                logger.info(f"Processing file {task[1]}")
                ofilename = ".".join(task[1].split(".")[:-1]) + ".xlsx"
                if path.isfile(ofilename):
                    logger.warning(f"File {ofilename} exists.This program will overwrite it.")
                    QMessageBox.warning(self,"警告",f"已经存在文件{ofilename}，本程序将覆盖其中内容")
                logger.info(f"{task[1]} -> info{ofilename}")
                self.ui.fileprogresstable.cellWidget(task[0],3).setText("Processing")
                self.repaint()
                wars,errs = process_file(task[1],ofilename,logger)
                sleep(0.5)
                self.ui.fileprogresstable.cellWidget(task[0],3).setText("Done")
                self.ui.fileprogresstable.cellWidget(task[0],4).setText(f"{wars}W/{errs}E")
                self.repaint()
            QMessageBox.information(self,"完成操作","所有任务已经完成。",QMessageBox.Ok)
        else:
            logger.warning("Operation canceled by user.")
    def render_log_message(self,message):
        if "warning" in message.lower():
            return f"<font color=\"#FFD700\">{message}</font>"
        elif "error" in message.lower():
            return f"<font color=\"#FF0000\">{message}</font>"
        elif "critical" in message.lower():
            return f"<font color=\"#A52A2A\">{message}</font>"
        elif "success" in message.lower():
            return f"<font color=\"#0000FF\">{message}</font>"
        else:
            return message
    def write(self,message):
        self.ui.log.setHtml(self.ui.log.toHtml() + self.render_log_message(message))
    def writeln(self,message):
        self.ui.log.setHtml(self.ui.log.toHtml() + self.render_log_message(message) + "\n")
    def resizeEvent(self,event):
        qsize = event.size()
        size = [qsize.width(),qsize.height()]
        self.ui.lselectfolder.setGeometry(QRect(30,40,180,30))
        self.ui.eselectfolder.setGeometry(QRect(210,40,size[0]-290,30))
        self.ui.bselectfolder.setGeometry(QRect(size[0]-80,40,50,30))
        self.ui.label.setGeometry(QRect(30,290,66,19))
        self.ui.log.setGeometry(QRect(30,310,size[0]-60,size[1]-340))
        self.ui.fileprogresstable.setGeometry(QRect(30,90,size[0]-60,170))
app = QApplication(sys.argv)
window = Window()
handler = log.StreamHandler(window)
handler.setLevel(log.INFO)
handler.setFormatter(log.Formatter("[%(levelname)-8s] - [%(asctime)s] : %(message)s"))
logger.addHandler(handler)
window.show()
app.exec_()