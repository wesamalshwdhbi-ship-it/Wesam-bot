import telebot

# --- بياناتك الشخصية المحدثة ---
API_TOKEN = '8449712362:AAGogl6fGVg07kAWi6ppafPClQ1dOVTMxds'
MY_GROUP_ID = -1005091383399  
MY_ADMIN_ID = 8201650441     

bot = telebot.TeleBot(API_TOKEN)

topic_to_client = {}
client_to_topic = {}

@bot.message_handler(content_types=['text', 'audio', 'voice', 'video', 'photo', 'document', 'location', 'contact'])
def handle_incoming_messages(message):
    # أولاً: إذا كانت الرسالة من داخل المجموعة (رد المهندس)
    if message.chat.id == MY_GROUP_ID:
        if message.is_topic_message:
            topic_id = message.message_thread_id
            if topic_id in topic_to_client:
                client_id = topic_to_client[topic_id]
                # إرسال رد المهندس للعميل في الخاص
                bot.copy_message(chat_id=client_id, from_chat_id=MY_GROUP_ID, message_id=message.message_id)
        return

    # ثانياً: إذا كانت الرسالة من العميل (في الخاص)
    client_id = message.chat.id
    
    # استثناء حسابك (وسام) لكي لا يفتح البوت ملفاً لنفسك
    if client_id == MY_ADMIN_ID:
        return

    # إذا كان العميل يراسل البوت لأول مرة، نفتح له "موضوع" (Topic)
    if client_id not in client_to_topic:
        user_name = message.from_user.first_name or "عميل جديد"
        try:
            new_topic = bot.create_forum_topic(MY_GROUP_ID, f"💼 {user_name}")
            topic_id = new_topic.message_thread_id
            client_to_topic[client_id] = topic_id
            topic_to_client[topic_id] = client_id
            
            # إشعار للمهندسين داخل الموضوع الجديد
            bot.send_message(MY_GROUP_ID, f"🔔 تم فتح ملف محادثة جديد للعميل: {user_name}", message_thread_id=topic_id)
        except Exception as e:
            print(f"Error: {e}")
            return

    # توجيه رسالة العميل إلى الموضوع المخصص له في المجموعة
    current_topic = client_to_topic.get(client_id)
    if current_topic:
        bot.copy_message(chat_id=MY_GROUP_ID, from_chat_id=client_id, message_id=message.message_id, message_thread_id=current_topic)

print("🚀 نظام المواضيع في مكتب المهندس وسام يعمل الآن...")
bot.polling(none_stop=True)
