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

    @commands.command(name="iplookup", aliases=["ip", "ipinfo"])
    async def iplookup(self, ctx, arg):
        if arg=="mine":
            arg = ""
        suffix = (arg)
        lookup = ("http://ip-api.com/json/" + suffix + "?fields=66846719")
        values = requests.get(lookup).json()
        if values['status']=="fail":
            return await ctx.send("Please provide a valid argument")
        embed = discord.Embed(
            colour=await self.bot.get_embed_color(ctx.channel)
        )
        embed.set_author(name="🌐 IP Lookup Details")
        embed.add_field(name="IP", value=values['query'] or "N/A", inline=False)
        embed.add_field(name="Mobile", value=values['mobile'] or "N/A", inline=True)
        embed.add_field(name="Proxy", value=values['proxy'] or "N/A", inline=True)
        embed.add_field(name="Hosting", value=values['hosting'] or "N/A", inline=True)
        embed.add_field(name="Continent", value=values['continent'] or "N/A", inline=True)
        embed.add_field(name="Country", value=values['country'] or "N/A", inline=True)
        embed.add_field(name="Region", value=values['regionName'] or "N/A", inline=True)
        embed.add_field(name="City", value=values['city'] or "N/A", inline=True)
        embed.add_field(name="District", value=values['district'] or "N/A", inline=True)
        embed.add_field(name="Zip", value=values['zip'] or "N/A", inline=True)
        embed.add_field(name="Latitude", value=values['lat'] or "N/A", inline=True)
        embed.add_field(name="Longitude", value=values['lon'] or "N/A", inline=True)
        embed.add_field(name="💸 Currency", value=values['currency'] or "N/A", inline=True)
        embed.add_field(name="⏲️ Timezone", value=values['timezone'] or "N/A", inline=True)
        embed.add_field(name="🌐 ISP/Organization", value=values['isp'] or values['org'] or "Not available", inline=False)
        await ctx.send(embed=embed)
