import asyncio
from typing import Callable

from bleak import BleakClient, BleakScanner

huawei_heartrate_char_uuid = "00002a37-0000-1000-8000-00805f9b34fb"


async def notification_handler(sender, data):
    heart_rate: int = data[1]

    print(f"Heart Rate: {heart_rate} BPM", end="\r")


async def find_address() -> str | None:
    devices = await BleakScanner.discover(timeout=5.0)

    for device in devices:
        if "HUAWEI" in (device.name or ""):
            return device.address


async def connect(address: str, notifier: Callable):
    async with BleakClient(address_or_ble_device=address) as client:
        await client.start_notify(huawei_heartrate_char_uuid, notifier)

        while True:
            await asyncio.sleep(1)
