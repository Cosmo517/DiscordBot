#@bot.command(name='milestones', help='Lists # of numbers user typed')
#async def milestones(ctx, start, end):
#    counting_channel = discord.utils.get(ctx.guild.channels, name='counting')
#    history_limit = start + end
#    messages = [message async for message in counting_channel.history(limit=history_limit)]
#    count_user_numbers = {}
#    numbers_sent = []
#    for x in messages:  # loop through all messages
#        number_to_check = 0
#        try:
#            number_to_check = int(x.content)
#        except ValueError:
#            print("dead on: " + x.content)
#            continue
#        if int(end) >= number_to_check >= int(start):  # make sure its within bounds
#            if number_to_check not in numbers_sent:  # check if we counted the number already
#                numbers_sent.append(number_to_check)
#                if x.author.name in count_user_numbers:
#                    count_user_numbers[x.author.name] += 1
#                else:
#                    count_user_numbers[x.author.name] = 1
#    final_message = f"Counting from {start} to {end}:\n\n"
#    count_user_numbers = sorted(count_user_numbers.items(), key=operator.itemgetter(1), reverse=True)
#    sum = 0
#    for user in count_user_numbers:
#        sum += user[1]
#        final_message += f"{user[0]}: {user[1]}\n"
#
#    print(final_message)
#    print(f'Total sum: {sum}')
#    await ctx.send(final_message)


# must_restart = False