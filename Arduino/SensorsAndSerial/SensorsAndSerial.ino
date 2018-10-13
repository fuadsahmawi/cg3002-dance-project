#include <Wire.h>
#include <Arduino_FreeRTOS.h>
#include <Arduino.h>
#include <task.h>

#define STACK_SIZE 500
#define HANDSHAKE_INIT 5
#define ACK 6
#define PERIOD_MS 20 //for period of periodic task
#define PACKET_SIZE 81

boolean debug = false;

//Sensor Variables
unsigned long currentticks, lastticks, lastticks_1;

int gyro_x, gyro_y, gyro_z;
long gyro_x_cal_1, gyro_y_cal_1, gyro_z_cal_1;
long gyro_x_cal_2, gyro_y_cal_2, gyro_z_cal_2;
long gyro_x_cal_3, gyro_y_cal_3, gyro_z_cal_3;
long gyro_x_cal_4, gyro_y_cal_4, gyro_z_cal_4;

float acc_x_f,acc_y_f,acc_z_f;
float acc_x, acc_y, acc_z;

int temperature;
//int counter = 0; //being modified used by readSensors()?

// Global Variables (used by Power())
float sensorValue;   // Variable to store value from analog read
float current = 0;       // Calculated current value
float voltage = 0;
float energy = 0;
float power = 0;
unsigned long Prevtime;

// Converts float to 4 bytes
void float2Bytes(float val, byte* bytes_array){
  // Create union of shared memory space
  union {
    float float_variable;
    byte temp_array[4];
  } u;
  // Overite bytes of union with float variable
  u.float_variable = val;
  // Assign bytes to input array
  memcpy(bytes_array, u.temp_array, 4);
}

void setup_mpu_6050_registers(){
  Wire.beginTransmission(0x68);                                        //Start communicating with the MPU-6050  (Slave Address)
  Wire.write(0x6B);                                                    //Send the requested starting register   (PWR_MGMT_1)  
  Wire.write(0x01);                                                    //Set the requested starting register    (Write all zeros + clock select x axis as gyro reference) 
  Wire.endTransmission();                                              //End the transmission
  //Configure the accelerometer (+/-8g)
  Wire.beginTransmission(0x68);                                        //Start communicating with the MPU-6050    
  Wire.write(0x1C);                                                    //Send the requested starting register   (ACCEL_CONFIG)
  Wire.write(0x18);                                                    //Set the requested starting register    (VALUE)
  Wire.endTransmission();                                              //End the transmission
  //Configure the gyro (500dps full scale)
  Wire.beginTransmission(0x68);                                        //Start communicating with the MPU-6050
  Wire.write(0x1B);                                                    //Send the requested starting register   (GYRO_CONFIG)
  Wire.write(0x08);                                                    //Set the requested starting register    (VALUE)
  Wire.endTransmission();
 
  Wire.beginTransmission(0x68);                                        //Start communicating with the MPU-6050
  Wire.write(0x1A);                                                    //Send the requested starting register   (GYRO_CONFIG)
  Wire.write(0x06);                                                    //Set the requested starting register    (VALUE)
  Wire.endTransmission();
}

void Power() {       
    float average = 0.0;
    float average_1 = 0.0;

    Prevtime = micros();
  
  for (int i = 0; i<10; i++){
    
   sensorValue = analogRead(A0);
   voltage = analogRead(A1);

   sensorValue = (sensorValue * 5) / 1023;
   voltage = (voltage * 5) / 1023;
   
   average += sensorValue;
   average_1 += voltage;
   //delay(5);
  }
     
   current = (average/10.0) / (10 * 0.1);
   average_1 = average_1 / 10;
   average_1 = average_1 * 2;
   power = average_1 * current;
   energy += power * ((micros()-Prevtime)/ 1000000.0); 
  
//  Serial.print(F("current = "));
//  Serial.print(current * 1000);
//  Serial.print(F("mA"));
//  Serial.print(F(" "));
//  Serial.print(F("voltage = "));
//  Serial.print(average_1, 2);
//  Serial.print(F("V"));
//  Serial.print(F(" "));
//  Serial.print(F("power = "));
//  Serial.print(power * 1000);
//  Serial.print(F("mW"));
//  Serial.print(F(" "));
//  Serial.print(F("energy = "));
//  Serial.print(energy,5);
//  Serial.print(F("J"));
//  Serial.println();
}

