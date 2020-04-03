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