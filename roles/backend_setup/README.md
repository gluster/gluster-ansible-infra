gluster.infra
=========

This role helps the user to setup the backend for GlusterFS filesystem.

backend_setup:
        - Create volume groups, logical volumes (thinpool, thin lv, thick lv)
        - Create xfs filesystem
        - Mount the filesystem

Requirements
------------

Ansible version 2.5 or above


Role Variables
--------------

### backend_setup
-----------------
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_vdo || UNDEF | Mandatory argument if vdo has to be setup. Key/Value pairs have to be given. name and device are the keys, see examples for syntax. |
| gluster_infra_disktype | JBOD / RAID6 / RAID10  | UNDEF   | Backend disk type. |
| gluster_infra_diskcount || UNDEF | RAID diskcount, can be ignored if disktype is JBOD  |
| gluster_infra_vg_name  || glusterfs_vg | Optional variable, if not provided glusterfs_vg is used as vgname. |
| gluster_infra_pvs  | | UNDEF | Comma-separated list of physical devices. If vdo is used this variable can be omitted. |
| gluster_infra_stripe_unit_size || UNDEF| Stripe unit size (KiB). *DO NOT* including trailing 'k' or 'K'  |
| gluster_infra_lv_poolmetadatasize || 16G | Metadata size for LV, recommended value 16G is used by default. That value can be overridden by setting the variable. Include the unit [G\|M\|K] |
| gluster_infra_lv_thinpoolname || glusterfs_thinpool | Optional variable. If omitted glusterfs_thinpool is used for thinpoolname. |
| gluster_infra_lv_thinpoolsize || 100%FREE | Thinpool size, if not set, entire disk is used. Include the unit [G\|M\|K] |
| gluster_infra_lv_logicalvols || UNDEF | This is a list of hash/dictionary variables, with keys, lvname and lvsize. See below for example. |
| gluster_infra_thick_lvs || UNDEF | Optional. Needed only if thick volume has to be created. This is a dictionary with name and size as keys. See below for example |
| gluster_infra_mount_devices | | UNDEF | This is a dictionary with mount values. path, and lv are the keys. |
| gluster_infra_ssd_disk | | UNDEF | SSD disk for cache setup, specific to HC setups. Should be absolute path. e.g /dev/sdc |
| gluster_infra_lv_cachelvname | | glusterfs_ssd_cache | Optional variable, if omitted glusterfs_ssd_cache is used by default. |
| gluster_infra_lv_cachelvsize | | UNDEF | Size of the cache logical volume. Used only while setting up cache. |
| gluster_infra_lv_cachemetalvname | | UNDEF | Optional. Cache metadata volume name. |
| gluster_infra_lv_cachemetalvsize | | UNDEF | Optional. Cache metadata volume size. |
| gluster_infra_cachemode | | writethrough | Optional. If omitted writethrough is used. |


#### VDO Variable
------------
If the backend disk has to be configured with VDO the variable gluster_infra_vdo has to be defined.

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_vdo || UNDEF | Mandatory argument if vdo has to be setup. Key/Value pairs have to be given. name and device are the keys, see examples for syntax. |


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


#### Logical Volume variable
-----------------------
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_lv_logicalvols || UNDEF | This is a list of hash/dictionary variables, with keys, lvname and lvsize. See below for example. |

```
For Example:
gluster_infra_lv_logicalvols:
   - { lvname: 'hc_images', lvsize: '500G' }
   - { lvname: 'hc_data', lvsize: '500G' }
```

#### Thick LV variable
-----------------------
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_thick_lvs || UNDEF | This is a list of hash/dictionary variables, with keys, name and size. See below for example. |


```
For Example:
gluster_infra_thick_lvs:
   - { name: 'thick_lv_1', size: '500G' }
   - { name: 'thick_lv_2', size: '100G' }
```


#### Variables for mounting the filesystem
-----------------------------------------
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_mount_devices | | UNDEF | This is a dictionary with mount values. path, and lv are the keys. |

```
For example:
gluster_infra_mount_devices:
        - { path: '/mnt/thinv', lv: <lvname> }
        - { path: '/mnt/thicklv', lv: 'thick_lv_1' }
```


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

     # Variables for creating volume group
     gluster_infra_vg_name: glusterfs_vg
     gluster_infra_pvs: /dev/vdb,/dev/vdc

     # Create a thick volume name
     gluster_infra_thick_lvs:
       { name: 'glusterfs_thicklv', size: '50G' }


     # Create a thinpool
     gluster_infra_lv_thinpoolname: glusterfs_thinpool
     gluster_infra_lv_thinpoolsize: 100G # If not provided entire disk is used

     # Create a thin volume
     gluster_infra_lv_logicalvols:
        - { lvname: 'hc_images', lvsize: '500G' }
        - { lvname: 'hc_data', lvsize: '500G' }


     # Mount the devices
     gluster_infra_mount_devices:
        - { path: '/mnt/thinv', lv: 'glusterfs_thinlv' }
        - { path: '/mnt/thicklv', lv: 'glusterfs_thicklv' }

  roles:
     - gluster.infra

```

Tests
-----
This role can now be tested with molecule.

### Dependencies
This setup is currently verified with the following setup
* Centos 7
* Docker CE
* Python 2

As we verify our tests with more distributions, we will document them.

### Setup
* Start and enable the Docker service with the following:

        $ systemctl start docker
        $ systemctl enable docker

* Ensure that your user is in the docker group.

        $ sudo groupadd docker
        $ sudo usermod -aG docker $USER

* Verify everything works with the following:

        $ docker run hello-world

* If you have SELinux enabled, run the following

        $ sudo yum install libselinux-python

* Create a virtualenv

        $ virtualenv --system-site-packaes env

  The system site packages are so that you can pick up the `libselinux-python`
  package.  This package is not available via PyPI.

* Install the python dependencies with

        $ pip install ansible molecule docker-py

### Running the tests

Molecule tests can be triggered from the directory with the molecule folder.
For triggering tests for this role, cd into this directory. Then run 
`molecule test`. If any of the steps fail, the errors are usually hidden unless
you re-run with 'molecule --debug test'.

License
-------

GPLv3
