import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    return commit_tree(
        gitdir=gitdir, tree=write_tree(gitdir, read_index(gitdir)), message=message, author=author
    )


def checkout(gitdir: pathlib.Path, obname: str) -> None:
    head = gitdir / "refs" / "heads" / obname
    if head.exists():
        with head.open("r") as f:
            obname = f.read()
    index = read_index(gitdir)
    for i in index:
        if pathlib.Path(i.name).is_file():
            name = i.name.split("/")
            if len(name) > 1:
                shutil.rmtree(name[0])
            else:
                os.chmod(i.name, 0o777)
                os.remove(i.name)
    objfile = gitdir / "objects" / obname[:2] / obname[2:]
    with objfile.open("rb") as f:
        com = f.read()
    for i in find_tree_files(commit_parse(com).decode(), gitdir):
        name = i[0].split("/")
        if len(name) > 1:
            pathlib.Path(name[0]).absolute().mkdir()
        with open(i[0], "w") as tree_path:
            content = read_object(i[1], gitdir)[1]
            tree_path.write(content.decode())
