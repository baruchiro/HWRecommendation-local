import psutil
import platform
import json
import shutil
import cpuinfo
import requests
import multiprocessing
import os
import webbrowser

if __name__ == "__main__":
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

    class SysInfo(object):
        cpu = cpuinfo.cpuinfo.get_cpu_info()
        memory = psutil.virtual_memory()
        disk = shutil.disk_usage("\\")

        def get_num_of_ram_slots(self):
            return 0

        def get_memories(self):
            return [{"capacity": sys_info.memory.total, "type": 0, "ghz": 0}]

    current_os = platform.uname().system
    if current_os == 'Windows':
        from wmi import WMI

        class Info(SysInfo):
            def __init__(self, *args, **kwargs):
                self.wmi = WMI()
                return super().__init__(*args, **kwargs)

            def get_num_of_ram_slots(self):
                memory = self.wmi.query(
                    "select MemoryDevices from win32_PhysicalMemoryArray")
                return int(memory[0].MemoryDevices)

            def get_memories(self):
                result = []
                memories = self.wmi.query("select * from Win32_PhysicalMemory")
                for memory in memories:
                    if hasattr(memory, "SMBIOSMemoryType"):
                        result.append(
                            {
                                "capacity": int(memory.Capacity),
                                "type": memory_types[int(memory.SMBIOSMemoryType)],
                                "ghz": int(memory.Speed)
                            }
                        )
                    else:
                        result.append(
                            {
                                "capacity": int(memory.Capacity),
                                "type": memory_types[int(memory.MemoryType)],
                                "ghz": int(memory.Speed)
                            }
                        )
                return result
            def get_motherboard(self):
                res = []
                mb = self.wmi.query("select * from Win32_baseboard")
                for mbs in mb:
                    res.append(
                        {
                            "manufacturer": str(mbs.Manufacturer),
                            "product": str(mbs.Product),
                            "version": str(mbs.Version)
                        }
                    )
                return res
            def get_gpu(self):
                res2 = []
                gpu = self.wmi.query("select * from Win32_VideoController")
                for gpus in gpu:
                    res2.append(
                        {
                            "name": str(gpus.Name),
                            "adapter ram": str(gpus.AdapterRAM)
                        }
                    )
                return res2



    sys_info = Info()
    # Still not full info about motherboard, but now we have info about the product himself.
    print(sys_info.get_motherboard())
    print(sys_info.get_gpu())

    data = {
        "processor": {
            "name": sys_info.cpu['brand'],
            "gHz": sys_info.cpu['hz_advertised_raw'][0],
            "numOfCores": sys_info.cpu['count'],
            "architecture": f"x{sys_info.cpu['bits']}"
        },
        "memories": sys_info.get_memories(),
        "disks": [
            {
                "type": 0,
                "rpm": 0,
                "capacity": sys_info.disk.total
            }
        ],
        "motherBoard": {
            "ddrSockets": 0,
            "maxRam": 0,
            "sataConnections": 0,
            "architecture": 0
        },
        "gpUs": [
            {
                "cores": 0
            }
        ]
    }

    headers = {'Content-Type': 'application/json'}
    r = requests.post(
        'https://hwwebapi.azurewebsites.net/api/Computers/Body', json=data, headers=headers)
    print(r.status_code)
    print(r.text)
    idS = str(r.json()['id'])
    webbrowser.open('https://baruchiro.github.io/HWRecommendation-WebAPI/?id='+idS)