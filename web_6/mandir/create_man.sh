#!/bin/bash

cp /usr/share/man/man1/pandoc.1.gz ./
gunzip pandoc.1.gz
pandoc -s pandoc.1 -t markdown -o pandoc.md
cat pandoc.md adding.md > pandoc.2.md
pandoc -s pandoc.2.md -t man -o pandoc.2
gzip pandoc.2
cp pandoc.2.gz /usr/share/man/man1/pandoc.1.gz