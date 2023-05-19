import discord
from discord.ext import commands
import requests
import json


class discordBot:
    def __init__(self):
        self.config = self._config
        self.key = self.config.get('key')
        self.prefix = self.config.get('prefix')
        self.token = self.config.get('token')
        assert self.key and self.prefix and self.token, "Key or Prefix or Token couldn't be found"

    @property
    def _config(self):
        with open("config.json", 'r') as f: return json.load(f)
    
    def get_roblox_id(self, discordId):
        request =  requests.get(f"https://v3.blox.link/developer/discord/{discordId}", headers={"api-key": self.key})
        if request.status_code == 200: return request.json()
        else: return {"success": False}
    
    def run(self):
        bot = commands.Bot(command_prefix=self.prefix, intents=discord.Intents.all())
        
        @bot.event
        async def on_ready():
            print("bot is online")
        
        @bot.command(name="get_roblox_id")
        async def get_roblox_id_command(ctx, user: discord.User):
            roblox_id = self.get_roblox_id(discordId=user.id)
            if roblox_id['success']: await ctx.reply(f"{roblox_id['user']['robloxId']}")
            else: await ctx.reply("user is too protected")
        
        bot.run(self.token)

discordBot().run()
