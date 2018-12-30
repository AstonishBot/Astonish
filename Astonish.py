import discord

from copy import copy
from inspect import getmembers, isroutine

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

        self.set_attributes()

    def set_attributes(self):
        attributes = getmembers(
            config, lambda a: not(
                isroutine(
                    a
                )
            )
        )

        for attribute in attributes:
            if not(
                attribute[0].startswith(
                    '__'
                ) and attribute[0].endswith(
                    '__'
                )
            ):
                setattr(
                    self,
                    attribute[
                        0
                    ],
                    attribute[
                        1
                    ] 
                )

    def tick(self, status: bool):

        if status is True:
            return self.status_emojis[
                "ok"
            ]
        
        return self.status_emojis[
            "error"
        ]
    
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