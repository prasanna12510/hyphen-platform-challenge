import csv
import requests
import sys

"""
A simple program to print the result of a Prometheus query as CSV.
"""

queryfile = open('promql', 'r')
queries = queryfile.readlines()
count = 0

# Strips the newline character
for query in queries:
    count += 1
    print("query{}: {}".format(count, query.strip()))
    response = requests.get('{0}/api/v1/query'.format('http://localhost:9090'),params={'query': query.strip()})
    results = response.json()['data']['result']

    # Build a list of all labelnames used.
    labelnames = set()
    for result in results:
          labelnames.update(result['metric'].keys())

    # Canonicalize
    labelnames.discard('__name__')
    labelnames = sorted(labelnames)

    writer = csv.writer(sys.stdout)
    # Write the header,
    writer.writerow(['name', 'timestamp', 'value'] + labelnames)

    # Write the samples.
    for result in results:
        l = [result['metric'].get('__name__', '')] + result['value']
        for label in labelnames:
            l.append(result['metric'].get(label, ''))
        writer.writerow(l)
