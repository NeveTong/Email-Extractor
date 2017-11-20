# Email-Extractor

This is an Email Address Extractor to retrieve a scholar's email address from Google search results of his/her name and affiliation.

## Usage

### 1. Prerequisites

* Python v3.5
* Proxy pool

### 2. Input files

* Put files exported from AMiner.org into directory "/data/Jonrnal_name/Project_name/Original".
* For first-time user, add proxy ip list into file "/data/proxy/ips.txt", then run the following to prepare proxy pool.
```
python proxies_info.py
```

### 3. Run

Run:
```
python main.py
```
That's all!

Then you can find the output files in directory "/data/Jonrnal_name/Project_name/Modified".
