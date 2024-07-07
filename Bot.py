import telebot
import requests

TELEGRAM_TOKEN = "coloque_seu_token_aqui"
bot = telebot.TeleBot(TELEGRAM_TOKEN)



@bot.message_handler(commands=['p', 'Preço'])
def promocao(message):
    base_url = 'https://www.cheapshark.com/api/1.0/deals?'
    params = message.text.split()[1:]
    title = ''
    store_id = None
    page = '5'
    onSale = '1'
    for i, param in enumerate(params):
        if param == '-s' and i+1 < len(params):
            store_id = params[i+1]
            
            del params[i:i+2]
            break
    for i, param in enumerate(params):
        if param == '-p' and i+1 < len(params):
            page = params[i+1]
            del params[i:i+2]
            break

    if params:
        title = ' '.join(params)

    url = f"{base_url}title={title}"
    if store_id:
        url += f"&storeID={store_id}"
    url += f"&pageSize={page}"
    url += f"&onSale={onSale}"
    
    r = requests.get(url)
    r.raise_for_status()
    dados = r.json()
    stores = requests.get('https://www.cheapshark.com/api/1.0/stores')
    stores  = stores.json()
    lojas = ''
    
    
    if not dados:
        bot.send_message(message.chat.id, "Nenhum resultado encontrado.")
    else:
        for dado in dados:
            for s in stores:
            	if s['storeID'] ==dado['storeID']:
            		lojas = s['storeName']
            		break
            dealID = dado['dealID']
            msg = (f"Título: {dado['title']}\n\n"
                   f"loja: {lojas}\n\n"
                   f"Preço em promoção: U${dado['salePrice']} ({float(dado['savings']):.2f}% OFF)\n\n"
                   f"Preço normal: U${dado['normalPrice']}\n\n"
                   f"<a href='https://www.cheapshark.com/redirect?dealID={dealID}'>Clique aqui para ver a promoção</a>")
                   
            bot.send_message(message.chat.id,msg,parse_mode='HTML')
            
@bot.message_handler(commands=['Documentação', 'docs', 'd'])
def docs(message):
    msg = """ℹ️ **Comandos Disponíveis:**
    
    /p [título] - Procura promoções com filtros opcionais. Deixe em branco para todas as promoções.
    
    ℹ️ **Filtros Disponíveis:**
    `-s [IDs]` - Filtra as ofertas por IDs específicos de lojas.
    
    ℹ️ **IDs Comuns:**
    - Steam: **1**
    - Epic Games Store: **25**
    - GOG: **7**
    - Origin: **8**
    - Humble Store: **11**
    - Fanatical: **15**
    - GreenManGaming: **3**
    - Uplay: **13**
    
    `-p [número]` - Define o número de ofertas por página (padrão: **5**).
    
    Exemplos:
    `/p Jogos -s 1 25` - Filtra ofertas das lojas Steam e Epic Games Store com título "Jogos".
    `/p -p 10` - Mostra 10 ofertas por página sem filtro de título.
    """
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')
	
@bot.message_handler(commands=['start'])
def bem_vindo(message):
    bot.send_message(message.chat.id, 
        "Olá! Eu sou o Bot de Promoções. Posso te ajudar a encontrar as melhores ofertas de jogos e mais. "
        "Para começar, utilize o comando /p seguido do título ou deixe em branco para ver todas as promoções. "
        "Os preços são exibidos em dólares (USD). "
        "Para mais informações sobre os comandos disponíveis, digite /docs."
    )
bot.polling(none_stop=True)
