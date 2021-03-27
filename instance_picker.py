### instance_picker.py: Allows users to run functions ("modules") on a specific instance they pick stored in a central database.
### Created by Cam Cuozzo (@camcuozzo on Github)
### This script is used as one of the functions in the front-end script for Lyra.

import asyncio
import discord
from discord.ext import commands
import re

emoji_nums = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟"] # For emoji reactions

# Make sure you create the bot object here and pass in your bot's token first!

# Async function to communicate to another back-end script through a local Unix socket
async def async_comms(command, args):
	reader, writer = await asyncio.open_unix_connection("/tmp/docker.socket")
	writer.write(json.dumps({'command': command, 'args': args}).encode())
	data = await reader.read(1024) # Increase this number if you need more
	print (data) # For debugging purposes - feel free to comment out
	return json.loads(data.decode())

# The full instance picker function
@bot.event
async def instance_picker(ctx, module, arg=None):
	json_data = await async_comms('request', {'request': 'name', 'owner': str(ctx.message.author.id)}) # 'Request' is a function we have made in the back-end: it returns what instances a user has based on their Discord UUID
	if json_data['status'] == 'success': # Our version of basic error handling that is implemented in the back-end script - feel free to change or remove
		names_list = json_data['result'] # Getting the list of instances that is returned
		inst_num = len(names_list)
		if (inst_num > 1): # We're only enabling the instance picker if the user has more than one instance
			emoji_list = [] # This will be the list of emojis in use by the picker
			for x in range(inst_num):
				list.append(emoji_list, emoji_nums[x]) # Add from emoji_nums into emoji_list until there are no more instances to account for
			inst_list = "\n".join("{} {}".format(first, second) for first, second in zip(emoji_list, names_list)) # Pairing the emojis with the instance name text with join() to make it look nice
			embed = discord.Embed(title = "Which instance would you like to select?", description = re.sub("\ |\[|'|\]", "", inst_list), color=0xCC00FF) # Regex line substitutes quotes and brackets from the instance names
			message = await ctx.send(embed=embed)
			for x in range(inst_num): 
				await message.add_reaction(emoji_list[x]) # Adding the emoji reactions
			@bot.event
			async def on_reaction_add(reaction, user):
				if user.id == ctx.message.author.id: 
					container_name = '{}'.format(*names_list[emoji_list.index(reaction.emoji)]) # Doing some more formatting stuff to make sure a valid string is being passed in
					await module(ctx, container_name) # You can add paramaters to this if you need more
		else: # If the user only has one instance
			container_name = '{}'.format(*names_list[0]) # Doing some more formatting stuff to make sure a valid string is being passed in
			await module(ctx, container_name) # You can add paramaters to this if you need more
