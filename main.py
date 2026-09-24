# Create unique kinds for projectiles and items
EnemyAttack = SpriteKind.create()
ItemKind = SpriteKind.create()

# Game State Variables
in_battle = False
saved_x = 0
saved_y = 0
ghost: Sprite = None
ghost_hp = 5
is_boss = False
has_crowbar = False
crowbar_item: Sprite = None
liquorice_item: Sprite = None
MAX_HP = 5

# Set up Player Life (Hearts display in top-left corner)
info.set_life(MAX_HP)

# Overworld starts with White Background (Color 1)
scene.set_background_color(1)

# Overworld Player Setup
hero = sprites.create(img("""
    . . . . . . . .
    . . 2 2 2 2 . .
    . . 2 2 2 2 . .
    . . . . . . . .
"""), SpriteKind.player)
controller.move_sprite(hero)

# Spawn Crowbar Item (Left side)
crowbar_item = sprites.create(img("""
    . . . . . . . c
    . . . . . . c c
    . . . . . c c .
    . . . . c c . .
    . . . c c . . .
    c c c c . . . .
    c c . . . . . .
"""), ItemKind)
crowbar_item.set_position(40, 60)

# Spawn Liquorice Healing Item (Right side)
liquorice_item = sprites.create(img("""
    . . . . . . . .
    . . f f f f . .
    . . f 3 3 f . .
    . . f f f f . .
    . . f 3 3 f . .
    . . f f f f . .
    . . . . . . . .
    . . . . . . . .
"""), ItemKind)
liquorice_item.set_position(120, 60)

# Smooth color palette fade functions
def fade_to_black():
    colors = [1, 11, 9, 8, 12, 15]
    for c in colors:
        scene.set_background_color(c)
        pause(50)

def fade_to_white():
    colors = [15, 12, 8, 9, 11, 1]
    for c in colors:
        scene.set_background_color(c)
        pause(50)

def start_battle(force_boss):
    global in_battle, saved_x, saved_y, ghost, ghost_hp, is_boss, crowbar_item, liquorice_item
    in_battle = True
    
    # Hide overworld items during battle
    if crowbar_item != None:
        crowbar_item.set_flag(SpriteFlag.INVISIBLE, True)
    if liquorice_item != None:
        liquorice_item.set_flag(SpriteFlag.INVISIBLE, True)
    
    # Save location & pause controls during fade
    saved_x = hero.x
    saved_y = hero.y
    controller.move_sprite(hero, 0, 0)
    
    # Gradual palette fade from White to Black
    fade_to_black()
    
    # Move hero into battle arena position
    hero.set_position(80, 100)
    controller.move_sprite(hero)
    
    # Determine if standard ghost or miniboss ghost
    if force_boss:
        is_boss = True
    else:
        is_boss = Math.percent_chance(5)
    
    if is_boss:
        ghost_hp = 10
        ghost = sprites.create(img("""
            . . . . 1 1 1 1 1 1 1 1 . . . .
            . . . 1 1 1 1 1 1 1 1 1 1 . . .
            . . 1 1 1 1 1 1 1 1 1 1 1 1 . .
            . 1 1 2 2 1 1 1 1 1 1 2 2 1 1 .
            . 1 1 1 2 2 1 1 1 1 2 2 1 1 1 .
            1 1 1 1 f f 1 1 1 1 f f 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 1 1 2 2 1 1 1 1 1 1 1
            1 1 1 1 1 1 2 2 2 2 1 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 . 1 1 1 1 1 1 1 1 . 1 1 1
            1 1 . . . 1 1 1 1 1 1 . . . 1 1
            1 . . . . . 1 1 1 1 . . . . . 1
        """), SpriteKind.enemy)
        ghost.say("MINIBOSS HP: " + str(ghost_hp))
    else:
        ghost_hp = 5
        ghost = sprites.create(img("""
            . . . 1 1 1 1 1 1 1 1 . . .
            . . 1 1 1 1 1 1 1 1 1 1 . .
            . 1 1 1 1 1 1 1 1 1 1 1 1 .
            . 1 1 f 1 1 1 1 1 1 f 1 1 .
            1 1 1 f 1 1 1 1 1 1 f 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 1 1 1 1 1 1 1 1 1 1 1
            1 1 1 . 1 1 1 1 1 1 . 1 1 1
            1 1 . . 1 1 1 1 1 1 . . 1 1
            1 . . . . . 1 1 . . . . . 1
        """), SpriteKind.enemy)
        ghost.say("HP: " + str(ghost_hp))
        
    ghost.set_position(80, 30)

