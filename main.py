import tkinter as tk
import math
import matplotlib.pyplot as plt
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()

def batch_reactor(C0, k, t):
    """Calculate concentration at time t in a batch reactor"""
    return C0 * math.exp(-k * t)

def flow_reactor(C0, k, t, Q, V):
    """Calculate concentration at time t in a flow reactor"""
    return C0 * math.exp(-k * t) + (Q/V) * (1 - math.exp(-k * t))

class App:
    def __init__(self, master):
        self.master = master
        master.title("Reactor Simulation")
        tk.Label(master, text="Initial Concentration (mol/L)").grid(row=0)
        tk.Label(master, text="Flow Rate (L/min)").grid(row=1)
        tk.Label(master, text="Volume (L)").grid(row=2)
        tk.Label(master, text="Reaction Rate Constant (1/min)").grid(row=3)
        tk.Label(master, text="Time (min)").grid(row=4)
        self.C0_entry = tk.Entry(master)
        self.Q_entry = tk.Entry(master)
        self.V_entry = tk.Entry(master)
        self.k_entry = tk.Entry(master)
        self.t_entry = tk.Entry(master)
        self.C0_entry.grid(row=0, column=1)
        self.Q_entry.grid(row=1, column=1)
        self.V_entry.grid(row=2, column=1)
        self.k_entry.grid(row=3, column=1)
        self.t_entry.grid(row=4, column=1)

        
        tk.Button(master, text="Run", command=self.run).grid(row=5, column=1)

        tk.Label(master, text="Batch Reactor Concentration (mol/L)").grid(row=6, column=0)
        tk.Label(master, text="Flow Reactor Concentration (mol/L)").grid(row=7, column=0)
        self.batch_label = tk.Label(master, text="")
        self.flow_label = tk.Label(master, text="")
        self.batch_label.grid(row=6, column=1)
        self.flow_label.grid(row=7, column=1)

    def run(self):
        try:
            C0 = float(self.C0_entry.get())
            Q = float(self.Q_entry.get())
            V = float(self.V_entry.get())
            k = float(self.k_entry.get())
            t = float(self.t_entry.get())

            C_batch = batch_reactor(C0, k, t)
            C_flow = flow_reactor(C0, k, t, Q, V)

            self.batch_label.configure(text=f"{C_batch:.2f} mol/L")
            self.flow_label.configure(text=f"{C_flow:.2f} mol/L")

            self.reactor_type = tk.StringVar(self.master)
            self.reactor_type.set("Batch")  
            reactor_options = ["Batch", "Flow"]
            self.reactor_menu = tk.OptionMenu(self.master, self.reactor_type, *reactor_options)
            self.reactor_menu.grid(row=0, column=2)

            if self.reactor_type.get() == "Batch":
                    C = batch_reactor(C0, k, t)
                    self.batch_label.configure(text=f"{C:.2f} mol/L")
            elif self.reactor_type.get() == "Flow":
                C = flow_reactor(C0, k, t, Q, V)
                self.flow_label.configure(text=f"{C:.2f} mol/L")
                times = float(range(0, t+1))
                batch_concentrations = [batch_reactor(C0, k, time) for time in times]
                flow_concentrations = [flow_reactor(C0, k, time, Q, V) for time in times]

            

            if C0 <= 0:
                raise ValueError("Initial concentration must be positive")
            if Q <= 0:
                raise ValueError("Flow rate must be positive")
            if V <= 0:
                raise ValueError("Volume must be positive")
            if k <= 0:
                raise ValueError("Reaction rate constant must be positive")
            if t < 0:
                raise ValueError("Time must be non-negative")


       

          
            self.progress = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
            self.progress.grid(row=5, column=2)
            self.progress.start()

            
        
            
            self.dt = tk.IntVar(self.master)
            self.dt.set(1)  
            self.dt_slider = tk.Scale(self.master, from_=1, to=10, orient="horizontal", variable=self.dt)
            self.dt_slider.grid(row=4, column=2)     
            dt = self.dt.get()

            times = float(range(0, t+1, dt))
            batch_concentrations = [batch_reactor(C0, k, time) for time in times]
            flow_concentrations = [flow_reactor(C0, k, time, Q, V) for time in times]

            batch=plt.plot(times, batch_concentrations, label="Batch")
            flow=plt.plot(times, flow_concentrations, label="Flow")
            plot1=FigureCanvasTkAgg(batch, root)
            plot1.show()
            plot1.get_tk_widget().grid(row=5, column=3) 
            plot1._tkcanvas.grid(row=5,column=3)

            plt.xlabel("Time (min)")
            plt.ylabel("Concentration (mol/L)")
            plt.legend()
           
            self.progress.stop()

        except ValueError as e:
         tk.messagebox.showerror("Error", str(e))
         tk.Button(self.master, text="Reset", command=self.reset).grid(row=5, column=2)



    def reset(self):
        self.C0_entry.delete(0, "end")
        self.Q_entry.delete(0, "end")
        self.V_entry.delete(0, "end")
        self.k_entry.delete(0, "end")
        self.t_entry.delete(0, "end")
        self.batch_label.configure(text="")
        self.flow_label.configure(text="")    
   


app = App(root)
root.mainloop()