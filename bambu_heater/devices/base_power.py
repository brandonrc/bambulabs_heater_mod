class BasePowerDevice:
    def __init__(self, name, host, outlet_index=None):
        self.name = name
        self.host = host
        self.outlet_index = outlet_index

    async def turn_on(self):
        """Turn on the power device."""
        raise NotImplementedError("Subclasses must implement this method")

    async def turn_off(self):
        """Turn off the power device."""
        raise NotImplementedError("Subclasses must implement this method")

    async def get_status(self):
        """Retrieve the current status of the power device."""
        raise NotImplementedError("Subclasses must implement this method")
