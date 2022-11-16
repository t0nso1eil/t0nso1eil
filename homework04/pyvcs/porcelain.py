import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    clean = f"{fmt} {len(data)}\0".encode() + data
    hash = hashlib.sha1(clean).hexdigest()
    if write:
        gitdir = repo_find()
        hash_path = gitdir / "objects" / hash[:2]
        hash_path.mkdir(exist_ok=True)
        with open(hash_path / hash[2:], "wb") as f:
            f.write(zlib.compress(clean))
    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if (4 <= len(obj_name) <= 40) == False:
        raise Exception(f"Not a valid object name {obj_name}")
    objects = []
    gitdir = repo_find()
    objpath = gitdir / "objects" / obj_name[:2]
    for i in objpath.iterdir():
        if i.name.find(obj_name[2:]) == 0:
            objects.append(obj_name[:2] + i.name)
    if len(objects) > 0:
        return objects
    else:
        raise Exception(f"Not a valid object name {obj_name}")


def find_object(obj_name: str, gitdir: pathlib.Path) -> tp.Optional[str]:
    if obj_name[2:] in str(gitdir.parts[-1]):
        return f"{gitdir.parts[-2]}{gitdir.parts[-1]}"
    else:
        return None


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with open(path, "rb") as f:
        content = zlib.decompress(f.read())
    part = content.find(b"\x00")
    head = content[:part]
    form = head[: head.find(b" ")]
    data = content[(part + 1) :]
    return form.decode(), data


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    res = []
    while len(data) > 0:
        mode = int(data[: data.find(b" ")].decode())
        data = data[data.find(b" ") + 1 :]
        name = data[: data.find(b"\x00")].decode()
        data = data[data.find(b"\x00") + 1 :]
        sha = bytes.hex(data[:20])
        data = data[20:]
        res.append((mode, name, sha))
    return res


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find()
    for obj in resolve_object(obj_name, gitdir):
        temp = read_object(obj, gitdir)
        header = temp[0]
        ins = temp[1]
        if header == "tree":
            res = ""
            trfiles = read_tree(ins)
            for f in trfiles:
                res += str(f[0]).zfill(6) + " "
                res += read_object(f[2], repo_find())[0] + " "
                res += f[2] + "\t"
                res += f[1] + "\n"
            print(res)
        else:
            print(ins.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    res = []
    data = read_object(tree_sha, gitdir)[1]
    for f in read_tree(data):
        if read_object(f[2], gitdir)[0] == "tree":
            tree = find_tree_files(f[2], gitdir)
            for i in tree:
                name = f[1] + "/" + i[0]
                res.append((name, i[1]))
        else:
            res.append((f[1], f[2]))
    return res


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    return data[data.find(b"tree") + 5 : data.find(b"tree") + 45]
