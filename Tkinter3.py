import tkinter as tk

netflix = {"mobile": 250, "basic": 350, "premium": 800, "advance": 1100}

BG = "#141414"
CARD = "#1f1f1f"
CARD_HOVER = "#2a2a2a"
BORDER = "#333333"
ACCENT = "#E50914"
ACCENT_DARK = "#b20710"
TEXT = "#ffffff"
MUTED = "#a3a3a3"
OK = "#46d369"
ERR = "#ff6b6b"
FONT = "Segoe UI"


def make_button(parent, text, command, primary=True):
    bg = ACCENT if primary else CARD
    hover = ACCENT_DARK if primary else CARD_HOVER
    btn = tk.Button(parent, text=text, command=command, bg=bg, fg=TEXT,
                    activebackground=hover, activeforeground=TEXT,
                    relief="flat", bd=0, cursor="hand2",
                    font=(FONT, 13, "bold"))
    btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
    btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
    return btn


class NetflixApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Netflix Payment")
        self.geometry("460x640")
        self.minsize(460, 640)
        self.resizable(True, True)
        self.configure(bg=BG)
        self.is_fullscreen = False

        self.main = tk.Frame(self, bg=BG, width=460, height=640)
        self.main.pack_propagate(False)
        self.main.place(relx=0.5, rely=0.5, anchor="center")

        self.fs_btn = tk.Button(self, text="Full screen", command=self.toggle_fullscreen,
                                bg=CARD, fg=TEXT, activebackground=CARD_HOVER,
                                activeforeground=TEXT, relief="flat", bd=0,
                                cursor="hand2", font=(FONT, 10, "bold"),
                                padx=12, pady=6)
        self.fs_btn.place(relx=1.0, x=-12, y=12, anchor="ne")
        self.fs_btn.bind("<Enter>", lambda e: self.fs_btn.configure(bg=CARD_HOVER))
        self.fs_btn.bind("<Leave>", lambda e: self.fs_btn.configure(bg=CARD))

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        self.selected = tk.StringVar(value="")
        self.acc_var = tk.StringVar()
        self.acc_var.trace_add("write", self.on_account_change)
        self.cards = {}

        header = tk.Frame(self.main, bg=BG)
        header.pack(fill="x", padx=28, pady=(28, 6))
        tk.Label(header, text="NETFLIX", fg=ACCENT, bg=BG,
                 font=(FONT, 26, "bold")).pack(anchor="w")
        self.subtitle = tk.Label(header, text="", fg=MUTED, bg=BG,
                                 font=(FONT, 11))
        self.subtitle.pack(anchor="w", pady=(2, 0))

        self.container = tk.Frame(self.main, bg=BG)
        self.container.pack(fill="both", expand=True, padx=28)

        self.plan_page = tk.Frame(self.container, bg=BG)
        self.account_page = tk.Frame(self.container, bg=BG)

        self.build_plan_page()
        self.build_account_page()
        self.show_plan_page()

    def build_plan_page(self):
        page = self.plan_page
        tk.Label(page, text="Choose a plan", fg=TEXT, bg=BG,
                 font=(FONT, 12, "bold")).pack(anchor="w", pady=(18, 8))

        for name, price in netflix.items():
            self.make_card(page, name, price)

        row = tk.Frame(page, bg=BG)
        row.pack(fill="x", pady=(20, 0))
        tk.Label(row, text="Total", fg=MUTED, bg=BG,
                 font=(FONT, 12)).pack(side="left")
        self.total = tk.Label(row, text="— PKR", fg=TEXT, bg=BG,
                              font=(FONT, 18, "bold"))
        self.total.pack(side="right")

        make_button(page, "Next", self.go_next).pack(fill="x", ipady=12,
                                                     pady=(16, 0))
        self.plan_status = tk.Label(page, text="", bg=BG, fg=ERR,
                                    font=(FONT, 11))
        self.plan_status.pack(pady=(12, 0))

    def make_card(self, parent, name, price):
        card = tk.Frame(parent, bg=CARD, highlightthickness=2,
                        highlightbackground=BORDER, cursor="hand2")
        card.pack(fill="x", pady=5)
        left = tk.Label(card, text=name.capitalize(), fg=TEXT, bg=CARD,
                        font=(FONT, 13, "bold"))
        left.pack(side="left", padx=16, pady=14)
        right = tk.Label(card, text=f"{price} PKR", fg=MUTED, bg=CARD,
                         font=(FONT, 12))
        right.pack(side="right", padx=16)

        for w in (card, left, right):
            w.bind("<Button-1>", lambda e, n=name: self.select_plan(n))
            w.bind("<Enter>", lambda e, n=name: self.hover(n, True))
            w.bind("<Leave>", lambda e, n=name: self.hover(n, False))
        self.cards[name] = (card, left, right)

    def hover(self, name, inside):
        if self.selected.get() == name:
            return
        color = CARD_HOVER if inside else CARD
        for w in self.cards[name]:
            w.configure(bg=color)

    def select_plan(self, name):
        self.selected.set(name)
        for n, (card, left, right) in self.cards.items():
            active = n == name
            for w in (card, left, right):
                w.configure(bg=CARD)
            card.configure(highlightbackground=ACCENT if active else BORDER)
            right.configure(fg=TEXT if active else MUTED)
        self.total.configure(text=f"{netflix[name]} PKR")
        self.plan_status.configure(text="")

    def go_next(self):
        if self.selected.get() not in netflix:
            self.plan_status.configure(text="Invalid data: please select a plan")
            return
        self.show_account_page()

    def build_account_page(self):
        page = self.account_page

        summary = tk.Frame(page, bg=CARD, highlightthickness=2,
                           highlightbackground=BORDER)
        summary.pack(fill="x", pady=(18, 0))
        self.sum_plan = tk.Label(summary, text="", fg=TEXT, bg=CARD,
                                 font=(FONT, 13, "bold"))
        self.sum_plan.pack(side="left", padx=16, pady=14)
        self.sum_price = tk.Label(summary, text="", fg=MUTED, bg=CARD,
                                  font=(FONT, 12))
        self.sum_price.pack(side="right", padx=16)

        tk.Label(page, text="Account number", fg=TEXT, bg=BG,
                 font=(FONT, 12, "bold")).pack(anchor="w", pady=(24, 8))

        self.acc_wrap = tk.Frame(page, bg=CARD, highlightthickness=2,
                                 highlightbackground=BORDER)
        self.acc_wrap.pack(fill="x")
        self.entry = tk.Entry(self.acc_wrap, textvariable=self.acc_var,
                              bg=CARD, fg=TEXT, insertbackground=TEXT,
                              relief="flat", font=(FONT, 13))
        self.entry.pack(fill="x", padx=14, pady=12)
        self.entry.bind("<FocusIn>",
                        lambda e: self.acc_wrap.configure(highlightbackground=ACCENT))
        self.entry.bind("<FocusOut>",
                        lambda e: self.acc_wrap.configure(highlightbackground=BORDER))

        self.counter = tk.Label(page, text="0 / 14", fg=MUTED, bg=BG,
                                font=(FONT, 10))
        self.counter.pack(anchor="e", pady=(4, 0))

        make_button(page, "Pay now", self.pay).pack(fill="x", ipady=12,
                                                    pady=(20, 0))
        make_button(page, "Back", self.show_plan_page,
                    primary=False).pack(fill="x", ipady=10, pady=(10, 0))

        self.status = tk.Label(page, text="", bg=BG, fg=MUTED,
                               font=(FONT, 11), wraplength=400,
                               justify="center")
        self.status.pack(pady=(16, 0))

    def on_account_change(self, *_):
        n = len(self.acc_var.get())
        if hasattr(self, "counter"):
            self.counter.configure(text=f"{n} / 14", fg=OK if n == 14 else MUTED)
            self.acc_wrap.configure(highlightbackground=ACCENT)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        self.fs_btn.configure(text="Exit full screen" if self.is_fullscreen
                              else "Full screen")

    def exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.toggle_fullscreen()

    def show_plan_page(self):
        self.account_page.pack_forget()
        self.plan_page.pack(fill="both", expand=True)
        self.subtitle.configure(text="Step 1 of 2: Choose your plan")

    def show_account_page(self):
        plan = self.selected.get()
        self.plan_page.pack_forget()
        self.sum_plan.configure(text=f"{plan.capitalize()} plan")
        self.sum_price.configure(text=f"{netflix[plan]} PKR")
        self.status.configure(text="")
        self.account_page.pack(fill="both", expand=True)
        self.subtitle.configure(text="Step 2 of 2: Enter your account number")
        self.entry.focus_set()

    def pay(self):
        if len(self.acc_var.get()) == 14:
            self.status.configure(text="Check Your App for Payment Approval",
                                  fg=OK)
        else:
            self.status.configure(text="Invalid Account Number", fg=ERR)
            self.acc_wrap.configure(highlightbackground=ERR)


if __name__ == "__main__":
    NetflixApp().mainloop()