module github.com/morgo/docs/scripts

go 1.16

require (
	github.com/BurntSushi/toml v0.4.1 // indirect
	github.com/StackExchange/wmi v1.2.1 // indirect
	github.com/cespare/xxhash/v2 v2.1.2 // indirect
	github.com/coocood/freecache v1.2.0 // indirect
	github.com/coreos/go-systemd v0.0.0-20191104093116-d3cd4ed1dbcf // indirect
	github.com/danjacques/gofslock v0.0.0-20200623023034-5d0bd0fa6ef0 // indirect
	github.com/dgryski/go-farm v0.0.0-20200201041132-a6ae2369ad13 // indirect
	github.com/go-ole/go-ole v1.2.6 // indirect
	github.com/golang/snappy v0.0.4 // indirect
	github.com/google/btree v1.0.1 // indirect
	github.com/google/uuid v1.3.0 // indirect
	github.com/grpc-ecosystem/go-grpc-middleware v1.3.0 // indirect
	github.com/hypnoglow/gormzap v0.3.0 // indirect
	github.com/jinzhu/gorm v1.9.12 // indirect
	github.com/opentracing/basictracer-go v1.1.0 // indirect
	github.com/opentracing/opentracing-go v1.2.0 // indirect
	github.com/pingcap/failpoint v0.0.0-20210918120811-547c13e3eb00 // indirect
	github.com/pingcap/parser v0.0.0-20211004012448-687005894c4e // indirect
	github.com/pingcap/tidb v1.1.0-beta.0.20211216143636-a6fc5c6ed4c4 // indirect
	github.com/pingcap/tidb-tools v5.2.2+incompatible // indirect
	github.com/pingcap/tidb/parser v0.0.0-20211117165147-5f340b88c98f // indirect
	github.com/prometheus/common v0.32.1 // indirect
	github.com/prometheus/procfs v0.7.3 // indirect
	github.com/shirou/gopsutil v3.21.10+incompatible // indirect
	github.com/twmb/murmur3 v1.1.6 // indirect
	github.com/uber-go/atomic v1.4.0 // indirect
	github.com/uber/jaeger-client-go v2.29.1+incompatible // indirect
	go.etcd.io/etcd v3.3.27+incompatible // indirect
	go.uber.org/atomic v1.9.0 // indirect
	golang.org/x/net v0.0.0-20211116231205-47ca1ff31462 // indirect
	golang.org/x/sys v0.0.0-20211116061358-0a5406a5449c // indirect
	google.golang.org/genproto v0.0.0-20211117155847-120650a500bb // indirect
	google.golang.org/grpc v1.42.0 // indirect
)

replace (
	github.com/coreos/etcd => github.com/coreos/etcd v3.3.13+incompatible
	go.etcd.io/bbolt => go.etcd.io/bbolt v1.3.5
	go.etcd.io/etcd => go.etcd.io/etcd v0.5.0-alpha.5.0.20200910180754-dd1b699fc489 // ae9734ed278b is the SHA for git tag v3.4.13
	google.golang.org/grpc => google.golang.org/grpc v1.27.1
)
