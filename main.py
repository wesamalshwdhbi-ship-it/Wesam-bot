import telebot

# --- بياناتك الشخصية ---
API_TOKEN = '8449712362:AAGogl6fGVg07kAWi6ppafPClQ1dOVTMxds'
MY_GROUP_ID = -1005091383399  # سنغير هذا الرقم بعد قليل بالرقم الجديد
MY_ADMIN_ID = 8201650441     

bot = telebot.TeleBot(API_TOKEN)

topic_to_client = {}
client_to_topic = {}

# --- 1. كود كاشف الـ ID (المضاف حديثاً) ---
@bot.message_handler(commands=['getid'])
def get_group_id(message):
    group_id = message.chat.id
    bot.reply_to(message, f"✅ الـ ID الصحيح لهذه المجموعة هو:\n`{group_id}`\n\nانسخ هذا الرقم وضعه في الكود مكان MY_GROUP_ID")
    print(f"🚀 تم استخراج الـ ID بنجاح: {group_id}")

# --- 2. معالج الرسائل الأساسي ---
@bot.message_handler(content_types=['text', 'audio', 'voice', 'video', 'photo', 'document', 'location', 'contact'])
def handle_incoming_messages(message):
    # إذا كانت الرسالة من داخل المجموعة (رد المهندس)
    if message.chat.id == MY_GROUP_ID:
        if message.is_topic_message:
            topic_id = message.message_thread_id
            if topic_id in topic_to_client:
                client_id = topic_to_client[topic_id]
                bot.copy_message(chat_id=client_id, from_chat_id=MY_GROUP_ID, message_id=message.message_id)
        return

    # إذا كانت الرسالة من العميل (في الخاص)
    client_id = message.chat.id
    
    if client_id == MY_ADMIN_ID:
        return

    if client_id not in client_to_topic:
        user_name = message.from_user.first_name or "عميل جديد"
        try:
            new_topic = bot.create_forum_topic(MY_GROUP_ID, f"💼 {user_name}")
            topic_id = new_topic.message_thread_id
            client_to_topic[client_id] = topic_id
            topic_to_client[topic_id] = client_id
            bot.send_message(MY_GROUP_ID, f"🔔 تم فتح ملف محادثة جديد للعميل: {user_name}", message_thread_id=topic_id)
        except Exception as e:
            print(f"Error creating topic: {e}")
            return

    current_topic = client_to_topic.get(client_id)
    if current_topic:
        try:
            bot.copy_message(chat_id=MY_GROUP_ID, from_chat_id=client_id, message_id=message.message_id, message_thread_id=current_topic)
        except Exception as e:
            print(f"Error forwarding to group: {e}")

# --- 3. تشغيل البوت ---
print("🚀 البوت يعمل الآن.. بانتظار أمر /getid داخل المجموعة...")
bot.polling(none_stop=True)