void read_mpu_6050_data(){
  //Serial.print("1");//Subroutine for reading the raw gyro and accelerometer data
  
  Wire.beginTransmission(0x68);                                        //Start communicating with the MPU-6050
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(0x68,14);//Request 14 bytes from the MPU-6050
  while(Wire.available()<14);
  acc_x = Wire.read()<<8|Wire.read();                                  //Add the low and high byte to the acc_x variable
  acc_y = Wire.read()<<8|Wire.read();                                  //Add the low and high byte to the acc_y variable
  acc_z = Wire.read()<<8|Wire.read();                                  //Add the low and high byte to the acc_z variable
  temperature = Wire.read()<<8|Wire.read();                            //Add the low and high byte to the temperature variable
  gyro_x = Wire.read()<<8|Wire.read();                                 //Add the low and high byte to the gyro_x variable
  gyro_y = Wire.read()<<8|Wire.read();                                 //Add the low and high byte to the gyro_y variable
  gyro_z = Wire.read()<<8|Wire.read();                                 //Add the low and high byte to the gyro_z variable                                              
}

void readSensors(byte* data) {   

  byte byte_low; //for changing int to byte
  byte byte_high; //for changing int to byte
  byte float_bytes[4]; //4 bytes in float format
  int index = 0; 
    
  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);
  
  read_mpu_6050_data();
  
  gyro_x -= gyro_x_cal_1;                                                
  gyro_y -= gyro_y_cal_1;                                                
  gyro_z -= gyro_z_cal_1;
                                                                       
  gyro_x = gyro_x / 65.5;
  gyro_y = gyro_y / 65.5;
  gyro_z = gyro_z / 65.5;

  byte_high = highByte(gyro_x);
  byte_low = lowByte(gyro_x);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  byte_high = highByte(gyro_y);
  byte_low = lowByte(gyro_y);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  byte_high = highByte(gyro_z);
  byte_low = lowByte(gyro_z);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  acc_x_f = acc_x / 2048.0;
  acc_y_f = acc_y / 2048.0;
  acc_z_f = acc_z / 2048.0;

  acc_x_f = acc_x_f * 9.8;
  acc_y_f = acc_y_f * 9.8;
  acc_z_f = acc_z_f * 9.8;

  float2Bytes(acc_x_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  float2Bytes(acc_y_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  float2Bytes(acc_z_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

//  Serial.print(F("x1_a= "));
//  Serial.print(acc_x_f);
//  Serial.print(F(","));
//  Serial.print(F("y1_a= "));
//  Serial.print(acc_y_f);
//  Serial.print(F(","));
//  Serial.print(F("z1_a= "));
//  Serial.print(acc_z_f);
//  Serial.print(F(","));
//  Serial.print(F("x1_g= "));
//  Serial.print(gyro_x);
//  Serial.print(F(","));
//  Serial.print(F("y1_g= "));
//  Serial.print(gyro_y);
//  Serial.print(F(","));
//  Serial.print(F("z1_g= "));
//  Serial.print(gyro_z);
//  Serial.println();
    
  digitalWrite(4, HIGH);
  digitalWrite(5, LOW);
  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);
  
  read_mpu_6050_data();
  
  gyro_x -= gyro_x_cal_2;                                                //Subtract the offset calibration value from the raw gyro_x value
  gyro_y -= gyro_y_cal_2;                                                //Subtract the offset calibration value from the raw gyro_y value
  gyro_z -= gyro_z_cal_2;
                                                                        //Subtract the offset calibration value from the raw gyro_z value
  gyro_x = gyro_x / 65.5;
  gyro_y = gyro_y / 65.5;
  gyro_z = gyro_z / 65.5;

  byte_high = highByte(gyro_x);
  byte_low = lowByte(gyro_x);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  byte_high = highByte(gyro_y);
  byte_low = lowByte(gyro_y);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  byte_high = highByte(gyro_z);
  byte_low = lowByte(gyro_z);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  acc_x_f = acc_x / 2048.0;
  acc_y_f = acc_y / 2048.0;
  acc_z_f = acc_z / 2048.0;

  acc_x_f = acc_x_f * 9.8;
  acc_y_f = acc_y_f * 9.8;
  acc_z_f = acc_z_f * 9.8;

  float2Bytes(acc_x_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  float2Bytes(acc_y_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  float2Bytes(acc_z_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

//  Serial.print(F("x2_a= "));
//  Serial.print(acc_x_f);
//  Serial.print(F(","));
//  Serial.print(F("y2_a= "));
//  Serial.print(acc_y_f);
//  Serial.print(F(","));
//  Serial.print(F("z2_a= "));
//  Serial.print(acc_z_f);
//  Serial.print(F(","));
//  Serial.print(F("x2_g= "));
//  Serial.print(gyro_x);
//  Serial.print(F(","));
//  Serial.print(F("y2_g= "));
//  Serial.print(gyro_y);
//  Serial.print(F(","));
//  Serial.print(F("z2_g= "));
//  Serial.print(gyro_z);
//  Serial.println();

  digitalWrite(4, HIGH);
  digitalWrite(5, HIGH);
  digitalWrite(6, LOW);
  digitalWrite(7, HIGH);
  
  read_mpu_6050_data();
  
  gyro_x -= gyro_x_cal_3;                                                //Subtract the offset calibration value from the raw gyro_x value
  gyro_y -= gyro_y_cal_3;                                                //Subtract the offset calibration value from the raw gyro_y value
  gyro_z -= gyro_z_cal_3;
                                                                        //Subtract the offset calibration value from the raw gyro_z value
  gyro_x = gyro_x / 65.5;
  gyro_y = gyro_y / 65.5;
  gyro_z = gyro_z / 65.5;

  byte_high = highByte(gyro_x);
  byte_low = lowByte(gyro_x);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  byte_high = highByte(gyro_y);
  byte_low = lowByte(gyro_y);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  byte_high = highByte(gyro_z);
  byte_low = lowByte(gyro_z);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  acc_x_f = acc_x / 2048.0;
  acc_y_f = acc_y / 2048.0;
  acc_z_f = acc_z / 2048.0;

  acc_x_f = acc_x_f * 9.8;
  acc_y_f = acc_y_f * 9.8;
  acc_z_f = acc_z_f * 9.8;

  float2Bytes(acc_x_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  float2Bytes(acc_y_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  float2Bytes(acc_z_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

//  Serial.print(F("x3_a= "));
//  Serial.print(acc_x_f);
//  Serial.print(F(","));
//  Serial.print(F("y3_a= "));
//  Serial.print(acc_y_f);
//  Serial.print(F(","));
//  Serial.print(F("z3_a= "));
//  Serial.print(acc_z_f);
//  Serial.print(F(","));
//  Serial.print(F("x3_g= "));
//  Serial.print(gyro_x);
//  Serial.print(F(","));
//  Serial.print(F("y3_g= "));
//  Serial.print(gyro_y);
//  Serial.print(F(","));
//  Serial.print(F("z3_g= "));
//  Serial.print(gyro_z);
//  Serial.println();
  
  digitalWrite(4, HIGH);
  digitalWrite(5, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);
  
  read_mpu_6050_data();
  
  gyro_x -= gyro_x_cal_4;                                                //Subtract the offset calibration value from the raw gyro_x value
  gyro_y -= gyro_y_cal_4;                                                //Subtract the offset calibration value from the raw gyro_y value
  gyro_z -= gyro_z_cal_4;
                                                                        //Subtract the offset calibration value from the raw gyro_z value
  gyro_x = gyro_x / 65.5;
  gyro_y = gyro_y / 65.5;
  gyro_z = gyro_z / 65.5;

  byte_high = highByte(gyro_x);
  byte_low = lowByte(gyro_x);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  byte_high = highByte(gyro_y);
  byte_low = lowByte(gyro_y);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  byte_high = highByte(gyro_z);
  byte_low = lowByte(gyro_z);
  data[index] = byte_high;
  index++;
  data[index] = byte_low;
  index++;
  
  acc_x_f = acc_x / 2048.0;
  acc_y_f = acc_y / 2048.0;
  acc_z_f = acc_z / 2048.0;

  acc_x_f = acc_x_f * 9.8;
  acc_y_f = acc_y_f * 9.8;
  acc_z_f = acc_z_f * 9.8;

  float2Bytes(acc_x_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  float2Bytes(acc_y_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  float2Bytes(acc_z_f, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  //voltage and current
  //Power();
  
  float2Bytes(current, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

  float2Bytes(voltage, float_bytes);
  data[index] = float_bytes[0];
  index++;
  data[index] = float_bytes[1];
  index++;
  data[index] = float_bytes[2];
  index++;
  data[index] = float_bytes[3];
  index++;

//  Serial.print(F("x4_a= "));
//  Serial.print(acc_x_f);
//  Serial.print(F(","));
//  Serial.print(F("y4_a= "));
//  Serial.print(acc_y_f);
//  Serial.print(F(","));
//  Serial.print(F("z4_a= "));
//  Serial.print(acc_z_f);
//  Serial.print(F(","));
//  Serial.print(F("x4_g= "));
//  Serial.print(gyro_x);
//  Serial.print(F(","));
//  Serial.print(F("y4_g= "));
//  Serial.print(gyro_y);
//  Serial.print(F(","));
//  Serial.print(F("z4_g= "));
//  Serial.print(gyro_z);
//  Serial.println();
}

void setupSensors() {
  Wire.begin();  
  
  pinMode(4, OUTPUT);                                             // sets the digital pin 4 as output
  pinMode(5, OUTPUT);                                             // sets the digital pin 5 as output 
  pinMode(6, OUTPUT);                                            // sets the digital pin 6 as output  
  pinMode(7, OUTPUT);                                            // sets the digital pin 7 as output

  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);

  if (debug) { Serial.println("passed pin setup"); }
  
  setup_mpu_6050_registers();                                 //Setup first MPU-6050 (500dfs / +/-8g) and start the gyro
  
  if (debug) { Serial.println("passed mpu6050 setup"); }
  
  for (int cal_int = 0; cal_int < 100 ; cal_int ++){
    read_mpu_6050_data(); 
    gyro_x_cal_1 += gyro_x;                                              //Add the gyro x-axis offset to the gyro_x_cal variable
    gyro_y_cal_1 += gyro_y;                                              //Add the gyro y-axis offset to the gyro_y_cal variable
    gyro_z_cal_1 += gyro_z;                                              //Add the gyro z-axis offset to the gyro_z_cal variable
    delay(3);                                                          //Delay 3us to simulate the 250Hz program loop
    
  }
  
  digitalWrite(4, HIGH);
  digitalWrite(5, LOW);
  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);
  setup_mpu_6050_registers();                                               //Setup second MPU-6050 (500dfs / +/-8g) and start the gyro  
  for (int cal_int = 0; cal_int < 100 ; cal_int ++){
    read_mpu_6050_data(); 
    gyro_x_cal_2 += gyro_x;                                              //Add the gyro x-axis offset to the gyro_x_cal variable
    gyro_y_cal_2 += gyro_y;                                              //Add the gyro y-axis offset to the gyro_y_cal variable
    gyro_z_cal_2 += gyro_z;                                              //Add the gyro z-axis offset to the gyro_z_cal variable
    delay(3);                                                              //Delay 3us to simulate the 250Hz program loop
  }

  digitalWrite(4, HIGH);
  digitalWrite(5, HIGH);
  digitalWrite(6, LOW);
  digitalWrite(7, HIGH);
  setup_mpu_6050_registers();                                 //Setup third MPU-6050 (500dfs / +/-8g) and start the gyro
  for (int cal_int = 0; cal_int < 100 ; cal_int ++){
    read_mpu_6050_data(); 
    gyro_x_cal_3 += gyro_x;                                              //Add the gyro x-axis offset to the gyro_x_cal variable
    gyro_y_cal_3 += gyro_y;                                              //Add the gyro y-axis offset to the gyro_y_cal variable
    gyro_z_cal_3 += gyro_z;                                              //Add the gyro z-axis offset to the gyro_z_cal variable
    delay(3);                                                          //Delay 3us to simulate the 250Hz program loop
  }

  digitalWrite(4, HIGH);
  digitalWrite(5, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);
  setup_mpu_6050_registers();                                              //Setup fourth MPU-6050 (500dfs / +/-8g) and start the gyro
  for (int cal_int = 0; cal_int < 100 ; cal_int ++){
    read_mpu_6050_data(); 
    gyro_x_cal_4 += gyro_x;                                              //Add the gyro x-axis offset to the gyro_x_cal variable
    gyro_y_cal_4 += gyro_y;                                              //Add the gyro y-axis offset to the gyro_y_cal variable
    gyro_z_cal_4 += gyro_z;                                              //Add the gyro z-axis offset to the gyro_z_cal variable
    delay(3);                                                              //Delay 3us to simulate the 250Hz program loop
  } 

  gyro_x_cal_1 /= 100;                                                  //Divide the gyro_x_cal variable by 2000 to get the avarage offset
  gyro_y_cal_1 /= 100;                                                  //Divide the gyro_y_cal variable by 2000 to get the avarage offset
  gyro_z_cal_1 /= 100;                                                  //Divide the gyro_z_cal variable by 2000 to get the avarage offset

  gyro_x_cal_2 /= 100;                                                  //Divide the gyro_x_cal variable by 2000 to get the avarage offset
  gyro_y_cal_2 /= 100;                                                  //Divide the gyro_y_cal variable by 2000 to get the avarage offset
  gyro_z_cal_2 /= 100;   

  gyro_x_cal_3 /= 100;                                                  //Divide the gyro_x_cal variable by 2000 to get the avarage offset
  gyro_y_cal_3 /= 100;                                                  //Divide the gyro_y_cal variable by 2000 to get the avarage offset
  gyro_z_cal_3 /= 100;

  gyro_x_cal_4 /= 100;                                                  //Divide the gyro_x_cal variable by 2000 to get the avarage offset
  gyro_y_cal_4 /= 100;                                                  //Divide the gyro_y_cal variable by 2000 to get the avarage offset
  gyro_z_cal_4 /= 100;
  
  //Serial.println(F("Calibration Done")); //DEBUG
  if (debug) { Serial.println("passed calibration"); }
}


boolean isConnected = false;

void task1(void *p) {
   if (debug) { Serial.println("entered task1"); }
   const TickType_t xDelayDuration = pdMS_TO_TICKS(PERIOD_MS);
   byte data[PACKET_SIZE] = {}; 
   
   TickType_t prevTime = xTaskGetTickCount();
   
   while(1) {
//      while (!isConnected) { // Handshaking between RPi and Arduino Mega -- consider refactoring
//        int handshake_init = Serial.read();
//        if (handshake_init == HANDSHAKE_INIT) {
//          Serial.write(ACK);
//          while (!Serial.available()) {
//          }
//          int ack = Serial.read();
//          if (ack == ACK) {
//            isConnected = true;
//          }
//        }
//      }
      //Handshaking passed

      prevTime = xTaskGetTickCount();
      
      // simulate collecting sensor data into a byte array
//      for (int j = 0; j < PACKET_SIZE; j++) {
//         data[j] = j;
//      }

      readSensors(data);
      
      //compute and assign checksum -- consider refactoring
      data[PACKET_SIZE - 1] = data[0];
      for (int i = 1; i < sizeof(data)-1; i++) {
        data[PACKET_SIZE - 1] = data[PACKET_SIZE - 1] ^ data[i];
      }
      
      //send data to Pi -- consider using a Queue if serial data is not sent in time 
      Serial.write(data, sizeof(data));
      //Serial.print(sizeof(data));
           
      // read ACK from Pi and retry
//      int ack = Serial.read();
//      if (ack != ACK) { //issue with ACK (as seen from double printing on pi side)
//        //retry sending
//        Serial.write(data, sizeof(data));
//        ack = Serial.read();
//        if (ack != ACK) {
//          vTaskSuspendAll();
//        }
//      }
      vTaskDelayUntil(&prevTime, xDelayDuration);
      
   }
}

void setup() {
  Serial.begin(57600);

  //Calibrate and setup sensors
  setupSensors();
  
  // Create Tasks
  xTaskCreate(task1, // Pointer to the task entry function
          "Task1", // Task name
          STACK_SIZE, // Stack size
          NULL, // Pointer that will be used as parameter
          1, // Task priority
          NULL);

}

void loop() {
  // put your main code here, to run repeatedly:
  vTaskStartScheduler();
}
