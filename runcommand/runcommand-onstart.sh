#$1 - the system (eg: atari2600, nes, snes, megadrive, fba, etc).
#$2 - the emulator (eg: lr-stella, lr-fceumm, lr-picodrive, pifba, etc).
#$3 - the full path to the rom file.
#$4 - the full command line used to launch the emulator.

#echo "message to log" >&2
#system="$1"
#emulator="$2"
#rom_path="$3"
#cmd="$4"

#echo "$system - $emulator - $rom_path - $cmd" > /tmp/rcstart.log

echo $@ > /tmp/rcstart.log;
