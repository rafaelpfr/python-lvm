A python script just to practice some Python and some Linux concepts.

LVM is an acronym for Logical Volume Manager. LVM is a device mapper that provides logical volume management for the Linux kernel. 
Introduces an extra layer between the physical disks and the file system allowing file systems to be:
- resized and moved easily and online without requiring a system-wide outage.
- Using discontinuous space on disk
- meaningful names to volumes, rather than the usual cryptic device names.
- span multiple physical disks

The script in this project acts as an interface for performing some basic LVM operations, such as:
- Show current LVM info
- Create a new Volume Group
- Create a new Logical Volume
- Extend an existing Volume Group
- Remove the Volume Group

At the end, a shell script will be generated with the commands that were executed in the background.
