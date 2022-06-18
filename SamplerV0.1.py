#!/usr/bin/python2.7

import Tkinter as tk
import ttk
MAIN_FONT = ("Constantia", 14)
LARGE_FONT = ("Verdana", 12)

class Sampler(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default='icon.ico')
        tk.Tk.wm_title(self, "Sampler G-code Maker v0.1")
        self.resizable(width=False, height=False)
        self.minsize(width=700, height=500)
        self.maxsize(width=700, height=500)

        self.app_data = {
            "project_name": [],
            "well_plate": [96],
            "from_well": [],
            "to_well": [],
            "mode": tk.StringVar(),
            "locations": [],
            "tip_locations": [],
            "well_locations": [],
            "output_file": [],
        }

        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, well96):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def qf(quickPrint):
        print(quickPrint)
        file = open("output.gcode","w")
        file.write(str(quickPrint))
        file.close()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="Welcome, to Sampler G-Code Maker", font=MAIN_FONT).grid(row=0,padx=10,pady=10)

        ttk.Label(self, text="Please Enter Project Name:").grid(row=1, column=1, sticky='e')
        self.job_name = tk.Entry(self)
        self.job_name.insert(0, "Sample1")
        self.job_name.grid(row=1, column=2)
        ttk.Button(self, text="Create Project", command=self.on_click).grid(row=4)
    def on_click(self):
        self.controller.app_data["project_name"].append(self.job_name.get())
        well96.change_project_name(self.controller.frames[well96], self.controller.app_data["project_name"][0])

        self.controller.show_frame(well96)

