import poke_battle_sim as pb
from functions import selection_func


############################## START TRAINER ASH

def Ash():
    # Pokemon number 1 on team number 1
    pikachu = pb.Pokemon(
        name_or_id="pikachu",                           # the pokemon 
        level=100,                                      # its level
        moves=[                                         # its moveset 
            "thunderbolt",
            "quick-attack",
            "iron-tail",
            "thunder-wave"
        ],
        gender="male",                                  # its gender
        stats_actual=[311, 73, 96, 68, 116, 216]        # its stats
    )

    ash = pb.Trainer('Ash', [pikachu], selection_func)

    return ash

############################## END TRAINER ASH


############################## START TRAINER MISTY

def Misty():
    starmie = pb.Pokemon(
        name_or_id = "staryu",
        level=100,
        moves=["water-gun"],
        gender="genderless",
        stats_actual=[100, 24, 24, 24, 24, 24]
    )

    bulbasaur = pb.Pokemon(
        name_or_id="bulbasaur", 
        level=100, 
        moves=["bullet-seed"], 
        gender="male", 
        stats_actual=[100, 67, 134, 83, 166, 300]
    )

    ivysaur = pb.Pokemon(
        name_or_id="ivysaur", 
        level=100, 
        moves=["bullet-seed"], 
        gender="male", 
        stats_actual=[231, 67, 186, 83, 80, 200]
    )

    misty = pb.Trainer('Misty', [starmie, bulbasaur, ivysaur], selection_func)

    return misty

############################## END TRAINER MISTY


############################## START TRAINER ANTHONY

def Anthony():
    feraligatr = pb.Pokemon(
        name_or_id="feraligatr", 
        level=100, 
        moves=[
            "waterfall",
            "ice-punch",
            "crunch",
            "aqua-jet"
            ], 
        gender="male", 
        stats_actual=[318, 170, 236, 86, 202, 249]
    )

    sceptile = pb.Pokemon(
        name_or_id="sceptile", 
        level=100, 
        moves=[
            "energy-ball",
            "focus-blast",
            "x-scissor",
            "dragon-pulse"
            ], 
        gender="male", 
        stats_actual=[282, 92, 166, 155, 206, 372]
    )

    gliscor = pb.Pokemon(
        name_or_id="gliscor", 
        level=100, 
        moves=[
            "cross-poison",
            "wing-attack",
            "night-slash",
            "toxic"
            ], 
        gender="female", 
        stats_actual=[291, 120, 303, 56, 273, 260]
    )

    anthony = pb.Trainer('Anthony', [gliscor, sceptile, feraligatr], selection_func)

    return anthony

############################## END TRAINER ANTHONY


############################## START TRAINER JERRICK

def Jerrick():
    drapion = pb.Pokemon(
        name_or_id="drapion", 
        level=100, 
        moves=[
            "iron-tail",
            "aqua-tail",
            "night-slash",
            "poison-jab"
            ], 
        gender="male", 
        stats_actual=[344, 108, 257, 70, 273, 226]
    )

    aggron = pb.Pokemon(
        name_or_id="aggron", 
        level=100, 
        moves=[
            "rock-slide",
            "aqua-tail",
            "iron-head",
            "brick-break"
            ], 
        gender="male", 
        stats_actual=[301, 150, 396, 70, 240, 136]
    )

    ttar = pb.Pokemon(
        name_or_id="tyranitar", 
        level=100, 
        moves=[
            "crunch",
            "fire-punch",
            "thunder-punch",
            "rock-slide"
            ], 
        gender="female", 
        stats_actual=[353, 189, 256, 101, 282, 178]
    )

    jerrick = pb.Trainer('Jerrick', [ttar, aggron, drapion], selection_func)

    return jerrick

############################## END TRAINER ANTHONY
