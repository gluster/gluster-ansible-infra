glusterfs.infra
=========

This role helps the user to get started in deploying GlusterFS filesystem. The
glusterfs.infra role has multiple sub-roles which are invoked depending on the
variables that are set. The sub-roles are

1. firewall_config - Set up firewall rules (open ports, add services to zone)
2. backend_setup:
        - Create volume groups, logical volumes (thinpool, thin lv, thick lv)
        - Create xfs filesystem
        - Mount the filesystem

Requirements
------------

Ansible version 2.5 or above
GlusterFS version 3.2 or above

Role Variables
--------------

These are the superset of role variables. They are explained again in the
respective sub-roles directory.

### firewall_config
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| glusterfs_infra_fw_state | enabled / disabled / present / absent    | UNDEF   | Enable or disable a setting. For ports: Should this port accept(enabled) or reject(disabled) connections. The states "present" and "absent" can only be used in zone level operations (i.e. when no other parameters but zone and state are set). |
| glusterfs_infra_fw_ports |    | UNDEF    | A list of ports in the format PORT/PROTO. For example 111/tcp. This is a list value.  |
| glusterfs_infra_fw_permanent  | true/false  | true | Whether to make the rule permanenet. |
| glusterfs_infra_fw_zone    | work / drop / internal / external / trusted / home / dmz / public / block | public   | The firewalld zone to add/remove to/from |
| glusterfs_infra_fw_services |    | UNDEF | Name of a service to add/remove to/from firewalld - service must be listed in output of firewall-cmd --get-services. This is a list variable

### backend_setup
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| glusterfs_infra_disktype | JBOD / RAID6 / RAID10  | UNDEF   | Backend disk type. |
| glusterfs_infra_diskcount || UNDEF | RAID diskcount, can be ignored if disktype is JBOD  |
| glusterfs_infra_vg_name  || UNDEF | Volume group name |
| glusterfs_infra_pvs  | | UNDEF | Comma-separated list of physical devices / VDO devices |
| glusterfs_infra_lv_thinpoolname || UNDEF| LV Thin pool name |
| glusterfs_infra_stripe_unit_size || UNDEF| Stripe unit size (KiB). *DO NOT* including trailing 'k' or 'K'  |
| glusterfs_infra_lv_poolmetadatasize || UNDEF| Metadata size for LV, recommended 16G. Include the unit [G\|M\|K] |
| glusterfs_infra_lv_thinpoolsize || UNDEF| Thinpool size, if not set, entire disk is used. Include the unit [G\|M\|K] |
| glusterfs_infra_lv_thinlvname || UNDEF | LV thin volume name |
| glusterfs_infra_lv_logicalvol_size || UNDEF | Size of the LV thin volume. Include the unit [G\|M\|K]|
| glusterfs_infra_lv_thicklvname || UNDEF | Optional. Needed only if thick volume has to be created. |
| glusterfs_infra_lv_thicklvsize || UNDEF | Optional. Needed only if thick volume has to be created. Include the unit [G\|M\|K]|

### Variables for filesystem creation
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| glusterfs_infra_fs_force | yes/no  | no | Use force while filesystem creation |
| glusterfs_infra_lvs || UNDEF | This is dictionary with vg and lv as keys. |

```
For example:
glusterfs_infra_lvs:
        - {
            vg: "{{ glusterfs_infra_vg_name }}",
            lv: "{{ glusterfs_infra_lv_thinlvname }}"
          }
```

### Variables for mounting the filesystem
| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| glusterfs_infra_mount_devices | | UNDEF | This is a dictionary with mount values. path, vg, and lv are the keys. |

```
For example:
glusterfs_infra_mount_devices:
        - {
            path: '/mnt/thinv',
            vg: "{{ glusterfs_infra_vg_name }}",
            lv: "{{ glusterfs_infra_lv_thinlvname }}"
          }
        - {
            path: '/mnt/thicklv',
            vg: "{{ glusterfs_infra_vg_name }}",
            lv: "{{ glusterfs_infra_lv_thicklvname }}"
          }
```

Example Playbook
----------------

Configure the ports and services related to GlusterFS, create logical volumes and mount them.


```yaml
---
- name: Setting up backend
  remote_user: root
  hosts: servers
  gather_facts: false

  vars:
     # Firewall setup
     glusterfs_infra_fw_ports:
        - 2049/tcp
        - 54321/tcp
        - 5900/tcp
        - 5900-6923/tcp
        - 5666/tcp
        - 16514/tcp
     glusterfs_infra_fw_permanent: true
     glusterfs_infra_fw_state: enabled
     glusterfs_infra_fw_zone: public
     glusterfs_infra_fw_services:
        - glusterfs

     # Set a disk type
     # Options: JBOD, RAID6, RAID10
     #
     glusterfs_infra_disktype: RAID6

     # RAID6 and RAID10 diskcount (Needed only when disktype is raid)
     glusterfs_infra_diskcount: 10
     # Stripe unit size always in KiB
     glusterfs_infra_stripe_unit_size: 128

     # Variables for creating volume group
     #
     glusterfs_infra_vg_name: role_test_vg
     glusterfs_infra_pvs: /dev/vdb,/dev/vdc

     # Create a thinpool
     glusterfs_infra_lv_thinpoolname: role_test_thinpool
     glusterfs_infra_lv_poolmetadatasize: 1G
     glusterfs_infra_lv_thinpoolsize: 50G # If not provided entire disk is used

     # Create a thin volume
     glusterfs_infra_lv_thinlvname: role_test_lv
     # The vitualsize option while creating thinpool
     glusterfs_infra_lv_logicalvol_size: 500G

     # Create a thick volume name
     glusterfs_infra_lv_thicklvname: one_thick_lv
     glusterfs_infra_lv_thicklvsize: 20G

     # Create filesystem
     glusterfs_infra_fs_force: yes
     glusterfs_infra_lvs:
        - {
            vg: "{{ glusterfs_infra_vg_name }}",
            lv: "{{ glusterfs_infra_lv_thinlvname }}"
          }

     # Mount the devices
     glusterfs_infra_mount_devices:
        - {
            path: '/mnt/thinv',
            vg: "{{ glusterfs_infra_vg_name }}",
            lv: "{{ glusterfs_infra_lv_thinlvname }}"
          }
        - {
            path: '/mnt/thicklv',
            vg: "{{ glusterfs_infra_vg_name }}",
            lv: "{{ glusterfs_infra_lv_thicklvname }}"
          }


  roles:
     - glusterfs.infra

```

License
-------

GPLv3

