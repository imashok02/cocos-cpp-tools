import json
import subprocess
import fileinput
import sys

config = None
config_keys = None
dir_path = None
grep_cmd = None
files = set()
accepted_files = [".java", ".cpp", ".plist", ".gradle", ".xml", ".txt", "json"]
pc2 = []
copy_path_src = '/build_bck' # create folder if backup needed
copy_path_des = '/'

def copy_res_files():
    global copy_path_src, copy_path_des, dir_path

    copy_path_src = dir_path + copy_path_src
    copy_path_des = dir_path + copy_path_des

    print "rsync -a " + copy_path_src + " " + copy_path_des
    subprocess.Popen("rsync -a " + copy_path_src + " " + copy_path_des,
        shell=True, stdout=subprocess.PIPE).stdout.read()

# Check whether the file extension is accepted or not
def isValidExtension(path_str):
    global accepted_files
    for ext in accepted_files:
        if path_str.find(ext) != -1:
            return True
    return False

def replaceAll(file):
    global config_keys, config

    for line in fileinput.input(file, inplace=1):
        for key in config_keys:
            if line.find(str(key)) != -1:
                line = line.replace(str(key), str(config['values'][key]))
                break
        sys.stdout.write(line)

def pre_build(tp, args):
    print " ******************* PRE-BUILD SCRIPT EXECUTION STARTED *******************1\n"
    global grep_cmd, dir_path, config_keys, config, files

    # Reading manifest
    with open(dir_path + "/manifest.json") as manifest:
        config = json.load(manifest)

    files = config['files']

    # Extracting search keys from manifest
    config_keys = config['values'].keys()

    # File modification starts here
    for file_list in files:
        file_list = dir_path + '/' + file_list
        if file_list != '' and file_list != None and isValidExtension(file_list):
            replaceAll(file_list)

    # call this if backup needed
    # copy_res_files()
    print " ******************* PRE-BUILD SCRIPT EXECUTION COMPLETED *******************\n"


def handle_event(event, tp, args):
    global dir_path

    dir_path = args["project-path"]
    event = event.replace('-', '_')
    if event in globals():
        eval(event + '(tp, args)')

