# PD Control instructions

As a command line tool of PD, PD Control is used for obtaining the cluster state information and tuning the cluster.

## Source code compiling

1. [*Go*](https://golang.org/) Version 1.7 or later
2. In the PD root directory, use `make` command to compile and generate bin/pd-ctl

## Usage

single-command mode:

    ./pd-ctl store -d -u 127.0.0.1:2379

interactive mode:

    ./pd-ctl -u 127.0.0.1:2379

use environment variables:

```bash
export PD_ADDR=http://127.0.0.1:2379
./pd-ctl
```

## command line flags

### \-\-pd,-u

+ PD address
+ Default address: http://127.0.0.1:2379
+ Enviroment variable: PD_ADDR

### \-\-detach,-d

+ Use single command line mode (not entering readline)
+ Default value: false

## command (command)

### store [delete] \<store_id\>

This is used for displaying the store information or deleting the specified store.

Sample:

```bash
>> store            // Display the information of all stores
{
  "count": 3,
  "stores": [...]
}
>> store 1          // Get the store with a store id 1
  ......
>> store delete 1   // Make the store with a store id 1 offline
  ......
```

### region \<region_id\>

This is used for displaying the region information.

Sample:

```bash
>> region                               //　Display the information of all regions
{
  "count": 1,
  "regions": [......]
}

>> region 2                             // Display the information of region id 2
{
  "region": {
      "id": 2,
      ......
  }
  "leader": {
      ......
  }
}
```

### region key [--format=raw|pb|proto|protobuf] \<key\>

This is used for querying the region that a specific key resides. It supports raw and protobuf format.

A sample of Raw format (default):

```bash
>> region key abc
{
  "region": {
    "id": 2,
    ......
  }
}
```

A sampel of Protobuf format:

```bash
>> region key --format=pb t\200\000\000\000\000\000\000\377\035_r\200\000\000\000\000\377\017U\320\000\000\000\000\000\372
{
  "region": {
    "id": 2,
    ......
  }
}
```

### member [leader | delete]

This is used for displaying PD member informaiton or deleting specified members.

Sample:

```bash
>> member                               // Display the information of all members
{
  "members": [......]
}
>> member leader                        // Display the information of leader
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
>> member delete pd2                    // Make "pd2" offline
Success!
```

### config [show | set \<option\> \<value\>]

This is used for displaying or modifying the configuration information.

Sample:

```bash
>> config show                             //　Dispaly the information of config
{
  "max-snapshot-count": 3,
  "max-store-down-time": "1h",
  "leader-schedule-limit": 8,
  "region-schedule-limit": 4,
  "replica-schedule-limit": 8,
}
```

By modifying `leader-schedule-limit`, you can control the number of simultaneously implementing leader schedule.
This value mainly impacts the speed of *leader balance*: the bigger the value is, the faster the schedule goes. If the value is set to 0, the schedule will be closed.
The overhead of the Leader schedule is smaller and it can set to be bigger when necessary.

```bash
>> config set leader-schedule-limit 4       // Up to 4 leader schedules can be implemented simutaneously
```

By modifying `region-



-limit`, you can control the number of simultaneously implementing region schedule.
This value mainly impacts the speed of *region balance*: the bigger the value is, the faster the schedule goes. If the value is set to 0, the schedule will be closed.
The overhead of the Region schedule is relatively big and it should not set to be too big.

```bash
>> config set region-schedule-limit 2       // Up to 2 region schedules can be implemented simutaneously
```

By modifying `replica-schedule-limit`, you can control the number of simultaneously implementing replica schedule.
This value mainly impacts the schedule speed when a node breaks down or becomes offline: the bigger the value is, the faster the schedule goes. If the value is set to 0, the schedule will be closed.
The overhead of the Replica schedule is relatively big and it should not set to be too big.

```bash
>> config set replica-schedule-limit 4      // Up to 4 replica schedules can be implemented simutaneously
```

### operator [show | add | remove]

This is used for displaying and controlling schedule operations.

Sample:

```bash
>> operator show                            // Display all operators
>> operator show admin                      // Display all admin operators
>> operator show leader                     // Display all leader operators
>> operator show region                     // Display all region operators
>> operator add transfer-leader 1 2         // Schedule the leader of region 1 to store 2
>> operator add transfer-region 1 2 3 4     // Schedule region 1 to store 2,3,4
>> operator add transfer-peer 1 2 3         // Schedule the replica of region 1 on store 2 to store 3
>> operator remove 1                        // Delete the schedule operation of region 1
```

### scheduler [show | add | remove]

This is used for displaying and controlling schedule strategies.

Sample:

```bash
>> scheduler show                             // Display all schedulers
>> scheduler add grant-leader-scheduler 1     // Schedule the leader of all regions on store 1 to store 1
>> scheduler add evict-leader-scheduler 1     // Schedule the leader of all regions on store 1 out of store 1
>> scheduler add shuffle-leader-scheduler     // Randomly exchange leaders on store
>> scheduler add shuffle-region-scheduler     // Randomly schedule regions on different stores
>> scheduler remove grant-leader-scheduler-1  // Delete the corresponding scheduler
```

