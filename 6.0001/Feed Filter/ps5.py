# RSS Feed Filter

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
from abc import ABC, abstractmethod

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)
        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Initializes a NewsStory object.
        
        guid (string): A globally unique identifier for this news story.
        title (string): The news story's headline.
        description (string): A paragraph or so summarizing the news
        story.
        link (string): A link to a website with the entire story.
        pubdate (datetime): Date the news was published.
        
        A NewsStory object has five attributes:
            self.guid (string, determined by input guid);
            self.title (string, determined by input title);
            self.description (string, determined by input description);
            self.link (string, determined by input link);
            self.pubdate (datetime, determined by input pubdate).
        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        '''
        Used to safely access self.guid outside of the class.
        
        Returns: self.guid.
        '''
        return self.guid
    
    def get_title(self):
        '''
        Used to safely access self.title outside of the class.
        
        Returns: self.title
        '''
        return self.title
    
    def get_description(self):
        '''
        Used to safely access self.description outside of the class.
        
        Returns: self.description
        '''
        return self.description
    
    def get_link(self):
        '''
        Used to safely access self.link outside of the class.
        
        Returns: self.link
        '''
        return self.link
    
    def get_pubdate(self):
        '''
        Used to safely access self.pubdate outside of the class.
        
        Returns: self.pubdate
        '''
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(ABC):
    @abstractmethod
    def evaluate(self, story):
        """
        Returns True if an alert should be generated for the given news
        item, or False otherwise.
        
        story (NewsStory object): News item being evaluated by the
        trigger
        """
        raise NotImplementedError("Please Implement this method")
        
# PHRASE TRIGGERS
        
class PhraseTrigger(Trigger, ABC):
    def __init__(self, phrase):
        '''
        Initializes a PhraseTrigger object
        
        phrase (string): One or more words separated by a single space
        between the words. Represents the phrase the user wants to be
        alerted of.
        
        A PhraseTrigger object has one attribute:
            self.phrase (string, determined by input phrase)
        '''
        self.phrase = phrase
        
    def is_phrase_in(self, text):
        '''
        Check if each word in self.phrase is present in its entirety and
        appears consecutively in text, separated only by spaces or
        punctuation. The method is not case sensitive.
        Assumes that self.phrase does not contain any punctuation.
        
        text (string): Some text where to search for self.phrase.
        
        Returns: True if self.phrase is in text; False otherwise.
        '''
        #Remove punctuation from text
        parsed_text = ""
        for char in text:
            if char not in string.punctuation:
                parsed_text += char
            else:
                parsed_text += " "
        #Remove duplicate spaces
        parsed_text = parsed_text.split()
        #Check if the words match
        parsed_phrase = self.phrase.split()
        i = 0
        for word in parsed_text:
            if parsed_phrase[i].lower() == word.lower():
                i += 1
                if i >= len(parsed_phrase):
                    return True
            else:
                i = 0
        return False
    
    def get_phrase(self):
        '''
        Used to safely access self.phrase outside of the class
        
        Returns: self.phrase
        '''
        return self.phrase

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
        Initializes a TitleTrigger object
        
        phrase (string): One or more words separated by a single space
        between the words. Represents the phrase the user wants to be
        alerted of.

        A TitleTrigger object inherits from PhraseTrigger and has one
        attribute:
            self.phrase (string, determined by input phrase)
        '''
        PhraseTrigger.__init__(self, phrase)
       
    def evaluate(self, story):
        """
        Determines if an alert should be generated for the given news
        based on its tittle.
        
        story (NewsStory object): News item being evaluated by the
        trigger
        
        Returns: True if the story has self.phrase on its tittle; False
        ottherwise
        """
        return self.is_phrase_in(story.get_title())
    
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
        Initializes a DescriptionTrigger object
        
        phrase (string): One or more words separated by a single space
        between the words. Represents the phrase the user wants to be
        alerted of.

        A DescriptionTrigger object inherits from PhraseTrigger and has
        one attribute:
            self.phrase (string, determined by input phrase)
        '''
        PhraseTrigger.__init__(self, phrase)
       
    def evaluate(self, story):
        """
        Determines if an alert should be generated for the given news
        based on its description.
        
        story (NewsStory object): News item being evaluated by the
        trigger
        
        Returns: True if the story has self.phrase on its description;
        False ottherwise
        """
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

