NAME=mqtt-panel
BINDIR=build
VERSION=0.1.0
BUILDTIME=$(shell date -u)
GOBUILD=cd src/server && go build -ldflags '-X "main.version=$(VERSION)" -X "main.buildTime=$(BUILDTIME)"'
FRONTBUILD=cd src/web && pnpm i && vite build --outDir=../../$(BINDIR)/dist --emptyOutDir

all: frontend linux-amd64

release:
	tar -zcvf $(NAME)-release.tar.gz $(BINDIR)/

frontend:
	$(FRONTBUILD)

windows-amd64: 
	GOARCH=amd64 GOOS=windows $(GOBUILD) -o ../../$(BINDIR)/$(NAME)-$@.exe

linux-amd64:
	GOOS=linux GOARCH=amd64 $(GOBUILD) -o ../../$(BINDIR)/$(NAME)-$@

clean:
	rm -rf build/*

env:
	export AMPY_PORT=/dev/ttyUSB0

tty:
	screen /dev/ttyUSB0 115200
