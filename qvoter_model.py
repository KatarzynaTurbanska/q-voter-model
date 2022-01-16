import math, random, matplotlib
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def normal_round(n):
    """Round value n."""
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

class QVoter_Model:
    def __init__(self, fig, L, x, type_of_nonconformity, p, q, replacement, f, fps):
        """Initialize the q-voter model.
        Args:
            fig: figure on which we draw plots;
            L [int]: size of the net;
            x [float]: concentration of positive opinion, value between 0 and 1;
            type_of_nonconformity [string]: type of nonconformity in the model, take value "independence" or "anticonformity";
            p [float]: probability of nonconformity, value between 0 and 1;
            q [int]: amount of agents which impact on chosen agent;
            replacement [boolean]: whether the sample is with or without replacement. True meaning that a value of a can be selected multiple times.
            f [float]: probability of being independent, value between 0 and 1;
            fps [int]: speed of animation.
        """
        self.opinion = []
        self.global_time = 0

        self.fig = fig

        ax = fig.add_gridspec(11, 9)
        self.ax1 = fig.add_subplot(ax[0:7, 0:])
        self.ax2 = fig.add_subplot(ax[8:, 0:])

        self.L = L
        self.N = L**2
        self.x = x

        self.initialize_net()

        self.nonconformity = type_of_nonconformity
        self.p = p
        self.q = q
        self.replace = replacement
        self.f = f

        self.fps = fps

        cmap = matplotlib.colors.ListedColormap(['red', 'limegreen'])
        self.heatmap = self.ax1.imshow(np.copy(self.agents), vmin=-1, vmax=1, cmap=cmap)
        self.ax1.axis("off")

        self.line, = self.ax2.plot(range(self.global_time), self.opinion, linewidth=0.6, color="#3eb0f7")
        self.ax2.set_ylim(-1.1, 1.1)

    def initialize_net(self):
        """Initialize net of agents."""
        self.agents = np.random.permutation([1]*normal_round(self.x*self.N) + [-1]*(self.N - normal_round(self.x*self.N)))
        self.agents = self.agents.reshape((self.L, self.L))

    def qvoter_animation(self, i):
        """One Monte Carlo step of q-voter model.
        
        Returns:
            heatmap with opinion of each agent;
            plot with average opinion in every Monte Carlo step.
        """
        if self.global_time == 0:
            self.global_time += 1
            self.opinion.append(np.sum(np.copy(self.agents))/self.N)
            self.ax1.set_title("Siatka agentów, czas: {} [MCS]".format(self.global_time-1))
            self.ax2.set_title("Średnia opinia w czasie, aktualnie: {}".format(round(self.opinion[-1],3)))

            return [self.heatmap], self.line,

        for _ in range(self.N):
            x = random.randint(0,self.L-1)
            y = random.randint(0,self.L-1)
            
            if x > 1:
                left_neighbour = self.agents[x-1, y]
            else:
                left_neighbour = 0
            
            if x < self.L-1:
                right_neighbour = self.agents[x+1, y]
            else:
                right_neighbour = 0

            if y > 1:
                upper_neighbour = self.agents[x, y-1]
            else:
                upper_neighbour = 0
            
            if y < self.L-1:
                lower_neighbour = self.agents[x, y+1]
            else:
                lower_neighbour = 0

            neighbours = [n for n in [left_neighbour, right_neighbour, upper_neighbour, lower_neighbour] if n != 0]

            if self.replace:
                group_of_influence = np.random.choice(neighbours, self.q, replace=self.replace)
            else:
                group_of_influence = np.random.choice(neighbours, min(self.q, len(neighbours)), replace=self.replace)

            U = random.random()
            if U > self.p:
                if abs(sum(group_of_influence)) == self.q:
                        self.agents[x, y] = sum(group_of_influence)/self.q
            else:
                if self.nonconformity == "independence":
                    U2 = random.random()
                    if U2 < self.f:
                        self.agents[x, y] *= -1

                elif self.nonconformity == "anticonformity":
                    if abs(sum(group_of_influence)) == self.q:
                        self.agents[x, y] = -1*sum(group_of_influence)/self.q

        self.global_time += 1
        self.opinion.append(np.sum(np.copy(self.agents))/self.N)
        self.heatmap.set_array(np.copy(self.agents))
        self.ax1.set_title("Agents net, time: {} [MCS]".format(self.global_time-1))
        self.ax2.set_title("Average opinion over the time, now: {}".format(round(self.opinion[-1],3)))
        self.ax2.set_xlim(0, self.global_time)
        self.line.set_data(range(self.global_time), self.opinion)

        return [self.heatmap], self.line,

    def show_animation(self):
        """Show animation on GUI window."""
        self.anim = animation.FuncAnimation(self.fig, self.qvoter_animation, interval=200/self.fps, repeat=False)
        plt.show()

