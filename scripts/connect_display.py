#!/usr/bin/env python3
import os
import time
import sys
import yaml


DISPLAYS_DIRECTORY = '/etc/jupyterhub-displays/'
DISPLAYS_YAML = 'users_displays.yml'


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
        print(TimeoutError("Some process is locking '/etc/jupyterhub-displays/users_displays.yaml' edition. \
                            Please, try again or contact support."))

        # This exception will be caught by the main function
        raise Exception           

    # Create lock to avoid data race
    create_lock(DISPLAYS_YAML)

    # Test the existence of DISPLAYS_YAML file. If DISPLAYS_YAML is missing, user should contact support.
    if not os.path.isfile(DISPLAYS_DIRECTORY + DISPLAYS_YAML):
        print("ERROR. There is no '" + DISPLAYS_YAML + "' file. Please, contact support.")
        delete_lock(DISPLAYS_YAML)
        
        # This exception will be caught by the main function
        raise Exception

    # Open DISPLAYS_YAML in read mode and load its contents. If the file is empty, YAML will return a
    # NoneType object, in this case we should create an empty dictionary
    with open(DISPLAYS_DIRECTORY + DISPLAYS_YAML, 'r') as read_displays_yaml_file:
        displays_yaml = yaml.safe_load(read_displays_yaml_file)
        
        if displays_yaml is None:
            displays_yaml = {}

    try:
        # Open DISPLAYS_YAML in write mode, and write the updated content.
        with open(DISPLAYS_DIRECTORY + DISPLAYS_YAML, 'w') as write_displays_yaml_file:
            displays_yaml[username] = display
            yaml.dump(displays_yaml, write_displays_yaml_file)
    except PermissionError as e:
        print(e)
        print("Please, contact support.")
        delete_lock(DISPLAYS_YAML)
        
        # This exception will be caught by the main function
        raise Exception
    
    # Ends edition
    delete_lock(DISPLAYS_YAML)


def main():
    # Get the user who is running the script
    user = os.environ['USER']
    display = os.environ['DISPLAY']

    # Check if a display script is already running for the user
    if test_lock(user):
        raise Exception('A session for the user "' + user + '" is already opened.')

    # Create a locker for the user
    create_lock(user)

    # Add user display to DISPLAYS_YAML
    try:
        add_user_display(user, display)
    except Exception:
        delete_lock(user)
        exit(1)

    # Stay connected until user manually 
    print("Connected to remote display.")
    print("Type 'q' and press 'Enter' to exit connection.")
    while True:
        try:
            key = input()

            if key == 'q' or key == 'Q':
                break
            else:
                print("Invalid key '" + key + "'.")
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
        
        time.sleep(0.1)
    
    # End connection, remove locker for the user
    delete_lock(user)


if __name__ == '__main__':
    main()
