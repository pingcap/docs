#!/bin/sh
#
# Copyright (c) 2016, Simon J Mudd
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# This is a 9-container setup which should work from scratch
# if you have previously pulled the following images.
#
#	docker pull pingcap/tidb:latest
#	docker pull pingcap/tikv:latest
#	docker pull pingcap/pd:latest
#
# run by calling the script with start to start all containers
# or stop to stop and remove them.
#
# Based heavily on the
# https://github.com/pingcap/docs/blob/master/op-guide/docker-deployment.md
# document which didn't work as shown (on 30/11/2016) as ip addresses
# and the attempt to export ports was not done properly.
#
# This script attempts to address that and start or stop the container
# group in a single script. Only tested on docker 1.12.3 on OSX.
#
# Note: some timing issues may make tidb not start properly. It
# would be good to have a better way to wait, or not add hard-coded
# timing values, or perhaps the different binaries should have a
# configurable (longer?) wait time to wait for things to be up and
# running.
#
# Note2: The network and ip addresses are using docker DHCP so work
# as shown but are not very flexible. Probably improving the network
# configuration and/or container startup (static DHCP addresses ?)
# would make it easier to add or remove pd / tikv or tidb containers.

set -e

network_name=tidb_cluster
network_prefix=192.168.2
network_definition="--network=${network_name}"

tistorehost=${network_prefix}.2

pdhost1=${network_prefix}.3
pdhost2=${network_prefix}.4
pdhost3=${network_prefix}.5

kvhost1=${network_prefix}.6
kvhost2=${network_prefix}.7
kvhost3=${network_prefix}.8

tidbhost=${network_prefix}.9

kvhost4=${network_prefix}.10

pd_port=2379
pd_peer_port=2380
kv_port=20160
tidb_port=4000
export_kv_ports="-p ${kv_port}:${kv_port}"

startpd () {
	local name=$1
	local pdhost=$2
	local expose_ports=$3
	local expose_pd_ports

	if [ "$expose_ports" = 1 ]; then
		expose_pd_ports="-p ${pd_port}:${pd_port} -p ${pd_peer_port}:${pd_peer_port}"
	else
		expose_pd_ports=
	fi

	echo "START $name"
	docker run -d --name $name \
		$network_definition \
		$expose_pd_ports \
		-v /etc/localtime:/etc/localtime:ro \
		--volumes-from tistore \
		pingcap/pd \
		--name="$name" \
		--data-dir="/tidata/$name" \
		--client-urls="http://0.0.0.0:${pd_port}" \
		--advertise-client-urls="http://${pdhost}:${pd_port}" \
		--peer-urls="http://0.0.0.0:${pd_peer_port}" \
		--advertise-peer-urls="http://${pdhost}:${pd_peer_port}" \
		--initial-cluster="pd1=http://${pdhost1}:${pd_peer_port},pd2=http://${pdhost2}:${pd_peer_port},pd3=http://${pdhost3}:${pd_peer_port}"
}

startkv () {
	local name=$1
	local kvhost=$2

	echo "Start $name"
	docker run -d --name $name \
		$network_definition \
		-v /etc/localtime:/etc/localtime:ro \
		--volumes-from tistore \
		pingcap/tikv \
		--addr="0.0.0.0:${kv_port}" \
		--advertise-addr="${kvhost}:${kv_port}" \
		--store="/tidata/$name" \
		--pd="${pdhost1}:${pd_port},${pdhost2}:${pd_port},${pdhost3}:${pd_port}" 
}

action=$1

case $action in
start)
	echo "CREATE NETWORK"
	docker network create --subnet=${network_prefix}.0/24 ${network_name}

	echo "START busybox container"
	docker run -d --name tistore \
		$network_definition \
		-v /tidata \
		busybox tail -f /dev/null

	startpd pd1 ${pdhost1} 1
	startpd pd2 ${pdhost2} 0 
	startpd pd3 ${pdhost3} 0

	startkv tikv1 ${kvhost1}
	startkv tikv2 ${kvhost2}
	startkv tikv3 ${kvhost3}

	sleep 5  # let everything start up

	echo "Start tidb"
	docker run -d --name tidb \
		$network_definition \
		-p ${tidb_port}:${tidb_port} \
		-p 10080:10080 \
		-v /etc/localtime:/etc/localtime:ro \
		pingcap/tidb \
		--store=tikv \
		--path="${pdhost1}:${pd_port},${pdhost2}:${pd_port},${pdhost3}:${pd_port}" \
		-L warn

	sleep 5 # for TIDB to initialise correctly


	echo "Adding some data"
	mysql -vvv -h 127.0.0.1 -P ${tidb_port} -u root -D test <<-EOF
	CREATE DATABASE mydb;
	USE mydb;
	CREATE TABLE mytable ( id INT, data VARCHAR(100), dt DATE, ts TIMESTAMP, PRIMARY KEY (id) );
	INSERT INTO mytable VALUES (1, 'test data', CURRENT_DATE(), NOW());
	INSERT INTO mytable SELECT 1+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	INSERT INTO mytable SELECT 2+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	INSERT INTO mytable SELECT 4+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	INSERT INTO mytable SELECT 8+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	INSERT INTO mytable SELECT 16+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	INSERT INTO mytable SELECT 32+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	INSERT INTO mytable SELECT 64+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	INSERT INTO mytable SELECT 128+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	INSERT INTO mytable SELECT 256+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	INSERT INTO mytable SELECT 512+id, 'test data', CURRENT_DATE(), NOW() FROM mytable;
	SELECT * FROM mytable ORDER BY id DESC LIMIT 5;
	EOF
	;;

startkv4)
	startkv tikv4 ${kvhost4}
	;;

stop)
	set +x
	for c in tidb tikv{3,2,1} pd{3,2,1} tistore; do
		echo "Stopping $c..."
		docker stop $c || :
		docker rm $c || :
	done
	docker network rm ${network_name}
	;;
*)
esac
