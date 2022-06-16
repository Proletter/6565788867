import re
from asyncore import read, write
import csv
from collections import Counter
import datetime
from datetime import timedelta

global_data = {

}
# 'ip address1': [ 'time_log1', 'time_log2'],

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
        format = '%d/%b/%Y:%X'
        stripped_date = date[0:20]
        new_date = datetime.datetime.strptime(stripped_date, format)
        matched_ip = re.search(regexp, ip).group(0)
        # unique_keys.append(matched_ip)
        # if global_data.__contains__(matched_ip):
        if matched_ip in global_data.keys():
            global_data[matched_ip].append(new_date)
        else:
            global_data[matched_ip] = [new_date]
    check_ips(global_data)


def check_ips(global_data):
    for ip in global_data.keys():
        data_for_ip = global_data[ip]
        check_if_40_in_1mins(ip, data_for_ip)
        check_if_20_in_10mins(ip, data_for_ip)
    write_csv(global_final_csv_data)

def count_data(start_time, end_time, data_to_check):
    sub_items = [i for i in data_to_check if (i >= start_time and i <= end_time)]
    return len(sub_items)



def check_if_40_in_1mins(ip, data_for_ip):
    for time in data_for_ip:
        format = '%d/%b/%Y:%X'
        end_time = time + timedelta(minutes=1)
        count_record = count_data(time, end_time, data_for_ip)
        if count_record >= 40:
            # log it to central csv
            global_final_csv_data.append(
                    {"timestamp": end_time,
                    "action": "BAN for 10 minutes",
                    "ipaddress": ip
                    }
                )

            break
        else:
            continue

# def check_if_100_in_10mins(ip, data_for_ip):
#     for time in data_for_ip:
#         start_time = time 
#         end_time = time + xMinutes
#         count_record = count_data(start_time, end_time, data_for_ip)
#         if count_record >= 40:
#             # log it to central csv
#                global_final_csv_data.append(
#                         {"timestamp": end_time,
#                         "action": "BAN for 1 hour",
#                         "ipaddress": ip
#                         }
#                    )
#              break
#         else:
#             continue


def check_if_20_in_10mins(ip, data_for_ip):
    for time in data_for_ip:
        format = '%d/%b/%Y:%X'
        end_time = time + timedelta(minutes=10)
        count_record = count_data(time, end_time, data_for_ip)
        if count_record >= 20:
            # log it to central csv
            global_final_csv_data.append(
                    {"timestamp": end_time,
                    "action": "BAN for 1 hour",
                    "ipaddress": ip
                    }
                )
            break


# write list to csv with headers 
def write_csv(list_to_write, filename = 'output.csv'):
    with open(filename, 'w') as csvfile:
        fieldnames = ['timestamp', 'action', 'ipaddress']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(list_to_write)
    
    
# def write_csv(list):
#     myheaders = ['timestamp', 'action',"ipaddress"]
#     filename = 'output.csv'
#     with open(filename, 'w', newline='') as myfile:
#         writer = csv.DictWriter(myfile, fieldnames=myheaders)
#         writer.writeheader()
#         writer.writerows(list)

if __name__ == '__main__':
    reader("access.log")
