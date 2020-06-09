import serial;
import string;
ser=serial.Serial('/dev/ttyACM0', baudrate=19200, timeout=10);

while 1:
    try:
        data=ser.readline();
        data=data.decode('utf-8');
        #print(repr(data));
        data=data.split("\t");
        data[-1]=data[-1].replace("\r\n", "")
        for i in range(len(data)):
                data[i]=int(data[i]);
        print(repr(data));
    except KeyboardInterrupt:
        ser.close();
        break;
    except:
        print("nope");
    
