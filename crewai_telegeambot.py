import telebot
from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

# Replace ‘YOUR_API_TOKEN’ with the API token you received from the BotFather
API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
bot = telebot.TeleBot(API_TOKEN)

llm =Ollama(model="llama3")

math_agent = Agent(
  role = "Math Professor",
  goal = """ Provide the solution to the students that are asking for mathematical
           questions and give them the answer.""",
  backstory = """ You are an excellent math professor that likes to solve math questions in a way that everyone can understand your solution""",
  allow_delegation = False,
  verbose = True,
  llm = llm
)

story_agent = Agent(
  role = "Stroy Writer",
  goal = """ Create the small story for the kids with the mathematical answer.""",
  backstory = """ You are an creative fictional story writer and create interesting story for given mathemetical answer in a way that everyone can like it""",
  allow_delegation = False,
  verbose = True,
  llm = llm
)

# Task
task = Task(
    description=("{topic}"), 
    expected_output='Step by step processes',
    agent = math_agent)

task2 = Task(
    description="Teach given mathematical answers to kids with small fictional story with 5 to 6 lines", 
    expected_output='creative fictional story',
    agent = story_agent)

crew = Crew(
  agents=[math_agent, story_agent ],
  tasks=[task, task2],
  verbose=2
)

# Define a message handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.text)
    inputs = {"topic":message.text}
    result = crew.kickoff(inputs=inputs)
    bot.reply_to(message, result)

# Start the bot
bot.polling()   