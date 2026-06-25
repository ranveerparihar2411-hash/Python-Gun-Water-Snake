import tkinter as tk
from tkinter import font
import random
import time

# ── Game Logic (your original backend) ──────────────────────────────────────
CHOICES = {
    "g": {"label": "🔫 Gun",   "value":  0},
    "w": {"label": "💧 Water", "value": -1},
    "s": {"label": "🐍 Snake", "value":  1},
}
REVERSE = {0: "Gun", -1: "Water", 1: "Snake"}
EMOJIS  = {0: "🔫",  -1: "💧",     1: "🐍"}

def get_result(you, computer):
    if computer == you:
        return "draw"
    wins = [(-1, 1), (1, 0), (0, -1)]   # (computer, you) → you win
    if (computer, you) in wins:
        return "win"
    return "lose"

# ── Color Palette ─────────────────────────────────────────────────────────────
BG        = "#0D1117"   # deep night
PANEL     = "#161B22"   # card bg
ACCENT    = "#58A6FF"   # electric blue
WIN_CLR   = "#3FB950"   # green
LOSE_CLR  = "#F85149"   # red
DRAW_CLR  = "#D29922"   # amber
TEXT      = "#E6EDF3"
SUBTEXT   = "#8B949E"
BTN_HOVER = "#1F6FEB"

