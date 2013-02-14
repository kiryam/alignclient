rm -R build
rm -R package
python3.3 setup.py build
python3.3 setup_reloader.py build

mkdir package
cp build/exe.macosx-10.6-intel-3.3/* package/
