gluster.infra
=========

The  gluster.infra role allows the user to deploy a GlusterFS cluster. It has sub-roles which can be invoked by setting the variables. The sub-roles are

1. firewall_config:
   * Set up firewall rules (open ports, add services to zone)
2. backend_setup:
   * Create VDO volume (If vdo is selected)
   * Create volume groups, logical volumes (thinpool, thin lv, thick lv)
   * Create xfs filesystem
   * Mount the filesystem

Requirements
------------

* Ansible version 2.5 or above
* GlusterFS version 3.2 or above
* VDO utilities (Optional)

Role Variables
--------------

These are the superset of role variables. They are explained again in the
respective sub-roles directory.

-------------------
### firewall_config

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_fw_state | enabled / disabled / present / absent    | UNDEF   | Enable or disable a setting. For ports: Should this port accept(enabled) or reject(disabled) connections. The states "present" and "absent" can only be used in zone level operations (i.e. when no other parameters but zone and state are set). |
| gluster_infra_fw_ports |    | UNDEF    | A list of ports in the format PORT/PROTO. For example 111/tcp. This is a list value.  |
| gluster_infra_fw_permanent  | true/false  | true | Whether to make the rule permanent. |
| gluster_infra_fw_zone    | work / drop / internal / external / trusted / home / dmz / public / block | public   | The firewalld zone to add/remove to/from |
| gluster_infra_fw_services |    | UNDEF | Name of a service to add/remove to/from firewalld - service must be listed in output of firewall-cmd --get-services. This is a list variable

-----------------
### backend_setup

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_vdo || UNDEF | Mandatory argument if vdo has to be setup. Key/Value pairs have to be given. See examples for syntax. |
| gluster_infra_disktype | JBOD / RAID6 / RAID10  | UNDEF   | Backend disk type. |
| gluster_infra_diskcount || UNDEF | Ignored if disktype is JBOD.  The number of data disks in your RAID6/RAID10 array.  Set this value to 10 if you're using RAID6 with 12 total disks (10 data + 2 parity disks).  |
| gluster_infra_volume_groups  || UNDEF | Key/value pairs of vgname and pvname. pvname can be comma-separated values if more than a single pv is needed for a vg. See below for syntax. This variable is mandatory when PVs are not specified in the LVs |
| gluster_infra_stripe_unit_size || UNDEF| Stripe unit size (KiB). *DO NOT* including trailing 'k' or 'K'  |
| gluster_infra_lv_poolmetadatasize || 16G | Metadata size for LV, recommended value 16G is used by default. That value can be overridden by setting the variable. Include the unit [G\|M\|K] |
| gluster_infra_thinpools || | Thinpool data. This is a dictionary with keys vgname, thinpoolname, thinpoolsize, and poolmetadatasize. See below for syntax and example. |
| gluster_infra_lv_logicalvols || UNDEF | This is a list of hash/dictionary variables, with keys, lvname and lvsize. See below for example. |
| gluster_infra_thick_lvs || UNDEF | Optional. Needed only if thick volume has to be created. This is a dictionary with vgname, lvname, and size as keys. See below for example |
| gluster_infra_mount_devices | | UNDEF | This is a dictionary with mount values. path, vgname, and lvname are the keys. |
| gluster_infra_cache_vars | | UNDEF | This variable contains list of dictionaries for setting up LV cache. Variable has following keys: vgname, cachedisk, cachethinpoolname, cachelvname, cachelvsize, cachemetalvname, cachemetalvsize, cachemode. The keys are explained in more detail below|
|gluster_infra_lvm|  | UNDEF | This variable contains a dictionary, which defines how lvm should autoextend thinpools
|fstrim_service|| UNDEF | This variable contains a dictionary, which enables when and how often a TRIM command should be send to the mounted fs, which support this

-----------------
#### VDO Variable

If the backend disk has to be configured with VDO the variable gluster_infra_vdo has to be defined.

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_vdo || UNDEF | Mandatory argument if vdo has to be setup. Key/Value pairs have to be given. gluster_infra_vdo supports the keys explained below, see examples for syntax. |

