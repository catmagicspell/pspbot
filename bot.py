from include import *

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.watching, name='https://github.com/catmagicspell/pspbot')
    )
    print(f'bot is logged in as {bot.user.name}')
    synced = await bot.tree.sync()

async def setup_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await setup_cogs()
    await bot.start(config.TOKEN)

if __name__ == '__main__':
    asyncio.run(main())