#!/usr/bin/env python3
import os
import time
import sys
import yaml


DISPLAYS_DIRECTORY = '/etc/jupyterhub-displays/'
DISPLAYS_YAML = 'users_displays.yaml'


def test_lock(filename):
    return os.path.isfile(DISPLAYS_DIRECTORY + filename + '.lock')


def create_lock(filename):
    lock_file = open(DISPLAYS_DIRECTORY + filename + '.lock', 'w')
    lock_file.write("locked")
    lock_file.close()


def delete_lock(filename):
    os.remove(DISPLAYS_DIRECTORY + filename + '.lock')


def add_user_display(username, display):
    # To avoid double write the DISPLAYS_YAML, a lock must be made for every execution of
    # this function. We first test if there are no lock, waiting for at least 5 seconds. If the lock
    # still exists after these 5 seconds, raise a timeout. If not, this process create the lock,
    # edit the DISPLAYS_YAML file, and then delete the lock
    start_time = time.time()

    while (time.time() - start_time < 5):
        if test_lock(DISPLAYS_YAML):
            time.sleep(0.1)
        else:
            break
    if test_lock(DISPLAYS_YAML):
        raise TimeoutError("Some process is locking '/etc/jupyterhub-displays/users_displays.yaml' edition. \
                            Please contact support")

    create_lock(DISPLAYS_YAML)

    with open(DISPLAYS_DIRECTORY + DISPLAYS_YAML, 'r+') as displays_yaml_file:
        displays_yaml = yaml.safe_load(displays_yaml_file)

        displays_yaml[username] = display
        yaml.dump(displays_yaml, displays_yaml_file)
    
    delete_lock(DISPLAYS_YAML)


def main():
    # Get the user who is running the script
    user = os.environ['USER']
    display = os.environ['DISPLAY']

    # # Check if a display script is already running for the user
    # if test_lock(user):
    #     raise Exception('A session for the user "' + user + '" is already opened.')

    # # Create a locker for the user
    # create_lock(user)

    # Add user display to DISPLAYS_YAML
    add_user_display(user, display)


if __name__ == '__main__':
    main()
