#include <Wire.h>

// I2C adress MPU
#define AD0 0x68
#define AD1 0x69
#define MPU9250_ADDRESS AD0

// Registers of accelerometer
#define ACCEL_XOUT_H 0x3B
#define ACCEL_XOUT_L 0x3C
#define ACCEL_YOUT_H 0x3D
#define ACCEL_YOUT_L 0x3E
#define ACCEL_ZOUT_H 0x3F
#define ACCEL_ZOUT_L 0x40

// Registers of thermometer
#define TEMP_OUT_H 0x41
#define TEMP_OUT_L 0x42

// Registers of gyroscope
#define GYRO_XOUT_H 0x43
#define GYRO_XOUT_L 0x44
#define GYRO_YOUT_H 0x45
#define GYRO_YOUT_L 0x46
#define GYRO_ZOUT_H 0x47
#define GYRO_ZOUT_L 0x48

// HW check registr
#define MPU_WHO_AM_I 0x75 // Should return 0x71 for MPU-9250

// Registers of accelerometer offsets
#define XA_OFFSET_H 0x77
#define XA_OFFSET_L 0x78
#define YA_OFFSET_H 0x7A
#define YA_OFFSET_L 0x7B
#define ZA_OFFSET_H 0x7D
#define ZA_OFFSET_L 0x7E

// Registers of gyroscope offsets
#define XG_OFFSET_H 0x13
#define XG_OFFSET_L 0x14
#define YG_OFFSET_H 0x15
#define YG_OFFSET_L 0x16
#define ZG_OFFSET_H 0x17
#define ZG_OFFSET_L 0x18

// Registers for range settings
#define GYRO_CONFIG 0x1B
#define GYRO_RANGE 3 // Select GYRO_FS_SEL (0 : +250dps; 1 : +500dps; 2 : +1000dps; 3 : +2000dps)
                     // divison: FS_SEL    (0 :  131   ; 1 :  65.5  ; 2    32.8   ; 3 :  16.4   ) 

#define ACCEL_CONFIG 0x1C
#define ACCEL_RANGE 3 // Select ACCEL_FS_SEL (0 : +-2g; 1 : +-4g; 2 : +-8g; 3 : +-16g)
                      // divison: FS_SEL     (0 : 2^14; 1 : 2^13; 2 : 2^12; 3 :  2^11) 

// Registry nastavení I2C
#define INT_PIN_CFG 0x37
#define INT_ENABLE  0x38
#define MAG_RANGE 1 // Select resolution (0 : 14 bits - 0.6mG/per LSB; 1 : 16 bits . 0.15mG per LSB
#define MAG_MODE  6 // Select MAG SPS (2 : 8Hz; 6 : 100Hz)

// Registry magnetometr
#define AK8963_ADDRESS   0x0C
#define AK_WHO_AM_I  0x00 // should return 0x48

#define AK8963_ST1     0x02
#define MAGX_XOUT_H    0x03
#define MAGX_XOUT_L    0x04
#define MAGY_XOUT_H    0x05
#define MAGY_XOUT_L    0x06
#define MAGZ_XOUT_H    0x07
#define MAGZ_XOUT_L    0x08
#define AK8963_ST2     0x09
#define AK8963_CNTL    0x0A



#define SPS 250      //Sample rate Hz
#define SPS_MAG 80   //Samples magnetometr - optimal
int skip = SPS/SPS_MAG;     //Number of skips in main loop
int mag_counter = 0;

#define FLEX_PIN A1
int flex;

uint32_t delay_1 = 1000000 / SPS;
uint32_t timer_1;

const int buff_MPU = 14;
uint8_t raw_data_MPU[buff_MPU];
int raw_int_data_MPU[6];

const int buff_AK = 7;
uint8_t raw_data_AK[buff_AK];
int raw_int_data_AK[3];


/*
  int32_t calib_x = 0;
  int32_t calib_y = 0;
  int32_t calib_z = 0;
  int counter = 0;
  int avg = 2500;
*/

// Obtained from MATLAB calibration
int mag_calib[3] = {355, 46, -165};


void setup() {
  Serial.begin(115200);
  Wire.begin();
  pinMode(FLEX_PIN, INPUT);

  delay(500);

  enable_AK(MPU9250_ADDRESS);

  manual_accel_calibration(MPU9250_ADDRESS);
  manual_gyro_calibration(MPU9250_ADDRESS);

  set_accel_range(MPU9250_ADDRESS, ACCEL_RANGE);
  set_gyro_range(MPU9250_ADDRESS, GYRO_RANGE);

  delay(500);

  // Connection test MPU-9250
  int x = read_byte(MPU9250_ADDRESS, MPU_WHO_AM_I);
  if (x != 0x71) {
    Serial.print("MPU-9250 Who Am I response: 0x");
    Serial.println(x, HEX);
    Serial.println("Should be 0x71 - ABORTED!");
    while (1) {
    }
  }

  // Connection test AK-8963
  int y = read_byte(AK8963_ADDRESS, AK_WHO_AM_I);
  if (y != 0x48) {
    Serial.print("AK-8963 Who Am I response: 0x");
    Serial.println(x, HEX);
    Serial.println("Should be 0x48 - ABORTED!");
    while (1) {
    }
  }

  if (SPS/skip > 95) {
    skip++; // Aby nevzniklo vyšší čtení z magnetometru než je 100 - jinak začne házet blbosti
  }
}

