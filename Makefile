# Codegen from the language-neutral proto: one source -> native per layer.
# The contract is `proto/agentweb.proto`; generated code lives in gen/ (git-ignored).

PROTO     := proto/agentweb.proto
PROTO_DIR := proto

.PHONY: gen gen-python gen-go gen-rust gen-ts clean

gen: gen-python gen-go        ## generate the targets whose toolchains are present

gen-python:
	mkdir -p gen/python
	protoc -I $(PROTO_DIR) --python_out=gen/python $(PROTO)

gen-go:
	mkdir -p gen/go
	protoc -I $(PROTO_DIR) --go_out=gen/go --go_opt=paths=source_relative $(PROTO)

gen-rust:                     ## needs: cargo install protoc-gen-prost
	mkdir -p gen/rust
	protoc -I $(PROTO_DIR) --prost_out=gen/rust $(PROTO)

gen-ts:                       ## needs: npm i -g ts-proto
	mkdir -p gen/ts
	protoc -I $(PROTO_DIR) --ts_proto_out=gen/ts $(PROTO)

clean:
	rm -rf gen
