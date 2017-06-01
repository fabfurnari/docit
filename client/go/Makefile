BINARY=docit
LDFLAGS=-ldflags "-s -w"
export GOOS = linux
export GOARCH = arm
export GOARM = 5

.DEFAULT_GOAL: $(BINARY)

$(BINARY):
	go build ${LDFLAGS} -o ${BINARY}

install:
	go install ${LDFLAGS} -o ${BINARY}

clean:
	if [ -f ${BINARY} ]; then rm ${BINARY} ; fi

.phony: clean install
