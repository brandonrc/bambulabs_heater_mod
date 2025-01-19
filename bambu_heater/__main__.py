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

# LUT for filament types and their corresponding chamber temperatures
FILAMENT_TEMP_MAP = {
    "PLA": 35,
    "PETG": 50,
    "TPU": 40,
    "PP": 55,
    "PPA": 60,
    "PAHT": 70,
    "PA-CF": 60
    # Add more as needed
}

async def update_status(data):
    global cur_temp, cur_tray, filament_type
    chamber_temp = data.get("print", {}).get("chamber_temper")
    print(chamber_temp)
    # .print.ams.tray_now
    tray_now = data.get("print", {}).get("ams", {}).get("tray_now")
    print(tray_now)
    # '.print.ams.ams[0].tray[1].tray_type'
    if tray_now != '255':
        cur_tray = tray_now
        filament_type = data.get("print", {}).get("ams", {}).get("ams")[0].get("tray")[int(cur_tray)].get("tray_type")
        print(filament_type)
    else:
        filament_type = None
    if chamber_temp is not None:
        cur_temp = float(chamber_temp)
        print(f"Chamber Temperature: {chamber_temp}")
    if filament_type is not None:
        print(f"Filament Type: {filament_type}")


async def monitor_tempature(device):
    global cur_temp, filament_type
    is_on = await device.get_status()
    while True:
        if cur_temp is not None:
            # Lookup the target temperature; default to 35°C if filament type is unknown
            if filament_type is not None:
                target_temp = FILAMENT_TEMP_MAP.get(filament_type.upper(), 35 if filament_type else None)
            else:
                target_temp = None

            if target_temp is not None:
                if cur_temp < target_temp and cur_tray is not None:
                    if not is_on:
                        print(f"Turning heater on (target: {target_temp}°C, current: {cur_temp}°C)")
                        await device.turn_on()
                        is_on = True
                else:
                    if is_on:
                        print(f"Turning heater off (target: {target_temp}°C, current: {cur_temp}°C)")
                        is_on = False
                        await device.turn_off()
            else:
                # Handle the case for materials explicitly requiring no heat (set to None)
                print("Unknown filament type. Turning heater off for safety.")
                if is_on:
                    await device.turn_off()
                    is_on = False
        else:
            print("Waiting for valid temperature and filament type readings.")
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
        monitor_tempature(device=tplink_device),
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