import poke_battle_sim as pb
import csv


############################## BEGIN MISCELLANEOUS

# returns the given pokemon's hp as a percentage of their max health
def get_cur_hp(pokemon):
    return 100*int(pokemon.cur_hp)/pokemon.stats_actual[0]

# process type chart into a dictionary
# returns the effectiveness multiplier
def effectiveness(move, target):
    # setting up the type chart 
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

    # get the list of type relations for the type of the attacking move
    eff_list = eff_dict[move.type]
    # base multiplier is 1
    ret = 1
    # add in the effectiveness multipliers of the target pokemon's type(s)
    for t in target.types:
        if t: ret *= float(eff_list[type_enum[t]])

    return ret

############################## END MISCELLANEOUS


############################## START PRINT FUNCTIONS

def print_battle_txt(battle_txt, mark, flagmat):
    for i in range(mark, len(battle_txt)):
        if "Turn" in battle_txt[i]:
            flagmat = 1
            print(battle_txt[i])
        elif flagmat:
            print(f"    {battle_txt[i]}")
        else:
            print(battle_txt[i])
        mark = i + 1

    print()

    return mark, flagmat

def print_dmg_range(p1, p2, used_move, bf):
    base = dmg_calc(p1, p2, used_move, bf)
    dmgMin, dmgMax = base[0], base[6]
    print(f"{p1.name} --> {p2.name} | Damage Range: ({dmgMin}, {dmgMax})")

def print_poke_health(p1, p2):
    print(f"{p1.name} HP: {p1.cur_hp} ({get_cur_hp(p1):.2f}%)")
    print(f"{p2.name} HP: {p2.cur_hp} ({get_cur_hp(p2):.2f}%)")
    print()

############################## END PRINT FUNCTIONS


############################## BEGIN DAMAGE CALCULATOR

# calculates following factors:
#   completed:  burn, weather, flash fire
#   not yet:    
#   might not:  targets
#   can't:      screens
def premod_calc(move, atk, env):
    mod = 1
    # Flash Fire
    if atk.has_ability("flash-fire") and atk.ability_activated and move.type == "fire":
        mod *= 1.5
    
    # weather
    if move.name == "solar-beam" and (env.weather != 1 or env.weather != 0): # sun; clear
        mod *= .5
    elif env.weather == 2: # rain
        if move.type == 'water': mod*=1.5
        elif move.type == 'fire': mod*=.5
    elif env.weather == 1: #sun
        if move.type == 'fire': mod*=1.5
        elif move.type == 'water': mod*=.5

    # burn
    if atk.nv_status == 1 and not atk.has_ability("guts") and move.category == 2: # burn; physical
        mod *= .5

    return mod

# calculates following factors:
#   completed:  stab, effectiveness, filter, solid-rock
#   not yet:    
#   might not:  items, berries
#   can't:      me first
def postmod_calc(move, atk, opp):
    mod = 1

    # type chart
    mod *= effectiveness(move, opp)
    
    # Tinted Lens
    if mod < 1 and atk.has_ability("tinted-lens"):
       mod *= 2
    elif mod > 1 and not atk.has_ability("mold-breaker") and (opp.has_ability("filter") or opp.has_ability("solid-rock")):
       mod *= .75
    
    # STAB
    if move.type in atk.types:
        mod *= 1.5
    
    return mod

# TODO may need to implement edge case checks for weird move
# returns a best and worst case estimate of damage done to opponent
def dmg_calc(atk, opp, move, env):
    # step 1: calc level effectiveness
    s1 = (2*atk.level)/5 + 2
    # step 2: get move power and modifiers of said power
    #   these include weather, burn, stab, and type effectiveness
    s2 = move.power
    #if move.ef_id == 10: s2 *= 3 # could hit 2-5 times, but most likely is 3
    # step 3: calc stat matchup
    if move.category == 1:
        # status effect so no damage done
        return [0, 0, 0, 0, 0, 0, 0]
    elif move.category == 2:
        s3 = (atk.stats_actual[1]*2 / opp.stats_actual[2])      # need to *2 here cuz div by 2 in pokemon creation
    elif move.category == 3:
        s3 = (atk.stats_actual[3]*2 / opp.stats_actual[4])      # need to *2 here cuz div by 2 in pokemon creation
    # step 4: return base damage, let receiving function d multipliers
    base = (((s1*s2*s3)/50)*premod_calc(move, atk, env) + 2) * postmod_calc(move, atk, opp) + 2

    #        worst      poor    pessimist   avg      optimist    good      best
    return [base*.85, base*.88, base*.91, base*.925, base*.94, base*.97, base*1.0]

############################## END DAMAGE CALCULATOR


############################## BEGIN AI LOGIC

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

# TODO implement a move_selection function
# TODO implement a shold_switch function
# TODO implement the opponent's pokemon's stat guessing/calculating function
#   do it for each of their pokemon and do something like scan the output text for 'sent out' to look for
#   new pokemon to keep track of

############################## END AI LOGIC
