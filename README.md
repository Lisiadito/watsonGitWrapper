A hacky wrapper (I build this mainly for my usage) for the awesome [Watson](https://github.com/TailorDev/Watson) time tracking CLI tool. 
I wanted that a tool which watches a git repository and changes the Watson tag based on the checked out branch.
For this tool to work you need to install Watson and to create a config file in the directory `~/.config/watson/` and add following line:
```
[options]
stop_on_start=true
```
Additionally for this script to work you need to install [PyInquirer](https://github.com/CITGuru/PyInquirer#installation)

# Usage
Run `./main.py` to start the script.
You will be prompted with following questions:
```
? What is the name of the project?  foo
? What is the path to the git repository?  /path/to/the/repo/
? What do you want to track? (Use arrow keys)
  ▶ Track repository
    Track only project 
```
When you select one of each you can change it by pressing `ctrl + c`. Then you get prompted again with:
```
? What do you want to track? (Use arrow keys)
  ▶ Track repository
    Track only project 
```
To quit the programm press `ctrl + c` again.

If you have any questions or problems feel free to open an issue.
