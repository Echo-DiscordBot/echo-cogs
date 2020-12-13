import discord
import os
import random
import json
import requests
from redbot.core import commands, Config


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #with open("utilities/gifs/error.txt") as f:
        #    self.choices_error = f.readlines()

    @commands.command()
    async def iplookup(self, ctx, arg: Optional):
        suffix = (arg)
        lookup = ("http://ip-api.com/json/" + suffix)
        values = requests.get(lookup).json()
        if values['status']=="fail":
            return await ctx.send("Please provide a valid argument")
        embed = discord.Embed(
            colour=await self.bot.get_embed_color(ctx.channel)
        )
        embed.set_author(name="IP Lookup Details")
        embed.add_field(name="IP", value=values['query'] or "N/A", inline=False)       
        embed.add_field(name="Country", value=values['country'] or "N/A", inline=True)
        embed.add_field(name="Region", value=values['regionName'] or "N/A", inline=True)
        embed.add_field(name="City", value=values['city'] or "N/A", inline=True)
        embed.add_field(name="Latitude", value=values['lat'] or "N/A", inline=True)
        embed.add_field(name="Longitude", value=values['lon'] or "N/A", inline=True)
        embed.add_field(name="Timezone", value=values['timezone'] or "N/A", inline=True)
        embed.add_field(name="ISP", value=values['isp'] or "Not available", inline=True)
        await ctx.send(embed=embed)

#     @iplookup.error
#     async def iplookup_error(self, ctx, error):
#         if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
#             author = ctx.message.author.mention
#             msg = "***{0} you need too input a ip!***"
#             image = "https://66.media.tumblr.com/98c6d9e942941712e0ef9518fca97a7c/tumblr_opni85yA931v8tshbo1_400.gif"
#             embed = discord.Embed(
#                 description=msg.format(author),
#                 colour=await self.bot.get_embed_color(ctx.channel)
#             )
#             embed.set_image(url=image)
#             await ctx.send(embed=embed)
