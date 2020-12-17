import discord
import os
import random
import json
import requests
import aiohttp
from redbot.core import commands, Config


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #with open("utilities/gifs/error.txt") as f:
        #    self.choices_error = f.readlines()
    
    def acquire_session(self):
        # will error if you run outside event loop:
        asyncio.get_running_loop()
        if not hasattr(self, "_session"):
            self._session = aiohttp.ClientSession(
                connector = aiohttp.TCPConnector(
                    limit = self._pool_size,
                )
            )
        return self._session

    @commands.command(name="iplookup", aliases=["ip", "ipinfo"])
    async def iplookup(self, ctx, arg):
        suffix = (arg)
        lookup = ("http://ip-api.com/json/" + suffix + "?fields=66846719")
        values = requests.get(lookup).json()
        if values['status']=="fail":
            return await ctx.send("Please provide a valid argument")
        embed = discord.Embed(
            colour=await self.bot.get_embed_color(ctx.channel)
        )
        embed.set_author(name=f"🌐 IP Lookup Details: {arg}")
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
        embed.set_footer(text=f"Requested by: {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=["ipaddr"])
    @commands.cooldown(rate=3, per=5, type=commands.BucketType.user)
    async def ipnew(self, ctx, ip: str = None):
        """
        Find out the information of an IP Address
        API Provided by: https://ipapi.co/
        """
        if ip is None:
            await ctx.send(embed=discord.Embed(description="⚠ Please Specify the IP Address!"))
            return

        if ip == "0.0.0.0" or ip == "127.0.0.1":
            await ctx.send(embed=discord.Embed(description="You have played yourself. Wait... You can't!"))
            return

        await ctx.trigger_typing()

        try:
            session = self.acquire_session()
            session.get(f'https://ipapi.co/{ip}/json/') as resp:
                resp.raise_for_status()
                data = json.loads(await resp.read(), object_hook=DictObject)
                    
            ipaddr = data["ip"]
            city = data["city"]
            region = data["region"]
            region_code = data["region_code"]
            country = data["country"]
            country_name = data["country_name"]
            country_code_iso3 = data["country_code_iso3"]
            continent_code = data["continent_code"]
            in_eu = data["in_eu"]
            postal = data["postal"]
            latitude = data["latitude"]
            longitude = data["longitude"]
            country_timezone = data["timezone"]
            utc_offset = data["utc_offset"]
            dial_code = data["country_calling_code"]
            currency = data["currency"]
            languages = data["languages"]
            organization = data["org"]
            asn = data["asn"]

            embd = discord.Embed(title="IP Information", color=ctx.author.color, timestamp=datetime.utcnow())
            embd.add_field(name="IP Address:", value=ipaddr, inline=False)
            embd.add_field(name="ISP Name/Organization:", value=organization, inline=False)
            embd.add_field(name="City:", value=city, inline=False)
            embd.add_field(name="Regional Area:", value=region)
            embd.add_field(name="Region Code:", value=region_code, inline=False)
            embd.add_field(name="Country:", value=country, inline=False)
            embd.add_field(name="Country Name:", value=country_name, inline=False)
            embd.add_field(name="Country Code (ISO):", value=country_code_iso3, inline=False)
            embd.add_field(name="Language Spoken:", value=languages, inline=False)
            embd.add_field(name="Continent Code:", value=continent_code, inline=False)
            embd.add_field(name="Is country a member of European Union (EU)?", value=in_eu, inline=False)
            embd.add_field(name="Postal Code:", value=postal, inline=False)
            embd.add_field(name="Latitude Coordinate:", value=latitude, inline=False)
            embd.add_field(name="Longitude Coordinate:", value=longitude, inline=False)
            embd.add_field(name="Timezone:", value=country_timezone, inline=False)
            embd.add_field(name="UTC Offset:", value=utc_offset, inline=False)
            embd.add_field(name="Country Dial Code:", value=dial_code, inline=False)
            embd.add_field(name="Currency:", value=currency, inline=False)
            embd.add_field(name="Autonomous System Number:", value=asn, inline=False)
            embd.set_footer(text=f"Requested by: {ctx.message.author}", icon_url=ctx.message.author.avatar_url)

            await ctx.send(embed=embd)
        except IndexError:
            await ctx.send(embed=discord.Embed(description="⚠ An Error Occured! Make sure the IP and the formatting are correct!"))
        except KeyError:
            await ctx.send(embed=discord.Embed(description="⚠ An Error Occured! Make sure the IP and the formatting are correct!"))
