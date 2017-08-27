# macos_installer
This role is under construction. The goal is to allow an Ansible user to automate:
* Downloading a list of .dmg files
* Installing the .dmg files
* Removing the downloaded .dmg files after installation.

#### Current Limitations
* Will only handle .app bundles in a .dmg
* Will not install anything if there is more than one .app bundle in a .dmg
