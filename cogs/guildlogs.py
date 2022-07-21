# Настройка
import nextcord
import typing
import asyncio
import json
import requests
import random
import aiohttp
import os
import sqlite3
import urllib.parse, urllib.request, re
from nextcord.utils import get
from itertools import cycle
from io import BytesIO
from nextcord.ext import commands, tasks
from nextcord import Member
from nextcord.ext.commands import has_permissions, MissingPermissions, cooldown, BucketType
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import psutil

class GuildLogs(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def getstatus(self, ctx, member:nextcord.Member):
        await ctx.send(f'Статус: {str(member.status)}')

def setup(client):
    client.add_cog(GuildLogs(client))