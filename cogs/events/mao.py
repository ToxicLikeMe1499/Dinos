from nextcord.ext import commands
import random

class mao(commands.Cog):
	def __init__(self, bot):
		self.bot=bot

	@commands.Cog.listener()
	async def on_message(self, message):
		await self.bot.wait_until_ready()
		if "mao" in message.content.lower():
			author = message.author
			if author.bot:
				return
			channel = message.channel
			await message.delete()
			await channel.send("Nix Mao das heißt Miau :cat:")
		if "pizza" in message.content.lower():
			if not message.author.bot:
				channel = message.channel
				if random.random() < 0.06:
					await channel.send("Pizzaparty :partying_face: :pizza: :mirrir_ball: :tada: :piza:")
				else:
					await channel.send("Sagte wer Pizza :pizza:")

def setup(bot):
	bot.add_cog(mao(bot))