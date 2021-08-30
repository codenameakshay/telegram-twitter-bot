from flask import Flask, request
import telegram
import tweepy
import re
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import bs4
import requests
import urllib
bot_token = "1570074278:AAG4e6LGkHIGEsQA3ov-k_LRG54L1sZaE8Q"
bot_user_name = "Tjhhhrbabot"
URL = "https://dmbbbbhjiu.herokuapp.com/"

consumer_key = 'SBEyu3zjgw0z0W3WdgpOkibf0'
consumer_secret = '1NbmlGyzektfKeNdgwvImdEj5C3TWWaL7wi0Hbn2jsv5sWn6Ug'
access_token = '772065071774179328-0zLTuQDKMZ3lVlZEjoatGC9M1hBVZIQ'
access_token_secret = 'E7JTCs9kKp0O11QjCOSQeUbDwx2nskjRpqjF1kbqs8Fcc'
global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
urlRegex = re.compile(r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)
    if text == "/start":
        bot_welcome = """
       Welcome to PrismTweetBot. Simply tweet anything, like links or images from here if you want. To do that type /tweet followed by your message and that will be tweeted by the official Prism Wallpapers Twitter Account. Developed by @CodeName_Akshay
       """
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)
    elif text[0:6] == "/link ":
        try:
            def copyright_apply(input_image_path,
                                output_image_path,
                                text):
                photo = Image.open(input_image_path)
                w, h = photo.size
                drawing = ImageDraw.Draw(photo)
                font = ImageFont.truetype("Roboto.ttf", 72)
                text_w, text_h = drawing.textsize(text, font)
                pos = (w - text_w)-50, (h - text_h) - 50
                c_text = Image.new('RGB', (text_w, (text_h)), color='#000000')
                drawing = ImageDraw.Draw(c_text)
                drawing.text((0, 0), text, fill="#ffffff", font=font)
                c_text.putalpha(75)
                photo.paste(c_text, pos, c_text)
                photo.save(output_image_path)
            url = urlRegex.search(text).group()
            r = requests.head(url, allow_redirects=True)
            imageUrl = r.url.split('socialImageUrl=')[1].split('&')[
                0].replace('thumb_', '')
            filename = 'temp.jpg'
            req = requests.get(imageUrl, stream=True)
            if req.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in req:
                        image.write(chunk)
                copyright_apply(filename, filename,
                                text='@PrismWallpapers'
                                )
                num = random.randint(0, 4)
                randomText = ["Sometimes happy little accidents are the push you need for a spark of life. Open up the app for our latest Wallpapers.", "The beautiful nature of life is what keeps us thriving. Re-inspire your life with this and more awesome wallpapers.", "Kicking off the day in style is an art. You know what also is an art?\n\nThis wallpaper😊😊.",
                              "Hard to resist, easy to apply. More amazing wallpapers on the app, download now. https://play.google.com/store/apps/details?id=com.hash.prism", "Live life to the fullest, and experience the best wallpapers with our exclusive collection featuring over 300+ walls filled with awesomeness. Download the app now for more such walls."]
                status = api.update_with_media(filename, randomText[num]+" "+url)
                bot.sendMessage(
                    chat_id=chat_id, text="Tweeted successfully!", reply_to_message_id=msg_id)
            else:
                print("Unable to download image")
                bot.sendMessage(
                    chat_id=chat_id, text="Tweet Failed!", reply_to_message_id=msg_id)
        except Exception as exc:
            bot.sendMessage(
                chat_id=chat_id, text="Some error in the script."+str(exc), reply_to_message_id=msg_id)
    elif text[0:7] == "/tweet ":
        try:
            text = text[7:len(text)]

            def copyright_apply(input_image_path,
                                output_image_path,
                                text):
                photo = Image.open(input_image_path)
                w, h = photo.size
                drawing = ImageDraw.Draw(photo)
                font = ImageFont.truetype("Roboto.ttf", 72)
                text_w, text_h = drawing.textsize(text, font)
                pos = (w - text_w)-50, (h - text_h) - 50
                c_text = Image.new('RGB', (text_w, (text_h)), color='#000000')
                drawing = ImageDraw.Draw(c_text)
                drawing.text((0, 0), text, fill="#ffffff", font=font)
                c_text.putalpha(75)
                photo.paste(c_text, pos, c_text)
                photo.save(output_image_path)
            url = urlRegex.search(text).group()
            r = requests.head(url, allow_redirects=True)
            imageUrl = r.url.split('socialImageUrl=')[1].split('&')[
                0].replace('thumb_', '')
            filename = 'temp.jpg'
            req = requests.get(imageUrl, stream=True)
            if req.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in req:
                        image.write(chunk)
                copyright_apply(filename, filename,
                                text='@PrismWallpapers'
                                )
                status = api.update_with_media(filename, text)
                bot.sendMessage(
                    chat_id=chat_id, text="Tweeted successfully!", reply_to_message_id=msg_id)
            else:
                print("Unable to download image")
                bot.sendMessage(
                    chat_id=chat_id, text="Tweet Failed!", reply_to_message_id=msg_id)
        except Exception as exc:
            bot.sendMessage(
                chat_id=chat_id, text="Some error in the script."+str(exc), reply_to_message_id=msg_id)
    else:
        bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)
