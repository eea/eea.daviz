#!/bin/sh

if [ -s "bin/activate" ]; then
  echo "Buildout is already installed. "
  echo "Please remove bin/activate if you want to re-run this script."
  exit 0
fi

ZCBUILDOUT=`grep "zc\.buildout" versions.cfg | sed 's/=/==/g'`

echo "Installing virtualenv"
wget "http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.5.2.tar.gz" -O "/tmp/virtualenv-1.5.2.tar.gz"
tar -zxvf "/tmp/virtualenv-1.5.2.tar.gz" -C "/tmp/"

echo "Running: python2.6 virtualenv.py --clear --no-site-packages ."
python2.6 "/tmp/virtualenv-1.5.2/virtualenv.py" --clear --no-site-packages .
rm "/tmp/virtualenv-1.5.2.tar.gz"
rm -r "/tmp/virtualenv-1.5.2"

echo "Installing zc.buildout: $ ./bin/easy_install" $ZCBUILDOUT
./bin/easy_install $ZCBUILDOUT

echo "All set. Now you can run ./bin/buildout"
