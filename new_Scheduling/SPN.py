import copy

class  SPN():
    def __init__(self, processor_num):
        self.processor_num = processor_num                  # 프로세서 수
        self.processor_run = [0] * processor_num            # 각 프로세서 일하는지 여부 (0: 쉼, 1: 일함)
        self.processor = [["."] for _ in range(processor_num)]  # 각 프로세서별 간트 차트
        self.process_num = 0                                # 프로세스 수
        self.process_run = []                               # 프로세스가 진행중인가 (-1: 종료, 0: 시작안함, 1: 진행중)
        self.process_id = []                                # 프로세스 명
        self.burst_time = []                                # 실행시간
        self.arrival_time = []                              # 도착시간
        self.ready_queue = []                               # 레디큐 리스트
        self.current_time = 0                               # 현재시간
        self.now_process = [0] * processor_num              # 프로세서별 현재 진행중인 프로세스
        self.result = []                                    # 결과 테이블   
        self.ready_queue_progress = []                      # 레디큐 변화를 저장할 리스트(GUI)


    def add_Process(self, id, at, bt) :                     # 프로세스 추가 함수
        self.process_id.append(id)                          # 프로세스 정보 리스트에 각각의 정보 추가
        self.arrival_time.append(at)
        self.burst_time.append(bt)
        self.result.append([id, at, bt])                    # 결과 테이블에 한번에 추가
        self.process_num += 1                               # 프로세스 수 1증가
        self.process_run.append(0)                          # 프로세스 아직 시작 안한 상태


    def add_Process_window(self, pro):                      # GUI에서 받아온 프로세서 정보 add_Process에 차례로 넣는 함수
        for i in range(0,int(len(pro)),3):
            self.add_Process(pro[i],int(pro[i+1]),int(pro[i+2]))
        


    def SPN_Scheduling(self):
        while sum(self.process_run) != (-1) * self.process_num:                 # 프로세스 모두 종료되면 반복 종료

            for j in range(self.process_num):
                if self.arrival_time[j] == self.current_time and self.process_run[j] == 0: # 현재시간에 도착한 프로세스가 있고 그게 아직 실행하지 않은 것이라면
                    self.ready_queue.append(j)                                  # 레디큐에 넣음
            self.ready_queue = self.priority(self.ready_queue)                  # 우선순위에 따라 재정렬

            temp = copy.deepcopy(self.ready_queue)                              # GUI에서 레디큐 진행상황을 보여주기위한 리스트에 추가
            self.ready_queue_progress.append(temp)

            for i in range(self.processor_num):                                 # 프로세서 수만큼 반복
                    if self.processor_run[i] == 0:                              # 현재 프로세서가 일하는 중이 아니고
                        if len(self.ready_queue) > 0:                           # 레디큐에 프로세스가 존재하면
                            job = self.ready_queue.pop(0)                       # 레디큐에서 프로세스를 뺌
                            
                            self.processor_run[i] = 1                           # 프로세서는 일하는 중(할당함)
                            self.process_run[job] = 1                           # 프로세스 진행중
                            self.now_process[i] = job                           # 이 프로세스는 현재 할당된 프로세스
                            #self.processor[i].append(job)                      # 프로세서에 실행중인 프로세스 표시
                            #self.burst_time[job] -= 1                          # 실행시간 1감소

                        
                    elif self.processor_run[i] == 1:                            # 프로세서 일 중                                            
                        self.burst_time[self.now_process[i]] -= 1               # 실행시간 1감소
                        self.processor[i][self.current_time] = self.now_process[i]      # 프로세서에 실행중인 프로세스 표시
                        if self.burst_time[self.now_process[i]] == 0:           # 실행시간이 0이 되면
                            self.processor_run[i] = 0                           # 프로세서는 쉬는 중
                            self.process_run[self.now_process[i]] = -1          # 프로세스 종료

                            TT = self.current_time - self.result[self.now_process[i]][1]    # TT = 현재시간 - AT
                            WT = TT - self.result[self.now_process[i]][2]                   # WT = TT - BT
                            NTT = round(TT / self.result[self.now_process[i]][2], 1)        # NTT = TT / BT
                            self.result[self.now_process[i]].append(WT)                     # 결과 테이블에 추가
                            self.result[self.now_process[i]].append(TT)
                            self.result[self.now_process[i]].append(NTT)

                            # 이전 프로세스 종료와 동시에 들어온 프로세스가 있으면                                                        
                            if len(self.ready_queue) > 0:                           # 레디큐에 프로세스가 존재하면
                                job = self.ready_queue.pop(0)                       # 레디큐에서 프로세스를 뺌
                                self.processor_run[i] = 1                           # 프로세서는 일하는중(할당함)
                                self.process_run[job] = 1                           # 프로세스 진행중
                                self.now_process[i] = job                           # 이 프로세스는 현재 할당된 프로세스
                
            self.current_time += 1                                                  # 시간 1증가
            for i in range(self.processor_num):
                self.processor[i].append(".")                                       # 간트차트 늘려줌




    def priority(self, list):                                                       # 우선순위 결정 함수
        tmp_list = []                                                               # 정렬을 위한 임시 리스트
        priority_list = []                                                          # 정렬후 반환하기 위한 리스트
        for i in range(len(list)):
            a = list.pop()                                                          # 정렬전의 레디큐의 프로세스 인덱스를 뽑아
            tmp_list.append(self.result[a])                                         # 임시 리스트에 해당 프로세서 정보 저장
        tmp_list.sort(key = lambda x: (x[2], x[1]))                                 # BT 낮은순 그 다음 AT 낮은순으로 정렬
                    
        for i in range(len(tmp_list)):
            tmp = tmp_list.pop(0)                                                   # 임시리스트에서 프로세스 정보를 뽑아
            for j in range(self.process_num):
                if self.process_id[j] == tmp[0]:                                    # 프로세스 명이 일치하는 것이 있으면 
                    priority_list.append(j)                                         # 인덱스를 저장

        return priority_list                                                        # 우선순위로 정렬된 리스트 반환





