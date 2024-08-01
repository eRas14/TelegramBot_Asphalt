import telebot
from telebot import types
from TOKEN import my_token

bot = telebot.TeleBot(my_token)

######ПОДСЧЕН АСФАЛЬТА:

#спрашиваем первую массу, держим ее и идем в функцию get_value2
def get_value1(message): 
    weight_P0 = bot.send_message(message.chat.id, text="Введите массу образца в сухом состоянии... P0 ")
    bot.register_next_step_handler(weight_P0, get_value2)
    
def get_value2(message): 
    global weight_P0
    weight_P0 = float(message.text) #переводим вводимый текст в текст с плавающей точкой
    weight_P1 = bot.send_message(message.chat.id, text="Введите массу образца на воздухе после 30мин. водонасыщения... P1 ")
    bot.register_next_step_handler(weight_P1, get_value3)

def get_value3(message): #спрашиваем третью массу массу, держим ее и идем в функцию get_value3
    global weight_P1
    weight_P1 = float(message.text)
    weight_P2 = bot.send_message(message.chat.id, text="Введите массу образца в воде после 30мин. водонасыщения... P2 ")
    bot.register_next_step_handler(weight_P2, get_value4)

def get_value4(message):
    global weight_P2
    weight_P2 = float(message.text)
    weight_P3 = bot.send_message(message.chat.id, text="Введите массу образца на воздуех после 1ч.30мин... P3")
    bot.register_next_step_handler(weight_P3, calculator_total)

def calculator_total(message): #Делаем расчет
    global weight_P3
    weight_P3 = float(message.text)
    V = weight_P1 - weight_P2
    W = ((weight_P3 - weight_P0) / (V)) * 100
    P_avg = weight_P0 / V
    bot.send_message(message.chat.id, f"\nОбъем = {round(V, 2)} гр/см3 \nСредняя плотность = {round(P_avg, 2)} гр/см3 \nВодонасыщение = {round(W, 1)} %") # Выводим результат
    



@bot.message_handler(commands=['start']) 
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Подсчет асфальта")
    markup.add(btn1)
    bot.send_message(message.chat.id, text=f"Приветсвую тебя, {message.from_user.first_name}!", reply_markup=markup)
                
                        
#Ловим текст, если текст совпал (а это кнопка, то идем в функцию get_value1)
@bot.message_handler(content_types=['text'])
def choose(message): #функция выббора кнопки
    if(message.text == "Подсчет асфальта"):
       get_value1(message)

                                  
@bot.message_handler(commands=['stop'])
def stop():
    sys.exit(0)

bot.polling()


