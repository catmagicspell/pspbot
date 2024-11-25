from include import *

class ResolveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_data = self.load_error_data("db.txt")

    def load_error_data(self, file_path):
        error_data = {}
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 3:
                        code, error_str, error_dsc = data
                        error_data[code] = (error_str, error_dsc)
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return error_data

    def find_error(self, input_code):
        return self.error_data.get(input_code, (None, None))

    def find_error_type(self, code):
        if code.startswith("8000"):
            return "Common (SCE_ERROR_FACILITY_NULL)"
        elif code.startswith("8001"):
            return "C Standard Library"
        elif code.startswith("8002"):
            return "Kernel"
        elif code.startswith("8011"):
            return "Utility"
        elif code.startswith("8021"):
            return "UMD"
        elif code.startswith("8022"):
            return "Memory Stick™"
        elif code.startswith("8024"):
            return "USB"
        elif code.startswith("8026"):
            return "Audio"
        elif code.startswith("8041"):
            return "psp_net/WLAN"
        elif code.startswith("8042"):
            return "SAS (Software Audio Synthesizer)"
        elif code.startswith("8043"):
            return "Network"
        elif code.startswith("8044"):
            return "lib_wave"
        elif code.startswith("8046"):
            return "lib_font"
        elif code.startswith("8051"):
            return "Psheet"
        elif code.startswith("8053"):
            return "DNAS (Dynamic Network Authentication System)"
        elif code.startswith("8055"):
            return "PSN"
        elif code.startswith("8061"):
            return "Audio/Video Decoder"
        elif code.startswith("8063"):
            return "lib_atrac3plus"
        else:
            return "Other"

    @app_commands.command(name="resolve", description="Input an error code and get details about it.")
    async def get_command(self, interaction: discord.Interaction, error: str):
        error = error.upper()
        error_type = self.find_error_type(error)
        error_str, error_dsc = self.find_error(error)
        
        if error_str:
            embed = discord.Embed(title="Error Code Resolver", description=error, color=0x2B2D31)
            embed.add_field(name="Error Type:", value=error_type, inline=True)
            embed.add_field(name="Hex Value:", value="0x" + error, inline=True)
            embed.add_field(name="String:", value=error_str, inline=True)
            embed.add_field(name="Description:", value=error_dsc, inline=False)
            embed.set_footer(text="Made with ❤️")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Cannot find the specified code in the database.")

async def setup(bot):
    await bot.add_cog(ResolveCog(bot))