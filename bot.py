import discord
from discord import app_commands
import os
import sqlite3
import sys

dbname = 'meds.db'

intents = discord.Intents.default()
intents.message_content = True

# BOT_TOKEN = os.environ['BOT_TOKEN']
# GUILD_ID = os.environ['GUILD_ID']
BOT_TOKEN='YOUR_TOKEN'
GUILD_ID='YOUR_GUILD_ID'

MY_GUILD = discord.Object(id=GUILD_ID)

#参照 https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self) #全てのコマンドを管理するCommandTree型オブジェクトを生成

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = MyClient(intents=intents)

@client.tree.command()
async def test(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f'BOT終了します。')
    sys.exit()

@client.tree.command()
async def add(interaction: discord.Interaction, hour: str, min: str, num: str):
    # await interaction.response.send_message(f'test text:{text}')
    print('-----')
    pass
    h = int(hour)
    m = int(min)
    n = int(num)
    # print(f'hour:{h}, min:{m}, amount:{n}')
    
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
   # sql = f'insert into time(time, amount) values ()'


    sql = f'insert into time(amount, time) values ({h}{m}, {n})' 
    print(sql)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print('-----')
    await interaction.response.send_message(f'hour:{h}, min:{m}, amount:{n}')

client.run(BOT_TOKEN)
