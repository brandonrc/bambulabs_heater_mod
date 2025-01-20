from kasa import SmartStrip, SmartDeviceException
from bambu_heater.devices.base_power import BasePowerDevice
import asyncio

class TPLINKHS300(BasePowerDevice):
    def __init__(self, name, host, outlet_index, *args, **kwargs):
        super().__init__(name, host, outlet_index)

    async def _get_device(self):
        retries = 3
        for attempt in range(retries):
            try:
                device = SmartStrip(self.host)
                await device.update()
                return device
            except SmartDeviceException as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    await asyncio.sleep(2)
                else:
                    print(f"Failed to connect to device {self.host} after {retries} attempts.")
                    raise

    async def turn_on(self):
        """Turn on the specified outlet."""
        device = await self._get_device()
        outlet = device.children[self.outlet_index]
        await outlet.turn_on()
        print(f"{self.name} (outlet {self.outlet_index}) turned ON")



    async def turn_off(self):
        """Turn off the specified outlet."""
        device = await self._get_device()
        print("Device")
        outlet = device.children[self.outlet_index]
        await outlet.turn_off()
        print(f"{self.name} (outlet {self.outlet_index}) turned OFF")


    async def get_status(self):
        """Retrieve the current status of the specified outlet."""
        device = await self._get_device()
        outlet = device.children[self.outlet_index]
        print(f"{self.name} (outlet {self.outlet_index}) status: {outlet.is_on}")
        return outlet.is_on


# async def main():
#     device = TPLINKHS300(name="BOOM", "")

# if __name__ == "__main__":
#     asyncio.run(main())