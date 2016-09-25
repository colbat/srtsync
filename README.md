# srtsync
Srtsync is a python script to synchronize a whole SubRip (.srt) subtitles file.

## Installation
```
git clone https://github.com/colbat/srtsync.git && cd srtsync
```

## Usage
### Command line
It can be run directly from the command line with the following options:
```
-i <input file>
-o <output file>
-t <syncing time in ms, can be negative>
-c <current unsynced time, string in format hh:mm:ss,ms>
-e <expected time, string in format hh:mm:ss,ms>
```

Examples:
```
./srtsync.py -i subtitles.srt -o synced-subtitles.srt -t 1500
./srtsync.py -i subtitles.srt -o synced-subtitles.srt -c "00:10:09,370" -e "00:10:10,870"
```

### Module
Or it can be used by importing it as module and calling the ```sync``` function:
```
from srtsync import sync

sync("subtitles.srt", "synced-subtitles.srt", 1500)
sync("subtitles.srt", "synced-subtitles.srt", "00:10:09,370", "00:10:10,870")
```

## Tests
To run the tests:
```
python -m unittest discover
```

## License
Copyright (c) 2016 Gaëtan Covelli.
Released under the [MIT License](https://github.com/colbat/srtsync/blob/master/LICENSE)
