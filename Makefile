.PHONY: test_lib clean

test_lib: sgxlib/enclave.signed.so sgxlib/sgxdb.so
	cd sgxlib && python sgxdblib.py

sgxlib/enclave.signed.so:
	cd sgxlib && make SGX_MODE=HW SGX_PRERELEASE=1

sgxlib/sgxdb.so:
	cd sgxlib && make SGX_MODE=HW SGX_PRERELEASE=1

clean:
	cd sgxlib && make clean
