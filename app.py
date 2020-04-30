# Libraries
from appJar import gui
from datetime import date
import pdf_extractor as ex
import webscrape as scr
import os
import pandas as pd

# Global Variables
exist = "Optional"
out = "Select path..."
total_urls = 0
curr_url = 0


# Uses given length of URLs array to calculate % out of 100
def increment_progress_bar(length):
    global curr_url
    app.setMeter("prog", curr_url/length * 100)
    curr_url += 1


def create_dict():
    data = {'Release Number': [],
            'URL': [],
            'Report Date':  [],
            'Country': [],
            'Location': [],
            'Number of Strikes': [],
            'Action': [],
            'Number of Units': [],
            'Unit': [],
            'Flagged': [],
            'Initials': []}
    return data


def execute():
    # TODO: Make existing data useful
    existingPath = app.getEntry("Existing Data")
    # Output logic
    today = date.today()
    d1 = today.strftime("%Y%m%d")
    if app.getEntry("Output") != "":
        out = app.getEntry("Output")
    else:
        out = os.path.normpath(os.path.expanduser("~/Desktop/"))

    # TODO: REMOVE DEBUG URLS ARRAY
    #urls = scr.url_scrape()
    urls = [
        "https://www.inherentresolve.mil/Portals/14/CJTF-OIR%20%2020190104_01%20Strike%20Release.pdf?ver=2019-01-04-114833-703",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2019/01%20JAN/CJTF-OIR%2020190115-02%20Strike%20Release.pdf?ver=2019-01-15-134948-363",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2019/01%20JAN/CJTF-OIR%20Press%20Release%2020190130-01%20Strike%20Release.pdf?ver=2019-01-31-030344-140",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2019/02%20FEB/CJTF-OIR%20Press%20Release%2020190213-01%20Strike%20Release.pdf?ver=2019-02-13-120327-537",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2019/02%20FEB/CJTF-OIR%20Press%20Release%2020190227-01%20Strike%20Release.pdf?ver=2019-02-28-014130-050",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2019/03%20MAR/CJTF-OIR%20Press%20Release%2020190313-02-Strike%20Release.pdf?ver=2019-03-13-140242-693",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2019/03%20MAR/CJTF-OIR%20Press%20Release%2020190326-01-Strike%20Release.pdf?ver=2019-03-26-110227-217",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike Releases/2019/04 APR/CJTF-OIR Press Release 201904010-01-Strike Release.pdf?ver=2019-04-12-025900-273",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike Releases/2019/04 APR/CJTF-OIR Press Release 201904024-01-Strike Release.pdf?ver=2019-04-24-114521-317",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike Releases/2019/05 May/CJTF-OIR Press Release 20190507-01-Strike Release.pdf?ver=2019-05-12-095008-057",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike Releases/2019/06 June/CJTF-OIR Press Release 20190604-02-Strike Release.pdf?ver=2019-06-04-115418-937",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike Releases/2019/07 July/CJTF-OIR Press Release 20190703-01-Strike Release.pdf?ver=2019-07-03-145312-280",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike Releases/2019/08 August/CJTF-OIR Press Release 20190806-01-Strike Release.pdf?ver=2019-08-06-105849-603",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike Releases/2019/09 September/CJTF-OIR Press Release 20190904-01-Strike Release Approved.pdf?ver=2019-09-04-104214-907",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2019/10%20October/CJTF-OIR%20Press%20Release%2020191113-01-Strike%20Release.pdf?ver=2019-12-29-063044-423",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2019/11%20November/CJTF-OIR%20Press%20Release%2020191116-01-Strike%20Release.pdf?ver=2019-12-29-063804-610",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2019/12%20Dec/CJTF-OIR%20Press%20Release%2020200102-02-Strike%20Release.pdf?ver=2020-01-07-031116-043",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike%20Releases/2020/CJTF-OIR%20Press%20Release-20200213-01%20DEC2019%20Strike%20Release.pdf?ver=2020-02-13-040146-190",
        "https://www.inherentresolve.mil/Portals/14/Documents/Strike Releases/2019/08 August/CJTF-OIR Press Release 20190806-01-Strike Release.pdf?ver=2019-08-06-105849-603",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180105-01.pdf?ver=2018-01-05-050143-310",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180112-01.pdf?ver=2018-01-12-055057-933",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%20%2020180119-01.pdf?ver=2018-01-19-060041-520",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180126-01.pdf?ver=2018-01-26-082049-090",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180202%20-.pdf?ver=2018-02-02-062427-670",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180209.pdf?ver=2018-02-09-061910-893",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/20180216%20Strike%20Release%20FINAL.pdf?ver=2018-02-16-072324-000",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/20180223%20Strike%20Release-Final.pdf?ver=2018-02-23-032050-180",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180302-%20March%202%202018.pdf?ver=2018-03-02-041905-320",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180309%20-%20March%209%202018.pdf?ver=2018-03-09-074557-320",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180316.pdf?ver=2018-03-16-085547-097",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180323.pdf?ver=2018-03-23-043713-180",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180330-02.pdf?ver=2018-03-30-093644-830",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180406.pdf?ver=2018-04-06-085602-570",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180413-01.pdf?ver=2018-04-13-093657-337",
        "https://www.inherentresolve.mil/Portals/14/2018StrikeReleases/CJTF-OIR%20Strike%20Release%2020180420-01.pdf?ver=2018-04-20-075001-643"
    ]
    if existingPath != "":
        recentData = pd.read_csv(existingPath)
        recentDataURLs = list(recentData['URL'].unique())
        for x in recentDataURLs:
            urls.remove(str(x))
    if os.path.exists(out):
        global total_urls
        total_urls = len(urls)
        out = os.path.normpath(out + "/" + d1 + ".csv")
        data = create_dict()
        # if not recent_file:
        #     stripped_entries = ex.strip_tags(scr.get_2014_strings())
        #     for entry in stripped_entries:
        #         ex.data_from_text(entry, data)
        for url in urls:
            app.after(100, ex.data_from_url(url, data))
            app.after(100, increment_progress_bar(total_urls))
        data = ex.fill_empty_values(data)
        data = ex.create_and_save_dataframe(data, out)
        app.after(100, app.setMeter("prog", 100))
        print(data)
        app.infoBox("Process Complete", "The .csv file has been saved to " + out, parent=None)
        app.stop()
    else:
        print("[ERROR] Cannot save output file to path: " + out)
        app.infoBox("Error", "Cannot save to specified output path", parent=None)
        app.stop()


# handle button events
def press(button):
    if button == "Close":
        app.stop()
    else:
        execute()


# create a GUI variable called app
app = gui("OIR Airstrike Collection", "450x275")
app.addStatusbar(fields=1)
app.setStatusbar("NOTICE: Program may freeze during execution, do not force close.", 0)
app.setStatusFont(8)
app.addLabel("title", "Airstrike Data Collection")
app.setBg("gold")
app.setFont(14)

app.startLabelFrame("File I/O")
# Stretch label frame to left and right, responsive
app.setSticky("ew")

app.setLabelBg("title", "green")
app.setLabelFg("title", "white")

app.addLabelFileEntry("Existing Data")
app.setEntryDefault("Existing Data", exist)
app.addLabelDirectoryEntry("Output")
app.setEntryDefault("Output", out)
app.stopLabelFrame()

# link the buttons to the function called press
app.addButtons(["Go", "Close"], press)

app.addLabel("Progress")
app.addMeter("prog")
app.setMeterFill("prog", "green")

# start the GUI
app.go()
