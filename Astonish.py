import discord

from aiohttp import ClientSession
from discord.ext import commands

from config.config import AstonishConfig as config

class Astonish(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(
                "a]"
            )
        )
        
        self.session = ClientSession(
            loop=self.loop
        )

        self.config = config()

        self.color = self.config.color
        self.cb_key = self.config.cb_key
        self.token = self.config.token
        self.initial_extensions = self.config.initial_extensions
        self.status_emojis = self.config.status_emojis

        self.base_embed = discord.Embed(
            color=self.color
        )

    def tick(self, status: bool):

        if status is True:
            return self.status_emojis[
                "ok"
            ]
        
        return self.status_emojis[
            "error"
        ]

    async def error(self, ctx: commands.Context, exc: Exception):

        try:
            
            embed = self.base_embed
            embed.description = f"{self.tick(False)} an error occured. {exc}"            

            await ctx.send(
                embed=embed
            )

        except BaseException as e:
            print(e)
    
    async def on_ready(self):

        await self.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.listening, 
                name="Discord users"
            )
        )

        print(
            "Ready!"
        )

    def run(self):
        
        self.remove_command(
            "help"
        )

        for extension in self.initial_extensions:

            try:

                self.load_extension(
                    extension
                )
            
            except Exception as e:
                print(
                    f"Failed to load {extension} due to: {e}"
                )

        super().run(
            self.token,
            bot=True
        )

if __name__ == "__main__":
    Astonish().run()