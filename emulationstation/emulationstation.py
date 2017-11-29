#restart ES CMD: echo "" > /tmp/es-restart && killall emulationstation
from subprocess import call

class EmulationStation:

    def __init__(self, runcommand_path):
        #TODO: validate runcommand path
        self.runcommand_path = runcommand_path

    def restart(self):
        call('echo "" > /tmp/es-restart && killall emulationstation')

    def launchROM(self, rom_path, emulator):
        #TODO: validate rom path and emulator
        call(
            "{0} 0 _SYS_ {1} {2}".format(
                self.runcommand_path,
                rom_path,
                emulator)
        )

