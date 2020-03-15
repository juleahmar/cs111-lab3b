# NAME: Karl Marrett,Jules Ahmar
# EMAIL: kdmarrett@gmail.com,juleahmar@g.ucla.edu
# ID: 705225374,205301445

default:
	echo 'python3 lab3b.py $$1' > lab3b
	chmod +x lab3b

clean:
	rm -rf *.tar.gz lab3b

dist: clean default
	tar -czvf lab3b-705225374.tar.gz lab3b.py README Makefile 

test: dist
	./sanitycheck.sh 705225374
