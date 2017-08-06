import os
import yaml
import re

# NOTE: must call `.decode("unicode-escape")` on unicode string to eval icon


class Core:
    def __init__(self, directory="."):
        self.directory = directory
        self.contents = self.get_directory_contents()
        self.files = self.read_yaml("files")
        self.file_aliases = self.read_yaml("file_aliases")
        self.folders = self.read_yaml("folders")
        self.folder_aliases = self.read_yaml("folder_aliases")
        rows, self.columns = os.popen('stty size', 'r').read().split()

    def get_directory_contents(self):
        contents = []
        for dirpath, dirs, files_ in os.walk(self.directory):
            for f in files_:
                contents.append([f, "file"])
            for d in dirs:
                contents.append([d, "dir"])
            break

        return contents

    def custom_sort(self, contents):
        return sorted(contents, key=lambda v: (v[0].upper(), v[0][0].islower()))

    def read_yaml(self, filename):
        filename = "yaml/" + filename + ".yaml"
        with open(filename, "r") as stream:
            try:
                return(yaml.load(stream))
            except yaml.YAMLError as e:
                print(e)
                exit(1)

    def add_icons(self):
        for i, f in enumerate(self.contents):
            if f[1] == "file":
                ext = f[0].split(".")[-1]
                if ext in self.files:
                    self.contents[i].append(self.files[ext])
                elif ext in self.file_aliases:
                    self.contents[i].append(self.files[self.file_aliases[ext]])
                else:
                    self.contents[i].append(self.files["file"])
            elif f[1] == "dir":
                if f[0] in self.folders:
                    self.contents[i].append(self.folders[f[0]])
                elif f[0] in self.folder_aliases:
                    self.contents[i].append(self.folders[self.folder_aliases[f[0]]])
                else:
                    self.contents[i].append(self.folders["folder"])

    def add_colors(self):
        for f in self.contents:
            if f[1] == "file":
                f[2] = "\x1b[32m" + f[2] + " "
            elif f[1] == "dir":
                f[2] = "\x1b[34m" + f[2] + " "
                f[0] = f[0] + "/"
            f[0] = f[0] + "\x1b[0m"

    def package_text(self, opts={}):
        self.contents = self.custom_sort(self.contents)
        self.add_icons()
        self.add_colors()
        contents = []
        for f in self.contents:
            contents.append(f[2] + " " + f[0])
        return '    '.join(contents)


core = Core()
print(core.package_text())
