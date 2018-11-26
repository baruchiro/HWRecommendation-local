import psutil
import platform

print("Machine: "+platform.machine())
print("Processor: "+platform.processor())
print("System OS: "+platform.system())
print("Version: "+platform.version())
print("CPU Number: "+str(psutil.cpu_count()))
#print("Physical CPU number: "+str(psutil.cpu_count(logical=False)))
print("Node: "+platform.node())
print("Memory info[RAM]: "+str(psutil.virtual_memory()))

#TODO::
#Ghz
#
#