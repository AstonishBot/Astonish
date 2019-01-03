import discord
import typing

from discord.ext import commands

class Play:
    """Play with bot"""
    def __init__(self, bot):
        self.bot = bot
        
        self.backend = "https://public-api.travitia.xyz/talk"
        self.cb_key = self.bot.cb_key

    async def __ask__(self, text: str) -> str:
        if not (3 <= len(text) <= 60):
            return "Text must be longer than 3 and shorter than 60 characters"
        
        async with self.bot.session.post(
            self.backend, 
            json={
                "text": text
            }, 
            headers={
                "authorization": self.cb_key
            }
            ) as reqest:
            
            try:
                return (await reqest.json())["response"]
            except Exception as e:
                return f"Uh oh, something broke. I can't talk to you now, buddy (`{e}`)"
    
    @commands.command(
        name="talk",
        aliases=(
            "tell",
            "speak",
            "ask"
        )
    )
    async def ask(self, ctx, *, text: str):
        async with ctx.typing():

            answer = await self.__ask__(
                text
            )

            await ctx.send(
                f"{ctx.author.mention}, {answer}"
            )
            
    @commands.command(
        name="mobile",
        aliases=(
            "amionmobile",
            "amimobile"
        )
    )
    async def _mobile(self, ctx, member: discord.Member = None):
        
        member = member or ctx.author
        
        if member.is_on_mobile():

            return await ctx.send(
                f"I think **{member.name}** is on :iphone:"
            )
        
        await ctx.send(
            f"I think **{member.name}** is on :computer:"
        )

def setup(bot):
    bot.add_cog(
        Play(
            bot
        )
    )
