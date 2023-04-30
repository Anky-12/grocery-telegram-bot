import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '6065958548:AAEknlGrQOTTTKKJpKnL277IBx831eL3S6s'

momos = {
    'veg_momos': {'price': 20, 'quantity': 10, 'weight': '50g', 'type': 'vegetarian', 'brand': 'Wow momos'},
    'paneer_momos': {'price': 30, 'quantity': 5, 'weight': '60g', 'type': 'vegetarian', 'brand': 'Nepali momos'},
    'chicken_momos': {'price': 40, 'quantity': 8, 'weight': '70g', 'type': 'non-vegetarian', 'brand': 'Momo mami'},
    'chicken_kurkure_momos': {'price': 50, 'quantity': 3, 'weight': '80g', 'type': 'non-vegetarian', 'brand': 'Kathmandu Momos'},
    'mushroom_momos': {'price': 25, 'quantity': 12, 'weight': '55g', 'type': 'vegetarian', 'brand': 'Momo Mania'},
    'corn_cheese_momos': {'price': 35, 'quantity': 6, 'weight': '65g', 'type': 'vegetarian', 'brand': 'Alok momos'},
    'chicken_fried_momos': {'price': 45, 'quantity': 9, 'weight': '75g', 'type': 'non-vegetarian', 'brand': 'Burnt'},
    'mushroom_fried_momos': {'price': 40, 'quantity': 19, 'weight': '75g', 'type': 'vegetarian', 'brand': 'Burnt'},
    'paneer_fried_momos': {'price': 50, 'quantity': 12, 'weight': '75g', 'type': 'vegetarian', 'brand': 'Burnt'},
    'veg_fried_momos': {'price': 40, 'quantity': 13, 'weight': '75g', 'type': 'vegetarian', 'brand': 'Burnt'}
}

def start(update, context):
    """Handler for the /start command."""
    update.message.reply_text('Welcome to the Momos Store Bot! Please use /momos to view the available items.')

def view_momos(update, context):
    """Handler for the /momos command."""
    items = '\n'.join([f'{item}: {details["quantity"]} (Price: {details["price"]}, Weight: {details["weight"]}, Type: {details["type"]}, Brand: {details["brand"]})' for item, details in momos.items()])
    update.message.reply_text(f'Momos:\n{items}\nPlease use /order <item> <quantity> to place an order.')


def order_item(update, context):
    """Handler for the /order command."""


    args = context.args
    if len(args) != 2:
        update.message.reply_text('Invalid command. Please use /order <item> <quantity> to place an order.')
    else:
        item = args[0]
        quantity = int(args[1])
        if item not in momos:
            update.message.reply_text('Item not found in momos. Please choose a valid item from the momos.')
        elif momos[item]['quantity'] < quantity:
            update.message.reply_text('Insufficient quantity in momos. Please choose a lower quantity.')
        else:
            price = momos[item]['price'] * quantity
            momos[item]['quantity'] -= quantity
            weight = momos[item]['weight']
            momo_type = momos[item]['type']
            brand = momos[item]['brand']
            update.message.reply_text(f'Order placed successfully!\nItem: {item}\nQuantity: {quantity}\nPrice: {price}\nWeight: {weight}\nType: {momo_type}\nBrand: {brand}\nRemaining quantity in momos: {momos[item]["quantity"]}.\nFor delivery use /delivery.\nFor rate use /rate command.\nFor review use /review command.')
            
def delivery_options(update, context):
    """Handler for the /delivery command."""
    options = [
        '1. I want delivery',
        '2. I will pick up my order'
    ]
    update.message.reply_text('Please select a delivery option:\n' + '\n'.join(options))
    
    delivery_choice_handler = MessageHandler(Filters.text & ~Filters.command, get_delivery_choice)
    context.dispatcher.add_handler(delivery_choice_handler)
    
def get_delivery_choice(update, context):
    """Handler for the user's delivery option choice."""
    choice = update.message.text.strip()
    if choice == '1':
        update.message.reply_text('Please enter your delivery address:')
        delivery_address_handler = MessageHandler(Filters.text & ~Filters.command, get_delivery_address)
        context.dispatcher.add_handler(delivery_address_handler)
    elif choice == '2':
        update.message.reply_text('Your order will be ready for pickup in 20 minutes at our store location. Thank you!')
    else:
        update.message.reply_text('Invalid option. Please select a valid option.')


def get_delivery_address(update, context):
    """Handler for the user's delivery address."""
    address = [
        '1. KIIT',
        '2. KIIT Square'
    ]
    update.message.reply_text('Please select a delivery address:\n' + '\n'.join(address))
    delivery_choice_handler2 = MessageHandler(Filters.text & ~Filters.command, get_delivery_choice2)
    context.dispatcher.add_handler(delivery_choice_handler2)
    

def get_delivery_choice2(update, context):
    """Handler for reply message after the address"""
    choice1 = update.message.text.strip()
    if choice1 == '1':
        update.message.reply_text('Thanku for your order, we will be likely to deliver in 20 minutes')
    elif choice1 == '2':
        update.message.reply_text('Thanku for your order, we will be likely to deliver in 20 minutes')
    else:
        update.message.reply_text('Invalid address. Please select a valid address.')
    



def rate(update, context):
    """Handler for the /rate command."""
    update.message.reply_text('Please rate our service from 1 to 5. 1 being the lowest and 5 being the highest.')

def review(update, context):
    """Handler for the /review command."""
    update.message.reply_text('Please write your review of our service.')

def process_rating(update, context):
    """Handler for processing the user's rating."""
    rating = int(update.message.text)
    if rating < 1 or rating > 5:
        update.message.reply_text('Invalid rating. Please rate our service from 1 to 5. 1 being the lowest and 5 being the highest.')
    else:
        update.message.reply_text(f'Thank you for your rating of {rating}!')

def process_review(update, context):
    """Handler for processing the user's review."""
    review_text = update.message.text
    update


bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('momos', view_momos))
dispatcher.add_handler(CommandHandler('order', order_item))
dispatcher.add_handler(CommandHandler('delivery', delivery_options))
dispatcher.add_handler(CommandHandler('rate', rate))
dispatcher.add_handler(CommandHandler('review', review))


updater.start_polling()
logging.info('Bot started!')
updater.idle()