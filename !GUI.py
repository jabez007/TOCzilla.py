from Tkinter import *
import tkMessageBox as box
import tkFileDialog

import json

import FindDirectAddresses


class TOCzilla(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        with open("config", 'r') as f:
            self.config = json.loads(f.read())

        self.IOfiles = None
        self.myCMS = None
        self.myPD = None
        self.providerDirectories = None

        # options for Frames
        self.frame_opt = options = {}
        options['side'] = LEFT
        options['fill'] = BOTH
        options['padx'] = 10
        options['expand'] = True

        # options for button bars
        self.buttonBar_opt = options = {}
        options['side'] = TOP
        options['fill'] = X
        options['expand'] = True

        # options for buttons
        self.button_opt = options = {}
        options['side'] = RIGHT
        options['fill'] = BOTH
        options['padx'] = 5
        options['pady'] = 5        
        
        self.initUI()

    def initUI(self):
        self.parent.title("TOCzilla")
        self.pack(fill=BOTH,
                  expand=True)

        ####
        
        menubar = Menu(self)

        importmenu = Menu(menubar, tearoff=0)
        importmenu.add_command(label='My InterOpportunity Report...',
                               command=self.SelectMyIOreport)
        importmenu.add_command(label='Provider Directories...',
                               command=self.SelectProviderDirectories)

        menubar.add_cascade(label="Open", menu=importmenu)
    
        self.parent.config(menu = menubar)

        ####

        ###Available Direct Addresses
        importFrame = Frame(self,
                            bd = 2)
        importFrame.pack(**self.frame_opt)
        
        #Text box
        importText = Frame(importFrame)
        importText.pack(side = TOP,
                        fill = BOTH,
                        expand = True)
        self.toSync_text = Text(importText,
                                height = 36,
                                width = 64)
        self.toSync_text.insert(INSERT,
                                 "Awaiting Directories")
        self.toSync_text.config(wrap = WORD)
        self.toSync_text.pack(side = LEFT,
                              fill = BOTH,
                              expand = True)
        syncScr = Scrollbar(importText,
                            command = self.toSync_text.yview)
        syncScr.pack(side=LEFT,
                     fill=Y,
                     expand=False)
        self.toSync_text['yscrollcommand'] = syncScr.set

        ##Button Bar
        importButtonBar = Frame(importFrame)
        importButtonBar.pack(**self.buttonBar_opt)

        #Buttons
        toSync_button = Button(importButtonBar,
                               text = 'Find Directories to Sync',
                               command = self.FindToSync)
        toSync_button.pack(**self.button_opt)
        
        ####

    def UpdateSyncTextBox(self):
        self.toSync_text.delete(1.0,
                                 END)

        self.toSync_text.insert(END,
                                "Using:\n")
        if self.myIO:
            self.toSync_text.insert(END,
                                     self.myIO.split("/")[-1]+"\n")
                
        self.toSync_text.insert(END,
                                 "Searching:\n") 
        if self.providerDirectories:
            for f in self.providerDirectories:
                self.toSync_text.insert(END,
                                        f.split("/")[-1]+"\n")
                
        return

    def SelectProviderDirectories(self):
        # get filenames
        self.providerDirectories = tkFileDialog.askopenfilename(initialdir = self.config["Provider Directory Dir"],
                                                                defaultextension = '.csv',
                                                                multiple = True,
                                                                parent = self.parent
                                                                )
        self.UpdateSyncTextBox()
        return

    def SelectMyIOreport(self):
        # get filenames
        self.myIO = tkFileDialog.askopenfilename(initialdir = self.config["InterOpportunity Dir"],
                                                 defaultextension = '.xlsx',
                                                 multiple = False,
                                                 parent = self.parent
                                                 )
        self.UpdateSyncTextBox()
        return

    def FindToSync(self):
        self.UpdateSyncTextBox()

        self.toSync_text.insert(END,
                                 "----\n\n")
        
        directories = FindDirectAddresses.main(self.myIO,
                                               self.providerDirectories)
        for d in directories.keys():
            if directories[d]['Providers']>0:
                directory = d.split("/")[-1]+"\n"
            
                directory += "Sync Providers: %d\n" % directories[d]['Providers']
                directory += "Total Transitions: %d\n" % directories[d]['Transitions']
                directory += "\tEP Transitions: %d\n" % directories[d]['EP Transitions']
                directory += "\tEH Transitions: %d\n" % directories[d]['EH Transitions']
            
                self.toSync_text.insert(END,
                                        directory+"\n")
        
        return

# # # #


def Main():
    root = Tk()
    gui = TOCzilla(root)
    root.mainloop()  


if __name__ == '__main__':
    Main()  
