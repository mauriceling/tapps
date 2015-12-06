mkdir tapps
cp -r copads tapps
cp -r plugins tapps
cp -r ply tapps
cp *.py tapps 
rm tapps/parsetab.py

epydoc --verbose \
       --pdf \
       --output=doc/epydoc \
       --name="TAPPS: Technical (Analysis) and Applied Statistics System" \
       --url=https://github.com/mauriceling/tapps \
       --show-imports \
       --show-private \
       --show-sourcecode \
       --show-frames \
       --navlink=https://github.com/mauriceling/tapps \
       tapps

mv doc/epydoc/api.pdf doc/TAPPS_API_Documentation.pdf
rm -rf doc/epydoc

epydoc --verbose \
       --html \
       --output=doc/epydoc \
       --name="TAPPS: Technical (Analysis) and Applied Statistics System" \
       --url=https://github.com/mauriceling/tapps \
       --show-imports \
       --show-private \
       --show-sourcecode \
       --show-frames \
       --navlink=https://github.com/mauriceling/tapps \
       tapps

rm -rf tapps
