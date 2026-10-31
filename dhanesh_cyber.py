
import tkinter as tk
import random
import math
import time

# ==================================================
# DHANESH.exe | PREMIUM CYBER ANIMATION
# ==================================================

BG = "#03040b"
NAME = "DHANESH"
FPS = 30

root = tk.Tk()
root.title("DHANESH.exe | Cyber Identity")
root.geometry("1100x700")
root.minsize(600, 400)
root.configure(bg=BG)

cv = tk.Canvas(root, bg=BG, highlightthickness=0)
cv.pack(fill="both", expand=True)

rng = random.Random()
particles = []
rain = []
frame = 0
start_time = time.time()
glitch_until = 0
reveal = 0
last_size = (0, 0)
name_bbox = None


# ---------------- COLORS ----------------

CYAN = "#00eaff"
BLUE = "#0878ff"
PURPLE = "#a855f7"
WHITE = "#eafcff"
DIM = "#123044"


# ---------------- UTILITIES ----------------

def text(x, y, value, size, color, anchor="center"):
    cv.create_text(
        x, y,
        text=value,
        font=("Consolas", size, "bold"),
        fill=color,
        anchor=anchor
    )


def line(x1, y1, x2, y2, color, width=1):
    cv.create_line(
        x1, y1, x2, y2,
        fill=color,
        width=width
    )


def polygon(points, color):
    cv.create_polygon(
        points,
        fill=color,
        outline=""
    )


# ---------------- PARTICLES ----------------

def spawn_particle(x, y, burst=False):
    angle = rng.uniform(0, math.tau)
    speed = rng.uniform(1, 7) if burst else rng.uniform(0.2, 1.2)

    particles.append({
        "x": x,
        "y": y,
        "vx": math.cos(angle) * speed,
        "vy": math.sin(angle) * speed,
        "life": rng.randint(20, 70) if burst else rng.randint(70, 180),
        "max_life": 70 if burst else 180,
        "size": rng.choice([1, 1, 2, 3]),
        "color": rng.choice([CYAN, BLUE, PURPLE, WHITE])
    })


