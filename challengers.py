import poke_battle_sim as pb


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

    ash = pb.Trainer('Ash', [pikachu])

    return ash

############################## END TRAINER ASH


############################## START TRAINER MISTY

def Misty():
    starmie = pb.Pokemon(
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

    misty = pb.Trainer('Misty', [starmie, ivysaur])

    return misty

############################## END TRAINER MISTY
