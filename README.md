
## Description
A Multisync TUI (Text User Interface) dashboard that monitors multisync server's metrics, QoS.<br/>
[Textual framework for python](https://textual.textualize.io/) is used for most of the heavy lifting.<br/><br/>

![Sample](assets/images/multisync_example1.png)

## Features
- values auto-refresh 
- auto-resizable widgets with terminal resize 
- color themes
- more to come


## Disclaimer
This is a work in progress-hobby project. Errors, bugs are expected.<br/><br/>

## Installation

1) Create python virtual environment
```
 python3 -m venv dashboard
```

2) Install dependecies
```
 pip install requests textual httpx rich
```

## Usage/Examples

> Activate virtual environment
```
cd dashboard
. bin/python3
```
<br/>

> View TUI dashboard for locally operated Multisync server (http://localhost:3000)
```
./dashboard.py
```
<br/>

> View TUI dashboard for remotely operated Multisync server (http://x.x.x.x:3000)

```
./dashboard.py --server 'http://x.x.x.x:3000'
```
