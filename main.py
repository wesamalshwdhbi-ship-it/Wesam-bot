import telebot

# --- بياناتك المحدثة بدقة ---
API_TOKEN = '8449712362:AAGogl6fGVg07kAWi6ppafPClQ1dOVTMxds'
MY_GROUP_ID = -5091383399    # تم تصحيح الرقم هنا
MY_ADMIN_ID = 8201650441     

bot = telebot.TeleBot(API_TOKEN)

# قواميس لحفظ الروابط بين العملاء والمواضيع (مؤقتة في الذاكرة)
topic_to_client = {}
client_to_topic = {}

@bot.message_handler(content_types=['text', 'audio', 'voice', 'video', 'photo', 'document', 'location', 'contact'])
def handle_incoming_messages(message):
    # 1. إذا كانت الرسالة قادمة من داخل المجموعة (رد المهندسين)
    if message.chat.id == MY_GROUP_ID:
        if message.is_topic_message:
            topic_id = message.message_thread_id
            if topic_id in topic_to_client:
                client_id = topic_to_client[topic_id]
                # إرسال الرد للعميل في الخاص
                bot.copy_message(chat_id=client_id, from_chat_id=MY_GROUP_ID, message_id=message.message_id)
        return

    # 2. إذا كانت الرسالة قادمة من عميل في الخاص
    client_id = message.chat.id
    
    # منع البوت من الرد على نفسه أو على الأدمن في الخاص إذا لم يكن عميلاً
    if client_id == MY_ADMIN_ID and not message.text.startswith('/'):
        pass 

    if client_id not in client_to_topic:
        user_name = message.from_user.first_name or "عميل جديد"
        try:
            # محاولة إنشاء موضوع جديد في المجموعة
            new_topic = bot.create_forum_topic(MY_GROUP_ID, f"💼 {user_name}")
            topic_id = new_topic.message_thread_id
            
            # ربط العميل بالموضوع
            client_to_topic[client_id] = topic_id
            topic_to_client[topic_id] = client_id
            
            bot.send_message(MY_GROUP_ID, f"🔔 طلب جديد من: {user_name}\nيمكنكم الرد عليه هنا مباشرة.", message_thread_id=topic_id)
            
            # رسالة ترحيبية للعميل
            bot.send_message(client_id, "أهلاً بك في مكتب المهندس وسام. تم استلام رسالتك وسيتم الرد عليك من قبل الفريق المختص قريباً.")
            
        except Exception as e:
            print(f"Error creating topic: {e}")
            return

    # توجيه رسالة العميل إلى الموضوع الخاص به في المجموعة
    current_topic = client_to_topic.get(client_id)
    if current_topic:
        bot.copy_message(chat_id=MY_GROUP_ID, from_chat_id=client_id, message_id=message.message_id, message_thread_id=current_topic)

print("🚀 البوت يعمل الآن بنظام المواضيع المحدث...")
bot.polling(none_stop=True)
