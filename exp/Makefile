.PHONY: all clean

times=100


sgx1.log:
	for i in `seq ${times}` ; do \
		time -o sgx1.log -a ansible-playbook -i ansible_hosts.py playbook.yml ; \
	done

sgx0.log:
	for i in `seq ${times}` ; do \
		time -o sgx0.log -a ansible-playbook playbook.yml ; \
	done

average: sgx1.log sgx0.log
	echo "sgx1.log" >> average
	cat sgx1.log | python calc_average.py >> average
	echo "sgx0.log" >> average
	cat sgx0.log | python calc_average.py >> average

clean:
	rm sgx1.log sgx0.log average
