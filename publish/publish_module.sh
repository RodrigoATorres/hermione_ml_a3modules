#!/bin/bash

git clone https://github.com/RodrigoATorres/hermione_ml_a3modules.git
cd hermione_ml_a3modules
git remote rm origin
git filter-branch --subdirectory-filter hermione_ml_a3modules/module_templates/$1 -- --all
mkdir -p hermione/module_templates/$1
git mv -k * hermione/module_templates/$1
git add .
git commit -m 'Adding module'

cd ..
git clone https://github.com/RodrigoATorres/hermione.git
cd hermione
git remote add $1 ../hermione_ml_a3modules
git fetch $1
git branch $1 remotes/$1/main
git merge $1 --allow-unrelated-histories
git remote rm $1