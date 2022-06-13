#include <Servo.h>
#include <SoftwareSerial.h>

Servo Left;     //좌측 주행용 서보모터 설정
Servo Right;    //우측 주행용 서보모터 설정
Servo Reload;   //발사 재장전용 서보모터 설정
Servo Height;   //발사각 설정용 서보모터 설정
Servo Feed;     //사료 지급 기능 수행용 서보모터 설정

int infred = 10;
int launch_angle = 45;
char in_data, input;
void move_front(int velocity);
void move_stop();
void move_left();
void move_right();
void launch();
void launch_height(int angle);
void give_feed();

void setup() {
              Serial.begin(9600);
              pinMode(3, OUTPUT);           //발사용 DC모터 3번 핀에 연결
              Left.attach(2);               //좌측 주행용 서보모터 2번 핀에 연결
              Right.attach(4);              //우측 주행용 서보모터 4번 핀에 연결
              Reload.attach(6);             //발사 재장전용 서보모터 6번 핀에 연결
              Height.attach(8);             //발사각 설정용 서보모터 8번 핀에 연결 
              Feed.attach(10);              //사료 지급 기능 수행용 서보모터 10번 핀에 연결
              pinMode(infred, INPUT);       //공 재장전 인식용 적외선 센서 10번 핀에 input으로 연결
             }

void loop() {
              if(Serial.available()){
                in_data = Serial.read();
                
                switch(in_data){
                  case 'g':                 //앞으로 주행하는 동작
                    input = Serial.read();  //회전속도를 입력받아 앞/뒤로 주행, 0=역주행, 180=정주행, 90=정지
                    move_front(input);
                    break;

                  case 's':       //정지하는 동작
                    move_stop();
                    break;

                  case 'l':       //좌측으로 회전하는 동작
                    move_left();
                    break;

                  case 'r':       //우측으로 회전하는 동작
                    move_right();
                    break;

                  case 'u':       //발사각도 상향 수정하는 동작, 5도씩 상승
                    launch_height(5);
                    break;

                  case 'd':       //발사각도 하향 수정하는 동작, 5도씩 하락
                    launch_height(-5);
                    break;

                  case 'f':       //공 발사하는 동작
                    launch();
                    break;
                }

                if(infred == 0){  //장전 부분의 적외선 센서가 감지되는 경우 작동
                 delay(1000);
                 give_feed();
                }
              }

}

void move_front(int velocity){
  if(velocity>180){
    Serial.print("Velocity is too high");
    velocity = 90; 
  }
  if(velocity<0){
    Serial.print("Velocity is too high");
    velocity = 90; 
  }
  Left.write(velocity);
  Right.write(velocity);
}

void move_stop(){
  Left.write(90);
  Right.write(90);   
}

void move_left(){
  Left.write(45);
  Right.write(135);  
}

void move_right(){
  Left.write(135);
  Right.write(45);  
}

void launch(){
  digitalWrite(3, HIGH);    //DC모터 동작, 이후 최고속도에 도달할때까지 대기
  delay(2000);
  Reload.write(35);         //장전되어 있는 공을 막고 있는 서보모터 각도 조절
  delay(200);
  Reload.write(0);          //장전용 서보모터 원위치
  delay(1000);
  digitalWrite(3, LOW);
}

void launch_height(int angle){
  launch_angle += angle;
  if(launch_angle <= 15){   //최저 각도 15도
    launch_angle = 15;
  }
  if(launch_angle >= 75){   //최고 각도 75도
    launch_angle = 75;
  }  
  Height.write(launch_angle);
}

void give_feed(){
  int pos_feed = 90;    //사료 지급용 서보모터 회전
  Feed.write(pos_feed);
  delay(200); 
  pos_feed = 00;        //사료 지급용 서보모터 재위치
  Feed.write(pos_feed);
}
