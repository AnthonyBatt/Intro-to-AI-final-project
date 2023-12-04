import poke_battle_sim as pb
import functions as fx

def Gym1():
    ''' returns the bug type gym leader '''
    heracross = pb.Pokemon(
        name_or_id="heracross",
        level=100,
        moves=[
            "close-combat",
            "megahorn",
            "stone-edge",
            "night-slash"
        ],
        gender="female",
        stats_actual=[302, 192, 186, 52, 226, 269]
    )

    armaldo = pb.Pokemon(
        name_or_id="armaldo",
        level=100,
        moves=[
            "rock-blast",
            "stealth-rock",
            "rapid-spin",
            "toxic"
        ],
        gender="male",
        stats_actual=[354, 144, 328, 79, 196, 126]
    )

    yanmega = pb.Pokemon(
        name_or_id="yanmega",
        level=100,
        moves=[
            "bug-buzz",
            "air-slash",
            "u-turn",
            "giga-drain"
        ],
        gender="male",
        stats_actual=[314, 85, 208, 116, 148, 317]
    )
    leader = pb.Trainer('Bug Type Leader', [armaldo, heracross, yanmega], fx.selection_func)

    return leader

def Gym2():
    ''' returns the ice type gym leader '''
    walrein = pb.Pokemon(
        name_or_id="walrein",
        level=100,
        moves=[
            "protect",
            "substitute",
            "toxic",
            "water-pulse"
        ],
        gender="male",
        stats_actual=[419, 88, 306, 116, 216, 166]
    )

    glaceon = pb.Pokemon(
        name_or_id="glaceon",
        level=100,
        moves=[
            "blizzard",
            "ice-beam",
            "shadow-ball",
            "toxic"
        ],
        gender="female",
        stats_actual=[362, 88, 216, 159, 216, 229]
    )

    froslass = pb.Pokemon(
        name_or_id="froslass",
        level=100,
        moves=[
            "icy-wind",
            "spikes",
            "shadow-ball",
            "destiny-bond"
        ],
        gender="female",
        stats_actual=[281, 88, 176, 130, 177, 350]
    )

    leader = pb.Trainer('Ice Type Leader', [froslass, glaceon, walrein], fx.selection_func)

    return leader

def Gym3():
    ''' returns the electric type gym leader '''
    electivire = pb.Pokemon(
        name_or_id="electivire",
        level=100,
        moves=[
            "brick-break",
            "flamethrower",
            "thunderbolt",
            "thunder-wave"
        ],
        gender="male",
        stats_actual=[291, 171, 153, 144, 206, 263]
    )

    raikou = pb.Pokemon(
        name_or_id="raikou",
        level=100,
        moves=[
            "thunderbolt",
            "aura-sphere",
            "shadow-ball",
            "extreme-speed"
        ],
        gender="male",
        stats_actual=[321, 103, 186, 180, 213, 329]
    )

    luxray = pb.Pokemon(
        name_or_id="luxray",
        level=100,
        moves=[
            "ice-fang",
            "fire-fang",
            "thunder-fang",
            "crunch"
        ],
        gender="female",
        stats_actual=[311, 186, 194, 102, 194, 230]
    )

    leader = pb.Trainer('Electric Type Leader', [electivire, luxray, raikou], fx.selection_func)

    return leader
