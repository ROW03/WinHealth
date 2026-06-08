import platform 
import psutil

def collect_clean_data():
    # operating system info
    hostname = platform.node()
    os_name = platform.system()
    
    #ram and cpu 
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()

    #c drive
    disk_info = psutil.disk_usage('C:')

    payload = {
        "pc_name": hostname,
        "os_type": os_name,
        "cpu_usage_pct": int(cpu_usage),
         # Convert bytes to GB
        "free_ram_gb": round(memory_info.available / (1024 ** 3), 2), 
        "total_ram_gb": round(memory_info.total / (1024 ** 3), 2),
        "disk_free_gb": round(disk_info.free / (1024 ** 3), 2)
    }

    return payload

