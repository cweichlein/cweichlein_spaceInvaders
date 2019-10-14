import sys
import pygame
from bullet import Bullet
import alien as al
from time import sleep
import bunker as bu
import bonus as bon


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:  # can use elif as each event is only connected to only one key
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:  # can use elif as each event is only connected to only one key
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, mode_button, sb, ship, bullets, aliens, alien_bullets,
                 bunkers, bonus, explosions):
    # check_events listens for user interaction and calls check_keyup_events() or check_keydown_events() accordingly
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, mouse_x, mouse_y, play_button, sb, ship, bullets, aliens,
                              alien_bullets, bunkers, bonus, explosions)
            check_mode_button(ai_settings, stats, mouse_x, mouse_y, mode_button)


def check_mode_button(ai_settings, stats, mouse_x, mouse_y, mode_button):
    # pull high scores screen overlay
    button_clicked = mode_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.mode *= -1


def check_play_button(ai_settings, screen, stats, mouse_x, mouse_y, play_button, sb, ship, bullets, aliens,
                      alien_bullets, bunkers, bonus, explosions):
    # new game when mouse clicked over button
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()  # resets all settings that change with stage back to level 1.
        pygame.mouse.set_visible(False)  # hide mouse

        stats.reset_stats()  # resets things like number of aliens left in field from any previous game
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()  # is this particular line really necessary? I thought prep_high_score has the prep called
        # automatically whenever it is changed in check_bullet_alien_collisions() via check_high_score(). Redundancy?
        sb.prep_level()
        sb.prep_ships()

        for res in aliens:
            res.reset = True
        for res_bonus in bonus:
            res_bonus.reset = True
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()
        bunkers.empty()
        bonus.empty()

        create_fleet(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, explosions)
        create_bunkers(ai_settings, bunkers)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, play_button, mode_button, sb, ship, bullets, aliens,
                  alien_bullets, bunkers, bonus, explosions):
    # redraw screen with color each loop pass
    if ship.respawn:
        ship.respawn = False
        reset(ai_settings, stats, screen, sb, ship, bullets, aliens, alien_bullets, bunkers, bonus, explosions)
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for a_bullet in alien_bullets.sprites():
        a_bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    bunkers.draw(screen)
    sb.show_score()
    bonus.draw(screen)
    explosions.draw(screen)
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        sb.display_main_menu()
        play_button.draw_button()
        mode_button.draw_button()
        if ai_settings.mode == 1:  # display black rect with words that give scores
            sb.display_high_scores()
        if stats.broke_high_score:
            save_high_score(stats, sb)
            stats.broke_high_score = False
    pygame.display.flip()  # Make recent screen visible, by flipping it over the old one


def update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens, alien_bullets, bunkers, bonus, explosions):
    bullets.update()  # move bullets
    for bullet in bullets.copy():  # remove bullets as they fly off screen
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens, alien_bullets, bunkers,
                                  bonus, explosions)
    check_bullet_bunker_collisions(bullets, bunkers)


def update_alien_bullets(ai_settings, stats, ship, alien_bullets, bunkers):
    alien_bullets.update()  # move bullets
    for a_bullet in alien_bullets.copy():  # remove bullets as they fly off screen
        if a_bullet.rect.bottom >= ai_settings.screen_height:
            alien_bullets.remove(a_bullet)
    check_bullet_bunker_collisions(alien_bullets, bunkers)
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(stats, ship)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens, alien_bullets, bunkers,
                                  bonus, explosions):
    collisions_bonus = pygame.sprite.groupcollide(bullets, bonus, True, True)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)  # collisions is a dictionary variable (a map)
    # Remember that each value in collisions is a bullet ID followed by a list of aliens its collided with
    if collisions:
        # for bullet in collisions.values():  # executes once for each bullet active in this game tic
        # indent////stats.score += ai_settings.alien_points * len(bullet)  # len(bullet) == size of alien list for the
        # bullet
        # we use a dictionary because, if our bullets are thick and capable of hitting multiple aliens, they will
        # acknowledge each alien rather than simply detect a single impact and increment points once.
        # Also, if two bullets were to somehow hit aliens at the same tic, the game needs to account for each bullet
        # individually and not merely scream "a bullet has hit during this tic, increment score once!"
        # sb.prep_score()
        for _ in collisions.values():
            check_high_score(stats, sb)
    if collisions_bonus:
        for _ in collisions_bonus.values():
            # stats.score += ai_settings.alien_points * len(bullet_bonus)
            # sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) < 10:
        stats.start_music(10)
    elif len(aliens) < 30:
        stats.start_music(30)
    elif len(aliens) < 50:
        stats.start_music(50)
    else:
        stats.start_music(100)
    if len(aliens) == 0:
        stats.music_reset()
        bullets.empty()  # destroy all bullets, spawn new fleet, increase speedup_scale in settings
        bunkers.empty()
        ai_settings.increase_speed()
        # increase the level and tell scoreboard to prep it
        stats.level += 1
        sb.prep_level()
        ai_settings.levelUp.play()  # play sound

        create_fleet(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, explosions)
        create_bunkers(ai_settings, bunkers)


