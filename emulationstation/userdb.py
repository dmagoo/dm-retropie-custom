import os
import io
import json

class UserDB:
    rom_bindings = {}
    
    def __init__(self, db_file):
        self.db_file = db_file
        self._load()
        
    def _load(self):
        if (os.path.isfile(self.db_file) and
        os.access(self.db_file, os.R_OK)):
            dat = json.loads(open(self.db_file).read())
            self.rom_bindings = dat.setdefault("rom_bindings", {})
        else:
            #put the file there, I guess
            self._save()

    def _save(self):
        with io.open(self.db_file, 'w', encoding="utf-8") as db_file:
            db_file.write(unicode(self.toJSON()))

    def toJSON(self):
        return json.dumps(
            {"rom_bindings": self.rom_bindings}
        )

    def getRomBinding(self, uid):
        return self.rom_bindings.get(uid)

    def setRomBinding(self, uid, rom_path, system, emulator=None):
        self.rom_bindings[uid] = {
            "rom": rom_path,
            "system": system,
            "emulator": emulator
        }
        self._save()
