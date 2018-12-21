
# -*- coding: <<encoding>> -*-
# -------------------------------------------------------------------------------
#   <<project>>
#
# -------------------------------------------------------------------------------

#import wxversion

#wxversion.select("2.8")
import wx, wx.html
import sys
import time
import Leap
import BookCleaning
from Leap import SwipeGesture





class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(800, 600)): #size in pixels
        wx.html.HtmlWindow.__init__(self, parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:   #assuring compatibility with softwares and macs
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())


class AboutBox(wx.Dialog):
    def __init__(self, textToDisplay):
        wx.Dialog.__init__(self, None, -1, "READER",
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER |
                                 wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400, 200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING       #Code required to allow library to function properly. (Boilerplate code)

        if(textToDisplay == ""):
            textToDisplay = aboutText
        hwin.SetPage(textToDisplay % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth() + 25, irep.GetHeight() + 10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()


class Frame(wx.Frame):

    m_html = None

    m_page_content = r"""

<html>
<body bgcolor="#E6E6FA">
<h1> <font color="blue">BOOKCASE: </font></h1>
<h1>HAMLET, 1603 BY WILLIAM SHAKESPEARE</h1>

</body>
</html>
    """

    bookLines = list()

    pageNum = 0

    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    controller = None
    """

      The class Frame sets up a Frame containing wx.Frame (wx and wx.html were imported libraries).
      The content and styling of the cover initial page is set through HTML tags. The background color, title color and heading size is set.
      The variable BookLines is set to hold a list which currently empty. The page number of the book is currently set to 0.
      The state_names variable links to the states set by the leap motion sensor. THe controller is used as a propety which will be set to detect the leap
       motion controller.
      """



    def __init__(self, title, bookTitle):
        super(Frame,self).__init__()
        wx.Frame.__init__(self, None, title=title, pos=(50, 50), size=(800, 600))
        self.m_html = wx.html.HtmlWindow(self)
        if "gtk2" in wx.PlatformInfo:
            self.m_html.SetStandardFonts()

        self.controller = Leap.Controller()
        self.controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        self.timer = wx.Timer(self)

        self.bookLines = BookCleaning.linesFromBook(bookTitle)
        self.pageNum = 0

        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPress)

        while not self.controller.is_connected:
            time.sleep(1)
        print "connected"
        self.timer.Start(40)
        self.m_html.SetPage(self.m_page_content)


    def update(self, event):
        print "\nupdated: ",
        print time.ctime()    #updates timer to detect events


        frame = self.controller.frame() #obtain the most recent frame
        print len(frame.gestures())  #eventually take out


        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)   #create a variable for the identified swipe gesture.
                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                    gesture.id, self.state_names[gesture.state],
                    swipe.position, swipe.direction, swipe.speed) #Print data about the gesture detected.
                if swipe.position > 0:  # change to left/right
                    self.pageNum -= 50
                    self.m_html.SetPage(self.getTextPage(self.pageNum))
                elif swipe.position < 0:
                    self.pageNum += 50
                    self.m_html.SetPage(self.getTextPage(self.pageNum))

        '''
        If the x coordinate on the plane of the data coordinates recieived is positive the swipe is towards the right and
        pageNum (of book being displayed) decreases by 50 lines meaning the page goes to the previous page.
        If the x coordinate on the plane of the data coordinates recieived is negative the swipe is towards the left and
        pageNum (of book being displayed) increases by 50 lines meaning the page goes to the next page of the book.
         '''


    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
            #If "OK" is pressed then the reader "messagedialog" is closed.

    def OnAbout(self, event):
        dlg = AboutBox("")
        dlg.ShowModal()
        dlg.Destroy()


    def OnKeyPress(self, event):
        keycode = event.GetKeyCode() #variable for keycode detected

        if keycode == wx.WXK_RIGHT:
            print
            self.pageNum += 40 #Increase page number
            self.m_html.SetPage(self.getTextPage(self.pageNum)) #set page
        elif keycode == wx.WXK_LEFT:
            self.pageNum -= 40 #Decrease page number
            self.m_html.SetPage(self.getTextPage(self.pageNum)) #set page
        elif keycode == wx.WXK_ESCAPE:
            self.OnClose(event)  #when escape pressed onClose is run.
        event.Skip()

    def getTextPage(self, pageNum):

        pageend = pageNum + 40
        aPage = ""
        for i in range(pageNum,pageend):
            aPage = aPage + self.bookLines[i]
        return aPage     #returning incremented page numbers into BookLines list.







if __name__ == '__main__':

    app = wx.App(redirect=False)  #Create app
    program = Frame("READER", "hamlet.epub")
    program.Show()
    app.MainLoop()

'''
A wx application is created. The frame, with the parameters created by the book Hamlet, is called
and named "program". "program" is shown and then the application is run through the main loop.
The book is presented through the reader and the mainloop running the algorithms to navigate the
pages is run.

'''




