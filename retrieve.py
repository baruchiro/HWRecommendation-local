import psutil
import platform
import json
import shutil
import cpuinfo

# import json2html
# import wmi # i try to retrieve motherboard with this library. FAILED for now.

print("Machine: " + platform.machine())
print("Processor: " + platform.processor())
print("System OS: " + platform.system())
print("Version: " + platform.version())
print("CPU Number: " + str(psutil.cpu_count()))
# print("Physical CPU number: "+str(psutil.cpu_count(logical=False)))
print("Node: " + platform.node())
print("Memory info[RAM]: " + str(psutil.virtual_memory()))


total, used, free = shutil.disk_usage("\\")
obj_Disk = psutil.disk_usage('/')
print("\nHard Disk info: ")
print("Total: %d GB" % (total // (2**30)))
print("Used: %d GB" % (used // (2**30)))
print("Free: %d GB" % (free // (2**30)))
print("Percentage of usage: "+str(obj_Disk.percent)+"%")

print("\ncpu info :"+cpuinfo.get_cpu_info()['brand'])
print("architecture: "+cpuinfo.get_cpu_info()['arch'])

# <!--TODO::
# MotherBoard
# GPU


data = {}
data['platform'] = []
data['platform'].append({
    'Machine': platform.machine(),
    'Processor': platform.processor(),
    'System_OS': platform.system(),
    'Version': platform.version(),
    'CPU_Number': str(psutil.cpu_count()),
    'Node': platform.node(),
    'Memory_info[RAM]': str(psutil.virtual_memory().total),
    'Cpu_info': cpuinfo.get_cpu_info()['brand'],
    'Architecture': cpuinfo.get_cpu_info()['arch'],
    'Free_MemorySpace(HD)': "Free: %d GB" % (free // (2**30))
})
#with open('data.txt', 'w') as outfile:
#    json.dump(data, outfile)
