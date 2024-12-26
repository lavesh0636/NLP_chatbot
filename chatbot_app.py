import streamlit as st
import spacy
import random
import subprocess
import sys

# Function to install spaCy model
def install_model():
    try:
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
    except Exception as e:
        print(f"An error occurred while installing the model: {e}")

# Call the function to ensure the model is installed
install_model()
# Responses dictionary

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
responses = {
    ("course", "classes", "courses offered", "study", "learn", "training"): (
        "We offer several UI/UX design courses, including Fundamentals of UX, Advanced UI Design, and Prototyping.",
        "Our programs cover topics like Interaction Design, Usability Testing, and Design Thinking.",
        "You can learn wireframing, user research, and responsive design in our advanced courses."
    ),
    ("enroll", "admission", "apply", "how to join", "register", "sign up"): (
        "To enroll, visit our website and complete the application form.",
        "Admissions are open year-round. Contact us if you need assistance.",
        "Joining is simple! Fill out the form online, and our team will guide you through the process."
    ),
    ("support", "help", "mentorship", "resources", "assist", "guidance"): (
        "We provide detailed course materials, access to mentors, and industry expert guidance.",
        "Our support resources include live Q&A sessions, project feedback, and community discussions.",
        "If you need help, our mentors are available to support you throughout the program."
    ),
    ("agent", "representative", "talk to human", "person", "real person"): (
        "I'll connect you to a human representative. Please hold on.",
        "Let me transfer you to a live agent who can assist further.",
        "A customer service representative will join shortly to address your query."
    ),
    ("feedback", "suggestion", "rate", "review", "opinion"): (
        "We appreciate your feedback! Please share your thoughts so we can improve.",
        "Your suggestions are valuable to us. Let us know how we can serve you better.",
        "Thank you for your feedback! It helps us enhance your experience."
    ),
    ("schedule", "timing", "class time", "batch", "when", "time"): (
        "Our classes run Monday to Friday, with weekend workshops available for working professionals.",
        "Check our website for a detailed schedule of upcoming batches and timings.",
        "We offer flexible schedules to accommodate your needs."
    ),
    ("fees", "cost", "price", "payment"): (
        "Our courses are priced competitively, with scholarships and installment plans available.",
        "The fees vary by program. Visit the fee structure section on our website for details.",
        "We offer flexible payment options to make learning accessible to everyone."
    ),
    ("certificate", "certification", "credential", "diploma"): (
        "Yes, we provide certifications upon course completion, recognized in the industry.",
        "All our programs come with a certificate of excellence to boost your career.",
        "You'll receive a professional certification once you complete the course."
    ),
    ("hi", "hello", "hey", "hola", "greetings", "good morning", "good afternoon", "good evening"): (
        "Hello! How can I help you today? 👋",
        "Hi there! Welcome to UI/UX Academy. What would you like to know?",
        "Hey! I'm here to help you with information about our UI/UX courses."
    ),
    ("bye", "goodbye", "see you", "farewell", "thanks", "thank you", "cya"): (
        "Goodbye! Feel free to come back if you have more questions! 👋",
        "Thanks for chatting! Have a great day!",
        "Bye! Hope I was able to help you today!"
    ),
    "default": (
        "I apologize, but I can only provide information about our UI/UX courses, admissions, schedules, and related topics. "
        "For other queries, please contact our support team.",
        "I'm specialized in UI/UX Academy related information only. "
        "Could you please ask something about our courses, admissions, or program details?",
        "I'm not able to provide information about that topic. "
        "I can help you with questions about our UI/UX courses, fees, schedules, and certifications."
    )
}

def most_similar_response(user_input):
    # Tokenize user input
    user_doc = nlp(user_input.lower())  # Convert to lowercase for better matching
    max_similarity = -1
    best_response = None

    for query_key, response in responses.items():
        if not isinstance(query_key, tuple):
            query_key = [query_key]

        for query in query_key:
            similarity = user_doc.similarity(nlp(query))
            if similarity > max_similarity:
                max_similarity = similarity
                best_response = random.choice(response) if isinstance(response, tuple) else response

    # Set a threshold for similarity to better handle off-topic queries
    if max_similarity < 0.5:  # You can adjust this threshold
        best_response = random.choice(responses["default"])

    return best_response

# Configure Streamlit page
st.set_page_config(
    page_title="UI/UX Academy Chatbot",
    page_icon="💬"
)

# Add custom CSS
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display header
st.title("UI/UX Academy Chatbot 💬")
st.markdown("Welcome! Ask me anything about our UI/UX courses.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    response = most_similar_response(prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
