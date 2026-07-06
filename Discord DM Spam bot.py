import discord
import asyncio
import random
import time

TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot's token

# ===== CONFIGURATION =====
TARGET_IDS = [ 1234567890 , 1234567890]# Target]

MESSAGES = [
    "@everyone https://cdn.discordapp.com/attachments/1439567435026923666/1454234445346504774/caption-4weasd.gif?ex=698e4f5e&is=698cfdde&hm=1d7b6809da165daa970051be7dda543eed21efec3aef829dccf6643324edf418",
]

DELAY_BETWEEN_MSGS = 0.5      # Seconds between each message
DELAY_BETWEEN_LOOPS = 0.1       # Seconds between full loops
MAX_LOOPS = 0                  # 0 = infinite, set a number to stop after X loops
RANDOMIZE = True               # Randomize message order each loop
# ==========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class SpamBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"Bot logged in as {self.user}\n")
        print(f"Targets: {TARGET_IDS}")
        print(f"Max Loops: {'Infinite' if MAX_LOOPS == 0 else MAX_LOOPS}")
        print(f"Delay between messages: {DELAY_BETWEEN_MSGS}s")
        print(f"Delay between loops: {DELAY_BETWEEN_LOOPS}s")
        print(f"\nPress Ctrl+C to stop\n")
        print("=" * 60)
        
        loop_count = 0
        start_time = time.time()
        
        while True:
            loop_count += 1
            elapsed = time.time() - start_time
            
            print(f"\n🔁 LOOP #{loop_count} | Runtime: {elapsed:.0f}s")
            print("-" * 50)
            
            # Shuffle targets each loop for variety
            targets = list(TARGET_IDS)
            if RANDOMIZE:
                random.shuffle(targets)
            
            # Use shuffled messages
            msgs = list(MESSAGES)
            if RANDOMIZE:
                random.shuffle(msgs)
            
            for target_id in targets:
                try:
                    user = await self.fetch_user(target_id)
                    
                    for msg in msgs:
                        timestamp = time.strftime("%H:%M:%S")
                        
                        print(f"[{timestamp}] [{target_id}] {user.name}", end=" | ")
                        print(f"Msg: {msg[:40]}{'..' if len(msg) > 40 else ''}", end=" | ")
                        
                        await user.send(msg)
                        
                        print("✅")
                        await asyncio.sleep(DELAY_BETWEEN_MSGS)
                        
                except discord.Forbidden:
                    print(f"[{time.strftime('%H:%M:%S')}] [{target_id}] ❌ DMs CLOSED")
                except discord.HTTPException as e:
                    print(f"[{time.strftime('%H:%M:%S')}] [{target_id}] ❌ {e}")
                except Exception as e:
                    print(f"[{time.strftime('%H:%M:%S')}] [{target_id}] ❌ ERROR: {e}")
            
            print("-" * 50)
            print(f"Loop #{loop_count} complete. Next round in {DELAY_BETWEEN_LOOPS}s...")
            
            if MAX_LOOPS > 0 and loop_count >= MAX_LOOPS:
                print(f"\n✅ Reached max {MAX_LOOPS} loops. Stopping.")
                break
            
            await asyncio.sleep(DELAY_BETWEEN_LOOPS)
        
        total_time = time.time() - start_time
        print(f"\nTotal runtime: {total_time:.0f}s ({total_time/60:.1f} minutes)")
        await self.close()

client = SpamBot()
client.run(TOKEN)
