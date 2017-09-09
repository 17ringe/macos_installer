# macos_installer
This role is under construction. The goal is to allow an Ansible user to automate:
* Installing .dmg files
* Removing the downloaded .dmg files after installation.

#### Notes
* Assumes your dmgs are downloaded to `{{ dmg_path }}` and the following attributes are set:
    * app_name (required) - used internally (string).
    * dmg_path (required) - full path to the dmg being installed (string).
    * state (required) - present to install, absent will not install (string).
        * removing an app by specifying state: absent is still in testing.
        * This would require the installed_name attribute to be set (string).
    * force (optional) will attempt to reinstall even if app is already present (boolean, True/False).
    
#### Example Usage
config.yml
```
dmg_path: "/path/to/download/dmgs"

dmgs:
  - {
      name: "Test",
      url: "https://example.com/path/to/app",
      force: False,
      installed_name: "no_path",
      state: "present"
    }
  - {
      name: "Test2"
      url: "https://example2.com/path/to/app",
      force: False,
      installed_name: "no_path",
      state: "present"
    }
```
playbook.yml
```
- hosts: all
  
  vars_files:
    - config.yml
  
  pre_tasks:
  
    - name: Download .dmgs
      get_url:
        url: "{{ item.url }}"
        dest: "{{ dmg_path }}/{{ item.name }}.dmg"
      with_items: "{{ dmgs }}"
      
  roles:
    - role: pipersniper.macos_installer
```

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
