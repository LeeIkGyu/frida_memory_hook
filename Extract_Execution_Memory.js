setImmediate(function(){
	Java.performNow(function () {
		Process.enumerateRanges('--x').forEach(function(range) {
			try{
				var MData = Memory.readByteArray(range.base, range.size);
				var bindata = new Uint8Array(MData).toString();
				send(bindata);
			}catch(e){
			}
		});
	});
})
