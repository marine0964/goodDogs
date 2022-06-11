#include <Servo.h>

Servo myservoboom;                
Servo myservofood;                

int posboom = 0; //대포 서보모터 초기 위치 셋팅 초기 셋팅하고 나서 실제 작동하는걸 현장에서 잘 봐야한다.
int posfood = 0; //음식 서보모터 초기 위치 셋팅
int infraredb  = 10; //대포 적외선 센서
int infraredfh  =1;//적외선 상부
int infraredfl  = 2;//적외선 하부
int infraredl  = 11;//적외선 왼쪽
int infraredr  = 12;//적외선 오른쪽
char b; // 장애물 시리얼 통신에 해당하는 변수 설정
char d; // 센서 시리얼 통신에 해당하는 변수 설정
char a; //공을 넣었다 
char t; //훈련 판단한다
void setup() {
  Serial.begin(9600); // 시리얼 통신 값- 작동 전에 확인해보기
  // initialize digital pin 대포를 아웃풋으로 설정 as an output.
  pinMode(3, OUTPUT); // 대포
  myservoboom.attach(6);  // 서보모터 대포
  myservofood.attach(8);  // 서보모터 음식
  pinMode(infraredb, INPUT); // 대포 적외선 센서 인풋 10번
  pinMode(infraredfh, INPUT); //  정면상부 적외선 센서 인풋 1번
  pinMode(infraredfl, INPUT); // 정면하부 적외선 센서 인풋 2번
  pinMode(infraredl, INPUT); // 적외선 센서 인풋 11번
  pinMode(infraredr, INPUT); // 적외선 센서 인풋 12번
} // 초기 셋팅 이후에 계속 켜져 있고 이때 사료와 공을 장전하자!

