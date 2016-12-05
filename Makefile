.PHONY: test_lib clean

test_lib: sgxlib/enclave.signed.so sgxlib/app
	cd sgxlib && ./app

sgxlib/enclave.signed.so:
	cd sgxlib && make SGX_MODE=HW SGX_DEBUG=1

sgxlib/app:
	cd sgxlib && make SGX_MODE=HW SGX_DEBUG=1

clean:
	cd sgxlib && make clean
