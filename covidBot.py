import telebot
import config
import COVID19Py

# Creating 'bot' and 'covid' variables

bot = telebot.TeleBot(config.TOKEN)
covid19 = COVID19Py.COVID19()


# Start message handler

@bot.message_handler(commands=['start'])
def start(message):
    send_message = f"<b>Hello {message.from_user.first_name}!</b>\nI'm here to show you latest statistics " \
                 f"information about the COVID-19 virus spread.\n<i>How can you interact with me? Oh, it's very simple!</i>\n- Type the " \
                 f"country name to receive statistics on specific country.\n- Type <b>'latest'</b> or <b>'general'</b> " \
                 f"for overall statistics information.\n- Type <b>'info'</b> if you want to know more about me.\n" \
                 f"- Type <b>'disclaimer'</b> for disclaimer information\n" \
                 f"NOTE: This bot version supports only <b>text</b> format messages."

    bot.send_message(message.chat.id, send_message, parse_mode='html')


# Message handler when input not equals 'text' content type

@bot.message_handler(content_types=['photo', 'audio', 'document', 'stickers'])
def other(message):
    other_message = "This bot version supports only <b>text</b> format messages. Sorry!"

    bot.send_message(message.chat.id, other_message, parse_mode='html')


# Message handler for 'text' inputs

@bot.message_handler(content_types=['text'])
def send_text(message):

    # Creating a dictionary with 'country name' as 'key' and 'country code' as 'value'

    c_key_list = []
    c_value_list = []
    countries = covid19.getLocations()

    for cntry in countries:
        key = cntry['country']
        value = cntry['country_code']
        c_key_list.append(key.lower())
        c_value_list.append(value)

    final_dict = dict(zip(c_key_list, c_value_list))

    # Creating lists for multiple inputs

    hello_dict = ['hi', 'hello', 'howdy', 'good morning', 'good evening', 'good afternoon']
    bye_dict = ['bye', 'good bye', 'see you', 'see ya', 'close']
    usa_dict = ['usa', 'united states']
    gb_dict = ['great britain', 'gb']
    latest_dict = ['latest', 'general']

    # Verifying 'hello' salute inputs

    if message.text.lower() in hello_dict:
        result = f"<b>Hello {message.from_user.first_name}!</b>\nI'm here to show you latest statistics " \
                 f"information about the COVID-19 virus spread.\n<i>How can you interact with me? Oh, it's very simple!</i>\n- Type the " \
                 f"country name to receive statistics on specified country.\n- Type <b>'latest'</b> or <b>'general'</b> " \
                 f"for overall statistics information.\n- Type <b>'info'</b> if you want to know more about me."

    # Verifying 'bye' salute inputs

    elif message.text.lower() in bye_dict:
        result = "Good bye! Keep safe!"

    # Checking countries as input

    elif message.text.lower() in final_dict.keys():
        c_name = ""
        c_population = ""
        c_confirmed = ""
        c_deaths = ""
        c_update_all = ""
        for k, v in final_dict.items():
            if k == message.text.lower():
                res = covid19.getLocationByCountryCode(v)
                for elem in res:
                    c_name = elem['country']
                    c_population = elem['country_population']
                    c_update = elem['last_updated']
                    c_update_date = c_update[:10]
                    c_update_time = c_update[11:16]
                    c_update_all = c_update_date + " " + c_update_time
                    c_latest = elem['latest']
                    c_confirmed = c_latest['confirmed']
                    c_deaths = c_latest['deaths']

        result = f"<b>Statistics for {c_name}:</b>\nPopulation: {c_population} people" \
                 f"\nLatest update: {c_update_all}\n<b>Confirmed cases: {c_confirmed}\nDeaths: {c_deaths}</b>"

    # Checking for USA country inputs

    elif message.text.lower() in usa_dict:
        c_usa_name = ""
        c_usa_population = ""
        c_usa_confirmed = ""
        c_usa_deaths = ""
        c_usa_update_all = ""
        res = covid19.getLocationByCountryCode("US")
        for elem in res:
            c_usa_name = elem['country']
            c_usa_population = elem['country_population']
            c_usa_update = elem['last_updated']
            c_usa_update_date = c_usa_update[:10]
            c_usa_update_time = c_usa_update[11:16]
            c_usa_update_all = c_usa_update_date + " " + c_usa_update_time
            c_usa_latest = elem['latest']
            c_usa_confirmed = c_usa_latest['confirmed']
            c_usa_deaths = c_usa_latest['deaths']

        result = f"<b>Statistics for {c_usa_name}:</b>\nPopulation: {c_usa_population} people" \
                 f"\nLatest update: {c_usa_update_all}\n<b>Confirmed cases: {c_usa_confirmed}\nDeaths: {c_usa_deaths}</b>"

    # Checking for GB country inputs

    elif message.text.lower() in gb_dict:
        c_gb_name = ""
        c_gb_population = ""
        c_gb_confirmed = ""
        c_gb_deaths = ""
        c_gb_update_all = ""
        res = covid19.getLocationByCountryCode("GB")
        for elem in res:
            c_gb_name = elem['country']
            c_gb_population = elem['country_population']
            c_gb_update = elem['last_updated']
            c_gb_update_date = c_gb_update[:10]
            c_gb_update_time = c_gb_update[11:16]
            c_gb_update_all = c_gb_update_date + " " + c_gb_update_time
            c_gb_latest = elem['latest']
            c_gb_confirmed = c_gb_latest['confirmed']
            c_gb_deaths = c_gb_latest['deaths']

        result = f"<b>Statistics for {c_gb_name}:</b>\nPopulation: {c_gb_population} people" \
                 f"\nLatest update: {c_gb_update_all}\n<b>Confirmed cases: {c_gb_confirmed}\nDeaths: {c_gb_deaths}</b>"

    # Checking for 'info' input

    elif message.text.lower() == "info":
        result = "- my name: <b>COVID-19 statistics bot</b>\n- my version: 0.1 (beta)\n- my creator: Valeriy B.\n" \
                 "- why created: test project\n- statistics data public API: https://coronavirus-tracker-api.herokuapp.com/v2/locations" \
                 "\n- programming language: Python\n- contact: @valeriybercha"

    # Checking for 'disclaimer' input

    elif message.text.lower() == "disclaimer":
        result = "The data found here has been produced and processed based on public " \
                 "API - https://coronavirus-tracker-api.herokuapp.com/v2/locations, no warranty expressed or implied" \
                 "is made regarding accuracy, adequacy, completeness, legality, reliability or usefulness of any " \
                 "information."

    # Checking 'latest' input

    elif message.text.lower() in latest_dict:
        var_res = covid19.getAll()
        var_latest = var_res['latest']
        var_confirmed = var_latest['confirmed']
        var_deaths = var_latest['deaths']

        result = f"General statistics:\n<b>Confirmed cases: {var_confirmed}\nDeaths: {var_deaths}</b>"

    # Checking for mistyped input

    else:
        result = "Ooops! Something went wrong! Try again!"

    bot.send_message(message.chat.id, result, parse_mode='html')


bot.polling(none_stop=True)