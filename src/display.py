import logging
import os
import tkinter as tk
from tkinter import ttk, font, StringVar

dirname = os.path.dirname(__file__)
iconpath = os.path.join(dirname, "../tt.ico")


class display:
    root = None
    trnstApi = None
    fullscreenFlag = None
    waitTime = None
    waitCounter = 0

    dispFont = None

    progressBar = None

    contextText = None
    contextLabel = None

    timeText = None
    timeFont = None
    timeLabel = None

    statusText = None
    statusLabel = None

    lastUpdateText = None
    lastUpdateLabel = None

    def __init__(self, tApi, fullscrn, wTime):
        self.root = tk.Tk()
        self.trnstApi = tApi
        self.fullscreenFlag = fullscrn
        self.waitTime = wTime

        self.contextText = StringVar()
        self.timeText = StringVar()
        self.statusText = StringVar()
        self.lastUpdateText = StringVar()

        self.dispFont = font.Font(family="Helvetica", size=20)
        self.timeFont = font.Font(family="Helvetica", size=50, weight="bold")

        self.contextLabel = ttk.Label(
            self.root,
            textvariable=self.contextText,
            font=self.dispFont,
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
        self.statusLabel = ttk.Label(
            self.root,
            textvariable=self.statusText,
            font=self.dispFont,
            foreground="white",
            background="black",
        )
        self.lastUpdateLabel = ttk.Label(
            self.root,
            textvariable=self.lastUpdateText,
            font=self.dispFont,
            foreground="white",
            background="black",
        )

        s = ttk.Style()
        s.configure(
            "gray.Horizontal.TProgressbar",
            troughcolor="black",
            bordercolor="black",
            background="gray",
            lightcolor="black",
            darkcolor="black",
        )
        self.progressBar = ttk.Progressbar(
            style="gray.Horizontal.TProgressbar", orient=tk.HORIZONTAL, length=500
        )

        self.progressBar.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        self.contextLabel.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.timeLabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.statusLabel.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        self.lastUpdateLabel.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def start(self):
        def onClick(event):
            [depMin, isRealTime, depTime] = self.trnstApi.get_TA_stop_time()

            contextLabel = "Next bus leaves at " + depTime + " in"
            timeLabel = str(depMin) + "min"
            updateLabel = ""
            self.setLabels(contextLabel, timeLabel, updateLabel)
            self.setStatus(isRealTime)

        self.root.bind("<Button-1>", onClick)
        if self.fullscreenFlag:
            self.root.attributes("-fullscreen", True)
        else:
            self.root.geometry("480x320")
        self.root.config(background="black", cursor="none")
        self.root.bind("x", quit)
        self.root.title("TransitTracker")
        try:
            self.root.iconbitmap(iconpath)
        except:
            logging.warning(".ico files not supported, will not use custom icons")
        self.root.after(1000, self.show_time)

        self.root.mainloop()

    def quit(self, *args):
        self.root.destroy()

    def show_time(self):
        try:
            res = self.trnstApi.get_TL_stop_info()
            if res:
                if len(res.json()) > 0 and res.status_code == 200:
                    resJson = res.json()[0]
                    closestSchedule = resJson["Schedules"][0]
                    contextLabel = (
                        "Next bus leaves at "
                        + closestSchedule["ExpectedLeaveTime"].split(" ")[0]
                        + " in"
                    )
                    timeLabel = str(closestSchedule["ExpectedCountdown"]) + "min"
                    updateLabel = "Last updated at " + closestSchedule["LastUpdate"]
                    self.setLabels(contextLabel, timeLabel, updateLabel)
                    self.setStatus(closestSchedule["ScheduleStatus"])
                elif len(res.json()) == 0:
                    contextLabel = ""
                    timeLabel = "N/A"
                    updateLabel = "No busses currently available"
                    self.setLabels(contextLabel, timeLabel, updateLabel)
                    self.setStatus("error")
                elif res != None and res.status_code and res.reason:
                    contextLabel = ""
                    timeLabel = "Error: " + str(res.status_code)
                    updateLabel = res.reason
                    self.setLabels(contextLabel, timeLabel, updateLabel)
                    self.setStatus("error")
            else:
                logging.warning(
                    "Unable to retrieve api data, trying again in "
                    + str(self.wait)
                    + " seconds"
                )
                contextLabel = ""
                timeLabel = "Error"
                updateLabel = "Error: Connection Issue"
                self.setLabels(contextLabel, timeLabel, updateLabel)
                self.setStatus("error")

        except Exception as err:
            logging.exception("Error retrieving api data")

        self.wait()

    def wait(self):
        if self.waitCounter < self.waitTime:
            self.waitCounter += 1
            self.progressBar.step((100 / self.waitTime))
            self.root.after(1000, self.wait)
        else:
            self.waitCounter = 0
            self.show_time()

    def setLabels(self, contextLabel, timeLabel, updateLabel):
        self.contextText.set(contextLabel)
        self.timeText.set(timeLabel)
        self.lastUpdateText.set(updateLabel)

    def setStatus(self, status):
        color = "white"
        text = ""

        match status:
            case "*":
                color = "white"
                text = "On time"
            case "-":
                color = "orange"
                text = "Delayed"
            case "+":
                color = "red"
                text = "Ahead of Schedule"
            case "error":
                color = "red"
                text = "Error"
            case True:
                color = "green"
                text = "Real Time"

        self.statusText.set(text)
        self.statusLabel.config(foreground=color)
