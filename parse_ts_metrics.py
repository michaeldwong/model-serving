from datetime import datetime


infile = '/home/mike/Documents/serve/logs/ts_metrics.log'
with open(infile, 'r') as f:
    timestamp_to_num_requests = {}
    for line in f.readlines():
#        raw_dt = line.split(' - ')[0].strip().replace(',', '.')
#        timestamp_format = "%Y-%m-%dT%H:%M:%S.%f"
        # Above includes ms, below excludes
        raw_dt = line.split(' - ')[0].split(',')[0]
        timestamp_format = "%Y-%m-%dT%H:%M:%S"
        # Parse the timestamp string
        timestamp = datetime.strptime(raw_dt, timestamp_format)
        if timestamp not in timestamp_to_num_requests:
            timestamp_to_num_requests[timestamp] = 0
        if 'ts_inference_requests_total.Count' in line.split(' - ')[1]:
            timestamp_to_num_requests[timestamp] += 1

total_requests = 0
for ts in timestamp_to_num_requests:
    print(ts, ' num requests ', timestamp_to_num_requests[ts])
    total_requests += timestamp_to_num_requests[ts]
print('total requests ', total_requests)


