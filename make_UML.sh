#!/bin/bash
pyreverse  -o png -p Chess .
mv *.png docs/fig
rm *.dot
