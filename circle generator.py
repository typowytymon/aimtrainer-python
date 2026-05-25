import turtle
import random
import math

# ─── Konfiguracja gry ───────────────────────────────────────────────
SZEROKOSC = 800
WYSOKOSC = 600
CZAS_GRY = 30          # sekundy
PROMIEN_CELU = 30
MARGINES = 60

# ─── Stan gry ───────────────────────────────────────────────────────
stan = {
    "punkty": 0,
    "czas": CZAS_GRY,
    "aktywna": False,
    "cel_x": 0,
    "cel_y": 0,
}

# ─── Konfiguracja ekranu ─────────────────────────────────────────────
ekran = turtle.Screen()
ekran.title("🎯 Kliknij cel!")
ekran.bgcolor("#000")
ekran.setup(width=SZEROKOSC, height=WYSOKOSC)
ekran.tracer(0)

# ─── Żółwie (rysowniki) ──────────────────────────────────────────────
pisak_cel = turtle.Turtle()
pisak_cel.hideturtle()
pisak_cel.speed(0)

pisak_ui = turtle.Turtle()
pisak_ui.hideturtle()
pisak_ui.speed(0)

pisak_tlo = turtle.Turtle()
pisak_tlo.hideturtle()
pisak_tlo.speed(0)


# ════════════════════════════════════════════════════════════════════
#  FUNKCJE GRY
# ════════════════════════════════════════════════════════════════════