```
For Example:
gluster_infra_vdo:
   - { name: 'hc_vdo_1', device: '/dev/vdb' }
   - { name: 'hc_vdo_2', device: '/dev/vdc' }
   - { name: 'hc_vdo_3', device: '/dev/vdd' }
```

The gluster_infra_vdo variable supports the following keys:

| VDO Key                 | Default value         | Comments                          |
|--------------------------|-----------------------|-----------------------------------|
| state | present | VDO state, if present VDO will be created, if absent VDO will be deleted. |
| activated | 'yes' | Whether VDO has to be activated upon creation. |
| running | 'yes' | Whether VDO has to be started |
| logicalsize | UNDEF | Logical size for the vdo |
| compression | 'enabled' | Whether compression has to be enabled |
| blockmapcachesize | '128M' | The amount of memory allocated for caching block map pages, in megabytes (or may be issued with an LVM-style suffix of K, M, G, or T). The default (and minimum) value is 128M. |
| readcache | 'disabled' | Enables or disables the read cache. |
| readcachesize | 0 | Specifies the extra VDO device read cache size in megabytes. |
| emulate512 | 'off' | Enables 512-byte emulation mode, allowing drivers or filesystems to access the VDO volume at 512-byte granularity, instead of the default 4096-byte granularity. |
| slabsize | '2G' | The size of the increment by which the physical size of a VDO volume is grown, in megabytes (or may be issued with an LVM-style suffix of K, M, G, or T). Must be a power of two between 128M and 32G. |
| writepolicy | 'sync' | Specifies the write policy of the VDO volume. The 'sync' mode acknowledges writes only after data is on stable storage. |
| indexmem | '0.25' | Specifies the amount of index memory in gigabytes. |
| indexmode | 'dense' | Specifies the index mode of the Albireo index. |
| ackthreads | '1' | Specifies the number of threads to use for acknowledging completion of requested VDO I/O operations. Valid values are integer values from 1 to 100 (lower numbers are preferable due to overhead). The default is 1.|
| biothreads | '4' | Specifies the number of threads to use for submitting I/O operations to the storage device. Valid values are integer values from 1 to 100 (lower numbers are preferable due to overhead). The default is 4. |
| cputhreads | '2' | Specifies the number of threads to use for CPU-intensive work such as hashing or compression. Valid values are integer values from 1 to 100 (lower numbers are preferable due to overhead). The default is 2. |
| logicalthreads | '1' | Specifies the number of threads across which to subdivide parts of the VDO processing based on logical block addresses. Valid values are integer values from 1 to 100 (lower numbers are preferable due to overhead). The default is 1.|
| physicalthreads | '1' | Specifies the number of threads across which to subdivide parts of the VDO processing based on physical block addresses. Valid values are integer values from 1 to 16 (lower numbers are preferable due to overhead). The physical space used by the VDO volume must be larger than (slabsize * physicalthreads). The default is 1. |

-----------------
#### Volume Groups variable

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_volume_groups || UNDEF | This is a list of hash/dictionary variables, with keys, vgname and pvname. See below for example. |

```
For Example:
gluster_infra_volume_groups:
   - { vgname: 'volgroup1', pvname: '/dev/sdb' }
   - { vgname: 'volgroup2', pvname: '/dev/mapper/vdo_device1' }
   - { vgname: 'volgroup3', pvname: '/dev/sdc,/dev/sdd' }
```

* vgname: Required, string defining the VG name to belong to
* pvname: Required, string defining the device paths to pass to the lvg module. Currently the behavior of passing multiple devices is undefined, but should be handled correctly in simple cases
-----------------------
#### Logical Volume variable

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_lv_logicalvols || UNDEF | This is a list of hash/dictionary variables, with keys, lvname, vgname, thinpool, and lvsize. See below for example. |