# ------------------------------ cmd 테스트 부분 ---------------------------------------


    def Print_result(self):
        process_title = ["P ","AT","BT","WT","TT","NTT",]
        for i in range(0,len(process_title)):
            print('%3s' % process_title[i] + ' l', end='')
        print()
        for i in range(0,len(self.result)):
            for j in range(0,len(self.result[i])):
                print('%3s' % self.result[i][j] + ' l', end='')
            print()

    def Progress_list(self):
        print('%7s' % "프로세서/시간", end= " ")
        for i in range(0, self.current_time):
            print('%3s' % str(i), end= " ")
        print()
        count = 1
        for i in range(0, self.processor_num):
            print('%4s' % "프로세서"+str(count), end= "     ")
            for j in range(self.current_time):
                if isinstance(self.processor[i][j], int) == True:
                    print('%3s' % self.process_id[self.processor[i][j]], end= " ")
                else:
                    print('%3s' % self.processor[i][j], end= " ")
                #print('%3s' % self.processor[i][j], end= " ")
            print()
            count += 1
        print("---------------------------------------------------------------------------")

            

"""
#프로세서 개수 설정
processor_num = 5
while(processor_num > 4):
    print('프로세서의 개수를 입력해주세요 : ',end='')
    processor_num = input()
    processor_num = int(processor_num)
    if(processor_num > 4):
        print("프로세서 개수는 4개 이하로 설정해주세요.",end="\n")
print("---------------------------------------------------------------------------")




a = SPN(processor_num)                                 # SPN 객체 생성



#프로세스 개수 설정
process_num = 16
while(process_num > 15):
    print('프로세스의 개수를 입력해주세요 : ',end='')
    process_num = input()
    process_num = int(process_num)
    if(process_num > 15):
        print("프로세스 개수는 15개 이하로 설정해주세요.",end="\n")
print("---------------------------------------------------------------------------")

#프로세스명, AT, BT 설정
process_name_num = 1
for i in range(0,process_num):
    process_name = "P"+str(process_name_num)            # 프로세서 이름
    process_name_num += 1                               # 다음 프로세서 이름
    print('프로세스 ' + str(process_name) + ' 의 AT BT : ',end='')
    AT,BT = input().split()
    a.add_Process(process_name, int(AT), int(BT))
print("---------------------------------------------------------------------------")



a.SPN_Scheduling()
a.Progress_list()
a.Print_result()
"""