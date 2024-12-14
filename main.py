import discord
from discord.ext import commands
import asyncio
from antiratelimit import antiratelimit

intents = discord.Intents.default()
nova = commands.Bot(command_prefix="!", intents=intents)

rate_limiter = antiratelimit(max_req=10, time=2000, slots=3, retry=2)

async def fetch_user_data(user_id):
    await asyncio.sleep(1)
    return f"Fetched data for user {user_id}"

@nova.command()
async def get_data(ctx, user_id: int):
    try:
        result = await rate_limiter.add(
            task_id=str(user_id),
            run=lambda: fetch_user_data(user_id),
            prio=1
        )
        await ctx.send(result)
    except Exception as e:
        await ctx.send(f"Cannot fetch data for user {user_id}: {str(e)}")

nova.run("Enter_Your_Token")
