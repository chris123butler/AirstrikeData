# import the library
from appJar import gui
import pdf_extractor as ex

exist = "Optional"
out = "Select path..."

# TODO REMOVE THIS
urls = ['https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2015/04April/1%20Apr%20Strike%20Release.pdf?ver=2017-01-13-131120-810',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2015/07July/20150707%20Strike%20Release%20final.pdf?ver=2017-01-13-131141-437',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/01January/20170125%20Strike%20Release%20Final.pdf?ver=2017-01-25-093917-853',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/02February/20170203%20Strike%20Release%20Final.pdf?ver=2017-02-03-074516-280',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/02February/20170217%20Strike%20Release%20Final.pdf?ver=2017-02-17-093725-800',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/10October/20171023%20Strike%20Release.pdf?ver=2017-10-23-033103-287',
       'https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2017/11November/20171103%20CJTF-OIR%20Strike%20Release.pdf?ver=2017-11-03-065958-837']


# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        # Existing logic
        if app.getEntry("Existing Data") != "Optional":
            exist = app.getEntry("Existing Data")
        else:
            exist = ""

        # Output logic
        if app.getEntry("Output") != "Select path...":
            out = app.getEntry("Output")
        else:
            out = ""

        data = ex.data_from_urls(urls, out)
        # TODO REMOVE THIS TOO
        print(data)




# create a GUI variable called app
app = gui("OIR Airstrike Collection", "450x200")
app.setBg("gold")
app.setFont(16)

app.addLabel("title", "Airstrike Data Collection")
app.setLabelBg("title", "green")
app.setLabelFg("title", "gold")

app.addLabelFileEntry("Existing Data")
app.setEntryDefault("Existing Data", exist)
app.addLabelDirectoryEntry("Output")
app.setEntryDefault("Output", out)

# link the buttons to the function called press
app.addButtons(["Go", "Cancel"], press)

# start the GUI
app.go()
