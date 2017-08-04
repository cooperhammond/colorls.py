import os
import yaml

# NOTE: must call `.decode("unicode-escape")` on unicode string to eval icon


class Core:
    def __init__(self, directory="."):
        self.directory = directory
        self.dfiles, self.dfolders = self.get_directory_contents()
        self.files = self.read_yaml("files")
        self.file_aliases = self.read_yaml("file_aliases")
        self.folders = self.read_yaml("folders")
        self.folder_aliases = self.read_yaml("folder_aliases")

    def get_directory_contents(self):
        files = []
        folders = []
        for dirpath, dirs, files_ in os.walk(self.directory):
            files.extend(files_)
            folders.extend(dirs)
            break

        return files, folders

    def csort(self, contents):
        return sorted(contents, key=lambda v: (v.upper(), v[0].islower()))

    def read_yaml(self, filename):
        filename = "yaml/" + filename + ".yaml"
        with open(filename, "r") as stream:
            try:
                return(yaml.load(stream))
            except yaml.YAMLError as e:
                print(e)
                exit(1)

    def add_icons(self):
        for i, f in enumerate(self.dfiles):
            ext = f.split(".")[-1]
            if ext in self.files:
                self.dfiles[i] = self.files[ext] + " " + f
            elif ext in self.file_aliases:
                self.dfiles[i] = self.files[self.file_aliases[ext]] + " " + f

        for i, f in enumerate(self.dfolders):

            if f in self.folders:
                self.dfolders[i] = self.folders[f] + " " + f + "/"
            elif f in self.folder_aliases:
                self.dfolders[i] = self.folders[self.folder_aliases[f]] + " " + f + "/"
            else:
                self.dfolders[i] = self.folders["folder"] + " " + f + "/"

    def add_colors(self):
        self.dfiles = ("\x1b[32m" + s + "\x1b[0m" for s in self.dfiles)
        self.dfolders = ("\x1b[34m" + s + "\x1b[0m" for s in self.dfolders)

core = Core()
core.add_icons()
core.add_colors()
print('    ' + '    '.join(core.dfiles))
print('    ' + '    '.join(core.dfolders))
