import discord

from checks.checks import *
from random import choice

from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class NSFW:
    """NSFW Commands 🔞"""

    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/ivmKTvu.png"
        self.tags = (
            "feet",
            "yuri",
            "trap",
            "futanari",
            "hololewd",
            "lewdkemo",
            "solog",
            "feetg",
            "cum",
            "erokemo",
            "les",
            "wallpaper",
            "lewdk",
            "ngif",
            "meow",
            "tickle",
            "lewd",
            "feed",
            "gecg",
            "eroyuri",
            "eron",
            "cum_jpg",
            "bj",
            "nsfw_neko_gif",
            "solo",
            "kemonomimi",
            "nsfw_avatar",
            "gasm",
            "poke",
            "anal",
            "slap",
            "hentai",
            "avatar",
            "erofeet",
            "holo",
            "keta",
            "blowjob",
            "pussy",
            "tits",
            "holoero",
            "lizard",
            "pussy_jpg",
            "pwankg",
            "classic",
            "kuni",
            "waifu",
            "pat",
            "8ball",
            "kiss",
            "femdom",
            "neko",
            "spank",
            "cuddle",
            "erok",
            "fox_girl",
            "boobs",
            "Random_hentai_gif",
            "smallboobs",
            "hug",
            "ero",
        )

    @nsfw()
    @commands.command(
        name="neko", 
        aliases=(
            "catgirl",
            "hentai"
        )
    )
    @commands.cooldown(
        1.0, 5.0, commands.BucketType.user
    )
    async def _neko(self, ctx, *, tag: str.lower = None):
        """
            Gives you random neko picture. Channel must be NSFW to use this command. Leave the tag field empty to randomize neko.
            ---
            Tags are: feet, yuri, trap, futanari, hololewd, lewdkemo, solog, feetg,
            cum, erokemo, les, wallpaper, lewdk, ngif, meow, tickle, lewd, feed, gecg,
            eroyuri, eron, cum_jpg, bj, nsfw_neko_gif, solo, kemonomimi, nsfw_avatar,
            gasm, poke, anal, slap, hentai, avatar, erofeet, holo, keta, blowjob, pussy,
            tits, holoero, lizard, pussy_jpg, pwankg, classic, kuni, waifu, pat, 8ball, kiss,
            femdom, neko, spank, cuddle, erok, fox_girl, boobs, Random_hentai_gif, smallboobs,
            hug, ero
        """
        try:
            if tag is None:
                tag = choice(
                    self.tags
                )

            if tag == "random_hentai_gif":
                tag = tag.capitalize()

            async with self.bot.session.get(
                f"https://nekos.life/api/v2/img/{tag}"
            ) as resp:
                data = await resp.json()
                embedneko = discord.Embed(
                    color=self.bot.color,
                    title=f"Neko :3 - {tag}",
                    timestamp=ctx.message.created_at,
                )
                embedneko.set_image(url=f'{data.get("url")}')
                embedneko.set_footer(
                    text=f"Requested by: {ctx.author}",
                    icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embedneko)
        
        except Exception as exc:
            await self.bot.error(
                ctx = ctx,
                exc = exc,
            )

    @nsfw()
    @commands.command(
        aliases=(
            "urb", 
            "ud", 
            "urban"
        )
    )
    @commands.cooldown(
        1.0, 10.0, commands.BucketType.user
    )
    async def urbandictionary(self, ctx, *, urbanword):
        """
        Looks up for word in Urban Dictionary
        For example, @Astonish ud cat will give you definition and more of word 'cat'
        """
        try:
            async with self.bot.session.get(
                f"http://api.urbandictionary.com/v0/define?term={urbanword}"
            ) as resp:
                data = await resp.json()
                try:
                    data["list"][0].get("word")
                except Exception as exc:
                    await self.bot.error(
                        ctx = ctx,
                        exc = exc,
                    )

                else:
                    async with self.bot.session.get(
                        f"http://api.urbandictionary.com/v0/define?term={urbanword}"
                    ) as resp:
                        data = await resp.json()
                        definition = data["list"][0].get("definition")
                        example = data["list"][0].get("example")
                        if definition == "":
                            definition = "No definition(s)."
                        elif example == "":
                            example = "No example(s)."
                        try:
                            if len(definition) >= 2000:
                                raise Exception("The definition is too long.")
                            else:
                                embed = discord.Embed(color=self.bot.color)
                                embed.add_field(
                                    name="**:baby_bottle: Definition**",
                                    value=definition,
                                    inline=True,
                                )
                                
                                embed.add_field(
                                    name="**:link: Permalink**",
                                    value=f'**[➤ Click Me!]({data["list"][0].get("permalink")})**',
                                    inline=True,
                                )

                                embed.add_field(
                                    name="**:notebook_with_decorative_cover: Word by**",
                                    value=f'**{data["list"][0].get("author")}**',
                                    inline=True,
                                )

                                embed.add_field(
                                    name="**:pen_ballpoint: Written on**",
                                    value=f'**{data["list"][0].get("written_on")}**',
                                    inline=True,
                                )

                                embed.add_field(
                                    name="**:star: Rating**",
                                    value=f':thumbsup: **{data["list"][0].get("thumbs_up")}**\n:thumbsdown: **{data["list"][0].get("thumbs_down")}**',
                                    inline=True,
                                )

                                embed.set_thumbnail(
                                    url=ctx.author.avatar_url,
                                )

                                await ctx.send(
                                    embed=embed,
                                )


                        except Exception as exc:
                            await ctx.send(
                                f"{self.bot.tick(False)} | **Maybe, the definition is too long**",
                                delete_after=5,
                            )
                            
        except Exception as exc:
            await ctx.send(
                f"{self.bot.tick(False)} | **Error or no results found for your query**",
                delete_after=5,
            )


def setup(bot):
    bot.add_cog(NSFW(bot))
