# macos_installer
This role is under construction. The goal is to allow an Ansible user to automate:
* Downloading a list of .dmg files
* Installing the .dmg files
* Removing the downloaded .dmg files after installation.

### alert
This role will be refactored. The download portion will be pulled from tasks. This role is expected to be used in conjunction with pipersniper\ansible_samba; e.g., when provisioning a system, a user can pull required .dmg files from URLs, then from samba shares, and then this role will be used to install all dmgs loaded.


#### Current Limitations
* If there is a single .app bundle in an attached .dmg, it will
be installed.
* If there is more than one .app bundle in an attached .dmg:
    * The program will search for 'Install.app'; enter that bundle,
    and search for a .pkg. If there is one .pkg, it will be installed.
    * If there is no 'Install.app', the role will do nothing. I'm just
    implementing this; once I get more .dmg files with different cases
    that fit here, I will update the role.
* The role will do nothing in all other cases. 
