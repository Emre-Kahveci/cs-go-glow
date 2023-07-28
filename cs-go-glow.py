import pymem
from time import sleep

# Offsets
localPlayer = 0xDEA98C
entityList = 0x4DFFF7C
glowObjectManager = 0x535AA08
teamNum = 0xF4
glowIndex = 0x10488

def glow() -> None:
    pm = pymem.Pymem('csgo.exe') # find csgo.exe
    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # access client.dll
    
    while True:

        local_player = pm.read_uint(client + localPlayer)
        glow_Object_Manager = pm.read_uint(client + glowObjectManager)

        for i in range(1,64):
            entity = pm.read_uint(client + entityList + i * 0x10)

            #if the entity is not empty and not local_player
            if entity == 0 or entity == local_player:
                continue
            
            #if entity and local_player are not on the same team
            if pm.read_uint(entity + teamNum) == pm.read_uint(local_player + teamNum):
                continue
            
            glow_Index = pm.read_uint(entity + glowIndex)
            glow_Object = glow_Object_Manager + (glow_Index * 0x38)

            #glow
            pm.write_float(glow_Object + 0x8, 0.0) # red
            pm.write_float(glow_Object + 0xC, 1.0) # green
            pm.write_float(glow_Object + 0x10, 0.0) # blue
            pm.write_float(glow_Object + 0x14, 1.0) # alpha
            pm.write_bool(glow_Object + 0x27, True)
            pm.write_bool(glow_Object + 0x28, True)

        sleep(0.01)
if __name__ == "__main__":
    glow()