import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from revChatGPT.V1 import Chatbot
from Bard import Chatbot as BardChatbot  
import asyncio
import nest_asyncio
from EdgeGPT.EdgeGPT import Chatbot as EdgeGPTChatbot, ConversationStyle  # Import EdgeGPT Chatbot here
import json
nest_asyncio.apply()

async def main():
    global edgegpt_chatbot

    try:
        cookies = json.loads(open("./bing_cookies.json", encoding="utf-8").read())  # might omit cookies option
        bot = await EdgeGPTChatbot.create(cookies=cookies) # Passing cookies is "optional", as explained above
        edgegpt_chatbot = bot
    except Exception as e:
        # Code to handle the exception
        # ...
        print("An error occurred:", str(e))

chatbot = Chatbot(config={
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ0b3ByYWtkaWtpY2kyOEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1jV0RnZHBNcEVzRUNCRW1hbkNKUUF6cVgifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAwMjE2MDM2MTI1MjkzODg3OTgwIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4NzM3NTc3NCwiZXhwIjoxNjg4NTg1Mzc0LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSJ9.KZlxR_JV7VN1ZVntY-U1PiusuaTd97zcx76rNf1fUbTRGD6XWrVWxuuOzlc3VWJOyZJM1gLBy81x6K8UWMcW2GU_PB5r0y4phGzUqfxtGQ-zDHJG_vFsqGcUi8zSmKJYnKgG-Y93sF1UbCe65vlCJYGbDgCcdbyDm27YLPTb1ICXL_GLE9gidlnFGWr8xqOZHpOoBdpoBICsfD_9tsvfFBJX61ddwfw-vklGeO07lNzFfeu-U-V75QbiQ6Odv_gc3uRFBzH0tp-y1s4-14f_c1NBrBVWUTULiPionMjqwk2ZnOMdGnHjf-CxX3V3BiBvDdycluLD7ekpnpqJddFFxA"
})
bard_chatbot = BardChatbot('XwgW_acRABspPmraM4tM_2cVAUHZL_omG8qkrdFynK-F702iQxdRGhQ7D6m93FLA_1E6Jw.')  # replace with your Bard token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Hello! I'm a bot that can use several AI models. Here's what I can do:\n\n"

    message += "🤖 /gpt [message] - Ask GPT-3 a question or give it a prompt\n"
    message += "🧠 /gpt4 [message] - Ask GPT-4 a question or give it a prompt\n"
    message += "🎭 /bard [message] - Interact with the Bard AI\n"
    message += "🌐 /edge_precise [message] - Ask EdgeGPT a question with precise conversation style\n"
    message += "🎨 /edge_creative [message] - Ask EdgeGPT a question with creative conversation style\n"
    message += "⚖️ /edge_balanced [message] - Ask EdgeGPT a question with balanced conversation style\n"
    message += "💻 /edge_precise_webpage [URL] [message] - Ask EdgeGPT a question related to a webpage with precise conversation style\n"
    message += "🖌️ /edge_creative_webpage [URL] [message] - Ask EdgeGPT a question related to a webpage with creative conversation style\n"
    message += "🔮 /edge_balanced_webpage [URL] [message] - Ask EdgeGPT a question related to a webpage with balanced conversation style\n"

    message += "\nRemember to replace [message] with your question or prompt, and [URL] with a webpage URL if using a webpage-related command."

    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def gpt(update: Update, context, model):
    message = ' '.join(context.args)
    logging.info(f"Asking ChatGPT with message: {message}")
    conversation_id = context.user_data.get('conversation_id', None)
    parent_id = context.user_data.get('parent_id', None)
    
    for data in chatbot.ask(message, model=model, conversation_id=conversation_id, parent_id=parent_id):
        chatgpt_response = data["message"]
        if "conversation_id" in data:
            context.user_data["conversation_id"] = data["conversation_id"]
        if "parent_id" in data:
            context.user_data["parent_id"] = data["parent_id"]
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=chatgpt_response)

async def gpt3(update: Update, context):
    await gpt(update, context, model='gpt-3')

async def gpt4(update: Update, context):
    await gpt(update, context, model='gpt-4')

async def bard(update: Update, context):
    message = ' '.join(context.args)
    logging.info(f"Asking Bard with message: {message}")
    bard_response = bard_chatbot.ask(message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=bard_response["content"])
async def edgegpt(update: Update, context, style, webpage_context=None):
    message = ' '.join(context.args)
    logging.info(f"Asking EdgeGPT with message: {message}")
    response = await edgegpt_chatbot.ask(message, conversation_style=style, webpage_context=webpage_context, simplify_response=True)
    edgegpt_response = response['text']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=edgegpt_response)

async def edgegpt_precise(update: Update, context):
    await edgegpt(update, context, style=ConversationStyle.precise)

async def edgegpt_creative(update: Update, context):
    await edgegpt(update, context, style=ConversationStyle.creative)

async def edgegpt_balanced(update: Update, context):
    await edgegpt(update, context, style=ConversationStyle.balanced)

async def edgegpt_precise_webpage(update: Update, context):
    webpage_context = context.args[0]
    message = ' '.join(context.args[1:])
    await edgegpt(update, context, style=ConversationStyle.precise, webpage_context=webpage_context)

async def edgegpt_creative_webpage(update: Update, context):
    webpage_context = context.args[0]
    message = ' '.join(context.args[1:])
    await edgegpt(update, context, style=ConversationStyle.creative, webpage_context=webpage_context)

async def edgegpt_balanced_webpage(update: Update, context):
    webpage_context = context.args[0]
    message = ' '.join(context.args[1:])
    await edgegpt(update, context, style=ConversationStyle.balanced, webpage_context=webpage_context)

if __name__ == '__main__':
    asyncio.run(main())
    application = ApplicationBuilder().token('6134739622:AAH9QitAz348jAyz_5f32G9j9axKevLSluk').build()
    
    start_handler = CommandHandler('start', start)
    gpt3_handler = CommandHandler('gpt', gpt3)
    gpt4_handler = CommandHandler('gpt4', gpt4)
    bard_handler = CommandHandler('bard', bard)
    
    edge_precise_handler = CommandHandler('edge_precise', edgegpt_precise)
    edge_creative_handler = CommandHandler('edge_creative', edgegpt_creative)
    edge_balanced_handler = CommandHandler('edge_balanced', edgegpt_balanced)
    
    edge_precise_webpage_handler = CommandHandler('edge_precise_webpage', edgegpt_precise_webpage)
    edge_creative_webpage_handler = CommandHandler('edge_creative_webpage', edgegpt_creative_webpage)
    edge_balanced_webpage_handler = CommandHandler('edge_balanced_webpage', edgegpt_balanced_webpage)
    
    application.add_handler(start_handler)
    application.add_handler(gpt3_handler)
    application.add_handler(gpt4_handler)
    application.add_handler(bard_handler)
    
    application.add_handler(edge_precise_handler)
    application.add_handler(edge_creative_handler)
    application.add_handler(edge_balanced_handler)
    
    application.add_handler(edge_precise_webpage_handler)
    application.add_handler(edge_creative_webpage_handler)
    application.add_handler(edge_balanced_webpage_handler)

    application.run_polling()
