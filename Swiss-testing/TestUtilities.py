import Tournament
import Player 

def simple_pairing_setup():
    t = Tournament.Tournament()
    for _ in range(2):
        low_player = Player.Player()
        high_player = Player.Player()
        high_player.score = 1
        t.add_player(low_player)
        t.add_player(high_player)
    return t

def eight_pairing_setup():
    t = Tournament.Tournament()
    for i in range(8):
        player = Player.Player()
        player.score = 1
        player.sos = i
        t.add_player(player)
    return t

def four_by_two_setup():
    t = Tournament.Tournament()
    for i in range(4):
        player = Player.Player()
        player.score = 1
        player.sos = i
        t.add_player(player)
    for i in range(4):
        player = Player.Player()
        player.sos = i
        t.add_player(player)
    return t

def eight_floater_down_setup():
    t = Tournament.Tournament()
    for i in range(7):
        player = Player.Player()
        player.sos = i
        t.add_player(player)
    player = Player.Player()
    player.score = 1
    player.is_floater = True
    t.add_player(player)
    return t

def nine_pairing_setup():
    t = Tournament.Tournament()
    for i in range(9):
        player = Player.Player()
        player.sos = i
        t.add_player(player)
    return t

def nine_pairing_floater_setup():
    t = Tournament.Tournament()
    for i in range(8):
        player = Player.Player()
        player.sos = i
        t.add_player(player)
    player = Player.Player()
    player.score = 1
    player.is_floater = True
    t.add_player(player)
    return t

def nine_pairing_floater_up_setup():
    t = Tournament.Tournament()
    for i in range(8):
        player = Player.Player()
        player.score = 1
        player.sos = i
        t.add_player(player)
    player = Player.Player()
    player.sos = 2
    player.is_floater = True
    t.add_player(player)
    return t