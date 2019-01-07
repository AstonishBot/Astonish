import discord

from discord.ext import commands
from utils.paginator import EmbedPages

from urllib.parse import quote


class Search:
    """Search what you want and where you want"""

    def __init__(self, bot):
        self.bot = bot

        self.thumbnail = "https://i.imgur.com/rKFyFCL.png"
        self.duckduckgo_backend = "https://api.duckduckgo.com"

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def search(self, ctx):
        """Search something (anime, manga, lyrics, wikipedia)"""
        await ctx.send(
            ":information_source: | **Please provide what to search (anime, manga, lyrics, wikipedia)**"
        )

    @search.command()
    async def anime(self, ctx, *, query: str):
        """Shows you information about anime"""
        async with ctx.typing():
            try:
                async with self.bot.session.get(
                    f"https://api.jikan.moe/search/anime/{query}"
                ) as resp:
                    data = await resp.json()
                    newdata = data["result"][0]
                    
                embed = discord.Embed(
                    color=self.bot.color,
                    timestamp=ctx.message.created_at,
                    title=newdata.get("title"),
                )
                embed.add_field(
                    name=":gem: Short description:",
                    value=f"{newdata.get('description')}**[Read more about {newdata.get('title')}...]({newdata.get('url')})**",
                    inline=True,
                )
                embed.add_field(
                    name=":clapper: Episodes:",
                    value=f"**{newdata.get('episodes')}**",
                    inline=True,
                )
                embed.add_field(
                    name=":heart_decoration: MyAnimeList rating:",
                    value=f"**{newdata.get('score')}/10**",
                    inline=True,
                )
                embed.add_field(
                    name=":busts_in_silhouette: Members:",
                    value=f"**{newdata.get('members')}**",
                    inline=True,
                )
                embed.add_field(
                    name=":performing_arts: Type:",
                    value=f"**{newdata.get('type')}**",
                    inline=True,
                )
                embed.set_thumbnail(url=newdata.get("image_url"))
                embed.set_footer(
                    text=f"Anime search for - {query}",
                    icon_url=ctx.author.avatar_url,
                )
                
                await ctx.send(
                    embed=embed
                )
            
            except BaseException:
                await ctx.send(
                    f"{self.bot.tick(False)} | **No results found**",
                    delete_after=5,
                )

    @search.command()
    async def manga(self, ctx, *, query: str):
        """Shows you information about manga"""
        async with ctx.typing():
            try:
                async with self.bot.session.get(
                    f"https://api.jikan.moe/search/manga/{query}"
                ) as resp:
                    data = await resp.json()
                    newdata = data["result"][0]

                embed = discord.Embed(
                    color=self.bot.color,
                    timestamp=ctx.message.created_at,
                    title=newdata.get("title"),
                )
                embed.add_field(
                    name=":gem: Short description:",
                    value=f"{newdata.get('description')}**[Read more about {newdata.get('title')}...]({newdata.get('url')})**",
                    inline=True,
                )
                embed.add_field(
                    name=":clapper: Volumes:",
                    value=f"**{newdata.get('volumes')}**",
                    inline=True,
                )
                embed.add_field(
                    name=":heart_decoration: MyAnimeList rating:",
                    value=f"**{newdata.get('score')}/10**",
                    inline=True,
                )
                embed.add_field(
                    name=":busts_in_silhouette: Members:",
                    value=f"**{newdata.get('members')}**",
                    inline=True,
                )
                embed.add_field(
                    name=":performing_arts: Type:",
                    value=f"**{newdata.get('type')}**",
                    inline=True,
                )
                embed.set_thumbnail(
                    url=newdata.get(
                        "image_url",
                    )
                )
                embed.set_footer(
                    text=f"Manga search for - {query}",
                    icon_url=ctx.author.avatar_url,
                )
                await ctx.send(embed=embed)

            except BaseException:
                await ctx.send(f"{self.bot.tick(False)} | **No results found**")

    @search.command()
    async def wikipedia(self, ctx, search: str, language: str = "en"):
        """
        Lets you search Wikipedia.
        For example, n.search wikipedia "cucumber" en
        Will give you definition of cucumber in english. Default language is english so you can just n.search wikipedia "cucumber"
        If you want to search in other language, for example word cucumber in russian (огурец), you need to specify language:
        n.search wikipedia "огурец" ru
        This will give you definition of word cucumber in russian.
        """
        async with ctx.typing():
            try:
                async with self.bot.session.get(
                    f"https://{language.lower()}.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={search}&redirects=1&indexpageids"
                ) as resp:
                    data = await resp.json()
            except BaseException:
                await ctx.send(
                    f"{self.bot.tick(False)} | **Invalid language provided (`{language.lower()}`). Example: ru - Russian; en - English**"
                )
            if (data["query"]["pages"][data["query"]
                                       ["pageids"][0]].get("extract") is None):
                await ctx.send(
                    f"{self.bot.tick(False)} | **No results found for `{search}` in `{language}` language.**"
                )
            else:
                try:
                    await ctx.send(
                        embed=discord.Embed(
                            color=self.bot.color,
                            title=f"Wikipedia Search - {search}",
                        )
                        .add_field(
                            name=f":information_source: Found - {data['query']['pages'][data['query']['pageids'][0]].get('title')}",
                            value=f"```fix\n{data['query']['pages'][data['query']['pageids'][0]].get('extract')}```",
                        )
                        .set_footer(
                            text=f"Wikipedia search by: {ctx.author}",
                            icon_url=ctx.author.avatar_url,
                        )
                    )
                except discord.errors.HTTPException:
                    await ctx.send(
                        ":information_source: | **Looks like text is too long. Trying upload to hastebin.**"
                    )
                    try:
                        async with self.bot.session.post(
                            "https://hastebin.com/documents",
                            data=f"Wikipedia Search - {search} | Language: {language.lower()}\nFound: {data['query']['pages'][data['query']['pageids'][0]].get('title')}\nText: {data['query']['pages'][data['query']['pageids'][0]].get('extract')}".encode(
                                "utf-8"
                            ),
                        ) as post:
                            post = await post.json()
                            await ctx.send(
                                f'{self.bot.tick(True)} | **Uploaded. URL: https://hastebin.com/{post["key"]}**'
                            )
                    except BaseException:
                        await ctx.send(
                            f"{self.bot.tick(False)} | **Uploading to hastebin failed**"
                        )

    @search.command(
        aliases=(
            "ddg", 
            "web"
        )
    )
    @commands.cooldown(
        1.0, 5.0, commands.BucketType.user
    )
    async def duckduckgo(self, ctx, *, query: str):
        """Search DuckDuckGo"""
        await ctx.trigger_typing()
        res = await self.bot.session.get(
            self.duckduckgo_backend,
            params={
                "q": quote(query),
                "t": "Astonish Discord Bot",
                "format": "json",
                "no_html": "1",
            },
        )

        resp_json = await res.json(
            content_type="application/x-javascript"
        )

        embeds = {}

        if resp_json["AbstractURL"] != "":
            embeds[f'Abstract: {resp_json["Heading"]}'
                   f' ({resp_json["AbstractSource"]})'] = {"image": resp_json["Image"],
                                                           "desc": f'{resp_json.get("AbstractText", "")}\n\n'
                                                           f'{resp_json["AbstractURL"]}',
                                                           }

        if resp_json["Definition"] != "":
            embeds["Definition"] = {
                "desc": f'{resp_json["Definition"]}\n'
                f'([{resp_json["DefinitionSource"]}]'
                f'({resp_json["DefinitionURL"]}))'
            }

        if resp_json["RelatedTopics"]:
            desc = []
            for topic in resp_json["RelatedTopics"]:
                try:
                    if len("\n".join(desc)) > 1000:
                        break
                    desc.append(f'[**{topic["Text"]}**]({topic["FirstURL"]})')
                except KeyError:
                    continue

            embeds["Related"] = {
                "desc": "\n".join(desc),
                "image": resp_json["RelatedTopics"][0]["Icon"]["URL"],
            }

        if resp_json["Results"]:
            desc = []
            for result in resp_json["Results"]:
                desc.append(f'[**{result["Text"]}**]({result["FirstURL"]})')
            embeds["Top Results"] = {
                "desc": "\n".join(desc),
                "image": resp_json["Results"][0]["Icon"]["URL"],
            }

        final_embeds = []

        for embed_title, embed_content in embeds.items():
            final_embeds.append(
                discord.Embed(
                    title=embed_title,
                    description=embed_content["desc"],
                    color=self.bot.color,
                )
                .set_image(url=embed_content["image"])
                .set_thumbnail(url="https://i.imgur.com/tA7ko5O.png")
            )

        if not final_embeds:
            return await ctx.send(
                f"{self.bot.tick(False)} | **Sorry, no results found**", 
                delete_after=5
            )

        await EmbedPages(ctx, embeds=final_embeds).paginate()


def setup(bot):
    bot.add_cog(Search(bot))