def create_rain(w, h):
    rain.clear()
    for _ in range(max(30, w // 12)):
        rain.append({
            "x": rng.randint(0, w),
            "y": rng.randint(-h, h),
            "speed": rng.uniform(1, 5),
            "length": rng.randint(8, 25),
            "char": rng.choice("01ABCDEF<>/{}"),
        })


def burst():
    global glitch_until

    glitch_until = frame + 35

    if name_bbox:
        x1, y1, x2, y2 = name_bbox
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    else:
        cx, cy = cv.winfo_width() / 2, cv.winfo_height() / 2

    for _ in range(150):
        spawn_particle(cx, cy, True)


# ---------------- BACKGROUND ----------------

def draw_background(w, h):
    cx, cy = w / 2, h / 2

    # Perspective grid floor
    horizon = int(h * 0.65)
    spacing = max(30, w // 25)

    for x in range(-w, w * 2, spacing * 2):
        line(cx, horizon, x, h, "#071629")

    for i in range(1, 15):
        k = (i / 14) ** 2
        y = horizon + (h - horizon) * k
        line(0, y, w, y, "#071629")

    # Background digital rain
    for drop in rain:
        x, y = drop["x"], drop["y"]
        length = drop["length"]

        text(x, y, drop["char"], 9, "#07506a")

        drop["y"] += drop["speed"]

        if drop["y"] > h + 20:
            drop["y"] = rng.randint(-200, -20)
            drop["x"] = rng.randint(0, w)

    # Subtle ambient particles
    if len(particles) < 100:
        for _ in range(2):
            spawn_particle(
                rng.uniform(0, w),
                rng.uniform(0, h)
            )


# ---------------- HUD ----------------

def draw_hud(w, h, tick):
    cx, cy = w / 2, h / 2

    # Rotating circles
    for radius, color, width, speed in [
        (min(w, h) * 0.29, "#0b3850", 1, 0.4),
        (min(w, h) * 0.34, "#10203e", 1, -0.25),
        (min(w, h) * 0.39, "#092333", 1, 0.15),
    ]:
        angle = tick * speed

        cv.create_arc(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            start=angle,
            extent=270,
            style="arc",
            outline=color,
            width=width
        )

    # HUD corner marks
    margin = 35
    size = 28

    for x, y, dx, dy in [
        (margin, margin, 1, 1),
        (w - margin, margin, -1, 1),
        (margin, h - margin, 1, -1),
        (w - margin, h - margin, -1, -1)
    ]:
        line(x, y, x + dx * size, y, CYAN)
        line(x, y, x, y + dy * size, CYAN)

    text(55, 70, "SYSTEM ONLINE", 10, CYAN, "w")
    text(55, 88, "IDENTITY: DHANESH", 9, "#467b91", "w")

    text(w - 55, 70, "CYBER / 01", 10, CYAN, "e")
    text(w - 55, 88, "SECURE CONNECTION", 9, "#467b91", "e")

    text(55, h - 55, "NEURAL INTERFACE", 9, "#467b91", "w")
    text(w - 55, h - 55, "v1.0.26", 9, "#467b91", "e")


# ---------------- NAME REVEAL ----------------

def draw_name(w, h, tick):
    global name_bbox

    cx, cy = w / 2, h / 2
    size = max(28, int(min(w * 0.105, h * 0.19)))

    # Reveal one character at a time
    count = min(len(NAME), int(reveal))
    shown = NAME[:count]

    # Small glitch offset
    jitter = 0
    if tick < glitch_until and rng.random() < 0.35:
        jitter = rng.randint(-8, 8)

    # Neon glow layers
    text(cx + jitter, cy, shown, size + 3, "#063b58")
    text(cx + jitter, cy, shown, size + 1, "#0878a8")
    text(cx, cy, shown, size, WHITE)

    # Cyan / violet offset highlights
    text(cx - 2, cy, shown, size, CYAN)
    text(cx + 2, cy, shown, size, PURPLE)

    # Keep white core on top
    text(cx, cy, shown, size, WHITE)

    name_bbox = (
        cx - size * len(NAME) * 0.35,
        cy - size,
        cx + size * len(NAME) * 0.35,
        cy + size
    )

    # Subtitle
    if count == len(NAME):
        text(cx, cy + size * 0.9, "FULL STACK DEVELOPER  //  CREATIVE MIND",
             max(9, size // 10), CYAN)

        # Decorative underline
        width = min(w * 0.45, size * 6)
        line(cx - width / 2, cy + size * 1.3,
             cx + width / 2, cy + size * 1.3, "#0b5970", 2)


# ---------------- SCANLINE ----------------

def draw_scanline(w, h, tick):
    y = (tick * 4) % h
    line(0, y, w, y, "#08202b")


# ---------------- GLITCH ----------------

def draw_glitch(w, h):
    if frame >= glitch_until:
        return

    for _ in range(5):
        x = rng.randint(0, w)
        y = rng.randint(0, h)
        width = rng.randint(30, 180)

        color = rng.choice([CYAN, PURPLE, WHITE])

        line(x, y, min(w, x + width), y, color, rng.randint(1, 3))


# ---------------- PARTICLE UPDATE ----------------

def update_particles():
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 1

        if p["life"] <= 0:
            particles.remove(p)
            continue

        size = p["size"]
        cv.create_oval(
            p["x"], p["y"],
            p["x"] + size, p["y"] + size,
            fill=p["color"],
            outline=""
        )


# ---------------- MAIN LOOP ----------------

def animate():
    global frame, reveal, last_size

    w = cv.winfo_width()
    h = cv.winfo_height()

    if w < 2 or h < 2:
        root.after(30, animate)
        return

    if (w, h) != last_size:
        last_size = (w, h)
        create_rain(w, h)

    cv.delete("all")

    elapsed = time.time() - start_time

    # Smooth letter reveal
    reveal = min(len(NAME), elapsed * 2.0)

    draw_background(w, h)
    draw_hud(w, h, frame)
    draw_name(w, h, frame)
    draw_scanline(w, h, frame)
    draw_glitch(w, h)
    update_particles()

    frame += 1
    root.after(int(1000 / FPS), animate)


# ---------------- INTERACTION ----------------

cv.bind("<Button-1>", lambda event: burst())
root.bind("<space>", lambda event: burst())

# Start
create_rain(1100, 700)
animate()

root.mainloop()