void loop() {
  if (micros() - timer_1 >= delay_1) {
    timer_1 = micros();
    read_bytes(MPU9250_ADDRESS, ACCEL_XOUT_H, buff_MPU, &raw_data_MPU[0]);
    if (mag_counter == 0){
        read_bytes(AK8963_ADDRESS, MAGX_XOUT_H, buff_AK, &raw_data_AK[0]);
        mag_counter = -skip;
    }
    mag_counter++;
    flex = analogRead(FLEX_PIN);    

    raw_int_data_MPU[0] = raw_data_MPU[1] | raw_data_MPU[0] << 8;
    raw_int_data_MPU[1] = raw_data_MPU[3] | raw_data_MPU[2] << 8;
    raw_int_data_MPU[2] = raw_data_MPU[5] | raw_data_MPU[4] << 8;
    // We dont need temperature (I guess?)
    raw_int_data_MPU[3] = raw_data_MPU[9] | raw_data_MPU[8] << 8;
    raw_int_data_MPU[4] = raw_data_MPU[11] | raw_data_MPU[10] << 8;
    raw_int_data_MPU[5] = raw_data_MPU[13] | raw_data_MPU[12] << 8;

    raw_int_data_AK[0] = (raw_data_AK[0] | raw_data_AK[1] << 8) - mag_calib[0];
    raw_int_data_AK[1] = (raw_data_AK[2] | raw_data_AK[3] << 8) - mag_calib[1];
    raw_int_data_AK[2] = (raw_data_AK[4] | raw_data_AK[5] << 8) - mag_calib[2];

    /*
        calib_x += raw_int_data_MPU[3];
        calib_y += raw_int_data_MPU[4];
        calib_z += raw_int_data_MPU[5];
        counter++;
    */

    for (int i = 0; i < 6; i++) {
      Serial.print(raw_int_data_MPU[i]);
      Serial.print(' ');
    }

    for (int i = 0; i < 3; i++) {
      Serial.print(raw_int_data_AK[i]);
      Serial.print(' ');
    }
    Serial.print(flex);
    Serial.print(" \n");
  }
  /*
    if (counter == avg) {
      Serial.print(calib_x/avg);
      Serial.print(' ');
      Serial.print(calib_y/avg);
      Serial.print(' ');
      Serial.print(calib_z/avg);
      Serial.println();
      counter = 0;
      calib_x = 0;
      calib_y = 0;
      calib_z = 0;
    }
  */
}


uint8_t read_byte(uint8_t addr, uint8_t reg) {
  uint8_t res;
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(addr, 1);
  res = Wire.read();
  return res;
}

void read_bytes(uint8_t addr, uint8_t reg, int count, uint8_t * data_buffer) {
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(addr, count);
  for (uint8_t i = 0; i < count; i++) {
    data_buffer[i] = Wire.read();
  }
}

void write_byte(uint8_t addr, uint8_t reg, uint8_t data)
{
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.write(data);
  Wire.endTransmission(true);
}

void manual_accel_calibration(uint8_t addr) {
  write_byte(addr, XA_OFFSET_H, -18);
  write_byte(addr, XA_OFFSET_L, 100); // (50 << 1);
  write_byte(addr, YA_OFFSET_H, -44);
  write_byte(addr, YA_OFFSET_L, 60);  // (30 << 1);
  write_byte(addr, ZA_OFFSET_H, 37);
  write_byte(addr, ZA_OFFSET_L, 220); // (110 << 1);
}

void manual_gyro_calibration(uint8_t addr) {
  write_byte(addr, XG_OFFSET_H, 0);
  write_byte(addr, XG_OFFSET_L, 27);
  write_byte(addr, YG_OFFSET_H, -1);
  write_byte(addr, YG_OFFSET_L, 205);
  write_byte(addr, ZG_OFFSET_H, 0);
  write_byte(addr, ZG_OFFSET_L, 232);
}

void set_accel_range(uint8_t addr, uint8_t range) {
  write_byte(addr, ACCEL_CONFIG, range << 3);
}

void set_gyro_range(uint8_t addr, uint8_t range) {
  write_byte(addr, GYRO_CONFIG, range << 3);
}

void enable_AK(uint8_t addr) {
  write_byte(addr, INT_PIN_CFG, 0x22); // Přenastavení do master modu
  write_byte(addr, INT_ENABLE, 0x01);
  write_byte(AK8963_ADDRESS, AK8963_CNTL, MAG_RANGE << 4 | MAG_MODE);
  delay(10);
}
