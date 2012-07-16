#!/bin/sh

rm -rf build
mkdir build
cp *.xml *.py *.plist icon.png README.md build/
cp -R requests build/

cd build
rm -r requests/*.py
rm -r requests/packages/*.py
rm -r requests/packages/chardet/*.py
rm -r requests/packages/chardet2/*.py
rm -r requests/packages/oauthlib/*.py
rm -r requests/packages/urllib3/*.py
cd ..
