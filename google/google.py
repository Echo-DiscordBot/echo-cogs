import discord

from redbot.core import commands
from datetime import datetime
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

class Google(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def google(self, ctx, *, search_query):
    """Search google with a simple URL."""
    querytemplate = f"https://www.google.co.uk/search?source=hp&ei=z07WX6SiGrXVgwfdpa3wAQ&q={search_query.capitalize()}"
    multipleargs = querytemplate.replace(' ', '%20')
    chfmi = "Click here for search results"
    now = datetime.now()
    strftime = now.strftime("Today at %H:%M %p")
    footer = f"{strftime}"
    hassearched = f"{ctx.author.name} searched for: **{search_query}**."
    e = discord.Embed(title=":desktop:  Google Search",
                      description="{}\n\n**[{}]({})**".format(hassearched, chfmi, multipleargs),
                      colour=discord.Colour.red())
    e.set_footer(text=footer)
    e.set_thumbnail(url="https://media.discordapp.net/attachments/769165401879478302/787742449987878972/google_icon_131222.png")
    await ctx.send(embed=e)
    
  @commands.command()
  async def googlenew(self, ctx, *, search_query):
    """Google New One"""
    percents = {" ": "+", "!": "%21", '"': "%22", "#": "%23", "$": "%24", "%": "%25", "&": "%26", "'": "%27",
                "(": "%28", ")": "%29", "*": "%2A", "+": "%2B", "`": "%60", ",": "%2C", "-": "%2D", ".": "%2E",
                "/": "%2F"}
    searchquery = ""
    for char in search_query:
        if char in percents.keys():
            char = percents[char]
        searchquery += char
    session = FuturesSession()
    future = session.get("https://google.com/search?q=" + searchquery)
    response_one = future.result()
    soup = BeautifulSoup(response_one.text, 'html.parser')
    try:
        title_ = soup.find('h3', class_="LC20lb DKV0Md")[0].text
        text_ = soup.find('span', class_="aCOpRe")[0].text
        await ctx.send(title_)
        await ctx.send(text_)
        #source_ = soup.find_all('span', class_="uEec3 AP7Wnd")[-1].get_text()
    except AttributeError:
        title_, text_ = "Not Found: {}".format(search_query), "Not Found: {}".format(search_query)
    e = discord.Embed(title=":desktop:  Google Search: {}".format(searchquery),
                    description="{}\n\n{}".format(title_,text_),
                    colour=discord.Colour.red())
    #e.set_footer(text=footer)
    e.set_thumbnail(url="https://media.discordapp.net/attachments/769165401879478302/787742449987878972/google_icon_131222.png")
    session.close()
    await ctx.send(embed=e)
