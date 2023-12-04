import poke_battle_sim as pb
import challengers as ch
import gyms
import csv


############################## BEGIN MISCELLANEOUS

# returns the given pokemon's hp as a percentage of their max health
def get_cur_hp(pokemon):
    return 100*int(pokemon.cur_hp)/pokemon.stats_actual[0]

# returns which move does the most damage
def most_damage(atk, opp, env):
    ret = atk.moves[0]
    for move in atk.moves:
        if dmg_calc(atk, opp, move, env)[4] > dmg_calc(atk, opp, ret, env)[4]:
            ret = move

    return ret

# process type chart into a dictionary
# returns the effectiveness multiplier
def effectiveness(mtype, target):
    if not mtype: return -1
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
    eff_list = eff_dict[mtype]
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

def print_dmg_range(p1, p2, used_move_name, bf):
    for move in p1.moves:
        if move.name == used_move_name:
            used_move = move
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
    mod *= effectiveness(move.type, opp)
    
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
    base1 = (((s1*s2*s3)/50)*premod_calc(move, atk, env) + 2) * postmod_calc(move, atk, opp)
    if base1: 
        base = base1 + 2
    else:
        base = base1

    #        worst      poor    pessimist   avg      optimist    good      best
    return [base*.85, base*.88, base*.91, base*.925, base*.94, base*.97, base*1.0]

############################## END DAMAGE CALCULATOR


############################## BEGIN AI LOGIC

# TODO make a swapping function and pass it into the CPU trainer's creation
# returns the action item to be passed into the turn thing
def action_selection(my, opp, env, me):
    # check who is quicker
    faster = my.stats_actual[5] > opp.stats_actual[5]
    # if opp quicker (or speed tie) 
    if not faster:
        # check if opp can oneshot
        ohko = False
        for move in opp.moves:
            if my.cur_hp < dmg_calc(opp, my, move, env)[4]:
                ohko = True
        # if yes see if there is a good swap
        if ohko:
            # return if a swap should occur, if so internally change the trainer's current_poke
            swap = should_swap(my, opp, env, me) # TODO
            if swap:
                perform_swap(swap, me)
                return ['other', 'switch']
            # if no good swap check if we have a priority move
            else:
                # if yes use it
                for move in my.moves:
                    if move.prio and dmg_calc(my, opp, move, env)[4]:
                        return ['move', move.name]
                # else just stay in and suffer

        # else if we dont get ohko'd check if we have a prio move that can one shot
        else:
            for move in my.moves:
                if move.prio and opp.cur_hp < dmg_calc(my, opp, move, env)[4]:
                    # if yes use it
                    return ['move', move.name]
        # otherwsie just proceed normally
        return move_selection(my, opp, env, me)
    # else (we are faster)
    else:
        return move_selection(my, opp, env, me)

