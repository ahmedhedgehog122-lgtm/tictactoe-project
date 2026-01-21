from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle
from kivy.clock import Clock
import random, os

class TicTacToeApp(App):
    def build(self):
        self.m, self.d, self.p, self.b, self.a = "f", "e", "X", [""]*9, True
        self.r = BoxLayout(orientation='vertical', padding=15, spacing=15)
        with self.r.canvas.before:
            self.bg = Rectangle(pos=self.r.pos, size=(800, 2000))
            if os.path.exists('menu_bg.jpg'): self.bg.source = 'menu_bg.jpg'
        self.r.bind(size=self.upd, pos=self.upd)
        self.t = Label(text="TIC TAC TOE", font_size='40sp', size_hint_y=0.2)
        self.menu()
        return self.r

    def upd(self, i, v): self.bg.pos, self.bg.size = i.pos, i.size

    def menu(self, *args):
        self.r.clear_widgets(); self.a = True; self.r.add_widget(self.t)
        f = Button(text="FRIEND", size_hint_y=0.2)
        if os.path.exists('friend_btn.png'): f.background_normal = 'friend_btn.png'
        f.bind(on_press=lambda x: self.start("f"))
        r = Button(text="ROBOT", size_hint_y=0.2)
        if os.path.exists('robot_btn.png'): r.background_normal = 'robot_btn.png'
        r.bind(on_press=self.diff_m)
        self.r.add_widget(f); self.r.add_widget(r)

    def diff_m(self, *args):
        self.r.clear_widgets(); self.r.add_widget(self.t)
        for d in [("EASY", "e"), ("SMART", "s")]:
            btn = Button(text=d[0], size_hint_y=0.2); btn.bind(on_press=lambda x, v=d[1]: self.start("r", v))
            self.r.add_widget(btn)
        bk = Button(text="BACK", size_hint_y=0.1); bk.bind(on_press=self.menu); self.r.add_widget(bk)

    def start(self, m, d="e"):
        self.m, self.d, self.p, self.b, self.a = m, d, "X", [""]*9, True
        self.r.clear_widgets(); self.g = GridLayout(cols=3, spacing=5); self.btns = []
        for i in range(9):
            btn = Button(text="", font_size='40sp'); btn.bind(on_press=self.click)
            self.btns.append(btn); self.g.add_widget(btn)
        self.r.add_widget(self.g)
        ex = Button(text="EXIT", size_hint_y=0.1); ex.bind(on_press=self.menu); self.r.add_widget(ex)

    def click(self, inst):
        i = self.btns.index(inst)
        if self.a and self.b[i] == "":
            self.b[i] = self.p; inst.text = self.p
            if not self.check() and "" in self.b:
                if self.m == "r": 
                    self.a = False; Clock.schedule_once(self.robo, 1)
                else: self.p = "O" if self.p == "X" else "X"

    def robo(self, dt):
        idx = self.get_m()
        self.b[idx], self.btns[idx].text = "O", "O"
        self.check(); self.p, self.a = "X", True

    def get_m(self):
        if self.d == "s":
            for p in ["O", "X"]:
                for c in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
                    v = [self.b[j] for j in c]
                    if v.count(p) == 2 and v.count("") == 1: return c[v.index("")]
        return random.choice([i for i,x in enumerate(self.b) if x==""])

    def check(self):
        for c in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
            if self.b[c[0]] == self.b[c[1]] == self.b[c[2]] != "":
                self.pop(f"Win: {self.b[c[0]]}"); return True
        if "" not in self.b: self.pop("Draw!"); return True
        return False

    def pop(self, m):
        p = Popup(title="Result", content=Label(text=m), size_hint=(0.6, 0.4))
        p.bind(on_dismiss=self.menu); p.open()

if __name__ == "__main__":
    TicTacToeApp().run()
    