def stworz_cel():
    """Losuje nową pozycję celu i rysuje kółko na ekranie."""
    stan["cel_x"] = random.randint(-SZEROKOSC // 2 + MARGINES, SZEROKOSC // 2 - MARGINES)
    stan["cel_y"] = random.randint(-WYSOKOSC // 2 + MARGINES, WYSOKOSC // 2 - MARGINES - 60)

    pisak_cel.clear()
    pisak_cel.penup()
    pisak_cel.goto(stan["cel_x"], stan["cel_y"] - PROMIEN_CELU)
    pisak_cel.pendown()

    # Zewnętrzny pierścień (biały)
    pisak_cel.fillcolor("#e94560")
    pisak_cel.pencolor("#ffffff")
    pisak_cel.pensize(3)
    pisak_cel.begin_fill()
    pisak_cel.circle(PROMIEN_CELU)
    pisak_cel.end_fill()

    # Wewnętrzny punkt (biały)
    pisak_cel.penup()
    pisak_cel.goto(stan["cel_x"], stan["cel_y"] - 10)
    pisak_cel.pendown()
    pisak_cel.fillcolor("#ffffff")
    pisak_cel.pencolor("#ffffff")
    pisak_cel.begin_fill()
    pisak_cel.circle(10)
    pisak_cel.end_fill()

    ekran.update()


def sprawdz_klik(x, y):
    """Sprawdza czy gracz kliknął w cel. Jeśli tak – dodaje punkt i przesuwa cel."""
    if not stan["aktywna"]:
        return

    odleglosc = math.sqrt((x - stan["cel_x"]) ** 2 + (y - stan["cel_y"]) ** 2)
    if odleglosc <= PROMIEN_CELU:
        stan["punkty"] += 1
        efekt_trafienia()
        stworz_cel()
        aktualizuj_wynik()


def aktualizuj_wynik():
    """Odświeża pasek UI z punktami i czasem."""
    pisak_ui.clear()
    pisak_ui.penup()

    # Tło paska UI
    pisak_ui.goto(-SZEROKOSC // 2, WYSOKOSC // 2 - 55)
    pisak_ui.pendown()
    pisak_ui.fillcolor("#16213e")
    pisak_ui.pencolor("#16213e")
    pisak_ui.begin_fill()
    for _ in range(2):
        pisak_ui.forward(SZEROKOSC)
        pisak_ui.right(90)
        pisak_ui.forward(55)
        pisak_ui.right(90)
    pisak_ui.end_fill()

    # Punkty
    pisak_ui.penup()
    pisak_ui.goto(-SZEROKOSC // 2 + 30, WYSOKOSC // 2 - 40)
    pisak_ui.pencolor("#e94560")
    pisak_ui.write(f"PUNKTY: {stan['punkty']}", font=("Courier", 18, "bold"))

    # Czas
    pisak_ui.goto(SZEROKOSC // 2 - 200, WYSOKOSC // 2 - 40)
    kolor_czasu = "#e94560" if stan["czas"] <= 5 else "#a8dadc"
    pisak_ui.pencolor(kolor_czasu)
    pisak_ui.write(f"CZAS: {stan['czas']}s", font=("Courier", 18, "bold"))

    ekran.update()


def efekt_trafienia():
    """Krótki efekt wizualny po trafieniu w cel."""
    pisak_tlo.clear()
    pisak_tlo.penup()
    pisak_tlo.goto(stan["cel_x"], stan["cel_y"] - PROMIEN_CELU - 15)
    pisak_tlo.pendown()
    pisak_tlo.pencolor("#f5a623")
    pisak_tlo.pensize(4)
    pisak_tlo.circle(PROMIEN_CELU + 15)
    ekran.update()
    ekran.ontimer(lambda: (pisak_tlo.clear(), ekran.update()), 150)


def odliczanie():
    """Odlicza czas co sekundę. Kończy grę gdy czas = 0."""
    if not stan["aktywna"]:
        return
    if stan["czas"] > 0:
        stan["czas"] -= 1
        aktualizuj_wynik()
        ekran.ontimer(odliczanie, 1000)
    else:
        koniec_gry()


def koniec_gry():
    """Wyświetla ekran końca gry."""
    stan["aktywna"] = False
    pisak_cel.clear()
    pisak_tlo.clear()

    # Przyciemnione tło
    pisak_tlo.penup()
    pisak_tlo.goto(-SZEROKOSC // 2, -WYSOKOSC // 2)
    pisak_tlo.pendown()
    pisak_tlo.fillcolor("#0f0f23")
    pisak_tlo.pencolor("#0f0f23")
    pisak_tlo.begin_fill()
    pisak_tlo.goto(SZEROKOSC // 2, -WYSOKOSC // 2)
    pisak_tlo.goto(SZEROKOSC // 2, WYSOKOSC // 2 - 55)
    pisak_tlo.goto(-SZEROKOSC // 2, WYSOKOSC // 2 - 55)
    pisak_tlo.goto(-SZEROKOSC // 2, -WYSOKOSC // 2)
    pisak_tlo.end_fill()

    # Tekst końca gry
    pisak_tlo.penup()
    pisak_tlo.goto(0, 80)
    pisak_tlo.pencolor("#e94560")
    pisak_tlo.write("KONIEC GRY!", align="center", font=("Courier", 36, "bold"))

    pisak_tlo.goto(0, 10)
    pisak_tlo.pencolor("#ffffff")
    pisak_tlo.write(f"Twój wynik: {stan['punkty']} pkt", align="center", font=("Courier", 24, "bold"))

    ocena = oceń_wynik(stan["punkty"])
    pisak_tlo.goto(0, -40)
    pisak_tlo.pencolor("#f5a623")
    pisak_tlo.write(ocena, align="center", font=("Courier", 16, "normal"))

    # Przycisk restart
    pisak_tlo.goto(0, -110)
    pisak_tlo.pencolor("#a8dadc")
    pisak_tlo.write("[ Kliknij tutaj aby zagrać ponownie ]",
                    align="center", font=("Courier", 14, "normal"))

    ekran.update()


def oceń_wynik(punkty):
    if punkty >= 20:
        return "⭐ Mistrz celności! Niesamowite!"
    elif punkty >= 12:
        return "👍 Bardzo dobry wynik! Tak trzymaj!"
    elif punkty >= 6:
        return "🙂 Nieźle! Poćwicz jeszcze trochę."
    else:
        return "😅 Trudne, prawda? Spróbuj jeszcze raz!"


def restart_gry():
    """Resetuje stan gry i zaczyna od nowa."""
    stan["punkty"] = 0
    stan["czas"] = CZAS_GRY
    stan["aktywna"] = True

    pisak_tlo.clear()
    pisak_cel.clear()
    pisak_ui.clear()

    aktualizuj_wynik()
    stworz_cel()
    odliczanie()


def obsluga_klikniecia(x, y):
    """Globalny handler kliknięcia – restart lub sprawdzenie celu."""
    if not stan["aktywna"]:
        restart_gry()
    else:
        sprawdz_klik(x, y)


# ════════════════════════════════════════════════════════════════════
#  EKRAN STARTOWY
# ════════════════════════════════════════════════════════════════════

def ekran_startowy():
    pisak_tlo.penup()
    pisak_tlo.goto(0, 120)
    pisak_tlo.pencolor("#e94560")
    pisak_tlo.write("🎯 KLIKNIJ CEL!", align="center", font=("Courier", 38, "bold"))

    pisak_tlo.goto(0, 50)
    pisak_tlo.pencolor("#a8dadc")
    pisak_tlo.write("Klikaj czerwone kółka jak najszybciej!", align="center",
                    font=("Courier", 15, "normal"))

    pisak_tlo.goto(0, 10)
    pisak_tlo.pencolor("#ffffff")
    pisak_tlo.write(f"Masz {CZAS_GRY} sekund. Każde trafienie = 1 punkt.",
                    align="center", font=("Courier", 13, "normal"))

    pisak_tlo.goto(0, -60)
    pisak_tlo.pencolor("#f5a623")
    pisak_tlo.write("[ Kliknij aby rozpocząć ]", align="center", font=("Courier", 16, "bold"))

    ekran.update()


# ─── Start ──────────────────────────────────────────────────────────
ekran_startowy()
ekran.onclick(obsluga_klikniecia)
ekran.listen()
turtle.mainloop()