```
For Example:
gluster_infra_lv_logicalvols:
   - { vgname: 'vg_vdb', thinpool: 'foo_thinpool', lvname: 'vg_vdb_thinlv', lvsize: '500G' }
   - { vgname: 'vg_vdc', thinpool: 'bar_thinpool', lvname: 'vg_vdc_thinlv', lvsize: '500G' }
   - { vgname: 'ans_vg', thinpool: 'ans_thinpool4', lvname: 'ans_thinlv5', lvsize: '1G', pvs: '/dev/sdd1,/dev/sdg1', opts: '--type raid1', meta_opts: '--type raid1', meta_pvs: '/dev/sde1,/dev/sdf1' }
   - { vgname: 'ans_vg3', thinpool: 'ans_thinpool8', lvname: 'ans_thinlv3', lvsize: '100M', raid: {level: 5, stripe: 64, devices: 3 }}
```

* vgname: Required, string defining the VG name to belong to
* lvname: Required, string defining the name of the LV
* thinpool: Required, string defining the name the thinpool this LV belongs to
* lvsize: Optional, Default 100%, size of LV
* pvs: Optional, Default empty, the physical devices the LV should be placed on
* opts: Optional, Default empty, additional parameters being passed to the lvm module, which uses those in lvcreate
* meta_pvs: Optional, Default empty, the physical devices the metadata volume should be placed on
* meta_opts: Optional, Default empty, additional parameters to pass to lvcreate for creating the metadata volume
* skipfs: Optional Boolean, Default no. When yes no XFS filesystem will be created on the 
* shrink: Optional Boolean, Default yes. When no the lvol module will not try to shrink the LV
* raid: Optional Dict, see _raid_. This should be equal to the raid config of the thinpool! example: {level: 5, stripe: 64, devices: 3 }

-----------------------
#### Thick LV variable

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_thick_lvs || UNDEF | This is a list of hash/dictionary variables, with keys, vgname, lvname, and size. See below for example. |


```
For Example:
gluster_infra_thick_lvs:
   - { vgname: 'vg_sdb', lvname: 'thick_lv_1', size: '500G' }
   - { vgname: 'vg_sdc', lvname: 'thick_lv_2', size: '100G' }
   - { vgname: 'ans_vg', lvname: 'ans_thick2_vdo', size: '9G', atboot: yes, skipfs: yes, opts: "", pvs: '/dev/sdd1,/dev/sdg1' }
```

* vgname: Required, string defining the VG name to belong to
* lvname: Required, string defining the name of the LV
* lvsize: Optional, Default 100%, size of LV
* pvs: Optional, Default empty, the physical devices the LV should be placed on
* opts: Optional, Default empty, additional parameters being passed to the lvm module, which uses those in lvcreate
* skipfs: Optional Boolean, Default no. When yes no XFS filesystem will be created on the LV
* atboot: Optional Boolean, Default no. When yes the parameter "rd.lvm.lv=DM" will be added to the kernel parameters in grub
* shrink: Optional Boolean, Default yes. When no the lvol module will not try to shrink the LV
* raid: Optional Dict, see _raid_. example: {level: 5, stripe: 512, devices: 4 }

----------------------
#### Thinpool variable

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_thinpools || UNDEF | This is a list of hash/dictionary variables, with keys: vgname, thinpoolname, thinpoolsize, poolmetadatasize, pvs, opts, meta_pvs and meta_opts. See below for example. |


```
gluster_infra_thinpools:
  - {vgname: 'vg_vdb', thinpoolname: 'foo_thinpool', thinpoolsize: '10G', poolmetadatasize: '1G' }
  - {vgname: 'vg_vdc', thinpoolname: 'bar_thinpool', thinpoolsize: '20G', poolmetadatasize: '1G' }
  - {vgname: 'ans_vg', thinpoolname: 'ans_thinpool', thinpoolsize: '1G', poolmetadatasize: '15M', opts: "", pvs: '/dev/sdd1,/dev/sdg1', meta_opts: '--type raid1', meta_pvs: '/dev/sde1,/dev/sdf1' }
  - {vgname: 'ans_vg3', thinpoolname: 'ans_thinpool8', thinpoolsize: '1G', poolmetadatasize: '15M', opts: "--type raid5 --nosync -i 2", pvs: '/dev/sdb1,/dev/sdd1,/dev/sdg1', raid: {level: 5, stripe: 64, devices: 3 }}
```

