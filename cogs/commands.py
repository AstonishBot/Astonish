import discord

from json import dumps
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from utils.paginator import HelpPaginator, CannotPaginate

class Commands:
    def __init__(self, bot):
        self.bot = bot

        self.ss_api = "http://magmachain.herokuapp.com/api/v1"

    def cleanup_code(self, content):
        """Cleans the code up"""
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

    @commands.command(
        name="help",
        aliases=(
            "helpme",
            "commands"
        )
    )
    async def _help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        try:
            if command is None:
                p = await HelpPaginator.from_bot(ctx)
            else:
                entity = self.bot.get_cog(command) or self.bot.get_command(command)

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Command or category "{clean}" not found.')
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as e:
            await ctx.send(
                e
            )

    @commands.command(
        name="hello",
        aliases=(
            "hi",
            "h"
        )
    )
    async def _hi(self, ctx):
        """Say hello to me"""
        await ctx.send(
            f":wave: Hello there, {ctx.author.mention}"
        )


    @commands.command(
        name="python",
        aliases=(
            "sandbox", 
            "run"
        )
    )
    @commands.cooldown(
        1.0, 10.0, commands.BucketType.user
    )
    async def _python(self, ctx, *, code: commands.clean_content):
        """Runs a piece of code"""
        async with ctx.typing():
            async with self.bot.session.post(
                "http://coliru.stacked-crooked.com/compile",
                data=dumps(
                    {"cmd": "python3 main.cpp", "src": self.cleanup_code(code)}
                ),
            ) as resp:
                if resp.status != 200:
                    await ctx.send(":stopwatch: | **Timed out**", delete_after=5)

                else:
                    output = await resp.text(encoding="utf-8")

                    if len(output) < 1500:
                        embed=discord.Embed(
                            title="Python Sandbox",
                            description=f"```python\n{output}\n```",
                            color=self.bot.color,
                            timestamp=ctx.message.created_at,
                        )
                        
                        embed.set_thumbnail(url="http://i.imgur.com/9EftiVK.png")
                        embed.set_footer(
                            text="Interpreted at:", icon_url=ctx.author.avatar_url
                        )

                        await ctx.send(
                            embed=embed
                        )

                    else:
                        await ctx.send(
                            f"{self.bot.tick(False)} | **Output too long**", 
                            delete_after=5
                        )

    @commands.command(
        name="snapshot",
        aliases=(
            "ss", 
            "webscreen", 
            "capture"
        )
    )
    @commands.cooldown(
        1.0, 5.0, commands.BucketType.user
        )
    async def _snapshot(self, ctx, *, website: str):
        """
        Capture a website
        Example: @Astonish snapshot google.com
        """
        async with ctx.typing():
            async with self.bot.session.post(
                self.ss_api,
                headers={
                    "website": website
                }
            ) as r:
                try:
                    response = await r.json()
                    embed=discord.Embed(
                        color=self.bot.color,
                        title=website,
                        url=response["website"],
                        timestamp=ctx.message.created_at
                    )

                    embed.set_image(
                        url=response["snapshot"]
                    )

                    embed.set_footer(
                        text=f"Snapshotted by {ctx.author.name}",
                        icon_url=ctx.author.avatar_url
                    )

                    await ctx.send(
                        embed=embed
                    )

                except BaseException:
                    await ctx.send(
                        f"{self.bot.tick(False)} | **Failed to snapshot. Check your URL or try again**",
                        delete_after=5
                    )

def setup(bot):
    bot.add_cog(
        Commands(
            bot
        )
    )