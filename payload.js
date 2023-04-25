// 에뮬레이션이 느려질 경우, 시간초과 되어 연결을 자동으로 종료하는 경우가 있기 때문에 이를 막기 위해 사용
setImmediate(function(){
	// 현재 스레드가 가상머신에 연결되어 있는지 확인하고 function을 호출
	Java.performNow(function () {
		// 프로세스의 메모리에서 읽기 가능한 영역만 가져와 해당 값들을 forEach문으로 동작하게 함
		Process.enumerateRanges('r--').forEach(function(range) {
			try{
				// 메모리 영역을 읽어 옴
				var MData = Memory.readByteArray(range.base, range.size);
				// 메모리 영역의 값을 int형 obj로 바꾸고 동시에 str형식으로 바꿈
				var bindata = new Uint8Array(MData).toString();
				
				// 메모리 영역에서 dex의 file sginature가 있는지 확인
				if (bindata.includes('100,101,120,10,48,51')){
					// 메모리 영역에서 dex의 file sginature 부터 끝까지 만 가져와 파이썬으로 보냄
					const regex = /100,101,120,10,48,51(?:,(.*))?/;
					const matches = regex.exec(bindata);
					send(matches.toString());
				}
			}catch(e){
			}
		});
	});
})
