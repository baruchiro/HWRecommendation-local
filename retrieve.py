import psutil
import platform
import json
import shutil
import cpuinfo
import requests
import multiprocessing
import os
import webbrowser
from wmi import WMI
import sys


def log(text):
    if debug:
        print(text)


if __name__ == "__main__":
    debug = "debug" in sys.argv
    multiprocessing.freeze_support()
    memory_types = {
        1: "Other",
        2: "Unknown",
        3: "DRAM",
        4: "EDRAM",
        5: "VRAM",
        6: "SRAM",
        7: "RAM",
        8: "ROM",
        9: "FLASH",
        10: "EEPROM",
        11: "FEPROM   ",
        12: "EPROM",
        13: "CDRAM",
        14: "3DRAM",
        15: "SDRAM",
        16: "SGRAM",
        17: "RDRAM",
        18: "DDR",
        19: "DDR2",
        20: "DDR2 FB-DIMM",
        21: "Reserved",
        22: "Reserved",
        23: "Reserved",
        24: "DDR3",
        25: "FBD2",
        26: "DDR4",
        27: "LPDDR",
        28: "LPDDR2",
        29: "LPDDR3",
        30: "LPDDR4",
    }
    # 01h Other
    # 02h Unknown
    # 03h DRAM
    # 04h EDRAM
    # 05h VRAM
    # 06h SRAM
    # 07h RAM
    # 08h ROM
    # 09h FLASH
    # 0Ah EEPROM
    # 0Bh FEPROM
    # 0Ch EPROM
    # 0Dh CDRAM
    # 0Eh 3DRAM
    # 0Fh SDRAM
    # 10h SGRAM
    # 11h RDRAM
    # 12h DDR
    # 13h DDR2
    # 14h DDR2 FB-DIMM
    # 15h-17h Reserved
    # 18h DDR3
    # 19h FBD2
    # 1Ah DDR4
    # 1Bh LPDDR
    # 1Ch LPDDR2
    # 1Dh LPDDR3
    # 1Eh LPDDR4

    cpu = cpuinfo.cpuinfo.get_cpu_info()
    memory = psutil.virtual_memory()
    disk = shutil.disk_usage("\\")

    wmi = WMI()

    def get_num_of_ram_slots():
        memory = wmi.query(
            "select MemoryDevices from win32_PhysicalMemoryArray")
        return int(memory[0].MemoryDevices)

    def get_memories():
        result = []
        memories = wmi.query("select * from Win32_PhysicalMemory")
        for memory in memories:
            obj = {
                    "capacity": int(memory.Capacity),
                    "ghz": int(memory.Speed),
                    "bank label": memory.bankLabel,
                    "Device locator:": memory.DeviceLocator
                }
            if hasattr(memory, "SMBIOSMemoryType"):
                obj["type"] = memory_types[int(memory.SMBIOSMemoryType)]
            else:
                obj["type"] = memory_types[int(memory.MemoryType)]
            result.append(obj)
        return result

    def get_motherboard():
        return wmi.Win32_baseboard()[0]

    def get_gpus():
        res1 = []
        gpu = wmi.query("select * from Win32_VideoController")
        for gpus in gpu:
            if gpus.VideoProcessor is not None:
                res1.append(
                    {
                        "name": gpus.Name,
                        "processor": gpus.VideoProcessor
                    }
                )
        return res1

    def get_hardDisk():
        res2 = []
        hd = wmi.query("select * from Win32_DiskDrive")
        for hds in hd:
            res2.append(
                {
                    "model": hds.model,
                    "capacity": int(hds.Size)
                }
            )
        return res2

    def get_ram_maxcapacity():
        return wmi.Win32_PhysicalMemoryArray()[0].MaxCapacity

    # Same thing about mediaType HardDisk, and GPU details.

    mobo = get_motherboard()

    data = {
        "processor": {
            "name": cpu['brand'],
            "gHz": cpu['hz_advertised_raw'][0],
            "numOfCores": cpu['count'],
            "architecture": f"x{cpu['bits']}"
        },
        "memories": get_memories(),
        "disks": get_hardDisk(),
        "motherBoard": {
            "ddrSockets": get_num_of_ram_slots(),
            "maxRam": get_ram_maxcapacity(),
            "Manufacturer": mobo.Manufacturer,
            "product": mobo.Product
        },
        "gpus": get_gpus()
    }

    log(data)

    headers = {'Content-Type': 'application/json'}
    r = requests.post(
        'https://hwwebapi.azurewebsites.net/api/Computers/Body', json=data, headers=headers)
    log(r.status_code)
    log(r.text)
    idS = str(r.json()['id'])
    webbrowser.open('https://baruchiro.github.io/HWRecommendation-WebAPI/?id='+idS)