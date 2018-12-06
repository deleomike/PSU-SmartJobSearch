import sys
import os
import shutil
import json
import warnings
from watson_developer_cloud import DiscoveryV1

import tkinter
from tkinter import *
from tkinter import filedialog

import IndeedCrawler
from Evaluator import Evaluator


#global variables used in multiple functions
discovery = None
environmentID = None  #environment unique ID
collectionID = None   #collection unique ID 
keywords = ['PLC', 'Linux']     #dictionary containing all keywords extracted from resume
JobTitle = "Software Engineering"   #default job title for searching indeed
JobLocation = "Pittsburgh"            #default job location for searching indeed
Resume = None 
evaluator = None


#CREATES A COLLECTION TO STORE SEARCH RESULTS FROM JOB CRAWLER
#WATSON DISCOVERY ALLOWS US TO INTELLIGENTLY QUERY DOCUMENTS
#USES NATURAL LANGUAGE PROCESSING AND TRADITIONAL SEARCH METHODS
def InitDiscovery():
        global discovery
        global environmentID
        global collectionID
        APIKEY = 'gR4dbAo_IIcdVYAcL1VAafrQonD9FRJF-Imceur5LPXW'
        URL = "https://gateway.watsonplatform.net/discovery/api"
        #Active discovery instance
        discovery = DiscoveryV1(
        version='2017-11-07', 
        iam_apikey= APIKEY, 
        url= URL
        )
        global collectionID
        global environmentID
        #after we initialize the discovery instance using the apikey and url, 
        #we will need to get the environment id so that we can create a new collection
        environments = discovery.list_environments() 
        environmentID = environments.result['environments'][1]['environment_id']
        #before making the new collection, makes sure that we have the room to do so
        #by deleting the previous queries collection
        #this is the most efficient way to ensure that the documents
        #from previous job searches do not interfere with the queries related
        #to the current one
        collections = discovery.list_collections(environmentID).result['collections']
        for collection in collections:
            if collection['name'] == 'Collection':
                discovery.delete_collection(environmentID,collection['collection_id'])
        #creates the collection    
        collection = discovery.create_collection(
                environment_id = environmentID, 
                name='Collection', 
                description='{collection_desc}').get_result()
        collectionID = collection['collection_id']




def GetPostings(count):
    global JobTitle
    global JobLocation
    global environmentID
    global collectionID
    global discovery
    global keywords
    global JobTitle
    global JobLocation
    #UPLOADS A LIST OF DOCUMENT NAMES
    def UploadDocuments():
        data = os.listdir('Jobs') #gets all the filenames  in the directory
        for file in data: #iterates over each file, uploading each to watson discovery
            with open((os.path.join(os.getcwd(), 'Jobs', file))) as fileinfo: 
                        add_doc = discovery.add_document(environmentID, 
                                                         collectionID, 
                                                         file=fileinfo,   
                                                         file_content_type = 'text/html')   
    evaluator = Evaluator(Resume, count, JobTitle, JobLocation)
    #updates the resume keyword list
    keywords.clear()
    for word in evaluator.resume_words: #makes each one accessable to the user via dropdown
        keywords.append(word)
    UploadDocuments() #uploads all the jobs to discovery
    
    

#QUERIES THE KEYWORD IN THE COMPILED LIST OF JOB POSTINGS USING WATSON DISCOVERY                 
def QueryDiscovery(keyword):
    global environmentID
    global collectionID
    global discovery
    #queries keyword extracted by NLU from resume
    response = discovery.query(environmentID,collectionID,filter=keyword,query=keyword,count=5,passages=True) 
    results = response.result['passages'] #query returns a series of passages in which the search term appears
    for entity in results: #prints all the passages
        print('\n''\"...' + str(entity['passage_text']) + '...\"''\n')



class Redir(object):
    # This is what we're using for the redirect, it needs a text box
    def __init__(self, textbox):
        self.textbox = textbox
        self.textbox.config(state=NORMAL)
        self.fileno = sys.stdout.fileno


    def write(self, message):
        # provides a write function for the stdout
        self.textbox.insert(END, str(message))



def GetResume():
    global keywords
    global evaluator
    global Resume
    # get filename, this is the bit that opens up the dialog box this will
    # return a string of the file name you have clicked on.
    filename = filedialog.askopenfilename()
    if filename:
        # Will print the file name to the text box
        print(filename)
        Resume = filename
       
        


def InitGUI():
    #shutil.rmtree('Jobs')
    #os.mkdir("Jobs")
    global keywords
    try:
        shutil.rmtree("Jobs") #clears out any old web search files
    except:
        pass

    InitDiscovery()
    
    # Make the root window
    root = Tk()
    root.title("Resume Helper")
    
    #create dropdown menu
    keyword = StringVar(root)
    popupMenu = OptionMenu(root, keyword, *keywords)
    Label(root, text="Choose a keyword").grid(row = 0, column = 2)
    popupMenu.grid(row = 1, column =2)


    #creates two text entry bars to enter job location and title
    job = StringVar()
    jobfield = Entry(root, textvariable=job)
    jobfield.grid(row=0, column=0)
    job.set("{Enter Job Title}")

    loc = StringVar()
    locfield = Entry(root, textvariable=loc)
    locfield.grid(row=1, column=0)
    loc.set("{Enter Location}")

    count = IntVar()
    countfield = Entry(root, textvariable=count)
    countfield.grid(row=2, column=1)
    Label(root, text="# of search results").grid(row=1, column=1)
    # label

    #defines the search function for GO
    def go():
            JobTitle = job.get() #first it retrieves text for job search
            JobLocation = loc.get()
            GetPostings(count.get()) #then it calls the actual webcrawler + watson NLU
            menu = popupMenu["menu"]
            menu.delete(0, "end")   #updates the dropdown menu info
            for string in keywords:
                menu.add_command(label=string, 
                                 command=lambda value=string:
                                      keyword.set(value))
                    
    #simple function that prints the selection and updates the display             
    def change_dropdown(*args):
        print( "\n" + str(keyword.get()) + ":" )
    keyword.trace('w', change_dropdown)
    
    #Sets up button that initializes the search
    getpostings = Button(root, text='GO!', command = lambda : go())
    getpostings.grid(row=0, column=1)
    getpostings.event_add
    
    getresume = Button(root, text='Get Resume File', command = lambda : GetResume())
    getresume.grid(row=2, column=0)
    
    getpassages = Button(root, text='Get Passages', command = lambda : QueryDiscovery(keyword.get()))
    getpassages.grid(row=2, column=2)

    
    #create scrollbar
    scrollbar = Scrollbar(root, orient=VERTICAL)
    scrollbar.grid(row=2, column=3, sticky=N+S+E)
    
    #create textbox
    textbox = Text(root,font=("Helvetica", 10),state=DISABLED, 
                   yscrollcommand=scrollbar.set, wrap=WORD)
    textbox.grid(row=8, column=0, columnspan=3, sticky=N+S+W+E)
    scrollbar.config(command=textbox.yview)

    #Set up the redirection from terminal to the GUI window
    stdre = Redir(textbox)
    sys.stdout = stdre
    sys.stderr = stdre
    print("Hello, please enter job title and location\n")
    # Start the application mainloop
    root.mainloop()
    
InitGUI()