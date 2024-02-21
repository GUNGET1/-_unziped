import asyncio
import vk_api
import discord
import random
import sqlite3
import vk_sender
from discord.ext import commands


class Just_a_discord_bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.address = None
        self.msg_triggered = False
        self.new_contact = False
        self.msg_text = None
        self.curent_usr = None
        self.db = sqlite3.connect("data.sqlite")
        self.cursor = self.db.cursor()
        self.name_found = False

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.content == "dtv msg":
            await message.channel.send("кому пишем?")
            self.msg_triggered = not self.msg_triggered

            self.cursor.execute("SELECT * FROM call_book")
            results = self.cursor.fetchall()
            for i in results:
                if message.channel.send in i:
                    self.address = i[1]
                    self.name_found = True
                    break
                else:
                    self.name_found = False
            print(results)

        elif message.content == 'dtv stop':
            await message.channel.send("Принял")
            self.stop()

        elif 'vk.com/' in message.content and not self.new_contact:
            await message.channel.send("И что мы ему напишем?")
            self.address = message.content
            self.msg_triggered = not self.msg_triggered

        elif self.address is not None:
            self.msg_text = message.content
            print(''.join(self.address[6::]))
            vk_sender.send_message(''.join(self.address[7::]), self.msg_text)
            await message.channel.send("Отправляю пользователю " + self.address + " сообщение *" + self.msg_text + "*")

        elif message.content == "dtv add contact":
            await message.channel.send("Напишите контакт в формате: *ссылка на контакт* *имя контакта*")
            self.new_contact = True

        elif self.new_contact:
            c = message.content.split()
            self.cursor.execute("INSERT INTO call_book VALUES (1 , '" + c[0] + "','" + c[1]+"')")
            self.db.commit()
            self.new_contact = False

#   --------------------------------------------------------------------------------------------------------------------
#  Кусок кода ниже, теоретичски должен осуществлять поиск по базе данных. И в принципе он это делает, однако,
#  все валиться, из-за

        else:
            if self.msg_triggered:
                self.cursor.execute("SELECT * FROM call_book")
                results = self.cursor.fetchall()

                for t in results:
                    print(t)
                    if message.content in t:
                        self.address = t[1]
                        self.name_found = True
                        break

                if self.name_found:
                    self.name_found = False
                    await message.channel.send('И что мы ему напишем?')
                else:
                    await message.channel.send("Пользователь не найден. Желаете добавить? (*dtv запиши контакт*)")

    def stop(self):
        self.address = None
        self.msg_triggered = False
        self.msg_text = None
        self.curent_usr = None


client = Just_a_discord_bot()
client.run('''TOKEN''')
