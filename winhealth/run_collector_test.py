from winhealth.collector import collect_clean_data


def run_dashboard():
    data = collect_clean_data()

    print("LIVE RESULTS:")
    print(f"Device Name:     {data['pc_name']}")
    print(f"OS Installed:    {data['os_type']}")
    print(f"Current CPU:     {data['cpu_usage_pct']}%")
    print(f"Total RAM:       {data['total_ram_gb']} GB")
    print(f"Available RAM:   {data['free_ram_gb']} GB")
    print(f"C: Drive Free:   {data['disk_free_gb']} GB")

if __name__ == "__main__":
    run_dashboard()