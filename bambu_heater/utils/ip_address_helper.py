#TODO: How can we get the ip address fast without needing that hardcoded ip address...

# import nmap
# import psutil
# from ipaddress import ip_network
# from concurrent.futures import ThreadPoolExecutor

# def get_active_network_ranges():
#     """Retrieve the IP ranges for all active interfaces, excluding 127.0.0.0/8."""
#     network_ranges = []
#     interfaces = psutil.net_if_addrs()
    
#     for interface, addresses in interfaces.items():
#         for addr in addresses:
#             if addr.family == 2:  # AF_INET (IPv4)
#                 ip = addr.address
#                 netmask = addr.netmask
#                 if ip and netmask and not ip.startswith("127."):
#                     # Calculate the network range using ip_network
#                     network = ip_network(f"{ip}/{netmask}", strict=False)
#                     network_ranges.append(str(network))
#     return network_ranges

# def scan_range(network_range):
#     """Scan a single network range for Bambu Lab Printers."""
#     nm = nmap.PortScanner()
#     print(f"Scanning network range: {network_range}")

#     # Scan for devices with open port 990 (FTP) or 8883 (MQTT)
#     nm.scan(hosts=network_range, arguments="-p 990,8883 --open")

#     # Check each host in the range
#     for host in nm.all_hosts():
#         if nm[host].has_tcp(990) or nm[host].has_tcp(8883):
#             print(f"Bambu Lab Printer found at {host}")
#             return host
#     return None

# def scan_network_for_bambu_printer():
#     print("Scanning the network for Bambu Lab Printers...")
    
#     # Get active network ranges dynamically
#     network_ranges = get_active_network_ranges()
#     if not network_ranges:
#         print("No active network ranges found.")
#         return None

#     # Use ThreadPoolExecutor to parallelize the scanning
#     with ThreadPoolExecutor(max_workers=4) as executor:
#         # Submit scan tasks for each network range
#         futures = [executor.submit(scan_range, network_range) for network_range in network_ranges]

#         # Process results as they complete
#         for future in futures:
#             result = future.result()
#             if result:
#                 print(f"Bambu Lab Printer found at {result}")
#                 return result

#     print("No Bambu Lab Printer found.")
#     return None

# # Run the scanning function
# scan_network_for_bambu_printer()
