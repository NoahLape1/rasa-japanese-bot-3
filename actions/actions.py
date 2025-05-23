# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import Restarted
import smtplib
import os

# Runs if bot does not understand user's input
class ActionDefaultAskAffirmation(Action):

   def name(self):
       return "action_default_ask_affirmation"

   async def run(self, dispatcher, tracker, domain):
       print("in ActionDefaultAskAffirmation!!!")
	
       # Last thing user typed
       lastOutput = tracker.latest_message['text']
       # Gets the user's last intent by extracting it from tracker dict
       # lastUserIntentDictionary = tracker.latest_message['intent']
       
       #lastUserIntent = list(lastUserIntentDictionary.values())[1]
       #print("Last USER intent: " + lastUserIntent)
       #lastBotQuestion = tracker.latest_action_name
       #print(lastBotQuestion)
        
       # Gets last output of bot (last question that bot asked user)
       for event in tracker.events:
           if (event.get("event") == "bot"):
               lastBotMessage = event.get("text")
       print(lastBotMessage)
       
       # triggers different rules based on last bot question
       if lastBotMessage == "何時におきますか？":
           return [FollowupAction("activate_p1")]
       elif lastBotMessage == "何時にあさごはんをたべますか？":
           return [FollowupAction("activate_p2")]
       elif lastBotMessage == "何時にがっこうにいきますか？":
           return [FollowupAction("activate_p3")]
       elif lastBotMessage == "何時にひるごはんをたべますか？":
           return [FollowupAction("activate_p4")]
       elif lastBotMessage == "何時にいえにかえりますか？":
           return [FollowupAction("activate_p5")]
       elif lastBotMessage == "何時にばんごはんをたべますか？":
           return [FollowupAction("activate_p6")]
       elif lastBotMessage == "何時にテレビをみますか？":
           return [FollowupAction("activate_p7")]   
       elif lastBotMessage == "何時にねますか？":
           return [FollowupAction("activate_p8")]   
       elif lastBotMessage == "おなまえは？":
           return [FollowupAction("activate_p0")]   
       # Fallback for if the bot doesn't understand the receipient's name for the email or the email address
       elif "Please type the name of the person you want to email." in lastBotMessage:
           dispatcher.utter_message('The person you want to email is ' + lastOutput)
           SlotSet("recipient", lastOutput)
           return [FollowupAction("after_handle_did_not_understand_answer")]
       elif "Please enter the email address of the person you want to email." in lastBotMessage:
           dispatcher.utter_message('The email address is ' + lastOutput)
           SlotSet("email", lastOutput)
           return [FollowupAction("after_handle_did_not_understand_answer")]
       else:
           dispatcher.utter_message(text="すみません、わかりません。 Sorry, I don't quite understand (,,>﹏<,,).", image = "https://media.tenor.com/-caxkmc867EAAAAC/mochi-cat.gif")
           return [FollowupAction("after_handle_did_not_understand_answer")]

# Followup action from ActionDefaultAskAffirmation that
# generates the bot's next response        
class AfterHandleDidNotUnderstandAnswer(Action):

    def name(self) -> Text:
        return "after_handle_did_not_understand_answer"

    def run(self, dispatcher, tracker, domain):
        print("in AfterHandleDidNotUnderstandAnswer")
        
        # dispatcher.utter_message('We bonked at the beginning, so do not have any valid slots I can use to make bot look smart.  Ohe well.  Let us just resume the story with student asking bot a question.')

        # Gets last output of bot (based on dispatcher.utter_message from ActionDefaultAskAffirmation)
        for event in tracker.events:
            if (event.get("event") == "bot"):
                lastBotMessage = event.get("text")
        print(lastBotMessage)

        # Gets the user's last intent by extracting it from tracker dict
        lastUserIntentDictionary = tracker.latest_message['intent']
        lastUserIntent = list(lastUserIntentDictionary.values())[0]

	# Asks user for to ask bot a question
        # The lastBotMessage is coming from the ActionDefaultAskAffirmation
        # and these if/elif statements are checking what the bot last said
        # and using substrings of the last message to identify what the bot says next
        
        # Fallback for if the bot doesn't understand the receipient's name for the email or the email address
        if "The person you want to email is" in lastBotMessage:
            dispatcher.utter_message('Great. Now we need their email.')
        elif "The email address is" in lastBotMessage:
            dispatcher.utter_message('Thank you for the information.')
        # else
        else:
            dispatcher.utter_message("I am a simple bot. Please rephrase.")
        
        print(lastUserIntent)
        return [Restarted()]