* poolmetadatasize: Metadata size for LV, recommended value 16G is used by default. That value can be overridden by setting the variable. Include the unit [G\|M\|K]
* thinpoolname: Can be ignored, a name is formed using the given vgname followed by '_thinpool'
* vgname: Name of the volume group this thinpool should belong to.
* thinpoolsize: The size of the thinpool
* pvs: Optional, Default empty, the physical devices the LV should be placed on
* opts: Optional, Default empty, additional parameters being passed to the lvm module, which uses those in lvcreate
* meta_pvs: Optional, Default empty, the physical devices the metadata volume should be placed on
* meta_opts: Optional, Default empty, additional parameters to pass to lvcreate for creating the metadata volume
* raid: Optional Dict, see _raid_. example: {level: 5, stripe: 64, devices: 3 }


-----------------------------------------
#### Variables for setting up cache

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_cache_vars | | UNDEF | This is a dictionary with keys: vgname, cachedisk, cachetarget/cachethinpoolname, cachelvname, cachelvsize, cachemetalvname, cachemetalvsize, cachemode |

```
vgname - The vg which will be extended to setup cache.
cachedisk - Comma seperated list of asbsolute-paths of block devices (e.g. SSD, NVMe; /dev/ssd) to use as caching medium.
cachethinpoolname - (deprecated, see: cachetarget) The existing thinpool on the volume group mentioned above.
cachetarget - The target thinpool or thick LV that should be cached
cachelvname - Logical volume name for setting up cache, an lv with this name is created.
cachelvsize - Cache logical volume size
cachemetalvname - Meta LV name.
cachemetalvsize - Meta LV size
cachemode - Cachemode, default is writethrough.
meta_pvs - Optional, Default empty, the physical devices the metadata volume should be placed on
meta_opts - Optional, Default empty, additional parameters to pass to lvcreate for creating the metadata volume
```

For example:
```
   - { vgname: 'vg_vdb', cachedisk: '/dev/vdd', cachethinpoolname: 'foo_thinpool', cachelvname: 'cachelv', cachelvsize: '20G', cachemetalvname: 'cachemeta', cachemetalvsize: '100M', cachemode: 'writethrough' }
   - { vgname: 'ans_vg', cachedisk: '/dev/sde1,/dev/sdf1', cachetarget: 'ans_thick', cachelvname: 'cache-ans_thinpool', cachelvsize: '10G', cachemetalvsize: '1G', meta_opts: '--type raid1', meta_pvs: '/dev/sde1,/dev/sdh1', cachemode: 'writethrough' }
```


-----------------------------------------
#### Variables for raid configurations

this is a sub-structure for Thick/Thin, Pool LV's and XFS trying to achieve RAID alignment

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| level | 0,5,6,10 | UNDEF | The active raid level, when none defined the default or JBOD is assumed |
| stripe || UNDEF | Stripe unit size (KiB). *DO NOT* including trailing 'k' or 'K' |
| devices || UNDEF | The amount of devices the array consists of, this includes parity devices, thus for a RAID5 of 3 disks supply 3. The parity is calculated |

-----------------------------------------
#### Variables for mounting the filesystem

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_mount_devices | | UNDEF | This is a dictionary with mount values. path, vgname, and lvname are the keys. |

```
For example:
gluster_infra_mount_devices:
        - { path: '/mnt/thinv', vgname: <vgname>, lvname: <lvname> }
```

-----------------------------------------

#### Variables for configuring LVM auto extend for thin pools
-----------------------------------------
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_lvm | | UNDEF | This is a dictionary to configure the LVM auto extend. autoexpand_threshold and autoexpand_percentage are the keys. |

