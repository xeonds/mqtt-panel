NAME=mqtt-panel
BINDIR=bin
VERSION=0.1.0
BUILDTIME=$(shell date -u)
GOBUILD=go build -ldflags '-X "main.version=$(VERSION)" -X "main.buildTime=$(BUILDTIME)"'
FRONTBUILD=pnpm i && vite build --outDir=bin/dist

PLATFORM_LIST = \
	darwin-amd64 \
	linux-amd64 \
	linux-arm64 \
	linux-arm \
	windows-amd64\
	windows-amd64-v3

all: frontend linux-amd64

frontend:
	$(FRONTBUILD)

linux-amd64:
	GOOS=linux GOARCH=amd64 $(GOBUILD) -o $(BINDIR)/$(NAME)-$@-$(VERSION)

clean:
	rm -rf bin/*
