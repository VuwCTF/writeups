import struct
import websockets
import asyncio

def trimbytes(data, bytecount):
    return bytes.fromhex(data.hex()[bytecount * 2:])

def getFirstBytes(data, bytecount):
    return bytes.fromhex(data.hex()[:bytecount*2])

target_sec_x = 15
target_sec_y = 2
current_sec_x = 0
current_sec_y = 0

playerName = b'UNIQUESTRINGHELLO'

def parsePlayerLocs(rawResp):
    rawResp = rawResp[12:] # trim header

    numPlayers = struct.unpack(">H", rawResp[:2])[0]
    rawResp = rawResp[2:]

    print(str(numPlayers) + " players")
    for i in range(numPlayers):
        print("Player " + str(i) + ":")
        id = struct.unpack(">L", getFirstBytes(rawResp, 4))[0]
        print("Id: " + str(id))
        rawResp = trimbytes(rawResp, 4)

        name = struct.unpack(">17s", getFirstBytes(rawResp, 17))[0]
        print("Name: " + str(name))
        rawResp = trimbytes(rawResp, 17)
        
        color = struct.unpack(">3B", getFirstBytes(rawResp, 3))[0]
        print("Packed color: " + str(color))
        rawResp = trimbytes(rawResp, 3)

        sec_x = struct.unpack("<H", getFirstBytes(rawResp, 2))[0]
        print("Sector X: " + str(sec_x))
        rawResp = trimbytes(rawResp, 2)

        # skipping 2 bytes of padding
        rawResp = trimbytes(rawResp, 2)

        sec_y = struct.unpack("<H", getFirstBytes(rawResp, 2))[0]
        print("Sector Y: " + str(sec_y))
        rawResp = trimbytes(rawResp, 2)

        # skipping 2 bytes of padding
        rawResp = trimbytes(rawResp, 2)

        doubles = struct.unpack("<4d", getFirstBytes(rawResp, 32))
        map_x = doubles[0]
        map_y = doubles[1]
        map_vx = doubles[2]
        map_vy = doubles[3]
        print("Map X: " + str(map_x))
        print("Map Y: " + str(map_y))
        print("Map Vx: " + str(map_vx))
        print("Map Vy: " + str(map_vy))
        rawResp = trimbytes(rawResp, 32)

        if name == playerName:
            global current_sec_x
            global current_sec_y
            current_sec_x = sec_x
            current_sec_y = sec_y

def makeMoveMsg():
    keys = []
    keysNum = 0
    if (current_sec_x > target_sec_x):
        keys.append(80) # SDL_SCANCODE_LEFT
        keysNum += 1
    elif (current_sec_x < target_sec_x):
        keys.append(79) # SDL_SCANCODE_RIGHT
        keysNum += 1

    if (current_sec_y < target_sec_y):
        keys.append(81) # SDL_SCANCODE_UP
        keysNum += 1
    elif (current_sec_y > target_sec_y):
        keys.append(82) # SDL_SCANCODE_DOWN
        keysNum += 1
    
    if keysNum == 0:
        return None
    elif keysNum == 1:
        msg = struct.pack( # move
            ">4s H 2s L H "+ str(keysNum)+"H",
            b'SPGM', # sig char[4]
            2, # type uint16_t
            b'0', # padding char[2]
            keysNum * 2, # length uint32_t
            keysNum, # num_keys uint16_t
            keys[0] # keys uint16_t[keysNum]
            )
    else:
        msg = struct.pack( # move
            ">4s H 2s L H "+ str(keysNum)+"H",
            b'SPGM', # sig char[4]
            2, # type uint16_t
            b'0', # padding char[2]
            keysNum * 2, # length uint32_t
            keysNum, # num_keys uint16_t
            keys[0], # keys uint16_t[keysNum]
            keys[1] # keys uint16_t[keysNum]
            )
    return msg

async def main():
    async with websockets.connect("wss://spacegame.io:443") as ws:
        msg = struct.pack( # signup
            ">4s H 2s L 4B H 17s", 
            b'SPGM', # sig char[4]
            0, # type uint16_t
            b'0', # padding char[2]
            12, # length uint32_t
            255, # r uint8_t
            255, # g uint8_t
            255, # b uint8_t
            0, # padding uint8_t
            17, # name_size uint16_t
            playerName # name char[name_size]
            )
        
        await ws.send(msg)
        
        # print("sent " + str(msg))
        
        rawResp = await ws.recv()

        sign_up_resp = struct.unpack(">4s H 2s L L H", rawResp)
        # print(sign_up_resp)

        while True:
            rawResp = await ws.recv()
            print("Raw message: " + str(rawResp))
            playerlocs = parsePlayerLocs(rawResp)

            await ws.send(makeMoveMsg())

            await asyncio.sleep(1/20) # 20 fps
        
asyncio.run(main())