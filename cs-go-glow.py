import requests
import pymem
from time import sleep

def get_offset(url = "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the JSON file: {e}")
        return None

def glow(offsets = get_offset()) -> None:
    pm = pymem.Pymem('csgo.exe') # find csgo.exe
    
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll # access client.dll
    
    while True:

        localPlayer = pm.read_uint(client + offsets["signatures"]["dwLocalPlayer"])
        glowObjectManager = pm.read_uint(client + offsets["signatures"]["dwGlowObjectManager"])

        for i in range(1,64):
            entity = pm.read_uint(client + offsets["signatures"]["dwEntityList"] + i * 0x10)

            #if the entity is not empty and not localPlayer
            if entity == 0 or entity == localPlayer:
                continue
            
            #if entity and localPlayer are not on the same team
            if pm.read_uint(entity + offsets["netvars"]["m_iTeamNum"]) == pm.read_uint(localPlayer + offsets["netvars"]["m_iTeamNum"]):
                continue
            
            glowIndex = pm.read_uint(entity + offsets["netvars"]["m_iGlowIndex"])
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