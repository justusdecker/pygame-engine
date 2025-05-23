@echo off
cd data
cd modules
echo "run gcc"
gcc -fPIC -shared -o graphics_rendering.so graphics_rendering.c
gcc -fPIC -shared -o pixelarray_manipulation.so pixelarray_manipulation.c
echo "finished gcc"
pause 2>NUL