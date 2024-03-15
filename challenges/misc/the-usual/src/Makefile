build:
	mkdir -p out
	gcc -no-pie -Wstringop-overflow=0 -fno-stack-protector -o out/the-usual main.c

clean:
	rm -rf out

run: build
	./out/the-usual