def check_high_score(stats, sb):
    if stats.score > stats.high_score[9]:
        stats.broke_high_score = True
        sb.prep_high_score()
    if stats.score > stats.high_score[0]:
        stats.high_score[0] = stats.score
        stats.broke_high_score = True
        sb.prep_high_score()


def save_high_score(stats, sb):
    check = 0
    while stats.score < stats.high_score[check]:
        check += 1
    # copy all down one starting at index check
    temp = check
    check = 9
    while check != temp:
        stats.high_score[check] = stats.high_score[check - 1]
        check -= 1
    stats.high_score[temp] = stats.score
    sb.prep_high_score()  # see annotation above prep_score() in scoreboard.py for explanation


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (3 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, stats, sb, aliens, alien_number, row_number, alter_move, alien_bullets,
                 explosions):
    if row_number <= 2:
        new_alien = al.Alien3(ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions)
    elif row_number <= 4:
        new_alien = al.Alien2(ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions)
    else:
        new_alien = al.Alien1(ai_settings, screen, stats, sb, alter_move, alien_bullets, explosions)
    new_alien_width = new_alien.rect.width
    new_alien.x = (new_alien_width + 2 * new_alien_width * alien_number)
    new_alien.rect.x = new_alien.x
    new_alien.rect.y = new_alien.rect.height + 2 * new_alien.rect.height * row_number
    aliens.add(new_alien)


def create_bonus(ai_settings, screen, stats, sb, bullets, set_bonus, explosions):
    new_bonus = bon.Bonus(ai_settings, screen, stats, sb, bullets, explosions)
    set_bonus.add(new_bonus)


def create_fleet(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, explosions):
    set_dummy_alter_move = False
    # create a "dummy" alien to get its dimensions
    dummy_alien = al.Alien(ai_settings, screen, stats, sb, set_dummy_alter_move, alien_bullets, explosions)
    number_aliens_x = get_number_aliens_x(ai_settings, dummy_alien.rect.width)  # use those dimensions to find number
    number_rows = get_number_rows(ai_settings, ship.rect.height, dummy_alien.rect.height)
    # now spawn them
    alter_move = 1  # staggers movement
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, stats, sb, aliens, alien_number, row_number, alter_move, alien_bullets,
                         explosions)
            alter_move *= -1


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break  # break so we don't bother examining anymore aliens in the Group


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(stats, ship):
    if stats.ships_left >= 0:
        ship.die = True


def reset(ai_settings, stats, screen, sb, ship, bullets, aliens, alien_bullets, bunkers, bonus, explosions):
    # Respond to ship being hit by alien.
    ship.explode.play()
    for res in aliens:
        res.reset = True  # so they won't die normally, exploding and adding points
    for res_bonus in bonus:
        res_bonus.reset = True
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.music_reset()
        stats.ships_left -= 1

        # update scoreboard
        sb.prep_ships()

        # empty groups
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()
        bunkers.empty()
        bonus.empty()

        # restart fleet and spawn new ship (really just centering old one)
        create_fleet(ai_settings, screen, stats, sb, ship, aliens, alien_bullets, explosions)
        create_bunkers(ai_settings, bunkers)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        ai_settings.gameOver.play()
        stats.game_active = False
        stats.music_stop()
        pygame.mouse.set_visible(True)


def check_aliens_bottom(stats, screen, ship, aliens):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(stats, ship)
            aliens.empty()
            break  # break so we don't bother examining anymore aliens in the Group


def update_aliens(ai_settings, stats, screen, ship, aliens, bonus):
    check_fleet_edges(ai_settings, aliens)  # make sure to see if fleet is on an edge. If so, change their direction.
    aliens.update()
    bonus.update()
    # look for alien ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, ship)
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(stats, screen, ship, aliens)


def check_bullet_bunker_collisions(bullets, aliens):
    pygame.sprite.groupcollide(bullets, aliens, True, True)


def create_bunker_tile(ai_settings, bunker, tile_count, tile_row):
    for tile in range(6):
        new_tile = bu.BunkerTile(ai_settings)
        new_tile_width = new_tile.rect.width
        # new_tile.x = (new_tile_width + 9 * new_tile_width * (tile_count * 2)) + (tile * new_tile_width)
        new_tile.x = (new_tile_width + (6 * new_tile_width * (tile_count * 2))) + (tile * new_tile_width)
        new_tile.rect.x = new_tile.x
        new_tile.rect.y = ai_settings.screen_height - (new_tile.rect.height + 6 * new_tile.rect.height) - \
            (new_tile_width * tile_row)
        bunker.add(new_tile)


def create_bunkers(ai_settings, bunkers):
    dummy_bunker_tile = bu.BunkerTile(ai_settings)
    number_tiles_x = get_number_tiles_x(ai_settings, dummy_bunker_tile.rect.width)
    for tiles_vert in range(5):
        tiles_horiz = 1
        while tiles_horiz != (number_tiles_x + 1):
            create_bunker_tile(ai_settings, bunkers, tiles_horiz, tiles_vert)
            tiles_horiz += 1


def get_number_tiles_x(ai_settings, tile_width):
    available_space_x = ai_settings.screen_width - 2 * tile_width
    number_tiles_x = int(available_space_x / (14 * tile_width))
    return number_tiles_x


def explosion_update(explosion):
    explosion.update()
