import frida, os, itertools

from pathlib import Path
from androguard.core.bytecodes.apk import APK
from glob import glob
from time import sleep

# dex 파일들이 담길 리스트 선언
memory_list = []

# on_message 함수에서 frida script의 결과를 받아옴
def on_message(message, data):
    if message['type'] == 'send':
        # 받아와진 값은 str이기 때문에 int형으로 변경해 줌
        payload = message['payload']
        payload = payload.split(",")
        payload = ' '.join(payload).split()
        payload = list(map(int, payload))
        
        # dex 파일 size를 찾음
        dex_size = payload[0x20:0x24]
        dex_size.reverse()
        hex_str = ''
        
        # dex 파일 size를 int형으로 변경
        for num in dex_size:
            hex_value = hex(num)
            hex_str += hex_value[2:]
        hex_int = int(hex_str, 16)
        
        # 리스트에 추가
        memory_list.append(payload[0:hex_int])
    else:
        print(message)

def mem_data(mem_dataset, detected, PACKAGE_NAME):
    # 정상과 악성을 따로 모아두는 폴더를 생성
    try:
        if not os.path.exists(detected):
            os.makedirs(detected)
    except OSError:
        print ('Error: Creating directory. ' +  detected)

    # dex 파일들의 값을 패키지 명으로된 bin 파일로 생성
    with open(r"{}\{}.bin".format(detected, PACKAGE_NAME), "wb") as f:
        f.write(bytes(mem_dataset))


def dex_operation(apk_list):
    global memory_list
    detected = ""
    
    # 샘플 apk가 정상인지 악성인지 확인
    if "benign" in apk_list[0]:
        detected = "benign"
    else:
        detected = "malware"
    
    for apk in apk_list:
        try:
            # 에뮬레이션에 샘플 파일 설치
            os.system('adb install -t -r {}'.format(apk))

            # 샘플 파일의 패키지 명을 가져 옴
            apkf = APK(apk)
            PACKAGE_NAME = apkf.get_package()

            # frida script 경로 지정
            js_path = r"C:\Users\apk82\Desktop\payload2.js"
            # frida script를 가져 옴
            jscode = Path(js_path).read_text()

            # frida 연결 후 샘플 파일 실행
            device = frida.get_usb_device(1)
            pid = device.spawn(PACKAGE_NAME)
            session = device.attach(pid)

            # frida script 실행
            script = session.create_script(jscode)
            script.on('message', on_message)
            script.load()
            # frida script가 전부 다 실행될 동안 대기
            sleep(110)

            # 샘플 파일 실행 종료
            os.system('frida-kill -U {}'.format(pid))
            # 샘플 파일 삭제
            os.system('adb uninstall {}'.format(PACKAGE_NAME))
            
            # 다중 리스트를 하나의 리스트로 만듦
            memory_list = list(itertools.chain.from_iterable(memory_list))
        except Exception as e:
            print(e)
            continue
        
        # dex 파일들을 저장하는 함수
        mem_data(memory_list, detected, PACKAGE_NAME)
        memory_list = []

if __name__ == '__main__':
    # 샘플 파일들의 경로를 읽어 옴
    benign_list = glob(r'D:\benign_apk(23.2)\\'+'*.apk')
    malware_list = glob(r'D:\malware_apk(16.6~23.3)\\'+'*.apk')
    
    # dex 추출 시작
    dex_operation(benign_list)
    dex_operation(malware_list)
