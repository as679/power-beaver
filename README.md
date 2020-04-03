# power-beaver
---
Harness the phenomenal super power of the beaver for your delight and delectation!
:+1:
---
Some usage examples:

Get the IP addresses of some Virtual Services:
```
~$ for i in cca-a cca-b ccb-a ccb-b; do echo $i; ./avicli.py --controller $i virtualservice-inventory show gslb | jq '.[].runtime.vip_summary[].ip_address.addr'; done
cca-a
"10.10.2.59"
ccb-b
"10.11.2.59"
ccb-a
"10.10.2.61"
ccb-b
"10.11.2.61"
```

Get some GSLB information:
```
~$ for i in `./avicli.py --controller cca-a --tenant '*' --param fields=name gslbservice list | jq '.[].name' | grep app | tr -d '"'`; do echo $i; ./avicli.py --controller osp-a --tenant '*' gslbservice show $i | jq '.[] | .domain_names, .groups[].members[].ip.addr'; done
app-cloud-admin-ui
[
  "app-cloud-admin-ui.gslb-cca.example.com"
]
"10.10.1.35"
"10.11.1.35"
app-api-manager-ui
[
  "app-api-manager-ui.gslb-cca.example.com"
]
"10.10.1.37"
"10.11.1.37"
app-platform-api
[
  "app-platform-api.gslb-cca.example.com"
]
"10.10.1.38"
"10.11.1.39"
app-consumer-api
[
  "app-consumer-api.gslb-cca.example.com"
]
"10.10.1.39"
"10.11.1.40"
app-analytics-ingestion
[
  "app-analytics-ingestion.gslb-cca.example.com"
]
"10.10.1.40"
"10.11.1.41"
app-analytics-client
[
  "app-analytics-client.gslb-cca.example.com"
]
"10.10.1.41"
"10.11.1.43"
```

Find and delete some pools:
```
~$ for pool in $(./avicli.py --controller avi-ako-1 pool list | jq -r .[].uuid); do echo $pool; ./avicli.py --controller avi-ako-1 pool delete $pool; done
pool-9eea9ff3-ad60-412d-b9ed-2a95931f9431
pool-ede70601-2b5e-4d21-9c7b-7fd304962277
pool-e4e52920-3e09-43e8-8cde-1193d5c20c45
pool-02b89d56-6bcd-43b3-992a-6c2f043c7802
pool-61e49ba7-ddce-48bb-85a9-ef807a74c6e6
pool-b54ddfb0-de11-4a5e-b167-8a6263b33289
pool-fcb0c405-9ad2-4416-83e1-18e7c6cea6b3
pool-551e0137-10e2-492b-a861-6e36739478e2
pool-59370e8b-0074-42f1-910c-e04e1f251652
```