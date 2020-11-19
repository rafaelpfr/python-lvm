import os
import subprocess
import sys


def show_volume_groups():
  "Display information about volume groups"

  try:
    print("[!] Available Volume Groups")
    subprocess.run(['vgs', '-o', 'vg_name,pv_count,lv_count,vg_size,vg_free'], check = True)     
  except subprocess.CalledProcessError:
    print ("ERROR! Make sure you have LVM installed and configured correctly")


def show_logical_volumes():
  "Display information about logical volumes"

  try:
    print("\n[!] Available Logical Volumes")
    subprocess.run(['lvs', '-o', 'lv_name,vg_name,lv_size'], check = True)      
  except subprocess.CalledProcessError:
    print ("ERROR! Make sure you have LVM installed and configured correctly")


def select_disks():
  """Returns disks inserted by users"""

  disk_collection = []
  print ("\n[!] Available Disks:")
  subprocess.run(['lsblk', '-lnpo', 'NAME,SIZE'])    # listing all available block devices

  print ("\n[*] Type the disks (absolute path) that will be used as physical volumes. Type f to finish the insertions.")
  disk = input("[+] ")

  while (disk != "f"):
    disk_collection.append(disk)
    disk = input("[+] ")

  return disk_collection


def create_volume_group(shell_script):
  """The user inserts the group name and by the selected disks a new volume group is created"""

  group_name = input("[*] Type the name of the new volume group: ") 

  command = "vgcreate " + group_name + " " + " ".join(select_disks())
  print("\nExecuting the generated command:\n>>> " + command)

  try:
    subprocess.run(command.split(), check = True)    
    shell_script.write(command + "\n")
  except subprocess.CalledProcessError:
    print ("\nERROR! Check your generated command")


def create_logical_volume(shell_script):
  """Creates a new logical volume by asking the user for its size, name and volume group"""

  show_volume_groups()

  name = input ("\n[+] Type the name of the new logical volume: ")
  size = input("[+] Type the size (default is MiB, type G for GiB) of the logical volume: ")
  group = input ("[+] Type the volume group name: ")

  command = "lvcreate -L " + size + " -n " + name + " " + group
  print("\nExecuting the generated command:\n>>> " + command)

  try:
    subprocess.run(command.split(), check = True)    
    shell_script.write(command + "\n")
  except subprocess.CalledProcessError:
    print ("\nERROR! Check your generated command")


def extend_volume_group(shell_script):
  """Extends a specified volume group with new disks inserted by the user"""  
  
  show_volume_groups()

  group_name = input("\n[*] Type the volume group name that will be extended: ")
  command = "vgextend " + group_name + " " + " ".join(select_disks())
  print("\nExecuting the generated command:\n>>> " + command)

  try:
    subprocess.run(command.split(), check = True)    
    shell_script.write(command + "\n")
  except subprocess.CalledProcessError:
    print ("\nERROR! Check your generated command")


def remove_volume_group(shell_script):
  """Remove a volume group specified by the user """
  
  show_volume_groups()

  group_name = input("\n[+] Type the volume group to be removed: ")
  command = "vgremove -y " + group_name

  print("\nExecuting the generated command:\n>>> " + command)

  try:
    subprocess.run(command.split(), check = True)    
    shell_script.write(command + "\n")
  except subprocess.CalledProcessError:
    print ("\nERROR! Check your generated command")


 
if __name__ == '__main__':

  if os.getuid() != 0:
    print("You need administrative privileges to perform LVM operations")
    sys.exit(1)

  with open("lvm.sh", "w") as shell_script:
    shell_script.write("#!/bin/sh\n\n") 

    while True:
      print ("-" * 80)
      choice = input("* Select an option:\n"
                     "1 - Show current LVM info \n" 
                     "2 - Create a new Volume Group \n"
                     "3 - Create a new Logical Volume \n"
                     "4 - Extend an existing Volume Group \n"
                     "5 - Remove a Volume Group \n"
                     "0 - Quit\n> ")

      print("-" * 80)
      if (choice == "1"):
        show_volume_groups()
        show_logical_volumes()

      elif (choice == "2"):  
        create_volume_group(shell_script)    

      elif (choice == "3"): 
        create_logical_volume(shell_script)

      elif (choice == "4"):
        extend_volume_group(shell_script)

      elif (choice == "5"):
        remove_volume_group(shell_script)

      elif (choice == "0"):
        print("Exiting... shell script lvm.sh generated")
        print("-" * 80)
        sys.exit(0)

      else:
          print("Invalid Option!")
