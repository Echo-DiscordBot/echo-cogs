import discord

from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

class LyricsFinder(commands.Cog):
    """Get Song Lyrics."""

    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self._cache = {}

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def whois(self, ctx, ip=None):
      if ip is None:
          print('\n[LOGS] Must enter a ip!')
            await ctx.send('Must enter a ip!')
        else:
            print(f'\n[LOGS] Running whois on {ip}')
            host = socket.gethostbyname(ip)
            w = IPWhois(host)
            res = w.lookup_whois(inc_nir=True)
            final_res = """
    IP: {}
    IP Range: {}
    Name: {}
    Handle: {}
    Registry: {}
    Description: {}
    Date: {}
    Updated: {}
    Country: {} 
    State: {}
    City: {}
    Address: {}
    Postal Code: {}
            """.format(res['query'], res['nets'][0]['range'], res['nets'][0]['name'], res['nets'][0]['handle'], res['asn_registry'], res['asn_description'], res['asn_date'], res['nets'][0]['updated'], res['nets'][0]['country'], res['nets'][0]['state'], res['nets'][0]['city'], res['nets'][0]['address'], res['nets'][0]['postal_code'])
            print(final_res)
            await ctx.send(final_res)
        
 