```
For example:
gluster_infra_lvm: {
      autoexpand_threshold: 70,
      autoexpand_percentage: 15,
   }
```

* autoexpand_threshold: Optional default empty, the threshold in percentage when LVM should try to expand the thinpool (see lvm.conf)
* autoexpand_percentage: Optional default empty, the percentage the thinpool should be expanded with (see lvm.conf)

#### Variables for configuring fstimer service and timer
-----------------------------------------
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| fstrim_service | | UNDEF | This is a dictionary to configure the fstrim service. enabled and schedule are the keys. |

```
For example:
fstrim_service: {
      enabled: yes,
      schedule: {         
         hour: "{{ range(1, 4) | random() }}"
      }
   }
```

* enabled: Boolean default no. When yes the fstrim.timer unit will be enabled
* schedule: Optional dictionary, to set the timer, by default doesn't override the schedule. can be usefull to not trigger the trim at the same time across the cluster. optionable subkeys;
   * dow: Optional String, specifying the Day of Week as required by the systemd calander. When empty a random day is chosen.
   * hour: Optional int, default a random hour, setting the hour the fstrim should run
   * minute: Optional int, default a random minute, setting the minute the fstrim should run
   * second: Optional int, default a random second, setting the second the fstrim should run

Example Playbook
----------------

Configure the ports and services related to GlusterFS, create logical volumes and mount them.


```
---
- name: Setting up backend
  remote_user: root
  hosts: gluster_servers
  gather_facts: false

  vars:
     # Firewall setup
     gluster_infra_fw_ports:
        - 2049/tcp
        - 54321/tcp
        - 5900/tcp
        - 5900-6923/tcp
        - 5666/tcp
        - 16514/tcp
     gluster_infra_fw_services:
        - glusterfs

     # Set a disk type, Options: JBOD, RAID6, RAID10
     gluster_infra_disktype: RAID6

     # RAID6 and RAID10 diskcount (Needed only when disktype is raid)
     gluster_infra_diskcount: 10
     # Stripe unit size always in KiB
     gluster_infra_stripe_unit_size: 128

     # enable lvm auto-extend feature so that when the pool is at 70% it will be extended with 15%
     gluster_infra_lvm: {
      autoexpand_threshold: 70,
      autoexpand_percentage: 15,
     }
   
     # enable fstrim service so the TRIM command is executed once in a while to clean either ssd or thin/vdo volumes
     fstrim_service: {
       enabled: yes,
       schedule: {         
         hour: "{{ range(1, 4) | random() }}"
       }
      }

     # Variables for creating volume group
     gluster_infra_volume_groups:
       - { vgname: 'vg_vdb', pvname: '/dev/vdb' }
       - { vgname: 'vg_vdc', pvname: '/dev/vdc' }

     # Create thinpools
     gluster_infra_thinpools:
       - {vgname: 'vg_vdb', thinpoolname: 'foo_thinpool', thinpoolsize: '100G', poolmetadatasize: '16G'}
       - {vgname: 'vg_vdc', thinpoolname: 'bar_thinpool', thinpoolsize: '500G', poolmetadatasize: '16G'}

     # Create a thin volume
     gluster_infra_lv_logicalvols:
       - { vgname: 'vg_vdb', thinpool: 'foo_thinpool', lvname: 'vg_vdb_thinlv', lvsize: '500G' }
       - { vgname: 'vg_vdc', thinpool: 'bar_thinpool', lvname: 'vg_vdc_thinlv', lvsize: '500G' }

     # Mount the devices
     gluster_infra_mount_devices:
       - { path: '/mnt/brick1', vgname: 'vg_vdb', lvname: 'vg_vdb_thinlv' }
       - { path: '/mnt/brick2', vgname: 'vg_vdc', lvname: 'vg_vdc_thinlv' }

  roles:
     - gluster.infra

```

See also: https://github.com/gluster/gluster-ansible-infra/tree/master/playbooks

-------
License


GPLv3
