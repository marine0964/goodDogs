#$ cd
#$ cd yahboom-jetbot
#$ sudo python3 // 파이썬 실행
#파이썬 코드 시작
#서보모터 제어
from servoserial import ServoSerial
import serial
import time
import random
import playsound
from jetbot import robot
robot = Robot()
print('주행모드를 실행합니다.')
#시리얼 신호 on c는 아두이노로 보내는 신호 (0주행,1발사,2놀이반복,3놀이정지,4훈련보상,5.훈련실패)
#b는 정면판단 받는 신호
#아두이노에 좌우판단 코드 d 받는 신호
#a는 공 넣음 판단
#t는 훈련 보상
#높낮이 코드는 생략
#주행 코드 시작 주행 중간에 잿슨으로 신호을 받음
def bfuc(x):#뒤에 두글자에 불필요한 값 삭제
    b = arduino.readline()
    b = b.decode()[:-2]
    b = str(b)
    return b
def dfuc(y):
    d = arduino.readline()
    d = d.decode()[:-2]
    d = str(d)
    return d
def afuc(z):
    a = arduino.readline()
    a = a.decode()[:-2]
    a = str(a)
    return a
arduino=serial.Serial('COM3', 9600) #포트 위치 확인
c='0'
c=c.encode('utf-8')
arduino.write(c)
#robot.forward(1)   
    bfuc(b)
while b!='23': # 장애물과 배설물을 피해 개가 근처에 있을 때 까지 반복구문
    if b=='20':
        print('전진가능')
        #robot.forward(1)
        time.sleep(1) #아무것도 없을 때 1초간 전진
    if  b=='21' :
        print('배설물이 있다.')
        dfuc(d)   
        if  d=='41': #정면에 배설물이 있고 왼쪽에 뭐 있음
            print('왼쪽을 피해 오른쪽으로가자')
            #robot.right(1) #따라서 오른쪽으로 꺽음
            time.sleep(1)
            #robot.stop()
        elif  d=='42': #정면에 배설물이 있고 오른쪽에 뭐 있음
            print('오른쪽을 피해 왼쪽으로가자')
            #robot.left(1) #왼쪽으로 꺽음
            time.sleep(1)
            #robot.stop()
        elif d=='43': #사방에 뭐가 있어서 뒤로 후진
            print('뒤로 가자')
            #robot.backward(0.8)
            time.sleep(1.5)
            #robot.stop()
    if b=='22':
        print('장애물이 있다.')    
        dfuc(d)
        if  d=='41': #정면에 장애물이 있고 왼쪽에 뭐 있음
            print('왼쪽을 피해 오른쪽으로가자')
            #robot.right(1) #따라서 오른쪽으로 꺽음
            time.sleep(1)
            #robot.stop()
        elif  d=='42': #정면에 장애물이 있고 오른쪽에 뭐 있음
            print('오른쪽을 피해 왼쪽으로가자')
            #robot.left(1) #왼쪽으로 꺽음
            time.sleep(1)
            #robot.stop()
        elif d=='43': #사방에 뭐가 있어서 뒤로 후진
            print('뒤로 가자')
            #robot.backward(0.8)
time.sleep(1.5)
#robot.stop()
#while 조건문 끝 개가 근처에 있다


#개를 호명 엔비아!! 출력
#import playsound
playsound.playsound('name.mp3') #개 이름 부르기
#카메라 회전 
#servo_device = ServoSerial() #카메라 위치 조정 코드
#servo_device.Servo_serial_control(1, 1600)
#servo_device.Servo_serial_control(1, 2600)
#servo_device.Servo_serial_control(1, 2100)
#def Decode(b):
#b= b.decode()
#b= str(b)
bfuc(b)
if b=='23' :
    print('개가 있다.')
    #robot.stop()
# 주행 코드 스탑
#놀이 시작 출력
    print('개가 있으므로 놀이를 시작합니다.')
    c='1'
    c=c.encode('utf-8')
    arduino.write(c)
    
 #놀이 시작
 #공을 1회 발사

#개가 공을 넣음
c='2'
c=c.encode('utf-8')
arduino.write(c)
afuc(a)
while a!='12':
 #a: 0공을 못 가져옴 1 강아지가 공을 넣음, 2놀이 종료
    afuc(a)
    if a=='11': 
#import playsound
        playsound.playsound('good.mp3') #잘했어

    afuc(a)
if a=='12':
    print('놀이 종료') 

print('훈련을 시작합니다')
#Ai 파트
#랜덤으로 모델 선택
ai = random.randint(1, 5) #0~5번으로 임의로 숫자매김

#훈련성공
#if 행동이 맞다!
playsound.playsound('good.mp3') #잘했어



print('사료와 클릭커를 출력합니다')
c='4'
c=c.encode('utf-8')
arduino.write(c)
playsound.playsound('clicker.mp3')
