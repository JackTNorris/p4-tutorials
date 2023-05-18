
import random
import json
import argparse

def generate_n_percent_missing(n_percent, data_size):

    sample = []
    while len(sample) < data_size * (n_percent / 100):
        sample.append(random.randrange(data_size))
        #remove duplicates
        sample = list(set(sample))
    return sample


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog='missing-pmu-packet-index-generator',
                        description='Sends pmu packets',
                        epilog='Text at the bottom of help')
        
    parser.add_argument("-m", "--missing", default = 10)
    parser.add_argument("--data_size", default = 100)
    parser.add_argument("-o", "--output", default = "missing-data.json")
    args = parser.parse_args()
    data_size = args.data_size
    missing_indexes = generate_n_percent_missing(args.missing, args.data_size)

    with open(args.output, "w") as outfile:
        json.dump(missing_indexes, outfile, skipkeys=True, indent=4)