// the loop function runs over and over again forever
void loop() {
  //시리얼 통신 가능하다면? 실행하라!
while (Serial.available()>0){
char c = Serial.read(); // 시리얼 통신에 해당하는 변수 읽어주기
if (c=='0'){
   
//정면 장애물 센서 인식 주행모드 on c=0  소스 b 변수 활용
  // 적외선 감지 센서 부터 센서값을 읽습니다.
  // 감지되면 0, 감지되지 않으면 1이 나옵니다.
  int statefh = digitalRead(infraredfh);
  int statefl = digitalRead(infraredfl);
   if(statefl == 1 && statefh == 1){//아무것도 없음
   b=20;
   Serial.print(b); // 장애물 시리얼 통신에 해당하는 변수 띄워주기
   }
   if(statefl == 0 && statefh == 1){//배설물이 있음
   b=21;
   Serial.print(b); // 장애물 시리얼 통신에 해당하는 변수 띄워주기
   } 
   if(statefl == 0 && statefh == 0){//장애물이 있음
   b=22;
   Serial.print(b); // 장애물 시리얼 통신에 해당하는 변수 띄워주기
   }
   if(statefl == 1 && statefh == 0){//개가 있음
   b=23;
   Serial.print(b); // 개 시리얼 통신에 해당하는 변수 띄워주기
      }
Serial.print(d); // 좌우 센서 시리얼 통신에 해당하는 변수 띄워주기
  int statel = digitalRead(infraredl);
  int stater = digitalRead(infraredr);
   if(statel == 1 && stater == 1  ){//물체가 없음
   d=40;
   Serial.print(d); //  시리얼 통신에 해당하는 변수 띄워주기
   } 
  if(statel == 0 && stater == 1 ){//왼쪽에 물체가 있음
   d=41;
   Serial.print(d); //  시리얼 통신에 해당하는 변수 띄워주기
   } 
   if(stater == 0 && stater == 1 ){//오른쪽에 물체가 있음
   d=42;
   Serial.print(d); // 물체 시리얼 통신에 해당하는 변수 띄워주기
   }
   if(statel == 0 && stater == 0){//집안에서는 막힌 곳
   d=43;
   Serial.print(d); // 물체 통신에 해당하는 변수 띄워주기
   }
} //주행모드 종료
  // 측정된 센서값을 시리얼 모니터에 출력합니다.
//  Serial.print("Infrared = ");
//  Serial.println(state);

if (c=='1'){ // 1번은 그냥 발사하기
  printf(c);
        // 대포 발사
          digitalWrite(3, HIGH);   // turn the 대포 (HIGH is the voltage level) 여기서 HIGH로 바꾸면 실행됨                      
          delay(2000);  // wait for 2초 모터가 가속하기까지 기다림
          //모터가 구동하고 나서 대포 서보 모터가 구동되어야한다.
        posboom = 35; // 이것도 35도 차이로 하였을 때 장전되는걸 확인
        myservoboom.write(posboom); //붐은 0-35-0로 움직임
        delay(100); // 딜레이값 0.1초 이것도 맞춘 값.. 제발 현장에서도 맞길
        posboom = 0; //대포 서보모터 초기 위치 셋팅
        myservoboom.write(posboom);   
      delay(2000);
      digitalWrite(3, LOW);   // turn the 대포 off 
      delay(1000);                       // wait for a second
}
 
  if (c=='2'){ // 2번은 적외선 인식 시에 발사하기
 // 측정된 센서값이 0(감지)면 아래 블록을 실행합니다. 강아지가 공을 넣었다
 // 적외선센서로 인식햇을 때 반복해서 대포가 발사되는 코드
  // 적외선 감지 센서 부터 센서값을 읽습니다.
  // 감지되면 0, 감지되지 않으면 1이 나옵니다.
  printf(c);
  delay (3000);
  int i =0; //몇번 발사할지 선택가능
  int stateb = digitalRead(infraredb);
  // 측정된 센서값을 시리얼 모니터에 출력합니다.
  //Serial.print("Infrared = ");
  //Serial.println(stateb);
  // 측정된 센서값이 0(감지)면 아래 블록을 실행합니다. 강아지가 공을 넣었다
  if(stateb == 0){
    //공을 넣었으니 사료를 준다
         delay(2000);
        posfood = 90; //음식은 은 0-90-0로 움직임
        myservofood.write(posfood);
        delay(200); // 딜레이값 0.1초 이미 셋팅한 값 : 현장에서 수정하지 않기를..
        posfood = 00; //음식 서보모터 초기 위치 셋팅
        myservofood.write(posfood);        
      delay(10000); // 먹는데 10초를 준다

        // 대포 발사
          digitalWrite(3, HIGH);   // turn the 대포 (HIGH is the voltage level) 여기서 HIGH로 바꾸면 실행됨
                        
          delay(2000);  // wait for 2초 모터가 가속하기까지 기다림
                           //모터가 구동하고 나서 대포 서보 모터가 구동되어야한다.

        posboom = 35; // 이것도 35도 차이로 하였을 때 장전되는걸 확인
        myservoboom.write(posboom); //붐은 0-35-0로 움직임
        delay(100); // 딜레이값 0.1초 이것도 맞춘 값.. 제발 현장에서도 맞길
        posboom = 0; //음식 서보모터 초기 위치 셋팅
        myservoboom.write(posboom);
   
      delay(2000);

      digitalWrite(3, LOW);   // turn the 대포 off 
      delay(1000);                       // wait for a second
   a=11;//강아지가 공을 넣었습니다.
   Serial.print(a); // 물체 통신에 해당하는 변수 띄워주기
   i++; // 넣을 때마다 카운트 됩니다. 
   //if(i==2){ 
    //c='3';
    //a=12;
   //Serial.print(a); // 훈련을 종료합니다.
    }
    // 경보 메세지를 시리얼 모니터에 출력합니다.
    //Serial.println("Warning");
  }

  /// 측정된 센서값이 0 이외(감지되지 않음) 이면 아래 블록을 실행합니다. 강아지가 공을 넣지 못했다.
  else{
    // 
    // 메세지를 시리얼 모니터에 출력합니다.
   delay(10000);//  강아지가 공을 넣지 못했습니다.
   c='1';//다시 발사
   a=12;
   Serial.print(a);//한번 더 쏘아주고 종료합니다.
  }
 }// 2번 닫힘
if (c=='3'){//놀이를 정지합니다.
}//3번 닫아줌
if (c=='4'){//훈련보상
  printf(c);
        delay(2000);
        posfood = 90; //음식은 은 0-90-0로 움직임
        myservofood.write(posfood);
        delay(200); // 딜레이값 0.1초 이미 셋팅한 값 : 현장에서 수정하지 않기를..
        posfood = 00; //음식 서보모터 초기 위치 셋팅
        myservofood.write(posfood);        
      delay(10000); // 먹는데 10초를 준다
}//4번 닫아줌
if (c=='5'){//훈련을 실패하였습니다. 
 
}//5번 닫아줌
}//시리얼 통신 닫아줌
}//루프 닫아줌