# general case logic for what attack to use, may result in a swap if no good attacks available
def move_selection(my, opp, env, me):
    # TODO MAYBE: if they can't really hurt us, set up if possible # TODO figure out how tell which moves setup

    # check if I can one shot
    ohko = False
    for move in my.moves:
        if opp.cur_hp < dmg_calc(my, opp, move, env)[4]:
            ohko = True
    # if yes, return the move that will do the most damage
    if ohko:
        return ['move', most_damage(my, opp, env).name]

    conds = [0,0,0,0,0] # [ burn, para, pois, slee, toxi ]
    # if the opponenet doesn't already have a status condition
    if not opp.nv_status:
        # see which status conds we have access to
        for move in my.moves:
            # NEEDS ef_id == 13 for this to be relevant
            # ef_stat = 1 is burn
            # ef_stat = 3 is para
            # ef_stat = 4 is poison
            # ef_stat = 5 is sleep
            # ef_stat = 6 is toxic
            if move.ef_id == 13 and move.ef_stat == 1: conds[0] = 1 #burn
            if move.ef_id == 13 and move.ef_stat == 3: conds[1] = 1 #paralysis
            if move.ef_id == 13 and move.ef_stat == 4: conds[2] = 1 #poison
            if move.ef_id == 13 and move.ef_stat == 5: conds[3] = 1 #sleep
            if move.ef_id == 13 and move.ef_stat == 6: conds[4] = 1 #toxic

    # else if we can paralyze opp do so (slow them down, possible prevent another attack, etc.)
    if conds[1]:
        for move in my.moves:
            if move.ef_id == 13 and move.ef_stat == 3:
                if 'electric' not in opp.types and 'ground' not in opp.types: 
                    return ['move', move.name]
    # else if we can sleep opp do so
    if conds[3]:
        for move in my.moves:
            if move.ef_id == 13 and move.ef_stat == 5:
                return ['move', move.name]
    # else if we can two shot them just attack
    thko = False
    for move in my.moves:
        if opp.cur_hp/2 < dmg_calc(my, opp, move, env)[3]:
            thko = True
    # if yes, return the move that will do the most damage
    if ohko:
        return ['move', most_damage(my, opp, env).name]
    # else if they have a tanky pokemon, toxic them if we can
    if conds[4]:
        for move in my.moves:
            if move.ef_id == 13 and move.ef_stat == 6:
                if 'poison' not in opp.types and 'steel' not in opp.types: 
                    return ['move', move.name]
    # else if they are a phys attacker, burn them if we can
    if conds[0]:
        for move in my.moves:
            if move.ef_id == 13 and move.ef_stat == 1:
                if 'fire' not in opp.types: 
                    return ['move', move.name]
    # else just poison them if we can
    if conds[2]:
        for move in my.moves:
            if move.ef_id == 13 and move.ef_stat == 4:
                if 'poison' not in opp.types and 'steel' not in opp.types: 
                    return ['move', move.name]
            
    # else check for if there is a less valuable/better matchup pokemon to throw out right now
    swap = should_swap(my, opp, env, me) # TODO
    if swap:
        perform_swap(swap, me)
        return ['other', 'switch']

    #TODO MAYBE: else see if we have any moves that have secondary effects which would produce something good

    # else just attack with our best move
    return ['move', most_damage(my, opp, env).name]

# TODO implement a should_switch function
def should_swap(my, opp, env, me):
    # check effectiveness of our STAB on opp
    curr_off = max([ effectiveness(t, opp) for t in my.types ])
    # and opp's STAB on us

    curr_def = max([ effectiveness(t, my) for t in opp.types ])
    pote_off = -1  # min is 0
    pote_def = 100 # max is 4
    pote_switch = None

    for poke in me.poke_list:
        if not poke.is_alive: continue
        # check effectiveness of all bench poke's STAB on opp
        chek_off = max([ effectiveness(t, opp) for t in poke.types ])
        # check effectiveness of opp's STAB on all bench poke
        chek_def = max([ effectiveness(t, poke) for t in opp.types ])

        # check for finding which bench poke has the best matchup
        if chek_off >= pote_off and chek_def <= pote_def:
            pote_off = chek_off
            pote_def = chek_def
            pote_switch = poke

    # check if the best bench matchup is better than curr matchup
    #   Note: more stringent check here because on the swap will be vulnerable
    if pote_off >= curr_off and pote_def < curr_def:
        # switch in the better matchup
        return pote_switch
    else:
        # don't switch
        return None

# TODO find a way to use this also when a pokemon faints
def perform_swap(poke, trainer):
    trainer.current_poke = poke

# place holder for interfacing with lib
def selection_func(self):
    mfw = "Yippee"

# TODO MAYBE:   implement the opponent's pokemon's stat guessing/calculating function
#               do it for each of their pokemon and do something like scan the output 
#               text for 'sent out' to look for new pokemon to keep track of

############################## END AI LOGIC


############################## BEGIN UI

def own_team():
    print("Which challenger would you like to play as:")
    print("\t1. Anthony (Me)\n\t2. Jerrick\n\t3. Thomas")
    inp = int(input("Enter the number of the trainer you want: "))
    print()

    if inp == 1:
        return ch.Anthony()
    elif inp == 2:
        return ch.Jerrick()
    # TODO make lohmann
    elif inp == 3:
        return ch.Thomas()

    # secret challengers
    elif inp == 98:
        return ch.Ash()
    elif inp == 99:
        return ch.Misty()
    else:
        print("that is an invalid trainer number, please pick again")
        return own_team()

def opp_team():
    print("Which leader would you like to play against:")
    print("\t1. Bug\n\t2. Ice\n\t3. Electric")
    inp = int(input("Enter the number of the leader you want: "))
    print()

    if inp == 1:
        return gyms.Gym1()
    elif inp == 2:
        return gyms.Gym2()
    elif inp == 3:
        return gyms.Gym3()
    else:
        print("that is an invalid leader number, please pick again")
        return opp_team()

############################## END UI
