@ECHO OFF

set scriptDir=%~dp0
pushd %scriptDir%

set externalDir=%scriptDir%\external
if not exist %externalDir% (
    mkdir %externalDir
)

REM Clone pyboy
set pyboyDir=%externalDir%\pyboyDir
git submodule add https://github.com/Baekalfen/PyBoy.git %pyboyDir%

popd