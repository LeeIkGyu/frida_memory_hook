import frida, os, itertools

from pathlib import Path
from androguard.core.bytecodes.apk import APK
from glob import glob
from time import sleep

memory_list = []
def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        payload = payload.split(",")
        payload = ' '.join(payload).split()
        payload = list(map(int, payload))
        memory_list.append(payload)
    else:
        print(message)

def mem_data(mem_dataset, detected, PACKAGE_NAME):
    try:
        if not os.path.exists(detected):
            os.makedirs(detected)
    except OSError:
        print ('Error: Creating directory. ' +  detected)

    with open(r"{}\{}.bin".format(detected, PACKAGE_NAME), "wb") as f:
        f.write(bytes(mem_dataset))


def api_monitor(apk_list):
    global memory_list
    detected = ""
    
    if "benign" in apk_list[0]:
        detected = "benign"
    else:
        detected = "malware"
    
    for apk in apk_list:
        try:
            os.system('adb install -t -r {}'.format(apk))

            apkf = APK(apk)
            PACKAGE_NAME = apkf.get_package()

            js_path = r"C:\Users\apk82\Desktop\payload2.js"

            jscode = Path(js_path).read_text()

            device = frida.get_usb_device(1)
            pid = device.spawn(PACKAGE_NAME)
            session = device.attach(pid)

            script = session.create_script(jscode)
            script.on('message', on_message)
            script.load()
            sleep(105)
        
            os.system('frida-kill -U {}'.format(pid))
            os.system('adb uninstall {}'.format(PACKAGE_NAME))
            memory_list = list(itertools.chain.from_iterable(memory_list))
        except Exception as e:
            print(e)
            continue

        mem_data(memory_list, detected, PACKAGE_NAME)
        memory_list = []

if __name__ == '__main__':
    benign_list = glob(r'D:\benign_apk(23.2)\\'+'*.apk')
    malware_list = glob(r'D:\malware_apk(16.6~23.3)\\'+'*.apk')
    
    api_monitor(benign_list)
    api_monitor(malware_list)
