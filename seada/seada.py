#!/usr/bin/env python
# DEASOS - Data Extraction and Analysis System from Open sources

from argparse import ArgumentParser


def banner():
    f = open("banner2.txt",'r')
    banner = f.readlines()
    for line in banner:
        print(line.replace("\n",""))
    f.close()


def main():
    banner()

    argp = ArgumentParser(
        description='Descripción breve del programa',
        epilog='Copyright 2018 Autor bajo licencia GPL v3.0'
    )


if __name__ == '__main__':
    main()