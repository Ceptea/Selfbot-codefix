import discord
import random
from discord.ext import commands
from Backend.Modules.ecoCore import Economy as EcoCore

class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EcoCore(bot)
        self.symbols = ["🍒", "🍊", "🍋", "🍇", "💎", "7️⃣"]
        self.payouts = {
            "🍒": 2,
            "🍊": 2,
            "🍋": 3,
            "🍇": 4,
            "💎": 5,
            "7️⃣": 10
        }
        
    @commands.command(description="Play slots")
    async def slots_cmd(self, ctx, args):
        try:
            bet = int(args)
            
            # Generate results
            results = [random.choice(self.symbols) for _ in range(3)]
            
            # Check for wins
            if all(x == results[0] for x in results):
                winnings = bet * self.payouts[results[0]]
                self.db.add_balance(ctx.author.id, winnings)
                await ctx.send(f"🎰 [{' | '.join(results)}]\nJACKPOT! You won **${winnings}**!")
            else:
                self.db.remove_balance(ctx.author.id, bet)
                await ctx.send(f"🎰 [{' | '.join(results)}]\nYou lost **${bet}**!")
                
        except ValueError:
            await ctx.send("Invalid bet amount! Please use a number.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

async def setup(bot):
    slots_cog = Slots(bot)
    slots_cmd = slots_cog.slots_cmd
    slots_cmd.name = "slots"
    bot.eco.add_command(slots_cmd)
    await bot.add_cog(slots_cog) 