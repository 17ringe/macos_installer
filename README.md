# macos_installer
This role is under construction. The goal is to allow an Ansible user to install a program that is bundled in a .dmg file. It will eventually be packaged as a proper ansible-galaxy role.

#### Current Limitations
* Will only handle .app bundles in a .dmg
* May yield unpredictable results if more than one .app bundle is in a given .dmg
