@echo off
cd data
cd modules
echo "run gcc"
gcc -fPIC -shared -o graphics_rendering.so graphics_rendering.c
echo "finished gcc"
pause 2>NUL