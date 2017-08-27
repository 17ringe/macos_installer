#!/usr/bin/env python

"""
This assumes a user has already downloaded a .dmg and is trying
to install it to a mac os system.

@author: pipersniper
"""

from ansible.module_utils.basic import *
import subprocess
import shutil
import os


def install_app(appfile, mount_path, new_path, force):

    wd = os.getcwd()
    changed = True
    os.chdir(mount_path)
    copy_dir = '/Applications/{}'.format(appfile)
    already_installed = os.path.exists(copy_dir)

    if already_installed and force:
        shutil.rmtree(copy_dir)
        shutil.copytree(appfile, copy_dir)
        meta = dict(
            reinstalled=True,
            state='present'
        )
    elif already_installed and not force:
        changed = False
        meta = dict(
            reinstalled=False,
            state='present'
        )
    else:
        shutil.copytree(appfile, copy_dir)
        meta = dict(
            state='present'
        )

    os.chdir(wd)
    subprocess.call(['hdiutil', 'detach', mount_path])
    subprocess.call(['rm', new_path])

    return changed, meta


def install(data):

    path_to_dmg = data['dmg_path']
    name = data['app_name']
    new_path = '{}.cdr'.format(name)
    force = data['force']

    # Convert dmg to avoid potential EULA splash before mounting

    subprocess.call(['hdiutil', 'convert', path_to_dmg, '-format',
                     'UDTO', '-o', name])

    # Mount dmg

    subprocess.call(['hdiutil', 'attach', new_path])
    mount_path = '/Volumes/{}'.format(name)

    # Inspect mounted image.

    files = [f for f in os.listdir(mount_path)]

    # This version only handles copying one app to the /Applications folder
    # Need to handle pkg and zip installs
    # Need to handle cases where more than one .app is in the image

    matching = [s for s in files if ".app" in s]
    if len(matching) == 1:
        changed, meta = install_app(matching[0], mount_path, new_path, force)
    else:
        changed = False
        meta = dict(
            state='absent',
            msg='More than one .app or no .app files are found in the image!'
        )
    return changed, meta


def uninstall(data=None):
    pass


def main():

    amodule = AnsibleModule(
        argument_spec=dict(
            app_name=dict(required=True, type='str'),
            dmg_path=dict(required=True, type='str'),
            force=dict(default=False, type='bool'),
            state=dict(choices=['present', 'absent'],
                       type='str')
        )
    )
    choice_map = dict(
        present=install,
        absent=uninstall
    )
    has_changed, result = choice_map.get(amodule.params['state'])(amodule.params)
    amodule.exit_json(changed=has_changed, meta=result)

if __name__ == '__main__':
    main()