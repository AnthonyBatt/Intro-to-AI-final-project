import poke_battle_sim as pb

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
        stats_actual=[302, 383, 186, 104, 226, 269]
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
        stats_actual=[354, 287, 328, 158, 196, 126]
    )

    leader = pb.Trainer('Bug Type Leader', [armaldo, heracross])

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
            "surf"
        ],
        gender="male",
        stats_actual=[419, 176, 306, 232, 216, 166]
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
        stats_actual=[362, 176, 216, 317, 216, 229]
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
        stats_actual=[281, 176, 176, 259, 177, 350]
    )

    leader = pb.Trainer('Ice Type Leader', [froslass, glaceon, walrein])

    return leader
