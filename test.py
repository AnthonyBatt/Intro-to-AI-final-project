import poke_battle_sim as pb

# returns the given pokemon's hp as a percentage of their max health
def get_cur_hp(pokemon):
    return 100*int(pokemon.cur_hp)/pokemon.stats_actual[0]

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
    stats_actual=[211, 73, 96, 68, 116, 216]        # its stats
)

ash = pb.Trainer('Ash', [pikachu])

starmie = pb.Pokemon(
    name_or_id="bulbasaur", 
    level=100, 
    moves=["bullet-seed"], 
    gender="male", 
    stats_actual=[231, 67, 134, 83, 166, 300]
)

misty = pb.Trainer('Misty', [starmie])

battle = pb.Battle(ash, misty)
battle.start()

mark = 0
flagmat = 0

print(f"Starmie MAX HP: {starmie.cur_hp}")
print(f"Pikachu MAX HP: {pikachu.cur_hp}\n")

# TODO implement the opponent's pokemon's stat guessing/calculating function
#   do it for each of their pokemon and do something like scan the output text for 'sent out' to look for
#   new pokemon to keep track of

while not battle.get_winner():
    battle_txt = battle.get_all_text()

    # TODO implement a should_switch function
    if not starmie.nv_status:
        battle.turn(t1_turn=['move', 'thunder-wave'], t2_turn=['move', 'bullet-seed'])
    # TODO implement a calc probable damage function
    elif get_cur_hp(starmie) < 16.001:
        battle.turn(t1_turn=['move', 'quick-attack'], t2_turn=['move', 'bullet-seed'])
    # TODO implement a pick attack move function based on power and type effectiveness
    else:
        battle.turn(t1_turn=['move', 'iron-tail'], t2_turn=['move', 'bullet-seed'])
        
    for i in range(mark, len(battle_txt)):
        if "Turn" in battle_txt[i]:
            flagmat = 1
            print()
            print(battle_txt[i])
        elif flagmat:
            print(f"    {battle_txt[i]}")
        else:
            print(battle_txt[i])
        mark = i + 1
            
    print(starmie.stats_actual[5])
    print(f"\nStarmie HP: {starmie.cur_hp} ({get_cur_hp(starmie):.2f}%)")
    print(f"Pikachu HP: {pikachu.cur_hp} ({get_cur_hp(pikachu):.2f}%)")

