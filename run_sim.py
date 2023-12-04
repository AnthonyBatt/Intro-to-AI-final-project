import poke_battle_sim as pb
import challengers as ch
from functions import print_battle_txt
from functions import print_dmg_range
from functions import print_poke_health
from functions import action_selection
from functions import dmg_calc
from functions import own_team
from functions import opp_team

mark = 0
flagmat = 0     # formattig flag

trainer1 = own_team()
trainer2 = opp_team()

battle = pb.Battle(trainer1, trainer2)
battle.start()

while not battle.get_winner():
    battle_txt = battle.get_all_text()
    bf = battle.battlefield

    p1 = trainer1.current_poke
    p2 = trainer2.current_poke

    print_poke_health(p1, p2)

    act1 = action_selection(p1, p2, bf, trainer1)
    act2 = action_selection(p2, p1, bf, trainer2)

    battle.turn(t1_turn=act1, t2_turn=act2)

    mark, flagmat = print_battle_txt(battle_txt, mark, flagmat)

    if act1[1] == 'switch':
        p1 = trainer1.current_poke
    if act2[1] == 'switch':
        p2 = trainer2.current_poke

    if act1[0] == 'move':
        print_dmg_range(p1, p2, act1[1], bf)
    if act2[0] == 'move':
        print_dmg_range(p2, p1, act2[1], bf)
    print()


print_poke_health(p1, p2)
