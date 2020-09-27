from discord.ext.commands import Bot as BotBase
from glob import glob
import apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File
from datetime import datetime
from discord.ext.commands import CommandNotFound
from ..db import db
from apscheduler.triggers.cron import CronTrigger
import os

PREFIX = "+"
OWNER_IDS = [618038532665114624]
COGS = [path.split(os.sep)[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()


        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX, OWNER_IDS=OWNER_IDS)

        super().__init__(command_prefix = PREFIX, owner_ids = OWNER_IDS)

    def setup(self):
        for cog in COGS:
            print(cog)
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} was loaded!")

        print("Setup Completed!")

    def run(self, version):
        self.VERSION = version

        print("Running Setup...")
        self.setup()


        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def print_message(self):
        await self.stdout.send("Good Morning!")

    async def on_connect(self):
        print("BOT has been CONNECTED!")

    async def on_disconnect(self):
        print("BOT has been DISCONNECTED!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong!")

        else:
            channel = self.stdout
            await channel.send("Dude your code freaking sucks, and error occured right here!")

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.channel = self.get_channel(757016278060761178)
            self.ready = True
            self.guild = self.get_guild(746850984701198437)
            self.stdout = self.get_channel(757016278060761178)
            self.scheduler.add_job(self.print_message, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()
            #channel = self.channel
            await self.stdout.send("Now online!")

            # embed = Embed(title="Now online!", url="https://www.github.com/woosal1337",
            #               description="MadeInAZE is now online.",
            #               colour=0xFF0000,
            #               timestamp=datetime.utcnow())
            # fields = [("Name", "Value", True),
            #           ("Another field", "Next to the first one", True),
            #           ("A non-inline field", "This field will appear on third row.", False)]
            #
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            #
            # embed.set_author(name="@woosal1337", icon_url=self.guild.icon_url)
            # embed.set_footer(text="This is a footer xD?")
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)
            # await channel.send(embed=embed)
            #
            # await channel.send(file=File("./data/images/elon.gif"))

            print("BOT is ready!")

        else:
            print("BOT reconnected!")

    async def on_message(self, message):
        pass

bot = Bot()