def end_battle():
    global in_battle, ghost, crowbar_item, liquorice_item
    
    if ghost != None:
        ghost.say("")
    
    controller.move_sprite(hero, 0, 0)
    
    # Gradual palette fade back to White
    fade_to_white()
    
    # Restore overworld items if not picked up yet
    if crowbar_item != None:
        crowbar_item.set_flag(SpriteFlag.INVISIBLE, False)
    if liquorice_item != None:
        liquorice_item.set_flag(SpriteFlag.INVISIBLE, False)
    
    hero.set_position(saved_x, saved_y)
    controller.move_sprite(hero)
    in_battle = False

# Ghost Attack Loop
def on_ghost_attack():
    global in_battle, ghost, is_boss
    if in_battle and ghost != None:
        bullet_speed = 75 if is_boss else 50
        eball = sprites.create_projectile_from_sprite(
            img("""
                . 2 2 .
                2 2 2 2
                2 2 2 2
                . 2 2 .
            """), ghost, 0, bullet_speed
        )
        eball.set_kind(EnemyAttack)

game.on_update_interval(1000, on_ghost_attack)

# Press A: Shoot in battle OR interact with overworld items
def on_a_pressed():
    global in_battle, has_crowbar, crowbar_item, liquorice_item, MAX_HP
    if in_battle:
        if has_crowbar:
            # Crowbar Wave Projectile
            sprites.create_projectile_from_sprite(
                img("""
                    . . 5 5 5 5 5 5 5 5 5 5 . .
                    . 5 5 5 5 5 5 5 5 5 5 5 5 .
                    5 5 5 5 5 5 5 5 5 5 5 5 5 5
                    . . . . . . . . . . . . . .
                """), hero, 0, -100
            )
        else:
            # Standard Projectile
            sprites.create_projectile_from_sprite(
                img("""
                    . 5 5 .
                    5 5 5 5
                    5 5 5 5
                    . 5 5 .
                """), hero, 0, -100
            )
    else:
        # Overworld Item Pickups
        if crowbar_item != None and hero.overlaps_with(crowbar_item):
            has_crowbar = True
            sprites.destroy(crowbar_item)
            crowbar_item = None
            hero.say("Got Crowbar!", 1000)
            
        elif liquorice_item != None and hero.overlaps_with(liquorice_item):
            info.set_life(MAX_HP)
            sprites.destroy(liquorice_item)
            liquorice_item = None
            hero.say("Full HP Restored!", 1000)

controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

# Player hits Ghost
def on_ghost_hit(enemy_sprite, proj_sprite):
    global ghost_hp, is_boss
    sprites.destroy(proj_sprite)
    ghost_hp -= 1
    
    if ghost_hp > 0:
        prefix = "MINIBOSS HP: " if is_boss else "HP: "
        ghost.say(prefix + str(ghost_hp))
        scene.camera_shake(2, 100)
    else:
        sprites.destroy(enemy_sprite, effects.disintegrate, 500)
        pause(600)
        end_battle()

sprites.on_overlap(SpriteKind.enemy, SpriteKind.projectile, on_ghost_hit)

# Player hit by Ghost projectile -> Deduct 1 Heart
def on_player_hit(hero_sprite, attack_sprite):
    sprites.destroy(attack_sprite)
    info.change_life_by(-1)
    scene.camera_shake(3, 150)

sprites.on_overlap(SpriteKind.player, EnemyAttack, on_player_hit)

# Press B (X / S key) -> Standard Battle Trigger
def on_b_pressed():
    global in_battle
    if not in_battle:
        start_battle(False)

controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

# Press Menu (Enter key) -> Dev Shortcut to Force Miniboss Battle
def on_menu_pressed():
    global in_battle
    if not in_battle:
        start_battle(True)

controller.menu.on_event(ControllerButtonEvent.PRESSED, on_menu_pressed)