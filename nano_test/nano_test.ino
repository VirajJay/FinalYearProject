void setup(){

  Serial.begin(115200);
  Serial.println("demo");
  
  pinMode(13, OUTPUT);
  
}

String val;
int num=0;

void loop(){
  
  if (Serial.available()>0){
    val=Serial.readStringUntil('\n');
    num=val.toInt();
    digitalWrite(13, HIGH);
    delay(num);
    digitalWrite(13, LOW);
    Serial.println(val);
  }
}
