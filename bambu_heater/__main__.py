import asyncio
import os
import argparse
from bambu_heater.utils.status_helper import grab_status
from bambu_heater.utils.serial_helper import get_serial
import sys
from bambu_heater.devices.tplink_power import TPLINKHS300


cur_temp = None
cur_tray = None
filament_type = None

async def update_status(data):
    global cur_temp, cur_tray, filament_type
    chamber_temp = data.get("print", {}).get("chamber_temper")
    # .print.ams.tray_now
    tray_now = data.get("print", {}).get("ams", {}).get("tray_now")
    # '.print.ams.ams[0].tray[1].tray_type'
    if tray_now != '255':
        cur_tray = tray_now
        filament_type = data.get("print", {}).get("ams", {})[0].get("ams", {})[int(tray_now)].get("tray_type")
    else:
        cur_tray = None
    if chamber_temp is not None:
        cur_temp = float(chamber_temp)
        print(f"Chamber Temperature: {chamber_temp}")
    if filament_type is not None:
        print(f"Filament Type: {filament_type}")

async def monitor_tempature(temp, device):
    global cur_temp
    is_on =  await device.get_status()
    while True:
        if cur_temp is not None:
            if float(cur_temp) < temp and cur_tray is not None:
                if not is_on:
                    print("Turning heater on")
                    await device.turn_on()
                    is_on = True
            else:
                if is_on:
                    print("Turning heater off")
                    is_on = False
                    await device.turn_off()
        else:
            print("Waiting for first temp reading")
        await asyncio.sleep(1)


# Main application
async def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Bambu Lab Printer Temperature Monitor")
    parser.add_argument("--host", help="IP address of the Bambu Lab Printer")
    parser.add_argument("--password", help="Access code for the Bambu Lab Printer")
    args = parser.parse_args()

    tplink_device = TPLINKHS300(
        name="TP-Link Power Strip",
        host="192.168.42.37",
        outlet_index=0  # Control outlet 0 (first outlet)
    )

    # Determine the host and password with priority: CLI > Environment
    host = args.host or os.getenv("BAMBU_PRINTER_IP")
    password = args.password or os.getenv("BAMBU_PRINTER_ACCESS_CODE")

    # Validate that at least one source exists for both host and password
    if not (args.host or os.getenv("BAMBU_PRINTER_IP")):
        print("Error: Host is required. Provide it with --host or set BAMBU_PRINTER_IP in the environment.")
        sys.exit(1)

    if not (args.password or os.getenv("BAMBU_PRINTER_ACCESS_CODE")):
        print("Error: Password is required. Provide it with --password or set BAMBU_PRINTER_ACCESS_CODE in the environment.")
        sys.exit(1)

    print(f"Using host: {host}")
    print(f"Using password: {'*' * len(password)}")  # Mask the password for security

    # Static configuration
    port = 8883  # Bambu printers use this port
    username = "bblp"  # Username is hardcoded for all printers

    # Get the serial number for dynamic topic resolution
    serial = get_serial(host, 990)
    if not serial:
        print("Error: Failed to retrieve printer serial number.")
        sys.exit(1)

    print(f"Retrieved serial: {serial}")
    topic = f"device/{serial}/report"

    # Run the MQTT subscription
   

    await asyncio.gather(
        grab_status(host, port, username, password, topic, update_status),
        monitor_tempature(temp=60, 
                          device=tplink_device),
    )


# Entry point
if __name__ == "__main__":
    asyncio.run(main())


'''
└─$ mosquitto_sub -h 192.168.42.87 -p 8883 \
  -u 'bblp' -P '39646532' \
  --cafile ./blcert.pem \
  --insecure \
  -t device/00M09D492601136/report | jq '.print.ams.ams[0].tray[1].tray_type'
  '''

'''
┌──(env)─(khan㉿Brandons-MacBook-Pro)-[~/scratch/bambu-x1c-heater]
└─$ mosquitto_sub -h 192.168.42.87 -p 8883 \
  -u 'bblp' -P '39646532' \
  --cafile ./blcert.pem \
  --insecure \
  -t device/00M09D492601136/report | jq '.print.ams.tray_now'

"0"
"0"
"0"
"0"
"255"
"1"
"1"
"1"
"1"
"1"
"1"
"1"
'''