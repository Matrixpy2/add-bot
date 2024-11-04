from pyrogram import Client, filters
from pyrogram.types import  Message
import re
import time
import random
app = Client('selfbot', api_id='Your API Id',api_hash='Your API hash') #you can receive your API Id an API hash from https://my.telegram.org/

first_chat=''
secondchat=''
userids = []        

@app.on_message(filters.command(['firstchat' , 'secondchat']))
def get_chat_id(c:Client , message:Message):
    global first_chat , secondchat
    text = message.text
    if len(message.command) !=2:
        message.reply_text('Usage : /firstchat (name of group)\nor\n/secondchat (name of group)')
    elif len(message.command) == 2:
        try:
            if re.search('/firstchat' , text):
                x = text.split()
                first_chat = x[1]
                message.reply_text(f'the first chat is : {first_chat}')
            elif re.search('/secondchat' , text):
                y = text.split()
                secondchat = y[1]
                message.reply_text(f'the second chat is : {secondchat}')
            else:
                message.reply_text('یه چیزی اینجا درست کار نمیکنه دوباره امتحان کن')
                first_chat = ''
                secondchat = ''
        except Exception as e:
            message.reply_text(f'Error : {e}')


        
@app.on_message(filters.command('help'))
def help(c:Client , message : Message):
    Text = message.text 
    if Text == '/help':
        message.reply('''list of command:
1. /firstchat (username) = add first chat for analyze members \n
2. /secondchat (username) = Add a second chat to drop members into \n
3. /status = To see the number of members of the first group \n
4. /addmember = for drop memmber from firstchat to second chat''')

    
@app.on_message(filters.command(['status' , 'addmember' ,'start']))
def show_members(c:Client , message:Message):
    global userids , first_chat , secondchat , dmount
    if message.text == '/status':
        if first_chat!='' and secondchat!='':
            for member in app.get_chat_members(first_chat):
                
                userids.append(member.user.id)
            message.reply_text(f'تعداد اعضای چنل {first_chat} = {len(userids)}')
        elif first_chat!='':
            message.reply_text('چنل دوم رو ندارم')
        elif secondchat!='':
            message.reply_text('چنل اول رو ندارم')
        else:
            message.reply_text(' چنل ها رو وارد کن')        
            
    if message.text == '/start':
        first_chat=''
        secondchat=''
        userids = []
        message.reply_text('همه چی ریست شد میتونی دوباره گروه اول و دومت رو تعیین کنی')
    if message.text =='/addmember':
            addmember(c , message)
      
@app.on_message(filters.command('mount'))
def mount(c:Client , message:Message):
        global dmount
        text = message.text
        if len(message.command) !=2:
            message.reply_text('Usage :\n/mount (number)')
        elif len(message.command) == 2:
            try:
                if re.search('/mount' , text):
                    x = (text.split())
                    dmount = int(x[1])
                    print(dmount)
                    if 0<dmount<=len(userids):
                        message.reply_text(f'تعدادی که میخوای به گروه {secondchat} اضافه کنی : {dmount}')
                    elif dmount> len(userids):
                        message.reply_text('عددت قابل قبول نیست')
                
                else:
                    message.reply_text('یه چیزی اینجا درست کار نمیکنه دوباره امتحان کن')
            except Exception as e:
                message.reply_text(f'Error : {e}')
                
                    
def addmember(c:Client , message:Message):
    global dmount
    if not userids or not secondchat:
        message.reply_text('Please ensure both chats are set and members are retrieved.')
        return
    elif not dmount:
        message.reply_text('تعدادی که میخوای اد بشه رو مشخص کن')
        return
    
    added_count = 0
    max_to_add = dmount
    for userid in userids:
        if added_count>= max_to_add:
            message.reply_text('break')
        else:
            try:
                c.add_chat_members(chat_id=secondchat, user_ids=userid)
                message.reply_text(f'{userid} added to {secondchat}')
                added_count += 1  
                userids.remove(userid)
                time.sleep(random.randint(120, 300))
            except Exception as e:
                message.reply_text(f'Error adding {userid} to {secondchat} cause : {e}')
                added_count+=1
                time.sleep(random.randint(5, 10))
app.run()
