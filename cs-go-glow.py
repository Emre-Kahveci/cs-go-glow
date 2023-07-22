import pymem
from time import sleep

# Offsets (converted to decimal notation)
localPlayer = 0x00DEA98C
entityList = 0x04DFFF7C
glowObjectManager = 0x0535AA08
teamNum = 0x00F4
glowIndex = 0x010488

def glow() -> None:
    pm = pymem.Pymem('csgo.exe') # find csgo.exe
    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        local_player = pm.read_int(client + localPlayer)
        glow_Object_Manager = pm.read_int(client + glowObjectManager)

        for i in range(64):
            entity = pm.read_int(client + entityList + i * 0x10)

            if entity == 0 or entity == local_player:
                continue
            
            entityTeamNum = pm.read_int(entity + teamNum)
            localPlayerTeamNum = pm.read_int(local_player + teamNum)

            if entityTeamNum == localPlayerTeamNum:
                continue
            
            glow_Index = pm.read_int(entity + glowIndex)
            glow_Object = glow_Object_Manager + (glow_Index * 0x38)

            pm.write_float(glow_Object + 0x8, 0.0)
            pm.write_float(glow_Object + 0xC, 1.0)
            pm.write_float(glow_Object + 0x10, 0.0)
            pm.write_float(glow_Object + 0x14, 1.0)

            pm.write_bool(glow_Object + 0x27, True)
            pm.write_bool(glow_Object + 0x28, True)

        sleep(0.01)

if __name__ == "__main__":
    glow()
