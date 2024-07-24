from include import *

class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.psplibdoc = "https://raw.githubusercontent.com/artart78/PSPLibDoc/new_format/PSPLibDoc/PSPLibDoc.xml"

    async def fetch_xml(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()

    def parse_xml(self, xml_data):
        root = ET.fromstring(xml_data)
        prxfiles = []
        for prxfile in root.findall('.//PRXFILE'):
            prxfiles.append({
                'prx': prxfile.findtext('PRX', 'Unknown'),
                'prxname': prxfile.findtext('PRXNAME', 'Unknown'),
                'libraries': [
                    {
                        'name': library.findtext('NAME', 'Unknown'),
                        'functions': [
                            {
                                'nid': function.findtext('NID', 'Unknown'),
                                'name': function.findtext('NAME', 'Unknown')
                            }
                            for function in library.findall('.//FUNCTION')
                        ]
                    }
                    for library in prxfile.findall('.//LIBRARY')
                ]
            })
        return prxfiles

    async def create_embed(self, result, index, total_results):
        embed = discord.Embed(title="PSPLibDoc Searcher", color=0x2B2D31)
        embed.add_field(name='PRX File:', value=result['prx'])
        embed.add_field(name='PRX Name:', value=result['prxname'])
        embed.add_field(name='Library Name:', value=result.get('libname', 'Unknown'))
        embed.add_field(name='Function Name:', value=result.get('funcname', 'Unknown'))
        embed.add_field(name='Function NID:', value=result.get('funcnid', 'Unknown'))
        embed.set_footer(text=f'Page {index} of {total_results} | Made with ❤️')
        return embed

    class PaginatedView(discord.ui.View):
        def __init__(self, embeds):
            super().__init__()
            self.embeds = embeds
            self.current_page = 0
            self.update_buttons()

        def update_buttons(self):
            self.children[0].disabled = self.current_page == 0
            self.children[1].disabled = self.current_page == len(self.embeds) - 1

        async def update_message(self, interaction: discord.Interaction):
            await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

        @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary, disabled=True)
        async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.current_page > 0:
                self.current_page -= 1
                self.update_buttons()
                await self.update_message(interaction)

        @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary, disabled=True)
        async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.current_page < len(self.embeds) - 1:
                self.current_page += 1
                self.update_buttons()
                await self.update_message(interaction)

    @app_commands.command(name='search', description='Search NIDs in XML by their name or hexadecimal value.')
    async def search_command(self, interaction: discord.Interaction, nid: str = None, name: str = None):
        await interaction.response.defer()

        xml_data = await self.fetch_xml(self.psplibdoc)
        if not xml_data:
            await interaction.followup.send("Failed to fetch XML data.")
            return

        prxfiles = self.parse_xml(xml_data)

        results = [
            {
                'prx': prx['prx'],
                'prxname': prx['prxname'],
                'libname': library['name'],
                'funcnid': function['nid'],
                'funcname': function['name']
            }
            for prx in prxfiles
            for library in prx['libraries']
            for function in library['functions']
            if (nid and nid.lower() in function['nid'].lower()) or (name and name.lower() in function['name'].lower())
        ]

        if not results:
            await interaction.followup.send("No results found.")
            return

        embeds = [
            await self.create_embed(result, i + 1, len(results))
            for i, result in enumerate(results)
        ]

        await interaction.followup.send(embed=embeds[0], view=self.PaginatedView(embeds))

async def setup(bot):
    await bot.add_cog(SearchCog(bot))