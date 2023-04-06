setImmediate(function(){
	Java.performNow(function () {
		Process.enumerateRanges('r--').forEach(function(range) {
			try{
				var MData = Memory.readByteArray(range.base, range.size);
				var bindata = new Uint8Array(MData).toString();
				if (bindata.includes('100,101,120,10,48,51')){
					send(bindata);
				}
			}catch(e){
			}
		});
	});
})
