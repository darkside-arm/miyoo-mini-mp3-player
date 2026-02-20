#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../site-packages"))
import io
import time
import pygame
import config



try:
    from src.profile import PROFILES, ACTIVE_PROFILE
except ImportError:
    from profile import PROFILES, ACTIVE_PROFILE

profile_config = PROFILES[ACTIVE_PROFILE]

from player import MusicPlayer
from draw_button import draw_button
from input_handler import InputHandler
from playlist import PlaylistScreen


def load_image(path):
    """Carga una imagen y la devuelve como Surface de pygame."""
    print("Cargando imagen: %s" % path)
    if not os.path.exists(path):
        print("Error: Archivo no encontrado %s" % path)
        return None
    try:
        surface = pygame.image.load(path)
        return surface.convert()
    except pygame.error as e:
        print("Error cargando imagen %s: %s" % (path, e))
        return None


def render_text(screen, font, text, color, x, y, centered=False):
    """Renderiza texto en la pantalla con pygame.font."""
    if not font or not text:
        return
    surface = font.render(text, True, color)
    w, h = surface.get_size()
    if centered:
        x = x - w // 2
    screen.blit(surface, (x, y))


def main():
    # Inicializar pygame via config
    screen = config.init_pygame()
    if not screen:
        print("Fallo critico inicializando pygame. Saliendo.")
        return

    clock = pygame.time.Clock()

    # Inicializar joysticks
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    print("Joysticks detectados: %d" % joystick_count)
    for i in range(joystick_count):
        joy = pygame.joystick.Joystick(i)
        joy.init()
        print("  Joystick %d: %s (botones: %d, ejes: %d, hats: %d)" % (
            i, joy.get_name(), joy.get_numbuttons(), joy.get_numaxes(), joy.get_numhats()))

    player = MusicPlayer()
    input_handler = InputHandler(player)
    playlist_screen = PlaylistScreen(screen, player)

    current_view = "player"

    # Cargar lista de archivos automaticamente
    player.update_browser_items()

    # Cargar assets (imagenes)
    bg_path = os.path.join(config.ASSETS_DIR, 'bk1.jpg')
    cover_path = os.path.join(config.ASSETS_DIR, 'sl1.jpg')
    path_b = os.path.join(config.ASSETS_DIR, 'b.jpg')
    path_p = os.path.join(config.ASSETS_DIR, 'p.jpg')
    path_pause = os.path.join(config.ASSETS_DIR, 'pause.jpg')
    path_f = os.path.join(config.ASSETS_DIR, 'f.jpg')

    background_img = load_image(bg_path)
    album_cover_img = load_image(cover_path)
    btn_prev_img = load_image(path_b)
    btn_play_img = load_image(path_p)
    btn_pause_img = load_image(path_pause)
    btn_next_img = load_image(path_f)

    # Escalar fondo al tamano de ventana
    if background_img:
        background_img = pygame.transform.scale(background_img, (config.WIDTH, config.HEIGHT))

    # Definir areas de botones
    center_x = config.WIDTH // 2
    y_pos = 437
    spacing = 100
    btn_w, btn_h = config.BUTTON_SIZE

    rect_prev = pygame.Rect(center_x - spacing - btn_w // 2, y_pos - btn_h // 2, btn_w, btn_h)
    rect_play = pygame.Rect(center_x - btn_w // 2, y_pos - btn_h // 2, btn_w, btn_h)
    rect_next = pygame.Rect(center_x + spacing - btn_w // 2, y_pos - btn_h // 2, btn_w, btn_h)

    # Escalar imagenes de botones
    if btn_prev_img:
        btn_prev_img = pygame.transform.scale(btn_prev_img, (btn_w, btn_h))
    if btn_play_img:
        btn_play_img = pygame.transform.scale(btn_play_img, (btn_w, btn_h))
    if btn_pause_img:
        btn_pause_img = pygame.transform.scale(btn_pause_img, (btn_w, btn_h))
    if btn_next_img:
        btn_next_img = pygame.transform.scale(btn_next_img, (btn_w, btn_h))

    running = True

    # Variables para marquee
    marquee_offset = 0
    marquee_direction = 1
    marquee_wait = 0
    last_track_name = ""

    # Portada
    default_cover_img = album_cover_img
    current_cover_img = default_cover_img

    # Variables para animacion de botones
    btn_highlight_time = 0
    btn_highlight_target = None
    manual_transition = False

    # --- Control de inactividad y pantalla ---
    inactivity_black_timeout = 35   # segundos para poner pantalla negra
    inactivity_poweroff_timeout = 40  # segundos para intentar apagar pantalla
    last_input_time = time.time()
    screen_blacked = False
    screen_powered_off = False

    def apagar_pantalla():
        try:
            os.system('echo 1 > /sys/class/graphics/fb0/blank')
        except Exception:
            pass

    def encender_pantalla():
        try:
            os.system('echo 0 > /sys/class/graphics/fb0/blank')
        except Exception:
            pass

    while running:
        # Procesar eventos
        for event in pygame.event.get():
            # Detectar cualquier input para resetear inactividad
            if event.type in (pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION, pygame.JOYAXISMOTION, pygame.KEYDOWN, pygame.KEYUP):
                last_input_time = time.time()
                if screen_blacked or screen_powered_off:
                    encender_pantalla()
                    screen_blacked = False
                    screen_powered_off = False

            if event.type == pygame.QUIT:
                running = False
                break

            # Debug: imprimir eventos de joystick
            if event.type == pygame.JOYBUTTONDOWN:
                print("[JOY] Boton presionado: %d" % event.button)
            elif event.type == pygame.JOYBUTTONUP:
                print("[JOY] Boton soltado: %d" % event.button)
            elif event.type == pygame.JOYHATMOTION:
                print("[JOY] Hat movido: %s" % str(event.value))
            elif event.type == pygame.JOYAXISMOTION:
                if abs(event.value) > 0.5:
                    print("[JOY] Eje %d: %.2f" % (event.axis, event.value))

            action = input_handler.handle_input(event)
            if action == "QUIT":
                running = False
                break
            elif action == "TOGGLE_PLAYLIST":
                if current_view == "player":
                    current_view = "playlist"
                    input_handler.set_mode("playlist")
                else:
                    current_view = "player"
                    input_handler.set_mode("player")
            elif action == "NAV_UP":
                if current_view == "playlist":
                    playlist_screen.move_up()
            elif action == "NAV_DOWN":
                if current_view == "playlist":
                    playlist_screen.move_down()
            elif action == "PLAY_DIR":
                if current_view == "playlist":
                    files = [item['path'] for item in player.browser_items if item['type'] == 'file']
                    if files:
                        player.stop_music()
                        player.playlist = files
                        player.current_track_index = 0
                        player.play_music()
                        current_view = "player"
                        input_handler.set_mode("player")
            elif action == "SELECT_ITEM":
                if current_view == "playlist":
                    item = playlist_screen.get_selected_item()
                    if item:
                        if item['type'] == 'dir':
                            player.current_path = item['path']
                            player.update_browser_items()
                            playlist_screen.selected_index = 0
                        elif item['type'] == 'file':
                            files = [i['path'] for i in player.browser_items if i['type'] == 'file']
                            target_path = item['path']
                            start_index = 0
                            if target_path in files:
                                start_index = files.index(target_path)
                            player.stop_music()
                            player.playlist = files
                            player.current_track_index = start_index
                            player.play_music()
                            current_view = "player"
                            input_handler.set_mode("player")
            elif action == "NAV_RIGHT":
                if current_view == "playlist":
                    playlist_screen.move_down()

            if action == "NEXT_TRACK":
                btn_highlight_target = "next"
                btn_highlight_time = 1
                manual_transition = True
            elif action == "PREV_TRACK":
                btn_highlight_target = "prev"
                btn_highlight_time = 1
                manual_transition = True

            # Clics del mouse para botones (solo en vista player)
            if current_view == "player" and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    if rect_play.collidepoint(mx, my):
                        player.toggle_play_pause()
                    if rect_prev.collidepoint(mx, my):
                        player.prev_track()
                        btn_highlight_target = "prev"
                        btn_highlight_time = 1
                        manual_transition = True
                    if rect_next.collidepoint(mx, my):
                        player.next_track()
                        btn_highlight_target = "next"
                        btn_highlight_time = 1
                        manual_transition = True

        # --- Logica de inactividad: pantalla negra y apagado ---
        tiempo_inactivo = time.time() - last_input_time
        if not screen_blacked and tiempo_inactivo > inactivity_black_timeout:
            screen.fill((0, 0, 0))
            pygame.display.flip()
            screen_blacked = True
        if screen_blacked and not screen_powered_off and tiempo_inactivo > inactivity_poweroff_timeout:
            apagar_pantalla()
            screen_powered_off = True

        # Actualizar estado del player (auto-avance al terminar cancion)
        if player.is_playing and not player.is_paused:
            try:
                if not player.mpg_player.get_busy():
                    if player.repeat_mode == 2:
                        player.play_music()
                    elif player.repeat_mode == 1:
                        player.next_track()
                    else:
                        if player.current_track_index < len(player.playlist) - 1:
                            player.next_track()
                        else:
                            player.stop_music()
            except Exception:
                pass

        # Si la pantalla esta apagada, no renderizar, solo seguir el loop
        if screen_blacked:
            clock.tick(30)
            continue

        # Renderizado
        screen.fill((0, 0, 0))

        if current_view == "player":
            # Fondo
            if background_img:
                screen.blit(background_img, (0, 0))
            else:
                screen.fill((30, 30, 30))

            # Info de la cancion
            track_name = player.get_current_track_name() or "No hay musica seleccionada"

            # Actualizar portada y marquee si cambia la cancion
            if track_name != last_track_name:
                if not manual_transition:
                    btn_highlight_target = "next"
                    btn_highlight_time = 1
                manual_transition = False
                last_track_name = track_name
                marquee_offset = 0
                marquee_direction = 1
                marquee_wait = 60

                # Intentar cargar portada del MP3
                cover_data = player.get_current_track_cover()
                if cover_data and len(cover_data) > 0:
                    try:
                        cover_file = io.BytesIO(cover_data)
                        loaded_img = pygame.image.load(cover_file)
                        if loaded_img:
                            current_cover_img = loaded_img.convert()
                        else:
                            current_cover_img = default_cover_img
                    except Exception as e:
                        print("Error cargando portada: %s" % e)
                        current_cover_img = default_cover_img
                else:
                    current_cover_img = default_cover_img

            # Portada del album
            cover_x = config.WIDTH // 2 - 150
            cover_y = 10
            cover_w, cover_h = 300, 300

            if current_cover_img:
                # Marco
                border_width = 10
                border_rect = pygame.Rect(
                    cover_x - border_width,
                    cover_y - border_width,
                    cover_w + border_width * 2,
                    cover_h + border_width * 2
                )
                pygame.draw.rect(screen, (23, 3, 29), border_rect)

                scaled_cover = pygame.transform.scale(current_cover_img, (cover_w, cover_h))
                screen.blit(scaled_cover, (cover_x, cover_y))
            else:
                pygame.draw.rect(screen, (100, 100, 100), (cover_x, cover_y, cover_w, cover_h))

            # Texto de la cancion con marquee
            max_width = int(config.WIDTH * 0.8)
            text_x = config.WIDTH // 2
            text_y = 330

            if config.FONT_MEDIUM:
                text_w, text_h = config.FONT_MEDIUM.size(track_name)

                if text_w > max_width:
                    overflow = text_w - max_width
                    if marquee_wait > 0:
                        marquee_wait -= 1
                    else:
                        marquee_offset += marquee_direction
                        if marquee_offset >= overflow:
                            marquee_offset = overflow
                            marquee_direction = -1
                            marquee_wait = 60
                        elif marquee_offset <= 0:
                            marquee_offset = 0
                            marquee_direction = 1
                            marquee_wait = 60

                    start_visible = (config.WIDTH - max_width) // 2
                    draw_x = start_visible - marquee_offset

                    # Clip para marquee
                    clip_rect = pygame.Rect(start_visible, text_y, max_width, text_h)
                    screen.set_clip(clip_rect)
                    render_text(screen, config.FONT_MEDIUM, track_name, config.WHITE, draw_x, text_y)
                    screen.set_clip(None)
                else:
                    marquee_offset = 0
                    render_text(screen, config.FONT_MEDIUM, track_name, config.WHITE, text_x, text_y, centered=True)

            # Estado y volumen
            status_text = player.get_status_text()
            volume_text = "Volumen: %d%%" % int(player.get_volume() * 100)

            render_text(screen, config.FONT_SMALL, status_text, config.GRAY, config.WIDTH // 2, 364, centered=True)
            #render_text(screen, config.FONT_SMALL, volume_text, config.GRAY, config.WIDTH // 2, 400, centered=True)

            # Botones con highlight
            if btn_highlight_target == "prev":
                highlight = rect_prev.inflate(12, 12)
                pygame.draw.rect(screen, (248, 187, 68), highlight)

            draw_button(screen, rect_prev, btn_prev_img)

            current_play_img = btn_play_img
            if player.is_playing:
                current_play_img = btn_pause_img
            draw_button(screen, rect_play, current_play_img)

            if btn_highlight_target == "next":
                highlight = rect_next.inflate(12, 12)
                pygame.draw.rect(screen, (248, 187, 68), highlight)

            draw_button(screen, rect_next, btn_next_img)

        elif current_view == "playlist":
            playlist_screen.render()

        pygame.display.flip()

        # Decrementar highlight
        if btn_highlight_time > 0:
            btn_highlight_time -= 1
        else:
            btn_highlight_target = None

        # Limitar a 30 FPS por que el audio se desincroniza si el loop corre demasiado rapido (SDL_mixer no maneja bien el buffer en ese caso)
        clock.tick(30)

    # Limpieza
    player.stop_music()
    input_handler.cleanup()
    playlist_screen.cleanup()
    pygame.quit()


if __name__ == "__main__":
    main()
