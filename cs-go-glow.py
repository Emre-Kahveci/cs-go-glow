import pymem
from time import sleep

# Offsets
offsets = {
    'entityList': 0x4DFFF7C,
    'localPlayer': 0xDEA98C,
    'glowObjectManager': 0x535AA08,
    'teamNum': 0xF4,
    "glowIndex": 0x10488,
}

def glow() -> None:
    pm = pymem.Pymem('csgo.exe') # find csgo.exe
    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # access client.dll
    
    while True:

        localPlayer = pm.read_uint(client + offsets["localPlayer"])
        glowObjectManager = pm.read_uint(client + offsets["glowObjectManager"])

        for i in range(1,64):
            entity = pm.read_uint(client + offsets["entityList"] + i * 0x10)

            #if the entity is not empty and not localPlayer
            if entity == 0 or entity == localPlayer:
                continue
            
            #if entity and localPlayer are not on the same team
            if pm.read_uint(entity + offsets["teamNum"]) == pm.read_uint(localPlayer + offsets["teamNum"]):
                continue
            
            glowIndex = pm.read_uint(entity + offsets["glowIndex"])
            glowObject = glowObjectManager + (glowIndex * 0x38)

            #glow
            pm.write_float(glowObject + 0x8, 0.0) # red
            pm.write_float(glowObject + 0xC, 1.0) # green
            pm.write_float(glowObject + 0x10, 0.0) # blue
            pm.write_float(glowObject + 0x14, 1.0) # alpha
            pm.write_bool(glowObject + 0x27, True)
            pm.write_bool(glowObject + 0x28, True)

        sleep(0.01)
if __name__ == "__main__":
    glow()