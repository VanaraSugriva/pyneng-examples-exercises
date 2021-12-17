import time
import subprocess
from collections.abc import Iterable


# Setup constants
mngmnt_screen = 0
slp_time = 0.5
alld = range(1, 8)
allr = range(1, 8)
# allsw = range(11,15)


def coffee_break(devices, *, minutes, keep_alive):
    total_seconds = minutes * 60
    cycles = total_seconds / keep_alive
    for _ in range(int(cycles)):
        time.sleep(keep_alive)
        send_commands(devices, "\n", return_to_mngmt=True)


def send_commands(r_id, cmds, **kwargs):
    if type(r_id) == int:
        r_id = [r_id]
    for rid in r_id:
        write_to(rid, cmds, **kwargs)


def write_to(r_id, commands, return_to_mngmt=True, fast=True, prompt=None):
    if type(commands) == str:
        commands = [commands]
    for command in commands:
        if prompt:
            read_to_prompt(r_id, command, prompt)
        else:
            write_to_window(r_id, command, fast=fast)

    if return_to_mngmt:
        run(f"tmux select-window -t {mngmnt_screen}")


def write_to_window(r_id, command, fast=False):
    run(f"tmux select-window -t {r_id}")
    run(f'tmux send-keys -t {r_id} "{command}" Enter')
    if fast:
        time.sleep(slp_time)
    else:
        time.sleep(5)


def read_to_prompt(r_id, command, prompt="#"):
    run(f"tmux select-window -t {r_id}")
    run(f'tmux send-keys -t {r_id} "{command}" Enter')
    time.sleep(2)
    while True:
        run("tmux capture-pane -S -10 ; tmux save-buffer '/tmp/buffer_file' ; tmux delete-buffer")
        with open("/tmp/buffer_file") as f:
            content = f.read().strip().splitlines()
            if prompt in content[-1]:
                break
        time.sleep(1)


def run(line):
    subprocess.run(line, shell=True)


if __name__ == "__main__":
    from IPython import embed
    from traitlets.config import get_config
    c = get_config()
    c.InteractiveShellEmbed.colors = "Linux"
    embed(config=c)
