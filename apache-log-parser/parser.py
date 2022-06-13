import re
from asyncore import read, write
import csv
from collections import Counter
import datetime


def loadLogs(filename):
    with open(filename) as logFile:
        log = logFile.read()
        return log


def reader(filename):
    with open(filename) as logFile:
        log = logFile.read()
        regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        ips_list = re.findall(regexp, log)
        return ips_list


globalLog = loadLogs('accesss.log')


def countIpOccurence(ips_list):
    return Counter(ips_list)


def calculateTimeSpan(startTime, endTime):
    start = startTime[12:20]
    end = endTime[12:20]
    format = '%H:%M:%S'
    startTime = datetime.datetime.strptime(start, format)
    endTime = datetime.datetime.strptime(end, format)
    diff = endTime - startTime
    return diff.total_seconds()


def bannedIpsFortyOccurence(ipcount):
    banIps = []
    # print(ipcount)
    for item in ipcount:
            firstOccurenceRegexp = re.search(rf'{item}(.*)',globalLog).group(0)
            lastOccurenceRegexp = re.findall(rf"{item}(.*)", globalLog)[-1]
            startDateTime = firstOccurenceRegexp.split("[")[1].split("]")[0]
            endDateTime = lastOccurenceRegexp.split("]")[0].split("[")[1]
            print("condition",ipcount[item])
            if((ipcount[item] > 40 and ipcount[item] < 100)):
                    banIps.append(
                        {"timestamp": endDateTime,
                        "action": "BAN for 10 minutes",
                        "ipaddress": item
                        }
                        )
            elif (ipcount[item] >=100 and (calculateTimeSpan(startDateTime,endDateTime) > 60 and calculateTimeSpan(startDateTime,endDateTime) < 1000)):

                        banIps.append(
                        {"timestamp": endDateTime,
                        "action": "BAN for 1 hour",
                        "ipaddress": item
                        }
                  )
    # print(banIps)
    return banIps
    
def write_csv(list):
    myheaders = ['timestamp', 'action',"ipaddress"]
    filename = 'output.csv'
    with open(filename, 'w', newline='') as myfile:
        writer = csv.DictWriter(myfile, fieldnames=myheaders)
        writer.writeheader()
        writer.writerows(list)

if __name__ == '__main__':
    write_csv(bannedIpsFortyOccurence(countIpOccurence(reader("accesss.log"))))
