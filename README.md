# Getting Started

## One time installation
To begin installation, need Git for Windows. Install from here: https://git-scm.com/download/win
- Make sure to check "Add to PATH" when installing
- After installing, open a command prompt. Make sure when you type "git", it works

### Steps
1. Open command prompt
2. Navigate to the directory of your choice
3. Clone the repository
4. Run install-one-time.bat
```
cd C:\repo\
git clone https://github.com/jchan91/cosmos-plays-pokemon.git
cd cosmos-plays-pokemon
install-one-time.bat
```
5. You now have the 3rd party open source project, PyBoy. It's a Gameboy Color emulator. You need to follow those instructions there to install the libraries to run the emulator. Instructions are here: https://github.com/Baekalfen/PyBoy
    - Do the "Starting the Emulator" section. Can skip the "Download SDL2 Runtime" step, as it's already checked into this repository.

## Running the Emulator
TODO: Work in progress.

### Steps
1. Run start.bat
```
cd <repository_root>
start.bat
```

# Open issues
- Need to get a Pokemon ROM that works with the PyBoy emulator. See https://github.com/Baekalfen/PyBoy, "Setup and Run"