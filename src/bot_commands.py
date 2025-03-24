import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime, timedelta
import asyncio

NOTICE_CHANNEL_ID = 1318964126290284604  # Replace with your actual channel ID
bot: commands.Bot = None


async def setup(bot_instance: commands.Bot):
    """Setup function to initialize commands and tasks."""
    global bot
    bot = bot_instance
    send_events.start()  # Start the task when the bot is ready
    logging.info("Event scheduling task started.")


def calculate_event_dates(start_date, loop_count):
    """Calculate event dates dynamically."""
    events = {}
    for loop in range(loop_count):
        if loop == 0:
            impenetrable_start = start_date
        else:
            impenetrable_start = powerful_equipment_start + timedelta(days=4)
        events[f"Impenetrable Territory (Buildings) {loop + 1}"] = (impenetrable_start, impenetrable_start + timedelta(days=4))

        merchant_start = impenetrable_start + timedelta(days=4) - timedelta(days=1)
        events[f"Merchant Ship Plunder {loop + 1}"] = (merchant_start, merchant_start + timedelta(days=4))

        use_store_start = merchant_start + timedelta(days=4) - timedelta(days=2)
        events[f"Use store points {loop + 1}"] = (use_store_start, use_store_start + timedelta(days=4))

        eitc_attack_start = use_store_start + timedelta(days=4) - timedelta(days=1)
        events[f"EITC ATTACK {loop + 1}"] = (eitc_attack_start, eitc_attack_start + timedelta(days=4))

        earn_store_start = eitc_attack_start + timedelta(days=4) - timedelta(days=1)
        events[f"Earn store points {loop + 1}"] = (earn_store_start, earn_store_start + timedelta(days=4))

        best_hunter_start = earn_store_start + timedelta(days=4) - timedelta(days=2)
        events[f"The Best Hunter {loop + 1}"] = (best_hunter_start, best_hunter_start + timedelta(days=4))

        best_researcher_start = best_hunter_start + timedelta(days=4) - timedelta(days=1)
        events[f"The best researcher {loop + 1}"] = (best_researcher_start, best_researcher_start + timedelta(days=4))

        count_on_ships_start = best_researcher_start + timedelta(days=4)
        events[f"Count on ships {loop + 1}"] = (count_on_ships_start, count_on_ships_start + timedelta(days=4))

        reliable_tacticians_start = count_on_ships_start + timedelta(days=4)
        events[f"Reliable Tacticians {loop + 1}"] = (reliable_tacticians_start, reliable_tacticians_start + timedelta(days=4))

        powerful_equipment_start = reliable_tacticians_start + timedelta(days=4)
        events[f"Powerful Equipment {loop + 1}"] = (powerful_equipment_start, powerful_equipment_start + timedelta(days=4))

    return events

def format_date(date):
    """Format the date to 'February 7th, 2025'."""
    day = date.day
    suffix = "th" if 4 <= day <= 20 or 24 <= day <= 30 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return f"{date.strftime('%B')} {day}{suffix} {date.year}"


@tasks.loop(seconds=10)
async def send_events():
    """Send the upcoming events every 24 hours at 00:01 UTC."""
    await bot.wait_until_ready()  # Ensure the bot is fully ready

    channel = bot.get_channel(NOTICE_CHANNEL_ID)
    if not channel:
        logging.error(f"Channel ID {NOTICE_CHANNEL_ID} not found.")
        return

    start_date = datetime(2025, 2, 7)  # Start date of "Impenetrable Territory (Buildings)"
    loop_count = 6  # Number of cycles to generate

    events = calculate_event_dates(start_date, loop_count)
    today = datetime.utcnow()

    # Prepare today's events
    today_events = [
        f"🟢 {format_date(start)}: *{event}*"
        for event, (start, _) in events.items()
        if start.date() == today.date()
    ]

    # Prepare upcoming events (next 14 days)
    upcoming_events = [
    f"⏳{event.replace(' 1', '')}: 🟢{start.strftime('%B %d, %Y')} - 🔴{end.strftime('%B %d, %Y')}"
    for event, (start, end) in events.items()
    if today <= start <= today + timedelta(days=14)
    ]

    # Construct the embed
    embed = discord.Embed(title="Server 86 Events", color=discord.Color.blue())

    # Add "Today's Events"
    if today_events:
        embed.add_field(name="Today's Events:", value="\n".join(today_events), inline=False)
    else:
        embed.add_field(name="Today's Events:", value="No event is starting or happening today.", inline=False)

    # Add "Your Horizons Event Calendar"
    if upcoming_events:
        embed.add_field(name="Your Horizons Event Calendar:", value="\n\n".join(upcoming_events), inline=False)

    # Send the embed message
    await channel.send(embed=embed)
    logging.info("Posted upcoming events to Discord.")