#Create action to log conversation, each time called will capture last bot output
class LogConversationBot(Action):
  
    def name(self) -> Text:
         # Name of the action
        return "log_conversation_bot"
  
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
	
	# Get last conversation for bot
        for event in tracker.events:
            if (event.get("event") == "bot"):
                lastBotMessage = "Bot message: " + event.get("text")

        print("Last bot message: " + lastBotMessage)

        # Creates/Open function to open the file "conversation_[senderID].txt" 
        # with the senderID being unique to each user
        uniqueFile = "conversationLogs/conversation_" + tracker.sender_id + ".txt"
        conversation_txt = open(uniqueFile,"a")


        conversation_log_bot = "\n" + lastBotMessage 
        
        # write latest conversations to txt file
        conversation_txt.write(conversation_log_bot)

        conversation_txt.close()

#Create action to log conversation, each time called will capture last user response
class LogConversationUser(Action):
  
    def name(self) -> Text:
         # Name of the action
        return "log_conversation_user"
  
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
	
        # print last user message
        print("Last user message: " + tracker.latest_message.get("text"))


        # Creates/Open function to open the file "conversation_[senderID].txt" 
        # with the senderID being unique to each user
        uniqueFile = "conversationLogs/conversation_" + tracker.sender_id + ".txt"
        conversation_txt = open(uniqueFile,"a")

        # Get last conversation from user
        conversation_log_user = tracker.latest_message.get("text")
        
        # write latest conversations to txt file
        conversation_txt.write("\nUser message: " + conversation_log_user)
        conversation_txt.close()         


# Action to create text file with information to send email
class CollectEmailInfo(Action):
  
   def name(self) -> Text:
        # Name of the action
       return "collect_email_info"
  
   def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       # Get last conversation from user
       conversation_log_user = tracker.latest_message.get("text")

       # Extracting user name, recipient of email name, and email address
       # Gets the user's last intent by extracting it from tracker dict
       lastUserIntentDictionary = tracker.latest_message['intent']
       lastUserIntent = list(lastUserIntentDictionary.values())[0]

       if "inform_recipient" in lastUserIntent:
           emailFile = "emailInfo/emailInfo_" + tracker.sender_id + ".txt"
           email_txt = open(emailFile,"a")
           email_txt.write(conversation_log_user +"\n")
            

       emailAd = ''
       if "inform_email" in lastUserIntent:
           print("intent is inform email")
           emailFile = "emailInfo/emailInfo_" + tracker.sender_id + ".txt"
           email_txt = open(emailFile,"a")
           words = conversation_log_user.split()
           for word in words:
               if "@" in word:
                   email_txt.write(word + "\n")
       email_txt.close()


# Creating new class to send emails.
class ActionEmail(Action):
  
    def name(self) -> Text:
         # Name of the action
        return "action_email"
  
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Tracker message log
        # message_log = tracker.latest_message['text']
        # conversation_log = str(tracker.get_slot("conversation_log"))        

        # Getting the data stored in the
        # slots and storing them in variables.
        # these are for the person RECIEVING the mail

        emailFile = "emailInfo/emailInfo_" + tracker.sender_id + ".txt"
        email_txt = open(emailFile,"r") 

        name = tracker.get_slot("name")
        recipient = email_txt.readline()
        email_id = email_txt.readline()
 
        email_txt.close()        
        
        # recipient = tracker.get_slot("recipient")
        # email_id = tracker.get_slot("email")
        # name = tracker.get_slot("name")
        # recipient = "Leah"
        # email_id = "goldberl@dickinson.edu"
          
        # Code to send email
        # Creating connection using smtplib module
        s = smtplib.SMTP('localhost')
          
        # Making connection secured
        s.starttls() 
         
        # Authentication
        # s.login("goldberl@dickinson.edu")

        
        # Open the file "conversation_[senderID].txt" 
        # with the senderID being unique to each user
        uniqueFile = "conversationLogs/conversation_" + tracker.sender_id + ".txt"
        conversation_txt = open(uniqueFile,"r")

        conversation_log = ''
        # Using for loop
        for line in conversation_txt:
            conversation_log = conversation_log + line +'\n'
    
        # Closing files
        conversation_txt.close()
          
        # Message to be sent
        # Ideally we would like to say who this conversation is from which can be extracted 
        # from the NAME slot if the bot did not delete all the slots
        # But the bot sometimes deletes all the slots
        # One way we can fix this is storing the user's name in a text file and reading it
        # Additionally, to ensure the bot understands the email address, we can put that in a 
        # txt file as well and read it
        message = "Subject: Japanese Chatbot Message Log\n\n Hello {} \n\nThis is a message from the RASA Japanese chatbot!\n\nRegards,\nThe Dickinson College RASA Japanese Chatbot".format(recipient) + "\n\nPlease find the message log below for the conversation: \n" + conversation_log
        
	# The email address below is the person who is SENDING the mail  
        # Sending the mail
        s.sendmail("academictechnology@dickinson.edu",email_id, message.encode("utf8"))
        s.sendmail("academictechnology@dickinson.edu","bryantt@dickinson.edu", message.encode("utf8")) #This line sends the email to Todd always
          
        # Closing the connection
        s.quit()

        # Delete contents of conversation_[senderID].txt
        uniqueFile = "conversationLogs/conversation_" + tracker.sender_id + ".txt"
        if os.path.exists(uniqueFile):
            os.remove(uniqueFile)
            # Confirmation message
            dispatcher.utter_message(text="Email has been sent.")
        
        emailFile = "emailInfo/emailInfo_" + tracker.sender_id + ".txt"
        if os.path.exists(emailFile):
            os.remove(emailFile)          

        return []
       

