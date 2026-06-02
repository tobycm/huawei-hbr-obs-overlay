import asyncio
import queue
import threading
import time
import tkinter
from tkinter.constants import BOTH

from bleak.backends.characteristic import BleakGATTCharacteristic
from PIL import Image, ImageTk

from bt import connect, find_address

q: queue.Queue[int] = queue.Queue()


def update_heart_rate(sender: BleakGATTCharacteristic, bt_data: bytearray):
    heart_rate: int = bt_data[1]
    q.put(heart_rate)
    # print(f"Updated heart rate: {heart_rate}")


async def start() -> str:
    print("Scanning for a Huawei device in HR Data Broadcast mode")

    address: str | None = await find_address()

    if not address:
        print("No Huawei device found")
        exit(0)

    return address


address = asyncio.run(start())


def async_worker(address: str):
    print(f"Connecting to Huawei device {address}")

    asyncio.run(connect(address, notifier=update_heart_rate))


threading.Thread(target=async_worker, daemon=True, args=(address,)).start()


tk = tkinter.Tk()
tk.config(background="green")

frame = tkinter.Frame(tk, relief=tkinter.RIDGE, borderwidth=0)
frame.pack(fill=BOTH, expand=1)


heart = Image.open("heart.png")
heart = heart.resize(size=(96, 96))
photo = ImageTk.PhotoImage(heart)

heart_label = tkinter.Label(frame, image=photo, background="green")
heart_label.pack(fill=tkinter.X, expand=1)

heart_rate_label = tkinter.Label(
    frame,
    text=f"{q.get() if not q.empty() else 0}",
    font=("Comic Mono", 48, "bold"),
    foreground="white",
    background="green",
)
heart_rate_label.pack(fill=tkinter.X, expand=1)

while True:
    if q.empty():
        continue

    heart_rate: int = q.get(block=True)
    # print(f"Updated heart rate: {heart_rate}")
    heart_rate_label.config(text=f"{heart_rate}")
    heart_rate_label.config(foreground="white")
    if heart_rate > 100:
        heart_rate_label.config(foreground="red")

    tk.update()
    time.sleep(0.01)
