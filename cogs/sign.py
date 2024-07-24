from include import *

class SignCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_dir = "./temp"
        self.pack_ms_game_script = "./utils/psptools/pack_ms_game.py"

    @app_commands.command(name="sign", description="Attach an unsigned EBOOT and get the signed version of it.")
    async def slash_command(self, interaction: discord.Interaction, file: discord.Attachment):
        if not file.filename.lower().endswith(".pbp"):
            await interaction.response.send_message("Please provide a valid PSP EBOOT.PBP file.", ephemeral=True)
            return

        os.makedirs(self.temp_dir, exist_ok=True)
        input_path = os.path.join(self.temp_dir, f"{file.filename}.DEC")
        output_path = os.path.join(self.temp_dir, f"{file.filename}.EC")

        try:
            await file.save(fp=input_path)

            result = subprocess.run(
                ["python", self.pack_ms_game_script, input_path, output_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if not os.path.isfile(output_path) or "Err" in result.stderr:
                await interaction.response.send_message("Signing process failed. Please try again.", ephemeral=True)
                return

            embed = discord.Embed(title="EBOOT Signer", description="Attaching the signed EBOOT now. It should only be seen by you.", color=0x2B2D31)
            embed.set_footer(text="Made with ❤️")

            signed_file = discord.File(output_path, filename="EBOOT.PBP")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await interaction.followup.send(file=signed_file, ephemeral=True)

        except subprocess.CalledProcessError as e:
            await interaction.response.send_message(f"Signing process failed with error: {e}", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred: {str(e)}", ephemeral=True)

        finally:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)

async def setup(bot):
    await bot.add_cog(SignCog(bot))