# Creating new class to send emails.
class DeleteConversationTxt(Action):
  
    def name(self) -> Text:
         # Name of the action
        return "action_delete_conversation_txt"
  
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Delete contents of conversation.txt
        uniqueFile = "conversationLogs/conversation_" + tracker.sender_id + ".txt"
        uniqueFileTwo = "conversationLogs/questionCounter_" + tracker.sender_id + ".txt"
        if os.path.exists(uniqueFile):
            os.remove(uniqueFile)
        if os.path.exists(uniqueFileTwo):
            os.remove(uniqueFileTwo)
        return []

class ActionCheckNumQuestions(Action):
# 8 questions currently
    def name(self) -> Text:
        return "action_check_numQ"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
	domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #keeps a counter in a text file of how many questions were asked.
        
        uniqueFile = "conversationLogs/questionCounter_" + tracker.sender_id + ".txt"
        question_txt = open(uniqueFile, "r")
        num_q=question_txt.read()
        question_txt.close()

        if int(num_q) < 7:
            question_txt = open(uniqueFile, "w")
            nextWrite=int(num_q)+1
            question_txt.write(str(nextWrite))
            question_txt.close()
            question_txt = open(uniqueFile, "r")
            num_q = question_txt.read()
            question_txt.close()
            dispatcher.utter_message(text="You asked " + num_q + " questions")
            print("NumQ after adding 1:　" + num_q)
            num_qTwo=int(num_q)

        else:
            print("User asked " + str(num_q))
            dispatcher.utter_message(text="You asked 8 questions. You're finished!")
            num_qTwo=int(num_q)
            question_txt = open(uniqueFile, "w")
            question_txt.write("0")
            question_txt.close()
            return [FollowupAction("utter_askifsendemail")]

        # return[] we aren't really returning anything
        

class ActionMakeFile(Action):
# this custom action makes it so that we initialize a file to write to for counting questions
    def name(self) -> Text:
        return "action_make_file"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
	domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
	
        uniqueFile = "conversationLogs/questionCounter_" + tracker.sender_id + ".txt"
        #conversation_txt = open(uniqueFile,"r") Refrence code to help with formatting
       	question_txt = open(uniqueFile, "w")
        question_txt.write("0")
        question_txt.close()

class ActionActivatePart1(Action):
    def name(self) -> Text:
        return "activate_p1"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Activating part 1 of the conversation")
        return[]

class ActionActivatePart2(Action):
    def name(self) -> Text:
        return "activate_p2"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Activating part 2 of the conversation")
        return[]

class ActionActivatePart3(Action):
    def name(self) -> Text:
        return "activate_p3"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Activating part 3 of the conversation")
        return[]


class ActionActivatePart4(Action):
    def name(self) -> Text:
        return "activate_p4"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Activating part 4 of the conversation")
        return[]

class ActionActivatePart5(Action):
    def name(self) -> Text:
        return "activate_p5"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Activating part 5 of the conversation")
        return[]

class ActionActivatePart6(Action):
    def name(self) -> Text:
        return "activate_p6"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Activating part 6 of the conversation")
        return[]

class ActionActivatePart7(Action):
    def name(self) -> Text:
        return "activate_p7"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Activating part 7 of the conversation")
        return[]

class ActionActivatePart8(Action):
    def name(self) -> Text:
        return "activate_p8"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Activating part 8 of the conversation")
        return[]

class ActionActivatePart8(Action):
    def name(self) -> Text:
        return "activate_p0"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Activating part 0 of the conversation")
        return[]

# class ActionTest(Action):
#
#     def name(self) -> Text:
#         return "action_test"
#
#     def run(self, dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         print("HELLO this is a test action")
#         return[]