# ── Main App ──────────────────────────────────────────────────────────────────
class GunWaterSnakeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gun · Water · Snake")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.geometry("520x680")

        self.score = {"wins": 0, "losses": 0, "draws": 0}
        self.round  = 0
        self._build_ui()

    # ── UI Construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        # Title bar
        title_frame = tk.Frame(self, bg=BG, pady=20)
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="GUN · WATER · SNAKE",
                 font=("Courier", 18, "bold"), fg=ACCENT, bg=BG).pack()
        tk.Label(title_frame, text="Choose your move",
                 font=("Courier", 10), fg=SUBTEXT, bg=BG).pack()

        # Score board
        self._score_frame = tk.Frame(self, bg=PANEL, bd=0, padx=20, pady=12)
        self._score_frame.pack(fill="x", padx=30, pady=(0, 10))
        self._build_scoreboard()

        # Battle arena
        arena = tk.Frame(self, bg=PANEL, padx=20, pady=20)
        arena.pack(fill="x", padx=30, pady=6)

        row = tk.Frame(arena, bg=PANEL)
        row.pack()

        # You column
        you_col = tk.Frame(row, bg=PANEL, width=160)
        you_col.pack(side="left", padx=10)
        tk.Label(you_col, text="YOU", font=("Courier", 10, "bold"),
                 fg=SUBTEXT, bg=PANEL).pack()
        self.you_emoji = tk.Label(you_col, text="❓",
                                  font=("Courier", 56), fg=TEXT, bg=PANEL)
        self.you_emoji.pack()
        self.you_label = tk.Label(you_col, text="—",
                                  font=("Courier", 11), fg=TEXT, bg=PANEL)
        self.you_label.pack()

        # VS
        tk.Label(row, text="VS", font=("Courier", 16, "bold"),
                 fg=SUBTEXT, bg=PANEL, width=4).pack(side="left")

        # Computer column
        cpu_col = tk.Frame(row, bg=PANEL, width=160)
        cpu_col.pack(side="left", padx=10)
        tk.Label(cpu_col, text="COMPUTER", font=("Courier", 10, "bold"),
                 fg=SUBTEXT, bg=PANEL).pack()
        self.cpu_emoji = tk.Label(cpu_col, text="❓",
                                  font=("Courier", 56), fg=TEXT, bg=PANEL)
        self.cpu_emoji.pack()
        self.cpu_label = tk.Label(cpu_col, text="—",
                                  font=("Courier", 11), fg=TEXT, bg=PANEL)
        self.cpu_label.pack()

        # Result banner
        self.result_var = tk.StringVar(value="")
        self.result_label = tk.Label(self, textvariable=self.result_var,
                                     font=("Courier", 20, "bold"),
                                     fg=TEXT, bg=BG, pady=8)
        self.result_label.pack()

        # Choice buttons
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=10)
        self.buttons = {}
        for key, info in CHOICES.items():
            b = tk.Button(btn_frame, text=info["label"],
                          font=("Courier", 13, "bold"),
                          fg=TEXT, bg=PANEL,
                          activebackground=BTN_HOVER, activeforeground=TEXT,
                          relief="flat", bd=0, padx=18, pady=12, cursor="hand2",
                          command=lambda k=key: self.play(k))
            b.pack(side="left", padx=8)
            self._bind_hover(b)
            self.buttons[key] = b

        # Reset button
        tk.Button(self, text="↺  Reset Score",
                  font=("Courier", 9), fg=SUBTEXT, bg=BG,
                  activebackground=BG, activeforeground=ACCENT,
                  relief="flat", bd=0, cursor="hand2",
                  command=self.reset_score).pack(pady=(6, 0))

        # Rules
        rules = tk.Frame(self, bg=PANEL, padx=16, pady=10)
        rules.pack(fill="x", padx=30, pady=(14, 20))
        tk.Label(rules, text="RULES", font=("Courier", 9, "bold"),
                 fg=ACCENT, bg=PANEL).pack(anchor="w")
        for line in ["🔫 Gun  beats  🐍 Snake",
                     "🐍 Snake beats  💧 Water",
                     "💧 Water beats  🔫 Gun"]:
            tk.Label(rules, text=line, font=("Courier", 9),
                     fg=SUBTEXT, bg=PANEL).pack(anchor="w")

    def _build_scoreboard(self):
        for w in self._score_frame.winfo_children():
            w.destroy()
        cols = [("WINS",   str(self.score["wins"]),   WIN_CLR),
                ("DRAWS",  str(self.score["draws"]),   DRAW_CLR),
                ("LOSSES", str(self.score["losses"]), LOSE_CLR)]
        for title, val, color in cols:
            col = tk.Frame(self._score_frame, bg=PANEL)
            col.pack(side="left", expand=True)
            tk.Label(col, text=val, font=("Courier", 24, "bold"),
                     fg=color, bg=PANEL).pack()
            tk.Label(col, text=title, font=("Courier", 8),
                     fg=SUBTEXT, bg=PANEL).pack()

    def _bind_hover(self, btn):
        btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=PANEL))

    # ── Game Logic ────────────────────────────────────────────────────────────
    def play(self, key):
        # Disable buttons during animation
        for b in self.buttons.values():
            b.config(state="disabled")

        you_val  = CHOICES[key]["value"]
        cpu_val  = random.choice([-1, 0, 1])
        result   = get_result(you_val, cpu_val)
        self.round += 1

        # Animate computer "thinking"
        self._animate_cpu(cpu_val, you_val, result, steps=8)

    def _animate_cpu(self, cpu_val, you_val, result, steps):
        choices_cycle = list(EMOJIS.values())
        def tick(n):
            if n > 0:
                fake = random.choice(choices_cycle)
                self.cpu_emoji.config(text=fake)
                self.after(80, lambda: tick(n - 1))
            else:
                self._show_result(you_val, cpu_val, result)
        tick(steps)

    def _show_result(self, you_val, cpu_val, result):
        # Update emoji displays
        self.you_emoji.config(text=EMOJIS[you_val])
        self.you_label.config(text=REVERSE[you_val])
        self.cpu_emoji.config(text=EMOJIS[cpu_val])
        self.cpu_label.config(text=REVERSE[cpu_val])

        # Result banner
        if result == "win":
            msg, color = "🎉  YOU WIN!", WIN_CLR
            self.score["wins"] += 1
        elif result == "lose":
            msg, color = "💀  YOU LOSE!", LOSE_CLR
            self.score["losses"] += 1
        else:
            msg, color = "🤝  IT'S A DRAW", DRAW_CLR
            self.score["draws"] += 1

        self.result_var.set(msg)
        self.result_label.config(fg=color)
        self._build_scoreboard()

        # Re-enable buttons
        for b in self.buttons.values():
            b.config(state="normal")

    def reset_score(self):
        self.score = {"wins": 0, "losses": 0, "draws": 0}
        self.round  = 0
        self.result_var.set("")
        self.result_label.config(fg=TEXT)
        self.you_emoji.config(text="❓")
        self.you_label.config(text="—")
        self.cpu_emoji.config(text="❓")
        self.cpu_label.config(text="—")
        self._build_scoreboard()


if __name__ == "__main__":
    app = GunWaterSnakeApp()
    app.mainloop()
