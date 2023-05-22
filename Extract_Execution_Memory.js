// 에뮬레이션이 느려질 경우, 시간초과 되어 연결을 자동으로 종료하는 경우가 있기 때문에 이를 막기 위해 사용
setImmediate(function(){
	// 현재 스레드가 가상머신에 연결되어 있는지 확인하고 function을 호출
	Java.performNow(function () {
		// 프로세스의 메모리에서 실행 가능한 영역만 가져와 해당 값들을 forEach문으로 동작하게 함
		Process.enumerateRanges('--x').forEach(function(range) {
			try{
				// 메모리 영역을 읽어 옴
				var MData = Memory.readByteArray(range.base, range.size);
				// 메모리 영역의 값을 int형 obj로 바꾸고 동시에 str형식으로 바꿈
				var bindata = new Uint8Array(MData).toString();
				// 실행 영역 전체를 python으로 보냄
				send(bindata);
			}catch(e){
			}
		});
	});
})
