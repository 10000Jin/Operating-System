
from FCFS import FCFS
from RR import RR
from SPN import SPN
from SRTN import SRTN
from HRRN import HRRN
from LS_SPN import LS_SPN
from LC_RR import LC_RR

import sys
import time
import random
import logging
logging.captureWarnings(True)
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType("scheduling_gui.ui")[0]     # ui파일 불러오기

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.process = []                               # gui에서 입력받은 프로세스의 AT와 BT를 저장하는 리스트
        self.window_process_num = 0                     # gui에서 입력받은 프로세스의 개수
        self.window_process_name_count = 1              # gui에서 입력받은 프로세스의 개수 카운트
        self.window_process_name = " "                  # 프로세스 이름을 설정하는 변수
        self.add_info.clicked.connect(self.add)         # "프로세스 추가"를 클릭했을 때 self.add 함수 실행
        self.run.clicked.connect(self.start)            # "실행"를 클릭했을 때 self.start 함수 실행
        self.stop.clicked.connect(self.clear)           # "초기화"를 클릭했을 때 self.clear 함수 실행
        self.sleep_time = 0.2                           # 진행상황의 시간 간격
        self.select_method.currentIndexChanged.connect(self.quantum_disabled)  # 해당 기법에 퀀텀 값이 필요할 때만 퀀텀 값을 수정 가능하게 설정
        self.set_quantum.setDisabled(True)              # 퀀텀값 수정 비활성화(디폴트) 설정
        self.msg = QMessageBox()                        # gui 조작시 경고 문구를 띄워주는 메시지 박스

    def quantum_disabled(self):                         # 해당 기법에 퀀텀 값이 필요할 때만 퀀텀 값을 수정 가능하게 설정
        if str(self.select_method.currentText()) == "RR" or str(self.select_method.currentText()) == "LC_RR": # RR과 LC_RR 기법에서만 수정 가능
            self.set_quantum.setDisabled(False)
        else:                                           # 나머지 기법들은 퀀텀 값 수정 불가능
            self.set_quantum.setDisabled(True)

    def keyPressEvent(self, e):                         # gui의 버튼과 키보드 이벤트 연결
        if e.key() == 16777220:                         # 16777220 = Key_Enter
            self.add()                                  # 엔터를 누를 시 프로세스 추가
            '''
        elif e.key() == 16777249: #Key_Ctrl
            self.start()
        elif e.key() == 16777251: #Key_Art
            self.clear()
            '''

    def messageBox(self, text):                         # gui 조작시 경고가 생기면 문구를 띄워주는 메시지 박스
        msgBox = QMessageBox()
        msgBox.setWindowTitle("경고")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)                            # 입력 받은 text를 경고로 출력

        return msgBox.exec_()


    def add(self):                                      # 프로세스 추가
        if(self.set_AT.text() == ''):                   # AT에 값이 안주어졌다면 값을 입력하라 메시지 출력
            self.messageBox("AT 값을 입력해주세요.")
            return 0
        elif(self.set_AT.text().isdigit() == 0):        # AT에 값이 숫자가 아니면 메시지 출력
            self.messageBox("AT 값은 숫자를 입력해야합니다.")
            return 0
        else:                                           # Set_AT에 입력된 값을 변수 AT에 저장
            AT = self.set_AT.text()

        if(self.set_BT.text() == '' or int(self.set_BT.text()) == 0): # BT에 값이 안주어졌다면 값을 입력하라 메시지 출력
            self.messageBox("BT 값을 입력해주세요.")
            return 0
        elif(self.set_BT.text().isdigit() == 0):        # BT에 값이 숫자가 아니면 메시지 출력
            self.messageBox("BT 값은 숫자를 입력해야합니다.")
            return 0
        else:                                           # Set_BT에 입력된 값을 변수 BT에 저장
            BT = self.set_BT.text()

        window_process_name = "P" + str(self.window_process_name_count)     # 프로세스 이름은 P0, P1 순으로 자동으로 설정되도록함

        self.show_process_info.setRowCount(self.window_process_num+1)       # 프로세스 정보를 보여주는 테이블의 행의 개수 유동적으로 설정
        self.show_process_info.setColumnCount(3)                            #프로세스 정보를 보여주는 테이블의 열의 개수는 3개로 설정(프로세스 이름, At, Bt)
        
        self.show_process_info.setItem(self.window_process_num,0,QTableWidgetItem(window_process_name))     # 테이블에 프로세스 이름 저장
        self.show_process_info.setItem(self.window_process_num,1,QTableWidgetItem(AT))                      # 테이블에 프로세스 AT 저장
        self.show_process_info.setItem(self.window_process_num,2,QTableWidgetItem(BT))                      # 테이블에 프로세스 BT 저장
        self.process.append(window_process_name)        # 리스트에 프로세스의 이름 저장
        self.process.append(AT)                         # 리스트에 프로세스의 AT 저장
        self.process.append(BT)                         # 리스트에 프로세스의 BT 저장

        self.set_AT.setText("")                         # set_AT를 공백으로 설정(초기화)
        self.set_BT.setText("")                         # set_BT를 공백으로 설정(초기화)
        self.window_process_num += 1                    # 프로세스의 개수를 1개 추가
        self.window_process_name_count += 1             # 프로세스의 이름 카운트를 1개 추가

    def start(self):                                    # "실행"
        method = str(self.select_method.currentText())  # 선택한 기법을 method에 저장

        if(self.set_processor_num.text() == ''):        # 프로세스 개수에 값이 없으면 메시지 출력
            self.messageBox("프로세서 수 미입력\n <1로 설정됨>")
            self.set_processor_num.setText("1")
            processor = 1
        elif(self.set_processor_num.text().isdigit() == 0): # 프로세스 개수에 값이 숫자가 아니면 메시지 출력
            self.messageBox("프로세서 수는 숫자를 입력해야합니다.\n <1로 설정됨>")
            self.set_processor_num.setText("1")
            processor = 1
        elif(int(self.set_processor_num.text())<1 or 4<int(self.set_processor_num.text())):     # 프로세스 개수가 1~4가 아니면 메시지 출력
            self.messageBox("프로세서 수는 1~4개입니다.\n <1로 설정됨>")
            self.set_processor_num.setText("1")
            processor = 1
        else:
            processor = self.set_processor_num.text()   # 프로세스 개수 변수에 저장

        if(self.set_quantum.text() == ''):
            self.messageBox("퀀텀 값 미입력\n <1로 설정됨>")
            self.set_quantum.setText("1")
            quantum = 1
        elif(self.set_quantum.text().isdigit() == 0):
            self.messageBox("퀀텀 값은 숫자를 입력해야합니다.\n <1로 설정됨>")
            self.set_quantum.setText("1")
            quantum = 1
        elif(int(self.set_quantum.text())<1):
            self.messageBox("퀀텀 값은 1이상으로 입력해야합니다.\n <1로 설정됨>")
            self.set_quantum.setText("1")
            quantum = 1
        else:
            quantum = self.set_quantum.text()           # 퀀텀값 변수에 저장

        self.show_progress.clear()                      # 진행상황을 보여주는 테이블 초기화
        self.show_ready_queue.clear()                   # 레디큐를 보여주는 테이블 초기화
        self.show_result.clear()                        # 결과를 보여주는 테이블 초기화
        self.show_progress.setRowCount(int(processor))  # 진행상황을 보여주는 테이블의 행을 프로세서의 개수만큼 설정
        
        self.show_result.setRowCount(self.window_process_num) # 결과를 보여주는 테이블의 행을 프로세스의 개수만큼 설정
        self.show_result.setColumnCount(6)              # 결과를 보여주는 테이블의 열을 6개로 설정(이름,AT,BT,WT,TT,NTT)
        self.show_ready_queue.setColumnCount(self.window_process_num) # 레디큐를 보여주는 테이블의 열을 프로세스의 개수만큼 설정
        self.show_ready_queue.setRowCount(1)            # 레디큐 행은 1개 (1차원 리스트)
        

        # 각 메소드에 맞는 클래스를 호출해 program 생성 후 스케쥴링
        if(method == "RR"): 
            program = RR(int(processor))
            program.set_Quantum(int(quantum))
            program.add_Process_window(self.process)
            program.RR_Scheduling()

        elif(method == "LC_RR"): 
            program = LC_RR(int(processor))
            program.set_Quantum(int(quantum))
            program.add_Process_window(self.process)
            program.LC_RR_Scheduling()

        elif(method == "FCFS"):
            program = FCFS(int(processor))              # 프로세서 수 입력
            program.add_Process_window(self.process)    # 프로세스 입력
            program.FCFS_Scheduling()                   # 스케쥴링

        elif(method == "SPN"):
            program = SPN(int(processor))
            program.add_Process_window(self.process)
            program.SPN_Scheduling()

        elif(method == "LS_SPN"):
            program = LS_SPN(int(processor))
            program.add_Process_window(self.process)
            program.LS_SPN_Scheduling()

        elif(method == "SRTN"):
            program = SRTN(int(processor))
            program.add_Process_window(self.process)
            program.SRTN_Scheduling()

        elif(method == "HRRN"):
            program = HRRN(int(processor))
            program.add_Process_window(self.process)
            program.HRRN_Scheduling()



        # 진행시간 간격 설정
        if(self.Set_sleep_time.text() == ''): 
            self.sleep_time = 0.2
        elif(float(self.Set_sleep_time.text()) > 0):
            self.sleep_time = float(self.Set_sleep_time.text())



        # 스케쥴링을 마친 program의 진행상황, 레디큐, 결과를 출력
        if(method == "FCFS" or method == "SRTN" or method == "SPN" or method == "RR" or method == "LC_RR" or method == "LS_SPN") :

            self.show_progress.setColumnCount(program.current_time+1)       # 진행상황 행의 개수 지정
            progress_colum_count = []                                       # 진행상황 행 초기화

            for i in range(0, program.current_time+1):
                progress_colum_count.append(str(i))
            self.show_progress.setHorizontalHeaderLabels(progress_colum_count)
            result_colum_count = ["이름","AT","BT","WT","TT","NTT"]           # 결과 테이블의 0번째 행의 제목들을 저장하는 변수
            self.show_result.setHorizontalHeaderLabels(result_colum_count)      # 위 변수에 따라 각 0번째 행에 저장

            # 진행상황 프로세스마다 랜덤 색 지정
            color = [["" for i in range(3)] for _ in range(len(program.result))] 
            for i in range(0, int(len(program.result))):
                for j in range(3):
                    rand_num = random.randrange(0,255)
                    color[i][j] = rand_num

            # 결과 테이블에 스케쥴링이 끝난 progam의 program.result 값들을 표시(result에는 "이름","AT","BT","WT","TT","NTT"가 저장되어있음 )
            for i in range(0,int(len(program.result))):
                for j in range(0,int(len(program.result[i]))):
                    self.show_result.setItem(i,j,QTableWidgetItem(str(program.result[i][j])))

            # repaint를 사용하기 위해 팔레트 선언
            palette = QPalette() 

            #진행상황과 레디큐 테이블에 스케쥴링이 끝난 progam의 각 초마다의 진행상황과 레디큐 현황을 표시해줌
            for j in range(1, program.current_time):
                for i in range(0,int(processor)):                               # 진행상황 테이블 표시
                    if program.processor[i][j] == '.':
                        self.show_progress.setItem(i,j-1,QTableWidgetItem(" "))
                    else :
                        proc = program.processor[i][j]          # 진행상황은 program.process에 몇번째 프로세서인지 저장되어있음, proc에 저장
                        self.show_progress.setItem(i,j-1,QTableWidgetItem(str(program.result[proc][0])))    # proc번째 프로세스의 프로세스명 테이블에 표시 
                        self.show_progress.item(i, j-1).setBackground(QColor(color[proc][0], color[proc][1], color[proc][2]))   # 색 재설정

                
                self.show_ready_queue.clear()                   # 레디큐 테이블 초기화
                for i in range(0,int(len(program.ready_queue_progress[j]))):    # 레디큐 테이블 표시
                    proc = program.ready_queue_progress[j][i]   # 레디큐에 저장되어있는 프로세스를 가져옴, proc에 저장
                    self.show_ready_queue.setItem(0,i,QTableWidgetItem(program.result[proc][0]))            # proc번째 프로세스의 프로세스명 테이블에 표시 
                    self.show_ready_queue.item(0,i).setBackground(QColor(color[proc][0], color[proc][1], color[proc][2]))       # 색 재설정

                self.show_progress.resizeColumnsToContents()    # 진행상황 테이블의 각 열의 간격을 재설정
                time.sleep(self.sleep_time)                     # 진행상황 수행간격만큼 sleep
                # 진행상황과 레디큐 테이블을 repaint해줌
                self.show_progress.repaint() 
                self.show_ready_queue.repaint()
                QApplication.processEvents()


        elif(method == "HRRN"):                                 # HRRN은 program.result가 한칸씩 밀려 HRRN의 경우 for문의 i값이 달라짐
            self.show_progress.setColumnCount(program.current_time+1)
            progress_colum_count = []
            for i in range(0, program.current_time+1):
                progress_colum_count.append(str(i))
            self.show_progress.setHorizontalHeaderLabels(progress_colum_count)
            result_colum_count = ["이름","AT","BT","WT","TT","NTT"]
            self.show_result.setHorizontalHeaderLabels(result_colum_count)

            color = [["" for i in range(3)] for _ in range(len(program.result))]
            for i in range(0, int(len(program.result))):
                for j in range(3):
                    rand_num = random.randrange(0,255)
                    color[i][j] = rand_num

            for i in range(0,int(len(program.result))):
                for j in range(1,int(len(program.result[i]))):
                    self.show_result.setItem(i,j-1,QTableWidgetItem(str(program.result[i][j])))

            palette = QPalette()
            for j in range(1, program.current_time):
                for i in range(0,int(processor)):
                    if program.processor[i][j] == '.':
                        self.show_progress.setItem(i,j-1,QTableWidgetItem(" "))
                    else :
                        proc = program.processor[i][j]
                        self.show_progress.setItem(i,j-1,QTableWidgetItem(str(program.result[proc][1])))
                        self.show_progress.item(i, j-1).setBackground(QColor(color[proc][0], color[proc][1], color[proc][2]))

                self.show_ready_queue.clear()
                for i in range(0,int(len(program.ready_queue_progress[j]))):
                    proc = program.ready_queue_progress[j][i]
                    self.show_ready_queue.setItem(0,i,QTableWidgetItem(program.result[program.ready_queue_progress[j][i]][1]))
                    self.show_ready_queue.item(0,i).setBackground(QColor(color[proc][0], color[proc][1], color[proc][2]))
                self.show_progress.resizeColumnsToContents()
                time.sleep(self.sleep_time)
                self.show_progress.repaint()
                self.show_ready_queue.repaint()
                QApplication.processEvents()




    def clear(self):                                        # "초기화" 시 모든 변수와 테이블들을 초기화해줌
        self.set_AT.setText("")
        self.set_BT.setText("")
        self.set_processor_num.setText("")
        self.set_quantum.setText("")
        self.process = []
        self.window_process_num = 0
        self.window_process_name_count = 1
        self.window_process_name = " "
        self.show_process_info.setRowCount(self.window_process_num)
        self.show_process_info.setColumnCount(3)
        self.show_progress.setRowCount(0)
        self.show_progress.setRowCount(0)
        self.show_result.setRowCount(0)
        self.show_result.setColumnCount(6)
        self.show_ready_queue.clear()

app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()
