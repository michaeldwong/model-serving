from datetime import datetime, timedelta
import sys


if len(sys.argv) != 5:
    print('Args: <subdir (e.g., 11-6)> <model> <network> <timedelta>')
    exit()
subdir = sys.argv[1]

model = sys.argv[2]
network = sys.argv[3]
td = int(sys.argv[4])
total_sent_requests = 0
#subdir = '11-6'
#model = 'resnet18'
#network = 'ucla'
infile = f'serve-logs/{subdir}/{model}-2gpus-{network}/{model}_send_trace.txt'
timestamp_to_num_sent_requests = {}

# Outdated output format
#with open(infile, 'r') as f:
#    current_count = 0
#    for line in f.readlines():
#        if len(line.split()) == 0:
#            continue
#        if 'Sending' in line:
#            current_count = int(line.split('  ')[1].strip())
#        else:
#            timestamp = datetime.strptime(line.strip(), "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=7)
#            timestamp_to_num_sent_requests[timestamp] = current_count
#            total_sent_requests += current_count

sent_timestamps = []
with open(infile, 'r') as f:
    current_count = 0
    for line in f.readlines():
        if len(line.split()) == 0:
            continue
        items = line.split(',')
        current_count = int(items[1])
        # NOTE: This timedelta may change, look at the logs to make sure this is accurate (5 for server 1
        # and 7 or 8 for UCLA
        timestamp = datetime.strptime(items[0].strip(), "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=td)
        timestamp_to_num_sent_requests[timestamp] = current_count
        sent_timestamps.append(timestamp)
        total_sent_requests += current_count


infile = f'serve-logs/{subdir}/{model}-2gpus-{network}/ts_metrics.log'
print('sent timestamps ', sent_timestamps)


sent_timestamp_idx = 0
timestamp_to_num_requests = {}
queue_times = []
inference_latencies = []
network_times = []
total_inference_rounds = 0
last_timestamp = None
with open(infile, 'r') as f:
    for line in f.readlines():
        items = line.split(' - ')
        full_raw_dt = line.split(' - ')[0].strip().replace(',', '.')
        full_timestamp_format = "%Y-%m-%dT%H:%M:%S.%f"

        full_timestamp = datetime.strptime(full_raw_dt, full_timestamp_format)
        # Above includes ms, below excludes
        raw_dt = items[0].split(',')[0]
        timestamp_format = "%Y-%m-%dT%H:%M:%S"
        # Parse the timestamp string
        timestamp = datetime.strptime(raw_dt, timestamp_format)


        
        if timestamp not in timestamp_to_num_requests:
            timestamp_to_num_requests[timestamp] = 0
        if 'ts_inference_requests_total.Count' in items[1]:

#            if last_timestamp is None:
#                last_timestamp = timestamp
#            # timestamp is the matching one
#            diff = (timestamp - last_timestamp).total_seconds() * 1000
#            if diff >= 900 and sent_timestamp_idx < len(sent_timestamps) - 1:
#                sent_timestamp_idx += 1
#                last_timestamp = sent_timestamps[sent_timestamp_idx]
#
#            timestamp_to_num_requests[timestamp] += 1
            min_diff = 100000000
            best_timestamp = None
            for sent_ts in timestamp_to_num_sent_requests:
                if full_timestamp < sent_ts:
                    continue
                else:
                    # assume that the timestamps are in chronological order, so the 
                    # earliest sending timestamp that is earlier than the current
                    # timestamp is the matching one
                    diff = (full_timestamp - sent_ts).total_seconds() * 1000
                    if diff < min_diff:
                        best_timestamp =sent_ts 
                        min_diff = diff
            print(full_timestamp, ' - ', best_timestamp, ' = ', min_diff)

#            min_diff = (timestamp - sent_timestamps[sent_timestamp_idx]).total_seconds() * 1000
#
#            print(timestamp, ' - ', sent_timestamps[sent_timestamp_idx], ' = ', min_diff)
            network_times.append(min_diff)
        fields = items[1].split('|')
        if 'QueueTime' in fields[0]:
            queue_times.append(float(fields[0].split(':')[1]))
        elif 'ts_inference_latency_microseconds' in fields[0]:
            # DOes this include queue time??
            us_latency = float(fields[0].split(':')[1])
            inference_latencies.append(us_latency / 1000)
            total_inference_rounds += 1
        elif 'ts_queue_latency_microseconds' in fields[0]:
            us_latency = float(fields[0].split(':')[1])
            inference_latencies[-1] -= (us_latency / 1000)

total_requests = 0
for ts in timestamp_to_num_requests:
    print(ts, ' num requests ', timestamp_to_num_requests[ts])
    total_requests += timestamp_to_num_requests[ts]

print('total requests ', total_requests, ' / ' , total_sent_requests)
print('total rounds of inference ', total_inference_rounds)
print('Queue times ', queue_times)
print('Inference latencies ', inference_latencies)
print('Network times ', network_times)

