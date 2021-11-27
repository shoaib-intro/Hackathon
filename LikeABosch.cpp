# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 17:04:07 2021

@author: ashoaib
"""

int n=4;  //nos of sensor
int Tx[4]={12,8,6,4};       //pin number: sensor 1, sensor 2,...
int Rx[4]={11,7,5,3};       //pin number: sensor 1, sensor 2,...
float Raw[4];
float Position[4]={0,41,85,130}; //all sensor midpoint are located in one line only, 
                                 // position mentoined from mid point for left most sensor
float Calc_X[6];        //for 4 sensor, total calculated outpurt wil be 4C2=6 combinations
float Calc_Y[6];
int test[6];

float Final_X, Final_Y; // final calculated values wil be stored in these variables

void setup() 
{
      Serial.begin(250000); // Starting Serial Terminal

        for(int i=0;i<n;i++)
        {
         pinMode(Tx[i], OUTPUT);   
         pinMode(Rx[i], INPUT);
        }
}

void loop() 
{

Raw_cap();
Position_calc();
Fuse_data();
Serial.print(Final_X);  // X coordinate
Serial.print("\t");
Serial.println(Final_Y);

}






//==============================Functions==============================//



//Raw_cap is function to capture data from various sensor
//by setting value of samples, average of defined samples can be taken as output
void Raw_cap()          
{ 
  float sample=1;
  for(int i=0; i<n; i++)
        { 
          Raw[i]=0;
            for(int j=0; j<sample; j++)
             {              
                digitalWrite(Tx[i], LOW);   
                pinMode(Rx[i], INPUT);
                digitalWrite(Tx[i], LOW);
                delayMicroseconds(2);
                digitalWrite(Tx[i], HIGH);
                delayMicroseconds(10);
                digitalWrite(Tx[i], LOW);
                Raw[i] =Raw[i] +  pulseIn(Rx[i], HIGH,5000);
                delay(15);
             }
          Raw[i]=Raw[i]/sample;
          Raw[i]=Raw[i]*343/2000;
    //      Serial.println(Raw[i]);
          
        }
}


//-------------------------------------------------------------------------------------//
// this function applies tringle properties to find co-ordinates of 
// various combination of ultrasound sensor
void Position_calc()
{float d1,d2,a;
int  count,test_temp;
count=0;
  for(int i=0;i<n;i++)
  {
    for(int j=i+1;j<n;j++)
    {
    d1=Raw[i]; d2=Raw[j]; a=Position[j]- Position[i];
    test_temp=check(d1,d2,a);
   
      if(test_temp==0)
        {      
            Calc_X[count]=0;
            Calc_Y[count]=0;
            test[count]=0;        
        }
    
      if(test_temp==1)
        {
          
      //applying cosine rule to calculate angle    
              float theta=acos((((d1*d1)+(a*a)-(d2*d2)))/(2*d1*a));
              Calc_X[count]=d1*cos(theta)+ Position[i]; // y coordinate 
              Calc_Y[count]=d1*sin(theta);            // X coordinate  
              test[count]=1;  
        }  

      count=count+1;   
    } 
  }
}



//-------------------------------------------------------------------------------------//
// this function check if triangle is possible our not for selected combination of sensor data
int check(float d1,float d2,float a) 
{
  int temp_test;
if(d1>d2+a || d2>d1+a  ||  a>d2+d1){return 0;}
else{return 1;}
}


//-------------------------------------------------------------------------------------//
//this function combines data of various sensor data combination with
// weitage as per accuracy of perticular combination
// and proportional to distance in between sensors
void Fuse_data()
{
float temp_sum=0;
int count=0;
Final_X=0;
Final_Y=0;
for(int i=0;i<n;i++)
    {
    for(int j=i+1;j<n;j++)
      {
        if(test[count]==1){temp_sum=temp_sum+Position[j]-Position[i];}
   
        Final_X=Final_X+Calc_X[count]*test[count]*(Position[j]-Position[i]);
        Final_Y=Final_Y+Calc_Y[count]*test[count]*(Position[j]-Position[i]);
        
        count=count+1;
      }
    }
    
  Final_X=Final_X/temp_sum;
  Final_Y=Final_Y/temp_sum;

}