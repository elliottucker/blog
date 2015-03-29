Title: Adding a raw disk to a VirtualBox machine on OSX
Slug: adding-a-raw-disk-to-a-virtualbox-machine-on-osx
Date: 2015-03-07 15:53:24
Tags: osx, virtualbox, linux
x
This is useful if you need to creating partitition for Linux while using OSX. If you're trying to mount a raw disk to VirtualBox on OSX and you're getting ```VERR_ACCESS_DENIED``` and ```VBOX_E_OBJECT_NOT_FOUND``` errors (hello Google searchers), try this. 

Get the disk number
```diskutil list```

Assuming you want /dev/disk2 from here in.  Unmount the disk

```diskutil unmountDisk /dev/disk2```

We need full access to everyone to the block device.

```sudo chmod 777 /dev/disk2```

Create the a VirtualBox vmdk file linkink to the raw disk

```VBoxManage internalcommands createrawvmdk -filename sd.vmdk -rawdisk /dev/disk2```

In the VirtualBox GUI, make sure your guest machine is powered off.  Add the vmdk file from Setting->Storage...

![](https://dl-web.dropbox.com/get/Screenshots/Screenshot%202015-03-07%2016.18.55.png?_subject_uid=5763349&w=AAByhX7Jbfl7IFtEXicblEx9hA19-BZMz7RZYmrwOTPNVA)

For me this mounted the disk again, so unmount it before you start the machine again.





