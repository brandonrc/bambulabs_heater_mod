import asyncio
import os
import argparse
from bambu_heater.utils.temp_helper import grab_temperature
from bambu_heater.utils.serial_helper import get_serial
import sys

# Main application
async def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Bambu Lab Printer Temperature Monitor")
    parser.add_argument("--host", help="IP address of the Bambu Lab Printer")
    parser.add_argument("--password", help="Access code for the Bambu Lab Printer")
    args = parser.parse_args()

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
    await grab_temperature(host, port, username, password, topic)


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
