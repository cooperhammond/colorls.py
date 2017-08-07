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
        self.width = int(os.popen('stty size', 'r').read().split()[-1])

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
                f[2] = "\x1b[32m" + f[2] + " "  # 32 = green
            elif f[1] == "dir":
                f[2] = "\x1b[34m" + f[2] + " " # 34 = blue
                f[0] = f[0] + "/"
            f[0] = f[0] + "\x1b[0m"

    def package_text(self, opts={}):
        self.contents = self.custom_sort(self.contents)
        self.add_icons()
        self.add_colors()
        self.items = []
        for f in self.contents:
            self.items.append(f[2] + " " + f[0])
        return self.col_print(self.items)

    def wrap_text(self):
        # (\\x1b\[\d+m|\\u.{4}) The golden operator.
        s = "    "
        for f in self.contents:
            print(re.sub('(\\x1b\[\d+m|\\u.{4})', ' ', f))
            if len(s.split("\n")[-1]) + len(re.sub(r'\\u....', " ", f)) > self.columns:
                s = s[:-4]
                s += "\n" + f
            else:
                s += f + "    "
        return s

    def blank(self, s):
        # print(s + " - " + str(len(s)))
        s = re.sub("\x1b\[\d+m", "", s)
        s = re.sub("\\\u.{4}", "_", s.encode("unicode-escape"))
        # print(s + " - " + str(len(s)))
        return s

    def col_print(self, lines_, indent=4, pad=3):
        # From https://gist.github.com/critiqjo/2ca84db26daaeb1715e1
        lines = list(self.blank(line) for line in lines_)
        n_lines = len(lines)
        if n_lines == 0:
            return []

        col_width = max(len(self.blank(line)) for i, line in enumerate(lines))
        n_cols = int((self.width + pad - indent) / (col_width + pad))
        n_cols = min(n_lines, max(1, n_cols))

        col_len = int(n_lines / n_cols) + (0 if n_lines % n_cols == 0 else 1)
        if (n_cols - 1) * col_len >= n_lines:
            n_cols -= 1

        cols = [lines[i * col_len:i * col_len + col_len] for i in range(n_cols)]

        rows = list(zip(*cols))
        rows_missed = zip(*[col[len(rows):] for col in cols[:-1]])
        rows.extend(rows_missed)

        contents = []
        for row in rows:
            contents.append(''.join(" " * indent + (" " * pad).join(line.ljust(col_width) for line in row)))

        for i, line in enumerate(contents):
            for l in lines_:
                line = line.replace(self.blank(l), l)
                contents[i] = line

        return contents



core = Core()
for l in core.package_text():
    print(l)
