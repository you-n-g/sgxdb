.PHONY: all clean clean2

times=100


sgx1.1.log:
	for i in `seq ${times}` ; do \
		time -o sgx1.1.log -a ansible-playbook -i ansible_hosts.py playbook1.yml ; \
	done

sgx1.0.log:
	for i in `seq ${times}` ; do \
		time -o sgx1.0.log -a ansible-playbook playbook1.yml ; \
	done

average1: sgx1.1.log sgx1.0.log
	echo "sgx1.log" >> average1
	cat sgx1.1.log | python calc_average.py >> average1
	echo "sgx0.log" >> average1
	cat sgx1.0.log | python calc_average.py >> average1


clean2:
	rm sgx2.1.log sgx2.0.log average2

sgx2.1.log:
	for i in `seq ${times}` ; do \
		time -o sgx2.1.log -a ansible-playbook -i ansible_hosts.py playbook2.yml ; \
	done

sgx2.0.log:
	for i in `seq ${times}` ; do \
		time -o sgx2.0.log -a ansible-playbook playbook2.yml ; \
	done

average2: sgx2.1.log sgx2.0.log
	echo "sgx1.log" >> average2
	cat sgx2.1.log | python calc_average.py >> average2
	echo "sgx0.log" >> average2
	cat sgx2.0.log | python calc_average.py >> average2


clean3:
	rm sgx3.1.log sgx3.0.log average3

sgx3.1.log:
	for i in `seq ${times}` ; do \
		time -o sgx3.1.log -a ansible-playbook -i ansible_hosts.py playbook3.yml ; \
		ansible-playbook playbook3.helper.yml ; \
	done

sgx3.0.log:
	for i in `seq ${times}` ; do \
		time -o sgx3.0.log -a ansible-playbook playbook3.yml ; \
		ansible-playbook playbook3.helper.yml ; \
	done

average3: sgx3.1.log sgx3.0.log
	echo "sgx1.log" >> average3
	cat sgx3.1.log | python calc_average.py >> average3
	echo "sgx0.log" >> average3
	cat sgx3.0.log | python calc_average.py >> average3


clean:
	rm sgx*.1.log sgx*.0.log average*
