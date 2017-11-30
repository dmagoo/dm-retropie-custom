import logging
from subprocess import call

class EmulationStation:

    def __init__(self, runcommand_path):
        #TODO: validate runcommand path
        self.runcommand_path = runcommand_path

    def restart(self):
        call('echo "" > /tmp/es-restart && killall emulationstation')

    def launchROM(self, rom_path, system, emulator):
        """ raises a child_exception of subproc cannot execute command """
        #TODO: validate rom path and system
        #TODO: allow emulator to override _SYS_ default
        #if restart is true, re
        logging.info("{0} 0 _SYS_ {1} {2}".format(
            self.runcommand_path,
            system,
            rom_path
            ))

        cmd = "{0} 0 _SYS_ {1} {2}".format(
                self.runcommand_path,
                system,
                rom_path
                )

        #cmd = "(true || killall emulationstation) && (true || " + cmd + ") && emulationstation"

        call(cmd, shell=True)

