import pymem
from time import sleep

# Offsets
currentPlayer = 0x00DEA98C
entityList = 0x04DFFF7C
glowObjectManager = 0x0535AA08
teamNo = 0x00F4
glowIndex = 0x010488

def glow() -> None:
    pm = pymem.Pymem('csgo.exe') # find csgo.exe
    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # access client.dll

    while True:
        current_player = pm.read_int(client + currentPlayer)
        glow_Object_Manager = pm.read_int(client + glowObjectManager)

        for i in range(1,64):
            entity = pm.read_int(client + entityList + i * 0x10)

            #if the entity is not empty and not local_player
            if entity == 0 or entity == current_player:
                continue
            
            entityTeamNo = pm.read_int(entity + teamNo)
            localPlayerTeamNo = pm.read_int(current_player + teamNo)

            #if entity and local_player are not on the same team
            if entityTeamNo == localPlayerTeamNo:
                continue
            
            glow_Index = pm.read_int(entity + glowIndex)
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
