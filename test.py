import poke_battle_sim as pb
import csv

# process type chart into a dictionary
eff_dict = dict()
type_enum = {
    "normal"    : 0,
    "fire"      : 1,
    "water"     : 2,
    "electric"  : 3,
    "grass"     : 4,
    "ice"       : 5,
    "fighting"  : 6,
    "poison"    : 7,
    "ground"    : 8,
    "flying"    : 9,
    "psychic"   : 10,
    "bug"       : 11,
    "rock"      : 12,
    "ghost"     : 13,
    "dragon"    : 14,
    "dark"      : 15,
    "steel"     : 16
}

for r in csv.reader(open('data/type_effectiveness.csv')):
    eff_dict[r[0]] = r[1:]

#for k, v in eff_dict.items(): print(k, v)

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
flagmat = 0     # formattig flag

print(f"Starmie MAX HP: {starmie.cur_hp}")
print(f"Pikachu MAX HP: {pikachu.cur_hp}\n")

# TODO implement the opponent's pokemon's stat guessing/calculating function
#   do it for each of their pokemon and do something like scan the output text for 'sent out' to look for
#   new pokemon to keep track of

# returns the given pokemon's hp as a percentage of their max health
def get_cur_hp(pokemon):
    return 100*int(pokemon.cur_hp)/pokemon.stats_actual[0]

# TODO calc supereffective
def effectiveness(move, target):
    eff_list = eff_dict[move.type]
    ret = 1

    for t in target.types:
        ret *= float(eff_list[type_enum[t]])

    return ret

# TODO need to make a separate calculator for other attributes (i.e. burn and weather)
def postmod_calc(move, atk, opp):
    mod = 1
    # STAB
    if move.type in atk.types:
        mod *= 1.5
    # type chart
    mod *= effectiveness(move, opp)
    
    return mod

# TODO may need to implement edge case checks for weird move
# returns a best and worst case estimate of damage done to opponent
def dmg_calc_atk(atk, opp, move, powmod):
    # step 1: calc level effectiveness
    s1 = (2*atk.level)/5 + 2
    # step 2: get move power and modifiers of said power
    #   these include weather, burn, stab, and type effectiveness
    s2 = move.power
    # step 3: calc stat matchup
    if move.category == 2:
        s3 = (atk.stats_actual[1]*2 / opp.stats_actual[2])      # need to *2 here cuz div by 2 in pokemon creation
    elif move.category == 3:
        s3 = (atk.stats_actual[3]*2 / opp.stats_actual[4])      # need to *2 here cuz div by 2 in pokemon creation
    # step 4: return base damage, let receiving function d multipliers
    base = ((s1*s2*s3)/50 + 2) * postmod_calc(move, atk, opp) + 2

    #        worst      poor    pessimist   avg      optimist    good      best
    return [base*.85, base*.88, base*.91, base*.925, base*.94, base*.97, base*1.0]

def action_selection(poke1, poke2):
    '''
    if not starmie.nv_status:
        battle.turn(t1_turn=['move', 'thunder-wave'], t2_turn=['move', 'bullet-seed'])
    # TODO implement a calc probable damage function
    elif get_cur_hp(starmie) < 16.001:
        battle.turn(t1_turn=['move', 'quick-attack'], t2_turn=['move', 'bullet-seed'])
    # TODO implement a pick attack move function based on power and type effectiveness
    else:
        battle.turn(t1_turn=['move', 'quick-attack'], t2_turn=['move', 'bullet-seed'])
    '''
    pass

    # have two different functions with different logic based on if opp or us is quicker

    # check who is quicker
    # if opp quicker (or speed tie) check if opp can oneshot
    #   if yes see if there is a good swap
    #       if no good swap check if we have a priority move
    #           if yes use it
    #           else make a judgment call on which pokemon to sack
    #       else make the best swap
    #   else evaluate matchup and check if there is a better one via swapping
    #       if there is a better match up switch and go for it
    #   else (meaning there is no better swap)
    #       MOVE SELECTION
    #       if they can't really hurt us, set up if possible
    #       else if we can oneshot do so
    #       else if we can paralyze opp do so (slow them down, possible prevent another attack, etc.)
    #       else if we can two shot them just attack
    #       else if they have a tanky pokemon, poison/toxic them if we can
    #       else if they are a phys attacker, burn them if we can
    #       else check for if there is a less valuable/better matchup pokemon to throw out right now
    #       else see if we have any moves that have secondary effects which would produce something good
    #       else just attack with our best move
    # else (we are faster)
    #   enter MOVE SELECTION
    #   check for similar stuff above, like can they one shot us, do we have a better swap, etc.

    #return action, obj

while not battle.get_winner():
    battle_txt = battle.get_all_text()

    # TODO implement a should_switch function
    
    pick_move(pikachu, starmie)
    if not starmie.nv_status:
        battle.turn(t1_turn=['move', 'thunder-wave'], t2_turn=['move', 'bullet-seed'])
    # TODO implement a calc probable damage function
    elif get_cur_hp(starmie) < 16.001:
        battle.turn(t1_turn=['move', 'quick-attack'], t2_turn=['move', 'bullet-seed'])
    # TODO implement a pick attack move function based on power and type effectiveness
    else:
        battle.turn(t1_turn=['move', 'quick-attack'], t2_turn=['move', 'bullet-seed'])


    #print(effectiveness(pikachu.moves[2], starmie))
    base = dmg_calc_atk(pikachu, starmie, pikachu.moves[1], 1) 
    dmgMin, dmgMax = base[0], base[6]
    print(f"Range: ({dmgMin}, {dmgMax})")

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
            
    #print(starmie.stats_actual[5])
    print(f"\nStarmie HP: {starmie.cur_hp} ({get_cur_hp(starmie):.2f}%)")
    print(f"Pikachu HP: {pikachu.cur_hp} ({get_cur_hp(pikachu):.2f}%)")

