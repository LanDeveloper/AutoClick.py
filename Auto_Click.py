from pynput import mouse
from pynput.mouse import Controller , Button
from pynput.keyboard import Listener ,Key
import asyncio

auto_click_toggle:bool = False

async def click_loop():
    mouse_controller = Controller()
    global auto_click_toggle
    while True:
        if auto_click_toggle:
            mouse_controller.click(Button.left, 2)
            #print('click!!')
        await asyncio.sleep(0.1)

def on_press(key):
    global auto_click_toggle
    if key == Key.f8:
        auto_click_toggle = not auto_click_toggle

def transmit_keys():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    def on_press(key):
        loop.call_soon_threadsafe(queue.put_nowait, key)
    Listener(on_press=on_press).start()
    return queue

async def main():
    global auto_click_toggle
    print('auto click start!!')
    print('start/stop hot key is [F8]')
    print('leave hot key is [F9]')
    asyncio.ensure_future(click_loop())
    key_queue = transmit_keys()
    while True:
        key = await key_queue.get()
        if key == Key.f8:
            if auto_click_toggle:
                print("Loop Stop")
            else:
                print("Loop Start")
            auto_click_toggle = not auto_click_toggle
        elif key == Key.f9:
            break

asyncio.run(main())
print('leave auto click process')
