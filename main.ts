//  Create unique kinds for projectiles and items
let EnemyAttack = SpriteKind.create()
let ItemKind = SpriteKind.create()
//  Game State Variables
let in_battle = false
let saved_x = 0
let saved_y = 0
let ghost : Sprite = null
let ghost_hp = 5
let is_boss = false
let has_crowbar = false
let crowbar_item : Sprite = null
let liquorice_item : Sprite = null
let MAX_HP = 5
//  Set up Player Life (Hearts display in top-left corner)
info.setLife(MAX_HP)
//  Overworld starts with White Background (Color 1)
scene.setBackgroundColor(1)
//  Overworld Player Setup
let hero = sprites.create(img`
    . . . . . . . .
    . . 2 2 2 2 . .
    . . 2 2 2 2 . .
    . . . . . . . .
`, SpriteKind.Player)
controller.moveSprite(hero)
//  Spawn Crowbar Item (Left side)
crowbar_item = sprites.create(img`
    . . . . . . . c
    . . . . . . c c
    . . . . . c c .
    . . . . c c . .
    . . . c c . . .
    c c c c . . . .
    c . . . . . . .
`, ItemKind)
crowbar_item.setPosition(40, 60)
//  Spawn Liquorice Healing Item (Right side)
liquorice_item = sprites.create(img`
    . . . . . . . .
    . . f f f f . .
    . . f 3 3 f . .
    . . f f f f . .
    . . f 3 3 f . .
    . . f f f f . .
    . . . . . . . .
    . . . . . . . .
`, ItemKind)
liquorice_item.setPosition(120, 60)
//  Smooth color palette fade functions
function fade_to_black() {
    let colors = [1, 11, 9, 8, 12, 15]
    for (let c of colors) {
        scene.setBackgroundColor(c)
        pause(50)
    }
}

function fade_to_white() {
    let colors = [15, 12, 8, 9, 11, 1]
    for (let c of colors) {
        scene.setBackgroundColor(c)
        pause(50)
    }
}

function start_battle(force_boss: boolean) {
    
    in_battle = true
    //  Hide overworld items during battle
    if (crowbar_item != null) {
        crowbar_item.setFlag(SpriteFlag.Invisible, true)
    }
    
    if (liquorice_item != null) {
        liquorice_item.setFlag(SpriteFlag.Invisible, true)
    }
    
    //  Save location & pause controls during fade
    saved_x = hero.x
    saved_y = hero.y
    controller.moveSprite(hero, 0, 0)
    //  Gradual palette fade from White to Black
    fade_to_black()
    //  Move hero into battle arena position
    hero.setPosition(80, 100)
    controller.moveSprite(hero)
    //  Determine if standard ghost or miniboss ghost
    if (force_boss) {
        is_boss = true
    } else {
        is_boss = Math.percentChance(5)
    }
    
    if (is_boss) {
        ghost_hp = 10
        ghost = sprites.create(img`
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
        `, SpriteKind.Enemy)
        ghost.say("MINIBOSS HP: " + ("" + ghost_hp))
    } else {
        ghost_hp = 5
        ghost = sprites.create(img`
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
        `, SpriteKind.Enemy)
        ghost.say("HP: " + ("" + ghost_hp))
    }
    
    ghost.setPosition(80, 30)
}

function end_battle() {
    
    if (ghost != null) {
        ghost.say("")
    }
    
    controller.moveSprite(hero, 0, 0)
    //  Gradual palette fade back to White
    fade_to_white()
    //  Restore overworld items if not picked up yet
    if (crowbar_item != null) {
        crowbar_item.setFlag(SpriteFlag.Invisible, false)
    }
    
    if (liquorice_item != null) {
        liquorice_item.setFlag(SpriteFlag.Invisible, false)
    }
    
    hero.setPosition(saved_x, saved_y)
    controller.moveSprite(hero)
    in_battle = false
}

//  Ghost Attack Loop
game.onUpdateInterval(1000, function on_ghost_attack() {
    let bullet_speed: number;
    let eball: Sprite;
    
    if (in_battle && ghost != null) {
        bullet_speed = is_boss ? 75 : 50
        eball = sprites.createProjectileFromSprite(img`
                . 2 2 .
                2 2 2 2
                2 2 2 2
                . 2 2 .
            `, ghost, 0, bullet_speed)
        eball.setKind(EnemyAttack)
    }
    
})
//  Press A: Shoot in battle OR interact with overworld items
controller.A.onEvent(ControllerButtonEvent.Pressed, function on_a_pressed() {
    
    if (in_battle) {
        if (has_crowbar) {
            //  Crowbar Wave Projectile
            sprites.createProjectileFromSprite(img`
                    . . 5 5 5 5 5 5 5 5 5 5 . .
                    . 5 5 5 5 5 5 5 5 5 5 5 5 .
                    5 5 5 5 5 5 5 5 5 5 5 5 5 5
                    . . . . . . . . . . . . . .
                `, hero, 0, -100)
        } else {
            //  Standard Projectile
            sprites.createProjectileFromSprite(img`
                    . 5 5 .
                    5 5 5 5
                    5 5 5 5
                    . 5 5 .
                `, hero, 0, -100)
        }
        
    } else if (crowbar_item != null && hero.overlapsWith(crowbar_item)) {
        has_crowbar = true
        sprites.destroy(crowbar_item)
        crowbar_item = null
        hero.say("Got Crowbar!", 1000)
    } else if (liquorice_item != null && hero.overlapsWith(liquorice_item)) {
        info.setLife(MAX_HP)
        sprites.destroy(liquorice_item)
        liquorice_item = null
        hero.say("Full HP Restored!", 1000)
    }
    
})
//  Player hits Ghost
sprites.onOverlap(SpriteKind.Enemy, SpriteKind.Projectile, function on_ghost_hit(enemy_sprite: Sprite, proj_sprite: Sprite) {
    let prefix: any;
    
    sprites.destroy(proj_sprite)
    ghost_hp -= 1
    if (ghost_hp > 0) {
        prefix = is_boss ? "MINIBOSS HP: " : "HP: "
        ghost.say(prefix + ("" + ghost_hp))
        scene.cameraShake(2, 100)
    } else {
        sprites.destroy(enemy_sprite, effects.disintegrate, 500)
        pause(600)
        end_battle()
    }
    
})
//  Player hit by Ghost projectile -> Deduct 1 Heart
sprites.onOverlap(SpriteKind.Player, EnemyAttack, function on_player_hit(hero_sprite: Sprite, attack_sprite: Sprite) {
    sprites.destroy(attack_sprite)
    info.changeLifeBy(-1)
    scene.cameraShake(3, 150)
})
//  Press B (X / S key) -> Standard Battle Trigger
controller.B.onEvent(ControllerButtonEvent.Pressed, function on_b_pressed() {
    
    if (!in_battle) {
        start_battle(false)
    }
    
})
//  Press Menu (Enter key) -> Dev Shortcut to Force Miniboss Battle
controller.menu.onEvent(ControllerButtonEvent.Pressed, function on_menu_pressed() {
    
    if (!in_battle) {
        start_battle(true)
    }
    
})
