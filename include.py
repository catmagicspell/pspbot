import os
import asyncio
import config
import shutil
import subprocess

import aiohttp
import xml.etree.ElementTree as ET

import discord
from discord import app_commands
from discord.ext import tasks, commands