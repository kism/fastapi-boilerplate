#!/usr/bin/env python

from pathlib import Path
import os
import subprocess

__app_package = "{{ cookiecutter.__app_package }}"

print()
print(f"--- Running post generating scripts for: {__app_package} ---")

original_dir = Path.cwd()

print("Grabbing CSS:")

os.chdir(f"{__app_package}")

proc = subprocess.Popen(
    "curl -LsS https://github.com/kism/zy.css/releases/download/main/grab.sh | bash",
    shell=True,
    stdout=subprocess.PIPE,
)

proc_stdout = proc.stdout.read().decode("utf-8")

for line in proc_stdout.split("\n"):
    print(f"  {line}")

os.chdir(original_dir)

print("Done grabbing CSS!")

print("Doing some cleanup due to some templating conflicts...")

file_path = "{{cookiecutter.__app_package}}/templates/home.html.j2"

with open(file_path, "r") as file:
    j2_file_content = file.read()

j2_file_content = j2_file_content.replace(
    '<script src="PLACEHOLDER_DUE_TO_TEMPLATE_CONFLICT"></script>',
    f'<script src="/static/{__app_package}.js"></script>',
)

with open(file_path, "w") as file:
    file.write(j2_file_content)

