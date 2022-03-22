from __future__ import annotations
from abc import ABC, abstractmethod
from cgi import test
from enum import IntEnum, auto
import time
from enum import IntEnum, auto
import sys
from PyQt5.QtWidgets import *
import time
import serial
from threading import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow, QWidget, 
    QWidget, 
    QGridLayout, 
    QVBoxLayout, 
    QHBoxLayout, 
    QGridLayout,
    QLabel,
    QComboBox,
    QProgressBar,
    QPlainTextEdit,
    QFrame,
    QPushButton)
from PyQt5.QtCore import pyqtSignal , Qt, pyqtSlot
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QRunnable, QThreadPool


class QCStateMachine(IntEnum):
    QC_STATE_STANDBY = 0
    QC_STATE_TEST_POWER_RAIL = auto()
    QC_STATE_TEST_SENSOR = auto()
    QC_STATE_TEST_TAMPER = auto()
    QC_STATE_MODEM_ON = auto()
    QC_STATE_TEST_SIM_CARD = auto()
    QC_STATE_TEST_SIGNAL = auto()

class TaskRow(IntEnum):
    TEST1 = 0
    TEST2 = auto()
    TEST3 = auto()
    TEST4 = auto()

class MainWindow(QMainWindow,QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("FSM")
        self.setFixedSize(500,200)
        self._controller = Controller(self)
        self.parent = parent
        
        self.container = QVBoxLayout()
        self.inner = QGridLayout()
        self.container.addLayout(self.inner)
        
        
        self.button1 = QPushButton("START")
        self.button1.clicked.connect(self.control_btn)
        self.label1 = QLabel("N/A")

        self.button2 = QPushButton("TEST POWER")
        # self.button2.clicked.connect(self.power_btn)
        self.label2 = QLabel("N/A")

        self.button3 = QPushButton("TEST SENSOR")
        # self.button3.clicked.connect(self.sensor_btn)
        self.label3 = QLabel("N/A")

        self.button4 = QPushButton("TEST TAMPER")
        self.label4 = QLabel("N/A")
        
        self.pass_button = QPushButton("PASS")
        self.fail_button = QPushButton("FAIL")
        
        self.label_instruction = QLabel("STANDBY")
        self.label_instruction.setStyleSheet("border: 1px solid black;")
        self.label_instruction.setAlignment(Qt.AlignCenter)
        
        self.inner.addWidget(self.button1,TaskRow.TEST1,0,1,2)
        # self.inner.addWidget(self.label1,TaskRow.TEST1,1)
        self.inner.addWidget(self.button2,TaskRow.TEST2,0)
        self.inner.addWidget(self.label2,TaskRow.TEST2,1)
        self.inner.addWidget(self.button3,TaskRow.TEST3,0)
        self.inner.addWidget(self.label3,TaskRow.TEST3,1)
        self.inner.addWidget(self.button4,TaskRow.TEST4,0)
        self.inner.addWidget(self.label4,TaskRow.TEST4,1)
        self.inner.addWidget(self.label_instruction,8,0,1,2)
        self.inner.addWidget(self.pass_button,9,0)
        self.inner.addWidget(self.fail_button,9,1)
        
        widget = QWidget()
        widget.setLayout(self.container)
        self.setCentralWidget(widget) 

    def control_btn(self):
        self._controller.start_worker()
    
    # def power_btn(self):
    #     self._controller.control_power_btn()               
    
    # def sensor_btn(self):
    #     self._controller.control_sensor_btn()        
        


class Worker(QRunnable):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = parent
        
    @pyqtSlot()
    def run(self):
        # test = CallMethodFromController()
         
        
        # self._parent.update("PASS")
        test = Context(QC_STATE_STANDBY())
        test.pass_function()
        
        
            # self._parent.control_power_btn()
        # else:
            # self._parent.control_sensor_btn()           
            
        # test.pass_function()
        # test.pass_function()

        

class Controller:
    def __init__(self, parent):
        self._parent = parent
        self._threadpool = QThreadPool()
        
    def start_worker(self):
        self._worker = Worker(self)
        self._threadpool.start(self._worker)
    
    # def control_power_btn(self):
    #     test = Context(QC_STATE_TEST_POWER_RAIL())
    #     test.pass_function()
        
    # def control_sensor_btn(self):
    #     test = Context(QC_STATE_SENSOR())
    #     test.pass_function()
        
    def update(self, update_str):
        self._parent.label_instruction.setText(update_str)
        if update_str =="PASS":
            self._parent.pass_button.setStyleSheet("background-color: {}".format("#86b721"))
        elif update_str == "FAIL":
            self._parent.fail_button.setStyleSheet("background-color: {}".format("#fe1818"))



# the context class contains a _state that references the concrete state and setState method to change between states.
class Context:

    _state = None
    def __init__(self, state: State) -> None:
        self.setState(state)

    def setState(self, state: State):

        print(f"Context: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self
    
#the method for executing the state functionality, These depends on the current state of the object..

    def pass_function(self):
        self._state.pass_function()
        
    def fail_function(self):
        self._state.fail_function()
        
    # def update(self):
    #     self._state.update()


class State(ABC):
    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def pass_function(self) -> None:
        pass
    
    # @abstractmethod
    def fail_function(self) -> None:
        pass
    
    # @abstractmethod
    # def update(self):
    #     pass

class CallMethodFromController(Controller):
    def __init__(self):
        pass
    
        self.update("PASS")
           
class QC_STATE_STANDBY(State):

    def pass_function(self) -> None:
        print("STATE : QC_STATE_STANDBY.")
        print("QC_STATE_STANDBY now changes the state of the context.")
        time.sleep(2)
        # self.context.setState(QC_STATE_TEST_POWER_RAIL())
        power_test = Context(QC_STATE_TEST_POWER_RAIL())
        power_test.pass_function()
    
    def fail_function(self):
        print("if fail stay in standby mode")
        self.context.setState(QC_STATE_STANDBY())

    
class QC_STATE_TEST_POWER_RAIL(State):   
    def pass_function(self) -> None:
        print("STATE : QC_STATE_TEST_POWER_RAIL.")
        ser = serial.Serial("COM20", 9600)
        ser.write(b"{P?}")
        data = ser.readline()
        print(data)
        
        input1 = data[1:5]
        input2 = input1[0:2]
        input3 = input1[2:]
        
        integer1 = int.from_bytes(input2,"little")
        integer2 = int.from_bytes(input3,"little")
        print(integer1)
        print(integer2)
        th = 400
        while True:
            if integer1 > th and integer2 > th:
                print("PASS")
                break
            else:
                return self.fail_function()

        print("QC_STATE_TEST_POWER_RAIL wants to change the state of the context.")
        time.sleep(3)
        self.context.setState(QC_STATE_SENSOR())
        sensor_test = Context(QC_STATE_SENSOR())
        sensor_test.pass_function()
        
        
        
    def fail_function(self) -> None:
        print("if fail back to standby mode")
        self.context.setState(QC_STATE_STANDBY())
        print("STANDBY MODE")
        # else:
            # print("FAIL BACK TO STATE STANDBY")
            # self.context.setState(QC_STATE_STANDBY)
        

class QC_STATE_SENSOR(State):
    def pass_function(self) -> None:
        print("The context is in the state of QC_STATE_TEST_SENSOR.")
        print("QC_STATE_TEST_SENSOR wants to change the state of the context.")
        # time.sleep(5)
        # self.context.setState(QC_STATE_STANDBY())


        
        
# app = Context(QC_STATE_STANDBY())
# app.pass_function()    # this method is executed as in state 1
# app.pass_function()    # this method is executed as in state 2

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())