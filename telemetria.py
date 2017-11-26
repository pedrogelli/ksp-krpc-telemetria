import time
import krpc

# VARIÁVEIS 
conn = krpc.connect(name='Sub-orbital flight')
canvas = conn.ui.stock_canvas
vessel = conn.space_center.active_vessel
orbit = vessel.orbit
flight = vessel.flight()
obt_frame = vessel.orbit.body.non_rotating_reference_frame
srf_frame = vessel.orbit.body.reference_frame
cena = conn.krpc.current_game_scene
estagio = "Manual"
# TAMANHO DA TELA EM PX'S
screen_size = canvas.rect_transform.size

# SITUAÇÃO DA NAVE
t_nave_etapa = canvas.add_text("Etapa:")
t_nave_etapa.aligment = t_nave_etapa.alignment.upper_center
t_nave_etapa.style = t_nave_etapa.style.bold
t_nave_etapa.rect_transform.position = (screen_size[0]/2 - 150, screen_size[1]/2 - 30)
t_nave_etapa.rect_transform.size = 250, 30
t_nave_etapa.color = (1, 1, 0)
t_nave_etapa.size = 16

# ADICIONA O PAINEL
panel = canvas.add_panel()

# POSICIONA O PAINEL
rect = panel.rect_transform
rect.size = (200, 500)
rect.position = (-screen_size[0]/2 + 250, 40)

# TÍTULO DA JANELA
t_titulo = panel.add_text("TELEMETRIA")
t_titulo.aligment = t_titulo.alignment.upper_center
t_titulo.style = t_titulo.style.bold
t_titulo.rect_transform.position = (0, rect.upper_right[1] - 70)
t_titulo.color = (1, 1, 0)
t_titulo.size = 16

# TEXTO IMPULSO
t_impulso = panel.add_text("Impulso:")
t_impulso.rect_transform.position = (0, rect.upper_right[1] - 100)
t_impulso.color = (1, 1, 1)
t_impulso.size = 15

# TEXTO APOAPSIS
t_apoapsis = panel.add_text("Apoapsis:")
t_apoapsis.rect_transform.position = (0, rect.upper_right[1] - 130)
t_apoapsis.color = (1, 1, 1)
t_apoapsis.size = 15

# TEXTO APOAPSIS -T
t_apoapsis_tempo = panel.add_text("-T: ")
t_apoapsis_tempo.rect_transform.position = (0, rect.upper_right[1] - 150)
t_apoapsis_tempo.color = (1, 1, 1)
t_apoapsis_tempo.size = 15

# TEXTO PERIAPSIS
t_periapsis = panel.add_text("Periapsis:")
t_periapsis.rect_transform.position = (0, rect.upper_right[1] - 180)
t_periapsis.color = (1, 1, 1)
t_periapsis.size = 15

# TEXTO PERIAPSIS -T
t_periapsis_tempo = panel.add_text("-T: ")
t_periapsis_tempo.rect_transform.position = (0, rect.upper_right[1] - 200)
t_periapsis_tempo.color = (1, 1, 1)
t_periapsis_tempo.size = 15

# TEXTO ALTITUDE
t_alt = panel.add_text("Altitude:")
t_alt.rect_transform.position = (0, rect.upper_right[1] - 230)
t_alt.color = (1, 1, 1)
t_alt.size = 15

# TEXTO VELOCIDADE
t_vel = panel.add_text("VELOCIDADE")
t_vel.rect_transform.position = (0, rect.upper_right[1] - 260)
t_vel.style = t_vel.style.bold
t_vel.color = (1, 1, 0)
t_vel.size = 15

# TEXTO VELOCIDADE ORBITAL
t_vel_orb = panel.add_text("Orbita:")
t_vel_orb.rect_transform.position = (0, rect.upper_right[1] - 290)
t_vel_orb.color = (1, 1, 1)
t_vel_orb.size = 15

# TEXTO VELOCIDADE DA SUPERFCÍE
t_vel_super = panel.add_text("Superfície:")
t_vel_super.rect_transform.position = (0, rect.upper_right[1] - 320)
t_vel_super.color = (1, 1, 1)
t_vel_super.size = 15

# CONTROLE DA NAVE
# TÍTULO MOTOR
t_ctrl_nave = panel.add_text("MOTOR")
t_ctrl_nave.rect_transform.position = (20, rect.upper_right[1] - 360)
t_ctrl_nave.rect_transform.size = (200, 50)
t_ctrl_nave.style = t_titulo.style.bold
t_ctrl_nave.color = (1, 1, 0)
t_ctrl_nave.size = 15

