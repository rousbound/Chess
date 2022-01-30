#!/bin/bash
# Creates UML representation of the project
# in the docs fig folder.
cd src/mychess
pyreverse  -o png -p Chess .
mv *.png ../../docs/fig
rm *.dot
