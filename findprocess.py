import commands
import os


def command_exe(inputcmd):
    cmd = "ps -aux|tail -n 2|grep %s" % inputcmd
    out = commands.getoutput(cmd)
    processlist = out.split()
    return processlist


def file_write(prolist):
    processlogs = open("process.logs", "w+")
    for i in prolist:
        processlogs.write(str(i)+' ')
    return processlogs
    

if __name__ == "__main__":
    input_cmd = raw_input("enter the service:")
    proclist = command_exe(input_cmd)
    f_w = file_write(proclist)
    print "pid:%s" % proclist[1]
    print "mememory_usage:%s" % proclist[3]
    print "cpu_usage:%s" % proclist[2]
    print os.getcwd(), "file created in this path"
