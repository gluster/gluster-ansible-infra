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
| gluster_infra_vdo_state | present / absent  | present   | Optional variable, default is taken as present. |
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
| gluster_infra_lv_thicklvname || gluster_infra_lv_thicklvname | Optional. Needed only if thick volume has to be created. The variable will have default name gluster_infra_lv_thicklvname if thicklvsize is defined. |
| gluster_infra_lv_thicklvsize || UNDEF | Optional. Needed only if thick volume has to be created. Include the unit [G\|M\|K]|
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

#### Variables for mounting the filesystem
-----------------------------------------
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| gluster_infra_mount_devices | | UNDEF | This is a dictionary with mount values. path, and lv are the keys. |

```
For example:
gluster_infra_mount_devices:
        - { path: '/mnt/thinv', lv: <lvname> }
        - { path: '/mnt/thicklv', lv: "{{ gluster_infra_lv_thicklvname }}" }
```


Example Playbook
----------------

Configure the ports and services related to GlusterFS, create logical volumes and mount them.


```
---
- name: Setting up backend
  remote_user: root
  hosts: servers
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
     gluster_infra_lv_thicklvname: glusterfs_thicklv
     gluster_infra_lv_thicklvsize: 20G

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
        - { path: '/mnt/thicklv', lv: "{{ gluster_infra_lv_thicklvname }}" }

  roles:
     - gluster.infra

```

License
-------

GPLv3
