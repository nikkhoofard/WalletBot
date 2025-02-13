from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)

# Define states
SIGNUP, PHONE, PASSWORD = range(3)

user_information = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send sign-up button on /start"""
    signup_button = [[KeyboardButton("📝 Sign Up")]]
    reply_markup = ReplyKeyboardMarkup(
        signup_button,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        "Welcome! Tap below to register:",
        reply_markup=reply_markup
    )
    return SIGNUP

async def signup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Request phone number"""
    phone_button = [[KeyboardButton("📱 Share Phone", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(
        phone_button,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        "Please share your phone number:",
        reply_markup=reply_markup
    )
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store phone and request password"""
    phone = update.message.contact.phone_number
    context.user_data['phone'] = phone

    await update.message.reply_text(
        "Great! Now set your password (min 8 characters):",
        reply_markup=ReplyKeyboardRemove()
    )
    return PASSWORD


async def get_password(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate and store password"""
    password = update.message.text
    if len(password) < 8:
        await update.message.reply_text(
            "Password too short! Min 8 characters.")
        return PASSWORD

    context.user_data['password'] = password
    await complete_signup(update, context)
    return ConversationHandler.END


async def complete_signup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finalize registration"""
    user_data = context.user_data
    await update.message.reply_text(
        f"✅ Registration Complete!\n"
        f"Phone: {user_data['phone']}\n"
        f"Password: {'*' * len(user_data['password'])}"
    )

def main() -> None:
        application = Application.builder().token("7830109494:AAEVVc9ahVuuelyLsSoIJrxpc0eWRQON4FM").build()

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                SIGNUP: [MessageHandler(filters.Regex("^📝 Sign Up$"), signup)],
                PHONE: [MessageHandler(filters.CONTACT, get_phone)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                          get_password)]
            },
            fallbacks=[]
        )

        application.add_handler(conv_handler)
        application.run_polling()

if __name__ == "__main__":
        main()