class well96(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #well plate constants
        self.numperrow = 8
        self.numrows = 12

        self.padx_from_buttons = 10

        self.controller.app_data["mode"].set("from_well")


        self.button_frame = tk.Frame(self)  # 880
        self.button_frame.pack(side='right', padx=50, pady=50)

        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(side='left', fill='both', expand=True)

        self.label = ttk.Label(self.entry_frame, text="PROJECT MAIN PAGE", font=LARGE_FONT)
        self.label.grid(row=0, column=0, pady=5, padx=self.padx_from_buttons, sticky='w')

        self.buttons = []
        self.make_buttons()

    def change_project_name(self, name):
        self.label.config(text="Project: " + name)

    def add_well(self, button):
        self.controller.app_data[self.controller.app_data["mode"].get()].append(button)
        #print(self.controller.app_data["to_well"])
        self.buttons[button-1]['state'] = 'disabled'
        if self.controller.app_data["mode"].get() == "from_well":
            self.buttons[button-1]['bg'] = '#84b3ff'  # blue
        else:
            self.buttons[button-1]['bg'] = '#d18181'  # red


    def make_buttons(self):
        ttk.Label(self.button_frame, text="Well Plate", font=LARGE_FONT).grid(row=0, column=0, columnspan=8, pady=5, padx=self.padx_from_buttons, sticky='w')
        for button in range(self.controller.app_data["well_plate"][0]):
            self.buttons.append(tk.Button(self.button_frame,
                                           text=button+1, width=2, command=lambda b=button+1: self.add_well(b)))
        for button in self.buttons:  # place buttons in the frame
            button.grid(row=self.numrows - (self.buttons.index(button) / self.numperrow),
                        column=self.buttons.index(button) % self.numperrow, sticky='nw')
        self.switch_button = tk.Button(self.button_frame, text="Switch to Dispense", command=lambda: self.switch_mode())
        self.switch_button.grid(row=self.buttons.index(button) / self.numperrow + 2, columnspan=8)

    def switch_mode(self):  # change button to receive sample and finish project
        if self.controller.app_data["mode"].get() == "to_well":
            self.switch_button['state'] = 'disabled'
            self.complete_project()
        if self.controller.app_data["mode"].get() == "from_well":
            self.controller.app_data["mode"].set("to_well")
            #print(self.controller.app_data["mode"].get())
            self.switch_button['text'] = 'Complete Project'

    def get_tip_locations_from_file(self):
        load_tip_file = open("load_tip_locations.txt","r")
        load_tip = load_tip_file.read().splitlines()
        for loc in load_tip:
            self.controller.app_data["tip_locations"].append(loc.split('\t'))
        #print(self.controller.app_data["tip_locations"])

    def get_well_locations_from_file(self):
        load_well_file = open("well_locations.txt","r")
        well_pos = load_well_file.read().splitlines()
        for loc in well_pos:
            self.controller.app_data["well_locations"].append(loc.split('\t'))
        #print(self.controller.app_data["well_locations"])

    def get_locations_from_file(self):  # these are common locations used
        load_well_file = open("locations.txt","r")
        well_pos = load_well_file.read().splitlines()
        for loc in well_pos:
            self.controller.app_data["locations"].append(loc.split('\t'))


    def tip_load(self, location, z_heights):
        self.controller.app_data["output_file"].append(";###loadtip\n")
        self.controller.app_data["output_file"].append("G28\n")
        self.controller.app_data["output_file"].append("G0 Z10\n")
        self.controller.app_data["output_file"].append("G0 X")
        self.controller.app_data["output_file"].append(str(location[0]))
        self.controller.app_data["output_file"].append(" Y")
        self.controller.app_data["output_file"].append(str(location[1]))
        self.controller.app_data["output_file"].append(" F2000\n")
        self.controller.app_data["output_file"].append("G0 Z")
        self.controller.app_data["output_file"].append(str(z_heights[0]))
        self.controller.app_data["output_file"].append(" F1250\n")
        self.controller.app_data["output_file"].append("G0 Z")
        self.controller.app_data["output_file"].append(str(z_heights[1]))
        self.controller.app_data["output_file"].append(" F1500\n")

    def sample(self, sample, deposit, z_heights, sample_amounts):
        self.controller.app_data["output_file"].append(";###sample\n")
        self.controller.app_data["output_file"].append("G0 X")
        self.controller.app_data["output_file"].append(str(sample[0]))
        self.controller.app_data["output_file"].append(" Y")
        self.controller.app_data["output_file"].append(str(sample[1]))
        self.controller.app_data["output_file"].append(" F2000\n")
        self.controller.app_data["output_file"].append("G0 Z5 F1500\n")
        self.controller.app_data["output_file"].append("M400\n")
        self.controller.app_data["output_file"].append("M42 P45 S255\n")
        self.controller.app_data["output_file"].append("G4 S3\n")
        self.controller.app_data["output_file"].append("M42 P39 S255\n")
        self.controller.app_data["output_file"].append("G4 P1\n")
        self.controller.app_data["output_file"].append("M42 P39 S0\n")
        self.controller.app_data["output_file"].append("M42 P45 S0\n")
        self.controller.app_data["output_file"].append("G0 Z20\n")
        self.controller.app_data["output_file"].append("G0 X")
        self.controller.app_data["output_file"].append(str(deposit[0]))
        self.controller.app_data["output_file"].append(" Y")
        self.controller.app_data["output_file"].append(str(deposit[1]))
        self.controller.app_data["output_file"].append(" F2000\n")
        self.controller.app_data["output_file"].append("G0 Z5 F1500\n")
        self.controller.app_data["output_file"].append("M400\n")
        self.controller.app_data["output_file"].append("M42 P43 S255\n")
        self.controller.app_data["output_file"].append("G4 S3\n")
        self.controller.app_data["output_file"].append("M42 P41 S255\n")
        self.controller.app_data["output_file"].append("G4 P1\n")
        self.controller.app_data["output_file"].append("M42 P41 S0\n")
        self.controller.app_data["output_file"].append("M42 P43 S0\n")

    def eject_tip(self):
        self.controller.app_data["output_file"].append(";###eject tip\n")
        self.controller.app_data["output_file"].append("G0 Z30 F1000\n")
        self.controller.app_data["output_file"].append("G0 X110 Y70 F3000\n")
        self.controller.app_data["output_file"].append("G0 X190 F2000\n")
        self.controller.app_data["output_file"].append("M18 X Y\n")
        self.controller.app_data["output_file"].append("G0 Z37 F1500\n")
        self.controller.app_data["output_file"].append("G0 X110 F2000\n")
        self.controller.app_data["output_file"].append("G28\n")
        self.controller.app_data["output_file"].append("M18\n")


    def complete_project(self):
        self.get_tip_locations_from_file()
        self.get_well_locations_from_file()
        for sample_number in range(len(self.controller.app_data["from_well"])):  # number of samples to take
            print(sample_number)
            print(self.controller.app_data["tip_locations"][sample_number])
            print(self.controller.app_data["well_locations"][(self.controller.app_data["from_well"][sample_number]) - 1])
            print(self.controller.app_data["well_locations"][(self.controller.app_data["to_well"][sample_number]) - 1])

            self.tip_load(self.controller.app_data["tip_locations"][sample_number],
                          self.controller.app_data["locations"][sample_number])
            self.sample(self.controller.app_data["well_locations"][(self.controller.app_data["from_well"][sample_number]) - 1],
                        self.controller.app_data["well_locations"][(self.controller.app_data["to_well"][sample_number]) - 1])
            self.eject_tip()

        #print(len(self.controller.app_data["from_well"]))
        output = open(self.controller.app_data["project_name"][0] + ".gcode","w")
        output.write("".join(self.controller.app_data["output_file"]))
        output.close()
        app.quit()



app = Sampler()
app.mainloop()