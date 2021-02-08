import telegram
import config
TOKEN = config.token
bot = telegram.Bot(TOKEN)

def get_last_update_id(updates):
    """Возвращает ID последнего апдейта"""
    id_list = list() 
    for update in updates: 
        id_list.append(update["update_id"])
    return(max(id_list))

def solution():
    q = last_message_text.split()
    for i in range(4):
        q[i]=int(q[i])
    if q[0]==q[2]:
        if q[1]==q[3]:
            return "прямые совпадают"
        else:
            return "прямые параллельны"
    else:
        x = (q[3]-q[1])/(q[0]-q[2])
        y = q[0]*x + q[1]
        return str(x) + " " + str(y)
    
    

last_update_id = None
while True:
    updates = bot.getUpdates(last_update_id, timeout=100)
    if len(updates) > 0:
        last_update_id = get_last_update_id(updates) + 1
        for update in updates: # сообщения могут приходить быстро, быстрее, чем работает код
            try:
                last_message = update["message"] # взяли из него сообщение
                last_message_text = last_message['text'] # из сообщения - текст
                last_chat_id =  last_message['chat']['id'] # и идентификатор чата
                bot.sendMessage(last_chat_id, solution())
                
            except:
                last_message = update["edited_message"]
                last_message_text = last_message['text'] # из сообщения - текст
                last_chat_id =  last_message['chat']['id'] # и идентификатор чата
                bot.sendMessage(last_chat_id, last_message_text[::-1]) # отправили обратно последнее
                                                                   # сообщение задом наперёд   