# BOTÃO FORÇA TOTAL
b_impulso = panel.add_button("FORÇA TOTAL")
b_impulso.rect_transform.position = (0, rect.upper_right[1] - 380)

# TÍTULO ESTÁGIO
t_estagio_nave = panel.add_text("ESTÁGIO:")
t_estagio_nave.rect_transform.position = (20, rect.upper_right[1] - 440)
t_estagio_nave.rect_transform.size = (200, 50)
t_estagio_nave.style = t_titulo.style.bold
t_estagio_nave.color = (1, 1, 0)
t_estagio_nave.size = 15

# BOTÃO ESTÁGIO AUTOMÁTICO
b_est_auto = panel.add_button("AUTOMÁTICO")
b_est_auto.rect_transform.position = (0, rect.upper_right[1] - 460)

# BOTÃO ESTÁGIO MANUAL
b_est_manual = panel.add_button("MANUAL")
b_est_manual.rect_transform.position = (0, rect.upper_right[1] - 490)

# MONITORA OS BOTÕES COM STREAM
b_impulso_clicked = conn.add_stream(getattr, b_impulso, 'clicked')
b_est_auto_clicked = conn.add_stream(getattr, b_est_auto, 'clicked')
b_est_manual_clicked = conn.add_stream(getattr, b_est_manual, 'clicked')

# USER EXPERIENCE
if cena == conn.krpc.GameScene.space_center:
    print("Visão Geral")
elif cena == conn.krpc.GameScene.flight:
    print("Vamos voar!")
elif cena == conn.krpc.GameScene.tracking_station:
    print("Bugado! ='(")
elif cena == conn.krpc.GameScene.editor_vab:
    print("Rocket Science!")
elif cena == conn.krpc.GameScene.editor_sph:
    print("Vamos Voar Baixo!?")

print(vessel.control.current_stage)
print(vessel.resources.amount, 'SolidFuel')

while True:
    # Handle the throttle button being clicked
    if b_impulso_clicked():
        vessel.control.throttle = 1
        b_impulso.clicked = False
        
    elif b_est_auto_clicked():
        print("Sequência Automática de estágios ativada")
        estagio = "Automático"
        vessel.control.activate_next_stage()
        b_est_auto.clicked = False
        
    elif b_est_manual_clicked():
        print("Sequência Manual de estágios ativada")
        estagio = "Manual"
        b_est_manual.clicked = False


        
    # ATUALIZA TEXTOS
    if vessel.situation == vessel.situation.pre_launch:
        t_nave_etapa.content = 'Etapa: Pré Lançamento'
    elif vessel.situation == vessel.situation.flying:
        t_nave_etapa.content = 'Etapa: Voando'
    elif vessel.situation == vessel.situation.sub_orbital:
        t_nave_etapa.content = 'Etapa: Sub Orbita'
    elif vessel.situation == vessel.situation.orbiting:
        t_nave_etapa.content = 'Etapa: Orbitando'
    elif vessel.situation == vessel.situation.escaping:
        t_nave_etapa.content = 'Etapa: Escapando'
    elif vessel.situation == vessel.situation.landed:
        t_nave_etapa.content = 'Etapa: Pousado'
    elif vessel.situation == vessel.situation.docked:
        t_nave_etapa.content = 'Etapa: Acoplado'
    elif vessel.situation == vessel.situation.splashed:
        t_nave_etapa.content = 'Etapa: Destruido'
        
    t_impulso.content = 'Impulso: %d kN' % (vessel.thrust/1000)
    t_apoapsis.content = 'Apoapsis: %d m' % (orbit.apoapsis - 600072)
    t_apoapsis_tempo.content = '-T: %d s' % (orbit.time_to_apoapsis)
    t_periapsis.content = 'Periapsis: %d m' % (orbit.periapsis - 1564)
    t_periapsis_tempo.content = '-T: %d s' % (orbit.time_to_periapsis)
    t_alt.content = 'Altitude: %d m' % (flight.mean_altitude)
        # VELOCIDADES
    obt_speed = vessel.flight(obt_frame).speed
    srf_speed = vessel.flight(srf_frame).speed
    t_vel_orb.content = 'Orbita: %.1f m/s' % (obt_speed)
    t_vel_super.content = 'Superficie: %.1f m/s' % (srf_speed)
    t_estagio_nave.content = 'ESTÁGIO: ' + (estagio)

    # DELAY DO WHILE TRUE?
    time.sleep(0.1)
