import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(
    gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = ""
) -> str:
    tree = b""
    for i in index:
        path = i.name.split("/")
        if len(path) > 1:
            tree += b"40000 "
            temp = hash_object(
                oct(i.mode)[2:].encode()
                + b" "
                + "/".join(path[1:]).encode()
                + b"\0"
                + i.sha1,
                "tree",
                True,
            )
            tree += path[0].encode() + b"\0" + bytes.fromhex(temp)
        else:
            tree += oct(i.mode)[2:].encode() + b" " + path[0].encode() + b"\0" + i.sha1
    return hash_object(tree, "tree", True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if "GIT_DIR" not in os.environ:
        os.environ["GIT_DIR"] = ".git"
    if author == None:
        author = f"{os.environ['GIT_AUTHOR_NAME']} <{os.environ['GIT_AUTHOR_EMAIL']}>"
    flag = int(time.mktime(time.localtime()))
    if time.timezone < 0:
        start = "+"
    else:
        start = "-"
    hours = abs(time.timezone // 3600)
    if hours < 10:
        hs = "0" + str(hours)
    else:
        hs = str(hours)
    secs = abs((time.timezone // 60) % 60)
    if secs < 10:
        ss = "0" + str(secs)
    else:
        ss = str(secs)
    autime = f"{flag} {start}{hs}{ss}"
    content = f"tree {tree}\n"
    if parent:
        content += f"parent {parent}\n"
    content += f"author {author} {autime}\ncommitter {author} {autime}\n\n{message}\n"
    hash = hash_object(content.encode("ascii"), "commit", True)
    return hash
