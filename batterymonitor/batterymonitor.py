#!/usr/bin/env python3
import serial
import mariadb
import sys
import json
import logging

def instantiateConnection():
    conn = mariadb.connect(
        host="localhost", port=3306, database="batterymonitor",
        user="rpi", password="rpi_2022-03-23")

    return conn

def add_data_to_DB(connection, batteryVoltage, stateOfCharge):
    logging.debug(f"add_data_to_DB: {batteryVoltage}, {stateOfCharge}")
    try:
        statement = """insert into status (voltage, soc) values (%s, %s)"""
        data = (batteryVoltage, stateOfCharge)
        cur = connection.cursor(prepared=True,)
        cur.execute(statement, data)       
        connection.commit()
    except mariadb.Error as e:
        print(f"Error adding entry to database: {e}")
        
def main():
    logging.basicConfig(filename='batterymonitor.log', level=logging.DEBUG, filemode='w')
    
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    try:
        conn = instantiateConnection()
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode("utf-8")
                print(f"data read from serial: {data}")
                #logging.debug(f"data read from serial: {data}")
                dict_json = json.loads(data)
                voltage = round(dict_json["voltage"], 1)
                #print(f"voltage: {voltage}, {type(voltage)}\n")
                soc = round(dict_json["soc"] * 10)
                #print(f"soc: {soc}, {type(soc)}\n")
                logging.debug(f"voltage: {voltage}, soc: {soc}")
                add_data_to_DB(conn, voltage, soc)
    except json.JSONDecodeError as e:
        print("JSON:", e)
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Oh! you pressed CTRL + C.")
        print("Program interrupted.")
        conn.close()
    finally:
        #conn.close()
        print("This was an important code, ran at the end.")
        conn.close()

if __name__ == '__main__':
    main()