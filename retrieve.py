import psutil
import platform
import json

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
data={}
data['platform'] = []
data['platform'].append({
    'Machine: ': platform.machine(),
    'Processor: ': platform.processor(),
    'System OS: ': platform.system(),
    'Version: ': platform.version(),
    'CPU Number: ': str(psutil.cpu_count()),
    'Node: ': platform.node(),
    'Memory info[RAM]: ': str(psutil.virtual_memory())
})
with open('data.txt','w') as outfile:
    json.dump(data, outfile)