class App(tk.Frame):
    def __init__(self, master=None):
        """Initialize GUI window."""
        super().__init__(master)
        self.master = master
        self.master.title("Q-voter model (Katarzyna Turbańska)")
        self.master.geometry("691x535")

        self.labels()
        self.parameters()
        self.buttons()

        self.frame = tk.Frame(self.master)
        self.frame.place(x=240, y=-35)

    def labels(self):
        """Create labels."""
        tk.Label(self.master, text="Size of the net", fg="black", bg="#87cefa").place(x=0, y=0, width=240, height=25)
        tk.Label(self.master, text="Concentration of positive opinion", fg="black", bg="#87cefa").place(x=0, y=50, width=240, height=25)
        tk.Label(self.master, text="Type of nonconformity", fg="black", bg="#87cefa").place(x=0, y=120, width=240, height=25)
        tk.Label(self.master, text="Probability of nonconformity", fg="black", bg="#87cefa").place(x=0, y=170, width=240, height=25)
        tk.Label(self.master, text="Size of impact group", fg="black", bg="#87cefa").place(x=0, y=240, width=240, height=25)
        tk.Label(self.master, text="Sampling", fg="black", bg="#87cefa").place(x=0, y=290, width=240, height=25)
        tk.Label(self.master, text="Probability of being independent", fg="black", bg="#87cefa").place(x=0, y=340, width=240, height=25)
        tk.Label(self.master, text="Speed of animation", fg="black", bg="#87cefa").place(x=0, y=410, width=240, height=25)

    def parameters(self):
        """Create places to input parameters to q-voter model."""
        self.start_L = tk.IntVar(self.master, value=10)
        tk.Entry(self.master, textvariable=self.start_L, justify='center').place(x=0, y=25, width=240, height=25)
        self.start_x = tk.DoubleVar()
        tk.Scale(self.master, variable=self.start_x, orient=tk.HORIZONTAL, from_=0, to=1, resolution=0.01, troughcolor="#d0ecfd").place(x=0, y=75, width=240)
        self.type_of_nonconformity = tk.StringVar()
        self.is_anticonformity = tk.Radiobutton(self.master, text="anticonformity", variable=self.type_of_nonconformity, value="anticonformity", command=self.nonconformity_button)
        self.is_anticonformity.select()
        self.is_anticonformity.place(x=0, y=145, width=132, height=25)
        tk.Radiobutton(self.master, text="independence", variable=self.type_of_nonconformity, value="independence", command=self.nonconformity_button).place(x=140, y=145, width=100, height=25)
        self.start_p = tk.DoubleVar()
        tk.Scale(self.master, variable=self.start_p, orient=tk.HORIZONTAL, from_=0, to=1, resolution=0.01, troughcolor="#d0ecfd").place(x=0, y=195, width=240)
        self.start_q = tk.IntVar()
        q_value = ttk.Combobox(self.master, textvariable=self.start_q, values=("1", "2", "3", "4"), justify='center')
        q_value.current(0)
        q_value.place(x=0, y=265, width=240, height=25)
        self.is_replacement = tk.BooleanVar()
        tk.Checkbutton(self.master, text="with replacement", variable = self.is_replacement, onvalue=True, offvalue=False).place(x=0, y=315, width=240, height=25)
        self.start_f = tk.DoubleVar()
        self.f_ability = tk.Scale(self.master, variable = self.start_f, orient=tk.HORIZONTAL, from_=0, to=1, resolution=0.01, troughcolor="#d0ecfd")
        self.f_ability['state'] = tk.DISABLED
        self.f_ability.place(x=0, y=365, width=240)
        self.start_fps = tk.IntVar()
        tk.Scale(self.master, variable=self.start_fps, orient=tk.HORIZONTAL, from_=1, to=5, resolution=1, troughcolor="#d0ecfd").place(x=0, y=435, width=240)

    def nonconformity_button(self):
        """Function associated with radiobuttons determining type of nonconformity. If value of radiobuttons
        is "anticonformity", chosing probability of independence is disabled and comes back to value 0."""
        if self.type_of_nonconformity.get() == "anticonformity":
            self.f_ability['state'] = tk.DISABLED
            self.start_f.set(value = 0)
        if self.type_of_nonconformity.get() == "independence":
            self.f_ability['state'] = tk.NORMAL

    def buttons(self):
        """Create buttons to start, pause and continue animation and button to close application."""
        tk.Button(self.master, text="continue", fg="black", bg="white", activebackground="#87cefa", command=self.continue_animation).place(x=160, y=485, width=80, height=25)
        tk.Button(self.master, text="start", fg="black", bg="white", activebackground="#87cefa", command=self.animation_display).place(x=0, y=485, width=80, height=25)
        tk.Button(self.master, text="stop", fg="black", bg="white", activebackground="#87cefa", command=self.pause_animation).place(x=80, y=485, width=80, height=25)
        tk.Button(self.master, text="Close application", command=self.master.quit, fg="red", bg="white").place(x=0, y=510, width=240, height=25)
    
    def animate(self, fig):
        """Generate the QVoter_Model class with specified parameters."""
        for widget in self.frame.winfo_children():
            widget.destroy()

        anim = QVoter_Model(fig, self.start_L.get(), self.start_x.get(), self.type_of_nonconformity.get(), self.start_p.get(), self.start_q.get(), self.is_replacement.get(), self.start_f.get(), self.start_fps.get())
        return anim

    def animation_display(self):
        """Display animation on GUI window. Associated with start button."""
        fig = Figure(figsize=(4.5, 6))
        self.anim = self.animate(fig)
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        self.canvas.get_tk_widget().pack()
        self.anim.show_animation()

    def pause_animation(self):
        """Pause animation. Associated with pause button."""
        self.anim.anim.event_source.stop()

    def continue_animation(self):
        """Continue animation. Associated with continue button."""
        self.anim.anim.event_source.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()