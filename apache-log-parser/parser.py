import re
from asyncore import read, write
import csv
from collections import Counter
import datetime
from datetime import timedelta
from pprint import pprint

global_data = {

}
global_ban = {}
global_final_csv_data = []
unique_keys = []


def reader(filename):
    with open(filename) as logFile:
        log = logFile.read()
        ips_list = log.splitlines()
        populate_global_data(ips_list)

def populate_global_data(ip_list):
    for ip in ip_list:
        regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        date = ip.split(" ")[3].split("[")[1]
        endpoint = ip.split(" ")[6]
        format = '%d/%b/%Y:%X'
        stripped_date = date[0:20]
        new_date = datetime.datetime.strptime(stripped_date, format)
        matched_ip = re.search(regexp, ip).group(0)
        if matched_ip in global_data.keys():
            global_data[matched_ip].append({'date':new_date, 'endpoint':endpoint})
        else:
            global_data[matched_ip] = [{'date':new_date, 'endpoint':endpoint}]
    check_ips(global_data)


def check_ips(global_data):
    for ip in global_data.keys():
        data_for_ip = global_data[ip]
        check_if_40_in_1mins(ip, data_for_ip)
        check_if_100_in_10mins(ip, data_for_ip)
        check_if_20_in_10mins(ip, data_for_ip) 
    write_csv(global_final_csv_data)

def count_data(start_time, end_time, data_to_check):
    temp = []
    for data in data_to_check:
        if data["date"] >= start_time and data["date"] <= end_time:
            temp.append(data["date"])
    return len(temp)

def count_data_endpoint(start_time, end_time, data_to_check, end_point):
    temp = []
    for data in data_to_check:
        if (data["date"] >= start_time and data["date"] <= end_time) and (data["endpoint"] == end_point):
            temp.append(data["date"])
    return len(temp)



def check_if_40_in_1mins(ip, data_for_ip):
    for data in data_for_ip:
        format = '%d/%b/%Y:%X'
        end_time = data["date"] + timedelta(minutes=1)
        count_record = count_data(data["date"], end_time, data_for_ip)
        if count_record >= 40:
            global_final_csv_data.append(
                    {"timestamp": end_time.timestamp(),
                    "action": "BAN",
                    "ipaddress": ip
                    }
                )
            global_final_csv_data.append(
                    {
                    "timestamp": (end_time+timedelta(minutes=2)).timestamp(),
                    "action": "UNBAN",
                    "ipaddress": ip
                    }
                )

            break
        else:
            continue


def check_if_100_in_10mins(ip, data_for_ip):
    for data in data_for_ip:
        format = '%d/%b/%Y:%X'
        end_time = data["date"] + timedelta(minutes=10)
        count_record = count_data(data["date"], end_time, data_for_ip)
        if count_record >= 100:
            global_final_csv_data.append(
                    {"timestamp": end_time.timestamp(),
                    "action": "BAN",
                    "ipaddress": ip
                    }
                )
            global_final_csv_data.append(
                    {
                    "timestamp": (end_time+timedelta(hours=1)).timestamp(),
                    "action": "UNBAN",
                    "ipaddress": ip
                    }
                )
            break

def check_if_20_in_10mins(ip, data_for_ip):
    for data in data_for_ip:
        format = '%d/%b/%Y:%X'
        end_time = data["date"] + timedelta(minutes=10)
        end_point = "/login"
        count_record = count_data_endpoint(data["date"], end_time, data_for_ip, end_point)
        if count_record >= 20:
            global_final_csv_data.append(
                    {"timestamp": end_time.timestamp(),
                    "action": "BAN",
                    "ipaddress": ip
                    }
                )
            global_final_csv_data.append(
                    {
                    "timestamp": (end_time+timedelta(hours=2)).timestamp(),
                    "action": "UNBAN",
                    "ipaddress": ip
                    }
                )
            break


def write_csv(list_to_write, filename = 'output.csv'):
    with open(filename, 'w') as csvfile:
        fieldnames = ['timestamp', 'action', 'ipaddress']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(list_to_write)
    
    

if __name__ == '__main__':
    reader("access.log")
