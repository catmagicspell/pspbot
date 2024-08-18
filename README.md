# pspbot
pspbot is a Discord bot that helps with PSP homebrew development.<br/>
[Add pspbot to your server!](https://discord.com/oauth2/authorize?client_id=1203339222069809182)
# Commands
`/resolve` allows you to get details about a PSP error code (if it exists on the database).<br/>
`/search` allows you to search NIDs in PSPLibDoc by its' name or hexademical value.<br/>
`/sign` allows you to sign your homebrew using psptools to make them work on both CFW and OFW. <br/>

# Installation & Running
You need to have Python installed.<br/>
```
git clone https://github.com/catmagicspell/pspbot
cd pspbot
pip install -r ./requirements.txt
```
Add your Discord Bot Token to the `TOKEN` field of the `config.py`<br/>
Run `python bot.py` to start the bot.

# Credits
- [reha](https://github.com/rreha) and [PonpiK](https://github.com/PonpiK) of **[Cat Magic Spell](https://github.com/catmagicspell)** for leading the project and testing<br/>
- [Spenon-dev](https://github.com/Spenon-dev) for **[PSPLibDoc](https://github.com/Spenon-dev/PSPLibDoc)**<br/>
- [artart78](https://github.com/artart78) for **[the fork of PSPLibDoc](https://github.com/artart78/PSPLibDoc)**<br/>
- [galaxyhaxz](https://github.com/galaxyhaxz) for **[psptools](https://github.com/galaxyhaxz/Infinity/commit/6de980d8fbcaad8bf7a1e7d48a3b476a55752088)**<br/>
- [Yoti](https://github.com/RealYoti) for **[the fork of psptools](https://github.com/Yoti/psp_pspident/tree/master/psptools)**<br/>
- and many others who contributed to the PSP scene...<br/>
