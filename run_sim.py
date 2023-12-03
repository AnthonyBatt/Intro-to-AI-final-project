import poke_battle_sim as pb
import challengers as ch
from functions import print_battle_txt
from functions import print_dmg_range
from functions import print_poke_health
from functions import action_selection
from functions import dmg_calc

mark = 0
flagmat = 0     # formattig flag

trainer1 = ch.Ash()
trainer2 = ch.Misty()

battle = pb.Battle(trainer1, trainer2)
battle.start()

while not battle.get_winner():
    battle_txt = battle.get_all_text()
    bf = battle.battlefield

    p1 = trainer1.current_poke
    p2 = trainer2.current_poke

    print_poke_health(p1, p2)

    '''
    action_selection(p1, p2, env)
    if not p2.nv_status:
        battle.turn(t1_turn=['move', 'thunder-wave'], t2_turn=['move', 'bullet-seed'])
        used_move = p1.moves[3]
    elif p2.cur_hp < dmg_calc(p1, p2, p1.moves[1], bf)[4]:
        battle.turn(t1_turn=['move', 'quick-attack'], t2_turn=['move', 'bullet-seed'])
        used_move = p1.moves[1]
    # TODO implement a pick attack move function based on power and type effectiveness
    else:
        m0 = dmg_calc(p1, p2, p1.moves[0], bf)[3]
        m2 = dmg_calc(p1, p2, p1.moves[2], bf)[3]

        if m0 > m2:
            battle.turn(t1_turn=['move', 'thunderbolt'], t2_turn=['move', 'bullet-seed'])
            used_move = p1.moves[0]
        else:
            battle.turn(t1_turn=['move', 'iron-tail'], t2_turn=['move', 'bullet-seed'])
            used_move = p1.moves[2]
    '''

    act1 = action_selection(p1, p2, bf)
    act2 = action_selection(p2, p1, bf)

    battle.turn(t1_turn=act1, t2_turn=act2)

    mark, flagmat = print_battle_txt(battle_txt, mark, flagmat)

    print_dmg_range(p1, p2, act1[1], bf)
    #used_move = p2.moves[0]
    print_dmg_range(p2, p1, act2[1], bf)
    print()


print_poke_health(p1, p2)
