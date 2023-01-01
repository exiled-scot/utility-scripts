#!/usr/bin/env python3
"""
Inspired from here:
https://luator.de/linux/2022/03/05/xinput-rotate-mouse-axes.html

The “Coordinate Transformation Matrix” is a affine transformation matrix. To rotate by an angle α, you need the matrix
⎡cos(α)  -sin(α)  0⎤
⎢sin(α)   cos(α)  0⎥
⎣  0        0     1⎦
"""
import re
from argparse import ArgumentParser, Namespace
from math import acos, cos, degrees, radians, sin
from subprocess import run

LIST_REG = re.compile(
    r"(?P<name>\w[_\w\s-]+?)\s+id=(?P<id>\d+)\s+\[(master|slave)\s+pointer"
)


def rotate(degrees) -> list[float]:
    a = radians(degrees)
    return [
        cos(a),
        -sin(a),
        0.0,
        sin(a),
        cos(a),
        0.0,
        0.0,
        0.0,
        1.0,
    ]


def get_rotation(name):
    proc = run(["xinput", "list-props", name], capture_output=True, encoding="utf8")
    for line in proc.stdout.splitlines():
        if "Coordinate Transformation Matrix" in line:
            matrix = tuple(map(float, line.partition(":")[2].split(",")))
            deg = degrees(acos(matrix[0]))
            return deg


def get_args() -> Namespace:
    parser = ArgumentParser()
    sub = parser.add_subparsers(title="Commands", dest="command")
    ag_list = sub.add_parser("list", help="Command")
    ag_get = sub.add_parser("get")
    ag_get.add_argument("name", help="Name of the mouse pointer")
    ag_set = sub.add_parser("set")
    ag_reset = sub.add_parser("reset")
    ag_set.add_argument("name", help="Name of the mouse")
    ag_set.add_argument("angle", help="Angle in degrees", type=float)
    return parser.parse_args()


def list_dev(show=True):
    proc = run(["xinput", "list"], capture_output=True, encoding="utf8")
    devices = {}

    for line in proc.stdout.splitlines():
        if match := LIST_REG.search(line):
            name = match["name"]
            dev_id = int(match["id"])
            devices[dev_id] = name

    if not show:
        return devices

    for dev_id, name in sorted(devices.items()):
        rot = get_rotation(str(dev_id)) or 0.0
        print(f"[ {dev_id:3d} ] {name:<30} {rot:0.2f} °")


def set_prop(name: str | int, angle: float):
    name = str(name)
    transf_matrix = [str(v) for v in rotate(angle)]
    command = [
        "xinput",
        "set-prop",
        name,
        "Coordinate Transformation Matrix",
        *transf_matrix,
    ]
    run(command)


def main():
    args = get_args()

    match args.command:
        case "list":
            list_dev()

        case "get":
            deg = get_rotation(args.name)
            print(f"{deg:.2f} °")

        case "reset":
            for dev_id in list_dev(show=False):
                set_prop(dev_id, 0.0)

            list_dev()

        case "set":
            set_prop(args.name, args.angle)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
