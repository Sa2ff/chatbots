import re
import dateparser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI
import os

from datetime import datetime  #the current time and date

# Set your OpenAI API key (ensure this is kept secure)
os.environ["OPENAI_API_KEY"] = "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"  # Replace with your actual API key




# Sample documents defined separately
doc1 = "Our office hours are from 8 AM to 6 PM, Monday to Saturday. We are closed on Sundays and public holidays."
doc2 = "For any inquiries, you can reach us at info@example.com or call us at (987) 654-3210 during business hours."
doc3 = "To schedule an appointment, please visit our website at www.example.com/appointments or call us at (987) 654-3210."
doc4 = "We provide a range of services including graphic design, web development, and digital marketing. For more details, check our services page at www.example.com/services."
doc5 = "Our office is located at 456 Elm Street, Suite 200, YourCity, YourState. We are easily accessible via public transport and have parking available for visitors."

# Combine documents into a list
DOCUMENTS = [doc1, doc2, doc3, doc4, doc5]

# Initialize OpenAI Chat Model
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Function for document search
def document_search(query):
    query = query.lower()
    for doc in DOCUMENTS:
        if query in doc.lower():
            return doc
    return "I'm sorry, I couldn't find any information related to that."

# Validate email and phone number functions
def validate_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

def validate_phone(phone):
    return re.match(r"^\d+$", phone)

# Collect user information
def collect_user_info(ask_for_appointment=False):
    user_info = {}
    user_info["name"] = input("What is your name? ")
    
    phone = input("What is your phone number? ")
    while not validate_phone(phone):
        print("Invalid phone number. Please try again.")
        phone = input("What is your phone number? ")
    user_info["phone"] = phone

    email = input("What is your email? ")
    while not validate_email(email):
        print("Invalid email. Please try again.")
        email = input("What is your email? ")
    user_info["email"] = email

    print(f"Thank you {user_info['name']}, we will contact you at {user_info['phone']} or {user_info['email']}.")

    # Handle appointment scheduling if needed
    if ask_for_appointment:
        appointment_datetime = collect_appointment_datetime()
        if appointment_datetime:
            print(f"Your appointment is scheduled for: {appointment_datetime}")

def collect_appointment_datetime():
    while True:
        user_input = input("Please provide the appointment date and time: ")
        parsed_datetime = dateparser.parse(user_input)
        if parsed_datetime:
            return parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print("Invalid date/time format. Please try again.")

# Get current date and time
def get_current_date_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Chatbot main function
def chatbot():
    print("Welcome to the Chatbot! How can I assist you today?")
    
    while True:
        user_query = input("You: ").strip()
        if user_query.lower() in ["exit", "bye", "quit"]:
            print("Goodbye! Have a great day!")
            break

        # Handle greetings
        if any(greeting in user_query.lower() for greeting in ["hello", "hi", "hey"]):
            print("Chatbot: Hello! How can I help you?")
            continue
        
        # Handle call requests and appointment bookings
        if "call me" in user_query.lower() or "book an appointment" in user_query.lower():
            print("I need to collect your information first.")
            collect_user_info(ask_for_appointment="book an appointment" in user_query.lower())
            continue
        
        # Handle current date and time queries
        if "current date" in user_query.lower():
            print(f"Chatbot: Current Date: {get_current_date_time()}")
            continue
        
        if "current time" in user_query.lower():
            print(f"Chatbot: Current Time: {get_current_date_time()}")
            continue
        
        # Search documents for other queries
        response = document_search(user_query)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot()