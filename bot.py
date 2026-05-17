import discord
from discord.ext import tasks
import aiohttp
import json
import os
import asyncio
import re
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
DISCORD_TOKEN  = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID     = int(os.getenv("CHANNEL_ID", "1426992316098281514"))
CHECK_INTERVAL = 30

APIS = {
    # ── Game Icons ─────────────────────────────────────────────────────────
    "icon_metal_detecting": {
        "label": "Metal Detecting Simulator!",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=1509515037&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_1": {
        "label": "Pet Simulator!",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=1599679393&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_2": {
        "label": "Pet Simulator 2!",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=2818280787&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_x": {
        "label": "Pet Simulator X! 🐾",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=6284583030&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_x_indev": {
        "label": "Pet Simulator X [In-Dev]",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=7182690801&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_99": {
        "label": "🎲 Pet Simulator 99! 🌌",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=8737899170&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_unknown": {
        "label": "🔎🔎🔎🔎",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=9866021734&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_x_staging": {
        "label": "Pet Simulator X [Staging]",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=11307162716&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_x_playground": {
        "label": "Pet Simulator X [Playground]",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=11341706073&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_x_backup": {
        "label": "Pet Simulator X [Backup!]",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=11431155244&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_99_dev": {
        "label": "[Dev] Pet Simulator 99",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=15502302041&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_sim_99_debris": {
        "label": "[Debris] Pet Simulator 99",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=17888361903&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pets_go": {
        "label": "PETS GO! ✨",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=18901165922&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pets_go_dev": {
        "label": "PETS GO! [Dev]",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=90657294029159&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pickaxe": {
        "label": "Pickaxe Animations",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=119611268818951&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pet_research": {
        "label": "Pet Research",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=137227259928308&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_pets_go_playground": {
        "label": "PETS GO! [Playground]",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=76089518712064&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_steal_a_pet": {
        "label": "Steal a Pet 😹",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=74866348003583&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_renders_99": {
        "label": "Renders 99",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=94196509911249&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_steal_a_pet_dev": {
        "label": "[Dev] Steal a Pet",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=76756166164641&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },
    "icon_delete_this": {
        "label": "delete this",
        "url": "https://thumbnails.roblox.com/v1/places/gameicons?placeIds=135790766425247&size=512x512&format=Png&isCircular=false",
        "emoji": "🎮",
    },

    # ── Game Thumbnails ────────────────────────────────────────────────────
    "thumb_metal_detecting": {
        "label": "Metal Detecting Simulator!",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=593145418&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_1": {
        "label": "Pet Simulator!",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=619296292&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_2": {
        "label": "Pet Simulator 2!",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=1020741365&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_x": {
        "label": "Pet Simulator X! 🐾",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=2316994223&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_x_indev": {
        "label": "Pet Simulator X [In-Dev]",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=2790186720&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_99": {
        "label": "🎲 Pet Simulator 99! 👑",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=3317771874&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_unknown": {
        "label": "🔎🔎🔎🔎",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=3645364755&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_x_staging": {
        "label": "Pet Simulator X [Staging]",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=4028160520&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_x_playground": {
        "label": "Pet Simulator X [Playground]",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=4038126213&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_x_backup": {
        "label": "Pet Simulator X [Backup!]",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=4065238430&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_99_dev": {
        "label": "[Dev] Pet Simulator 99",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=5349377275&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_sim_99_debris": {
        "label": "[Debris] Pet Simulator 99",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=6130409592&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pets_rng": {
        "label": "Pets RNG! ✨",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=6401952734&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pets_go_dev": {
        "label": "PETS GO! [Dev]",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=6506286476&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pickaxe": {
        "label": "Pickaxe Animations",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=7025617125&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pet_research": {
        "label": "Pet Research",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=7392503703&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_pets_go_playground": {
        "label": "PETS GO! [Playground]",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=7473267135&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_steal_a_pet": {
        "label": "Steal a Pet 😹",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=7937194831&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_renders_99": {
        "label": "Renders 99",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=7970240424&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_steal_a_pet_dev": {
        "label": "[Dev] Steal a Pet",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=8041352072&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
    "thumb_delete_this": {
        "label": "delete this",
        "url": "https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=10124637799&countPerUniverse=10&defaults=true&size=768x432&format=Png&isCircular=false",
        "emoji": "🖼️",
    },
}

STATE_FILE = "state.json"
# ──────────────────────────────────────────────────────────────────────────────


def get_link_id(url: str) -> str:
    """
    Extract the stable filename from a rbxcdn URL so we're not fooled by
    rotating query-string tokens. For example:
      https://tr.rbxcdn.com/abc123/image.png?token=xyz  →  abc123/image.png
    If we can't parse it we fall back to the full URL.
    """
    # Grab everything between the host and the query string
    match = re.search(r"rbxcdn\.com/(.+?)(?:\?|$)", url)
    return match.group(1) if match else url


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def extract_cdn_links(data: dict) -> dict[str, str]:
    """
    Returns a dict of  { stable_id: full_url }
    so we compare by stable ID but still send the full URL.
    """
    links: dict[str, str] = {}
    for item in data.get("data", []):
        url = item.get("imageUrl", "")
        if url and "rbxcdn" in url:
            links[get_link_id(url)] = url
        for thumb in item.get("thumbnails", []):
            url = thumb.get("imageUrl", "")
            if url and "rbxcdn" in url:
                links[get_link_id(url)] = url
    return links


async def send_embed(channel, api, link, title, color):
    embed = discord.Embed(
        title=f"{api['emoji']}  {title} — {api['label']}",
        color=color,
        timestamp=datetime.now(timezone.utc),
    )
    embed.add_field(name="🔗 CDN URL", value=f"```\n{link}\n```", inline=False)
    embed.add_field(name="🌐 Preview", value=f"[Open image]({link})", inline=True)
    embed.set_image(url=link)
    embed.set_footer(text="Roblox CDN Monitor")
    await channel.send(content="@everyone", embed=embed)


# ── Bot ───────────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
state: dict = {}
first_run = True


@bot.event
async def on_ready():
    global state
    state = load_state()
    print(f"✅  Logged in as {bot.user}")
    print(f"📡  Monitoring {len(APIS)} endpoint(s) every {CHECK_INTERVAL}s")
    monitor_loop.start()


@tasks.loop(seconds=CHECK_INTERVAL)
async def monitor_loop():
    global state, first_run

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("⚠️  Channel not found — check CHANNEL_ID")
        return

    async with aiohttp.ClientSession() as session:
        for key, api in APIS.items():
            try:
                async with session.get(api["url"], timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status != 200:
                        print(f"[{datetime.now():%H:%M:%S}] {key}: HTTP {resp.status}")
                        continue
                    data = await resp.json()
            except Exception as exc:
                print(f"[{datetime.now():%H:%M:%S}] {key}: fetch error — {exc}")
                continue

            current = extract_cdn_links(data)           # { stable_id: full_url }
            previous_ids: set = set(state.get(key, {}).keys() if isinstance(state.get(key), dict) else state.get(key, []))

            # First run — silently save state, send nothing
            if first_run:
                state[key] = current
                save_state(state)
                print(f"[{datetime.now():%H:%M:%S}] INIT {key}: {len(current)} link(s) saved")
                continue

            current_ids  = set(current.keys())
            new_ids      = current_ids - previous_ids
            removed_ids  = previous_ids - current_ids

            if new_ids:
                state[key] = current
                save_state(state)
                for sid in sorted(new_ids):
                    full_url = current[sid]
                    await send_embed(channel, api, full_url, "New CDN link detected", 0x00FF88)
                    print(f"[{datetime.now():%H:%M:%S}] NEW  {key}: {full_url}")
                    await asyncio.sleep(1)

            if removed_ids:
                state[key] = current
                save_state(state)
                for sid in sorted(removed_ids):
                    embed = discord.Embed(
                        title=f"⚠️  CDN link removed — {api['label']}",
                        color=0xFF4444,
                        timestamp=datetime.now(timezone.utc),
                    )
                    embed.add_field(name="🔗 Removed ID", value=f"```\n{sid}\n```", inline=False)
                    embed.set_footer(text="Roblox CDN Monitor")
                    await channel.send(content="@everyone", embed=embed)
                    print(f"[{datetime.now():%H:%M:%S}] GONE {key}: {sid}")
                    await asyncio.sleep(1)

            if not new_ids and not removed_ids:
                print(f"[{datetime.now():%H:%M:%S}] {key}: no changes ({len(current_ids)} link(s))")

    if first_run:
        first_run = False


@monitor_loop.before_loop
async def before_monitor():
    await bot.wait_until_ready()


bot.run(DISCORD_TOKEN)
