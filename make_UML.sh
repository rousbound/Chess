#!/bin/bash
cd src/mychess
pyreverse  -o png -p Chess .
mv *.png ../../docs/fig
rm *.dot
