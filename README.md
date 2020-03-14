A hacky wrapper (I build this mainly for my usage) for the awesome [Watson][https://github.com/TailorDev/Watson] time tracking CLI tool. 
I wanted that a tool which watches a git repository and changes the Watson tag based on the checked out branch.
For this tool to work you need to install Watson and to create a config file in the directory `~/.config/watson/` and add following line:
```
[options]
stop_on_start=true
```
Additionally for this script to work you need to install [PyInquirer][https://github.com/CITGuru/PyInquirer#installation]

If you have any questions or problems feel free to open an issue.
