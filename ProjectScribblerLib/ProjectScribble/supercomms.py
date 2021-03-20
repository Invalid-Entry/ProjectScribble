"""
Super communications library for Project Scribbler main class
"""

import serial

class SuperComms():
    """
    Super comms serial protocol library
    """

    _ser = None # Internal serial port

    def connect(self, connection_str):
        """
        Pass a path to connect to
        """
        self._ser = serial.Serial(connection_str) 

    def disconnect(self):
        self._ser.close()

    def set_target(self, motor, location, output=True):
        """
        Set a target location in A/B distance from rest. Use output to trigger the debug prints.
        """
        if self._ser.is_open:
            neg_flag = False
            if location < 0:
                neg_flag = True
                location = abs(int(location))
            else:
                location = int(location)
            
            if motor =='A':
                if neg_flag:
                    self._ser.write(b'Z')
                else:
                    self._ser.write(b'A')
            else:
                if neg_flag:
                    self._ser.write(b'Y')
                else:
                    self._ser.write(b'B')
            
            target_bytes = location.to_bytes(4, byteorder='big')
            #print(target_bytes)
            self._ser.write(target_bytes)
            sleep(0.02)
            while(self._ser.in_waiting > 0):
                b = self._ser.read()
                if output:
                    print(b.decode('ascii'), end='')
        else:
            raise Exception("Serial is not open!")

    def get_debug(self):
        """
        Query the arduino for debug information (what its current position/target is)
        Prints output, not returns.
        """
        if self._ser.is_open:
            self._ser.write(b'D')
            sleep(0.02)
            while(self._ser.in_waiting > 0):
                b = self._ser.read()
                print(b.decode('ascii'), end='')
        
            print("---")
        else:
            raise Exception("Serial is not open!")

    def gogogo(self, wait=False, output=True):
        """
        Tell the arduino to start moving towards the target. Use wait=true to block
        until the arduino believes it has arrived (for easier control)
        """
        
        if self._ser.is_open:
            self._ser.write(b'G')
            sleep(0.02)
            
            if output:
                print("--- Making a move ---")
            
            if wait:
                end_found = False
                while not end_found:
                    sleep(0.002)

                    while(self._ser.in_waiting > 0):
                        b = self._ser.readline().decode('ascii')
                        if output:
                            print(b)
                        if "move-end" in b:
                            end_found = True
                    
            else:
                while(self._ser.in_waiting > 0):
                    b = self._ser.read()
                    print(b.decode('ascii'), end='')
        
                
        else:
            raise Exception("Serial is not open!")
    

    # def stop(self):
    #     """
    #     Note this function may not work with the current version of the arduino due to the motor lib
    #     being used for sequential steps.
    #     """
    #     if self._ser.is_open:
    #         self._ser.write(b'S')
    #         sleep(0.1)
    #         while(self._ser.in_waiting > 0):
    #             b = self._ser.read()
    #             print(b.decode('ascii'), end='')
        
    #         print("---")
    #     else:
    #         raise Exception("Serial is not open!")

    def penup(self):
        if self._ser.is_open:
            self._ser.write(b'C')
            sleep(0.1)
            while(self._ser.in_waiting > 0):
                b = self._ser.read()
                #print(b.decode('ascii'), end='')
        
            #print("---")
        else:
            raise Exception("Serial is not open!")

    def pendown(self):
        if self._ser.is_open:
            self._ser.write(b'X')
            sleep(0.1)
            while(self._ser.in_waiting > 0):
                b = self._ser.read()
                #print(b.decode('ascii'), end='')
        
            #print("---")
        else:
            raise Exception("Serial is not open!")

    def reset(self, output=True):
        if self._ser.is_open:
            self._ser.write(b'R')
            sleep(0.5)
            while(self._ser.in_waiting > 0):
                b = self._ser.read()
                if output:
                    print(b.decode('ascii'), end='')

        else:
            raise Exception("Serial is not open!")
