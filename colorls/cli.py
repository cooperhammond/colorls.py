import argparse
import core


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-A", "--all", dest="all", help="Display hidden files \
(dotfiles) as well.", action="store_true")

    args = parser.parse_args()

    c = core.Core(args)
    for s in c.package_text():
        print(s)


if __name__ == "__main__":
    main()
