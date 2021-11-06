import os
import sys
import datetime
import argparse
from subprocess import call
from git import Repo

def main():
    parser = argparse.ArgumentParser(
        description="A Tool for managing a \"box of notes\"")
    subparsers = parser.add_subparsers(dest="action")
    
    search_parser = subparsers.add_parser("search",
            help="search through notes")
    search_parser.add_argument("pattern",
            help="pattern to search in notes for")

    edit_parser = subparsers.add_parser("edit",
            help="edit note by id")
    edit_parser.add_argument("id",
            help="note id")
    
    create_parser = subparsers.add_parser("create",
            help="create new note")
    create_parser.add_argument("-t", "--title", type=str,
            default="# ", dest="title", help="desired title")

    delete_parser = subparsers.add_parser("delete",
            help="delete note by id")
    delete_parser.add_argument("id",
            help="note id")

    args = parser.parse_args()
    
    try:
        global PATH_TO_REPO
        PATH_TO_REPO = os.environ["ZETTA_BOX"]
    except KeyError as e:
        sys.stderr.write("Error: please set ZETTA_BOX environment variable\nto path to git repo to store notes in!\n\n")
        return -1

    if not (os.path.exists(PATH_TO_REPO) and os.path.isdir(PATH_TO_REPO)):
        sys.stderr.write("Error: path to repo is invalid!\n\n")
        return -1
    
    global REPO
    REPO = Repo(PATH_TO_REPO)

    actions = {
        "search": search,
        "edit": edit,
        "create": create,
        "delete": delete
    }
    
    if args.action in actions.keys():
        action = actions[args.action]
        if callable(action):
            action(args)
    
def search(args):
    pass

def edit(args):
    pass

def create(args):
    title = str(args.title)
    editor = os.environ.get("EDITOR") if os.environ.get("EDITOR") else "vi"
    note_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    path = f'{PATH_TO_REPO}{os.path.sep}{note_name}'
    os.mkdir(path)
    path_to_note_file = f"{path}/README.md"
    with open(path_to_note_file, "w") as note_file:
        note_file.write(title)
        note_file.flush()
        call([editor, path_to_note_file])
        
        note_file = open(path_to_note_file, "r") 
        commit_message = note_name + ": " + note_file.readline()

    commit = input("commit? (y/n): ")
    while (commit != "y") and (commit != "n"):
        commit = input("enter either \"y\" or \"n\": ")\
    
    if (commit == "y"):
        git = REPO.git
        git.add(path_to_note_file)
        git.commit(m=commit_message)
    

def delete(args):
   pass 

if __name__ == "__main__":
    exit(main())