class TimeTrigger(Trigger, ABC):
    def __init__(self, input_time):
        '''
        Initializes a TimeTrigger object
        
        input_time (string): EST time in the format of 
        "%d %b %Y %H:%M:%S". Time to be compared to the publication date
        of the story
        
        A PhraseTrigger object has one attribute:
            self.time (datetime, converted from the string input_time)
        '''
        self.time = datetime.strptime(input_time, "%d %b %Y %H:%M:%S")
        
    def get_time(self):
        '''
        Used to safely access self.time outside of the class
        
        Returns: self.time
        '''
        return self.time
    
class BeforeTrigger(TimeTrigger):
    def __init__(self, input_time):
        '''
        Initializes a BeforeTrigger object
        
        input_time (string): EST time in the format of 
        "%d %b %Y%H:%M:%S". Time to be compared to the publication date
        of the story
        
        A BeforeTrigger object inherits from TimeTrigger and has one
        attribute:
            self.time (datetime, converted from the string input_time)
        '''
        TimeTrigger.__init__(self, input_time)

    def evaluate(self, story):
        '''
        Determines if an alert should be generated for the given news
        based on its publication date
        
        story (NewsStory object): News item being evaluated by the
        trigger
        
        Returns: True if the story was published before self.time; False
        otherwise
        '''
        #Make both on the same time zone
        time_zone = story.get_pubdate().tzname()
        if time_zone != None:
            return (self.time.replace(tzinfo=pytz.timezone(time_zone))
                    > story.get_pubdate())
        else:
            return self.time > story.get_pubdate()
    
class AfterTrigger(TimeTrigger):
    def __init__(self, input_time):
        '''
        Initializes a AfterTrigger object
        
        input_time (string): EST time in the format of 
        "%d %b %Y%H:%M:%S". Time to be compared to the publication date
        of the story
        
        A AfterTrigger object inherits from TimeTrigger and has one
        attribute:
            self.time (datetime, converted from the string input_time)
        '''
        TimeTrigger.__init__(self, input_time)

    def evaluate(self, story):
        '''
        Determines if an alert should be generated for the given news
        based on its publication date
        
        story (NewsStory object): News item being evaluated by the
        trigger
        
        Returns: True if the story was published after self.time; False
        otherwise
        '''
        #Make both on the same time zone
        time_zone = story.get_pubdate().tzname()
        if time_zone != None:
            return (self.time.replace(tzinfo=pytz.timezone(time_zone))
                    < story.get_pubdate())
        else:
            return self.time < story.get_pubdate()
    
# COMPOSITE TRIGGERS

class NotTrigger(Trigger):
    def __init__(self, trigger):
        '''
        Initializes a NotTrigger object
        
        trigger (Trigger object): Trigger object to which it's desired
        to invert the output

        A NotTrigger object inherits from Trigger and has one attribute:
            self.trigger (Trigger object, determined by the input
            trigger)
        '''
        self.trigger = trigger
        
    def evaluate(self, story):
        '''
        Determines if an alert should be generated for the given news by
        inverting the output of another trigger applied to that story
        
        story (NewsStory object): News item being evaluated by the
        trigger
        
        Returns: True if self.trigger would NOT generate an alert; False
        otherwise
        '''
        return not self.trigger.evaluate(story)
    
class AndTrigger(Trigger):
    def __init__(self, triggerA, triggerB):
        '''
        Initializes a AndTrigger object
        
        triggerA (Trigger object): First Trigger object to which it's
        desired to apply the AND operation
        triggerB (Trigger object): Second Trigger object to which it's
        desired to apply the AND operation

        A AndTrigger object inherits from Trigger and has two attribute:
            self.triggerA (Trigger object, determined by the input
            triggerA)
            self.triggerB (Trigger object, determined by the input
            triggerB)
        '''
        self.triggerA = triggerA
        self.triggerB = triggerB
        
    def evaluate(self, story):
        '''
        Determines if an alert should be generated for the given news by
        by applying the AND operation to two other Triggers
        
        story (NewsStory object): News item being evaluated by the
        triggers
        
        Returns: True if both self.triggerA AND self.triggerB would
        generate an alert; False otherwise
        '''
        return self.triggerA.evaluate(story) and self.triggerB.evaluate(story)
    
