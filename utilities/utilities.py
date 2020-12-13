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
    async def iplookup(self, ctx, arg):
        suffix = (arg)
        lookup = ("http://ip-api.com/json/" + suffix)
        values = requests.get(lookup).json()
        embed = discord.Embed(
            colour=discord.Colour.blue()
        )
        embed.set_author(name="iplookup")

        embed.add_field(name="IP", value=values['query'], inline=False)
        embed.add_field(name="City", value=values['city'], inline=False)
        embed.add_field(name="Region", value=values['region'], inline=False)
        embed.add_field(name="Country", value=values['country'], inline=False)
        embed.add_field(name="lat", value=values['lat'], inline=False)
        embed.add_field(name="lon", value=values['lon'], inline=False)
        embed.add_field(name="ISP", value=values['isp'], inline=False)
        await ctx.send(embed=embed)

    @iplookup.error
    async def iplookup_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            author = ctx.message.author.mention
            msg = "***{0} you need too input a ip!***"
            image = "https://66.media.tumblr.com/98c6d9e942941712e0ef9518fca97a7c/tumblr_opni85yA931v8tshbo1_400.gif"
            embed = discord.Embed(
                description=msg.format(author),
                colour=discord.Colour.blue()
            )
            embed.set_image(url=image)
            await ctx.send(embed=embed)
