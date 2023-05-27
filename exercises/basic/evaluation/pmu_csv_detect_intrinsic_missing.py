import argparse
import sys
import datetime
sys.path.append('../')
from utilities.pmu_csv_parser import parse_csv_data


def parse_console_args(parser):
    parser.add_argument('filename')
    return parser.parse_args()

def detect_missing(pmu_csv_data_times):
    for i in range(len(pmu_csv_data_times) - 1):
        try:
            time1 = datetime.datetime.strptime(pmu_csv_data_times[i + 1][:26], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            time1 = datetime.datetime.strptime(pmu_csv_data_times[i + 1][:26], '%Y-%m-%d %H:%M:%S')
        try:
            time2 = datetime.datetime.strptime(pmu_csv_data_times[i][:26], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            time2 = datetime.datetime.strptime(pmu_csv_data_times[i][:26], '%Y-%m-%d %H:%M:%S')

        if((time1 - time2).total_seconds() > .017):
            #adding two since index starts at zero and first line for titles
            print("Data after this row is missing: ", i + 2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='missing-detector.py',
                        description='Detects the count of intrinsic missing data in a pmu csv file',
                        epilog='Text at the bottom of help')
    
    args = parse_console_args(parser)
    pmu_csv_data_times = parse_csv_data(
        args.filename,
        "TimeTag",
        ["Magnitude01", "Magnitude02", "Magnitude03"],
        ["Angle01", "Angle02", "Angle03"]
    )["times"]
    detect_missing(pmu_csv_data_times)