class OrTrigger(Trigger):
    def __init__(self, triggerA, triggerB):
        '''
        Initializes a OrTrigger object
        
        triggerA (Trigger object): First Trigger object to which it's
        desired to apply the OR operation
        triggerB (Trigger object): Second Trigger object to which it's
        desired to apply the OR operation

        A OrTrigger object inherits from Trigger and has two attribute:
            self.triggerA (Trigger object, determined by the input
            triggerA)
            self.triggerB (Trigger object, determined by the input
            triggerB)
        '''
        self.triggerA = triggerA
        self.triggerB = triggerB
        
    def evaluate(self, story):
        '''
        Determines if an alert should be generated for the given news by
        by applying the OR operation to two other Triggers
        
        story (NewsStory object): News item being evaluated by the
        triggers
        
        Returns: True if either self.triggerA OR self.triggerB would
        generate an alert; False otherwise
        '''
        return self.triggerA.evaluate(story) or self.triggerB.evaluate(story)

#======================
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Dertermines wich news stories trigger an alert.
    
    stories (list NewsStory): List of news being analyzed by the
    triggers.
    triggerlist (list Trigger): List of triggers that will be applied to
    each news.

    Returns: a list of only the news stories for which a trigger in
    triggerlist fires.
    """
    triggered_stories = []
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story):
                triggered_stories.append(story)
    return triggered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    Read a trigger configuration file and create the triggers from it.
    
    filename (string): the name of a trigger configuration file.

    Returns: a list of trigger objects specified by the trigger
    configuration file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    all_triggers = {}
    triggerlist = []
    #Check each valid line of the file
    for current_line in lines:
        commands = current_line.split(",")
        #If ADD, insert all listed triggers
        if commands[0] == "ADD":
            for current_command in commands[1:]:
                try:
                    triggerlist.append(all_triggers[current_command])
                except(KeyError):
                    print(current_command, "trigger not defined.")
        #Else, check for all other commands
        else:
            if commands[1] == "TITLE":
                all_triggers[commands[0]] = TitleTrigger(commands[2])
            elif commands[1] == "DESCRIPTION":
                all_triggers[commands[0]] = DescriptionTrigger(commands[2])
            elif commands[1] == "AFTER":
                all_triggers[commands[0]] = AfterTrigger(commands[2])
            elif commands[1] == "BEFORE":
                all_triggers[commands[0]] = BeforeTrigger(commands[2])
            elif commands[1] == "NOT":
                try:
                    all_triggers[commands[0]]\
                    = NotTrigger(all_triggers[commands[2]])
                except(KeyError):
                    print(commands[2], "trigger not defined.")
            elif commands[1] == "AND":
                try:
                    all_triggers[commands[0]]\
                    = AndTrigger(all_triggers[commands[2]],
                                 all_triggers[commands[3]])
                except(KeyError):
                    print(commands[2], "or", commands[3],
                          "trigger not defined.")
            elif commands[1] == "OR":
                try:
                    all_triggers[commands[0]]\
                    = OrTrigger(all_triggers[commands[2]],
                                all_triggers[commands[3]])
                except(KeyError):
                    print(commands[2], "or", commands[3],
                          "trigger not defined.")
            else:
                raise RuntimeError("Problem reading trigger configuration",
                                   "file.")
    return triggerlist

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
#        t1 = TitleTrigger("Trump")
#        t2 = DescriptionTrigger("Mexico")
#        t3 = DescriptionTrigger("Wall")
#        t4 = AndTrigger(t2, t3)
#        triggerlist = [t1, t4]

        #Reads trigger configuration file
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)

root = Tk()
root.title("Some RSS parser")
t = threading.Thread(target=main_thread, args=(root,))
t.start()
root.mainloop()

