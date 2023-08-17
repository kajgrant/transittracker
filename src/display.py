from tkinter import *
from tkinter import ttk
from tkinter import font
from helpers import *


class display:
    root = None
    transitApi = None
    waitTime = None

    contextText = None
    contextFont = None
    contextLabel = None

    timeText = None
    timeFont = None
    timeLabel = None

    scheduleText = None
    scheduleFont = None
    scheduleLabel = None

    def __init__(self, tApi, wtime):
        self.root = Tk()

        self.contextText = StringVar()
        self.timeText = StringVar()
        self.scheduleText = StringVar()

        self.contextFont = font.Font(family="Helvetica", size=20)
        self.timeFont = font.Font(family="Helvetica", size=35, weight="bold")
        self.scheduleFont = font.Font(family="Helvetica", size=10)

        self.contextLabel = ttk.Label(
            self.root,
            textvariable=self.txt,
            font=self.contextFont,
            foreground="white",
            background="black",
        )
        self.timeLabel = ttk.Label(
            self.root,
            textvariable=self.timeText,
            font=self.timeFont,
            foreground="white",
            background="black",
        )
        self.scheduleLabel = ttk.Label(
            self.root,
            textvariable=self.scheduleText,
            font=self.scheduleFont,
            foreground="white",
            background="black",
        )

        self.contextLabel.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.timeLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.scheduleLabel.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.transitApi = tApi
        self.waitTime = wtime

    def quit(self, *args):
        self.root.destroy()

    def show_time(self):
        res = self.transitApi.get_stop_info()
        resJson = res.json()[0]
        closestSchedule = resJson["Schedules"][0]
        self.contextText.set("The next bus leaves at")
        self.timeText.set(closestSchedule["ExpectedLeaveTime"])
        self.scheduleText.set(getScheduleLabel(closestSchedule["ScheduleStatus"]))

        self.root.after(self.waitTime * 1000, self.show_time)

    def show_display(self):
        self.root.attributes("-fullscreen", True)
        self.root.config(background="black", cursor="none")
        self.root.bind("x", quit)
        self.root.after(1000, self.show_time)

        self.root.mainloop()
