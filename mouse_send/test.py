import serial;
import string;
import time;
ser=serial.Serial('/dev/ttyACM0', baudrate=19200, timeout=10);


time_init=time.time();
new_data=[0]*(cap_count+1);
while 1:
        if(STOP_PROGRAM.value==1):
                source.close();
                print('cap_sensing stopped');
                sys.exit();
        try:
                data=ser.readline();
                data=data.decode('utf-8');
                #print(repr(data));
                data=data.split("\t");
                data[-1]=data[-1].replace("\r\n", "")
                new_data[0]=time.time()-time_init;
                print('lol');
                for i in range(len(data)):
                        new_data[i+1]=int(data[i]);
                print(repr(new_data));
        except KeyboardInterrupt:
                source.close();
                break;
        except:
                print("nope");
