import disnake
from disnake.ext import commands
from disnake import TextInputStyle
import payment
import config
import sqlApi
import MCApi
import sftp
import json

intents = disnake.Intents.default()
intents.presences = True
intents.messages = True
intents.reactions = True
intents.voice_states = True

bot = commands.Bot(command_prefix=None, intents=intents)

class Modal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label='ПРОВЕРЬТЕ ПРАВИЛЬНОЕ НАПИСАНИЕ НИКНЕЙМА',
                placeholder="Никнейм Игрока Java Edition",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=16,
            ),
        ]
        super().__init__(title="Покупка проходки на BMS", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Покупка проходки")
        guild = inter.guild

        channel = await guild.create_text_channel(f'{inter.user.name}-проходка', overwrites={
            guild.default_role: disnake.PermissionOverwrite(view_channel=False),
            guild.me: disnake.PermissionOverwrite(view_channel=True, send_messages=True),
            inter.author: disnake.PermissionOverwrite(view_channel=True, send_messages=True)
        })

        for key, value in inter.text_values.items():
            embed.add_field(
                name=f"На никнейм: **{value[:1024]}**",
                inline=False,
                value="",
            )

            sqlApi.add_to_db(int(inter.user.id), "None")
            sqlApi.add_to_db(int(inter.user.id), value[:1024])

        button_row = disnake.ui.ActionRow(
            disnake.ui.Button(style=disnake.ButtonStyle.green, label="Оплатить", url=payment.create_pay(config.BMS_PRICE, config.BMS_DESCRIPTION)),
            disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Проверить", custom_id="check_buy"),
            disnake.ui.Button(style=disnake.ButtonStyle.red, label="Закрыть канал", custom_id="close_channel")
        )

        await channel.send(inter.user.mention)
        await channel.send(embed=embed, components=button_row)

@bot.slash_command(name='buy', description='Покупка проходки на BMS')
async def buy(inter: disnake.AppCmdInter):
    await inter.response.send_modal(modal=Modal())

@bot.event
async def on_button_click(interaction: disnake.MessageInteraction):
    if interaction.component.custom_id == "check_buy":
        if payment.check_pay() == "Успешно!":
    
            nick = sqlApi.select_nick_from_db(interaction.user.id)
            print(nick)
            
            if MCApi.get_uuid(nick) is None:

                await interaction.send(f"**{nick}** Не был добавлен в вайтлист.\nПроверьте правильно ли вы написали никнейм, вскоре вам ответит наша администрация чтобы добавить вас.")
                
                channel = bot.get_channel(config.ChannelId)
                await channel.send(f"<@&1244002585795629177> Пользователю {interaction.user.mention} нужна помощь! Зайдите к нему в тикет и помогите бедолаге")

            else:
                state = False
                with open("whitelist.json", "r") as file:
                    data = json.load(file)
                    for i in data:
                        if i['name'] == nick:
                            await interaction.send(f"**{nick}** Уже есть в вайт листе!")
                            state = True
                            break
                if state == True:
                    state = False
                else:    
                    hostname = config.host
                    port = config.port
                    username = config.user
                    password = config.password
                    remote_filepath = 'whitelist.json'
                    local_filepath = 'whitelist.json'

                    role = disnake.utils.get(interaction.guild.roles, id = config.PlayerRole)
                    await interaction.user.add_roles(role)
                    await interaction.send(f"**{nick}** Добавлен в ВайтЛист!\n \nIp: **{config.ip}**\nВерсия: **{config.version}**\n\nОбязательно прочитайте правила в канале <#{config.RuleChannel}> и законы в <#{config.LawChannel}>")

                    sftp.download_file_sftp(hostname, port, username, password, remote_filepath, local_filepath)
                    MCApi.whitelist_add(nick, MCApi.get_uuid(nick))

        else:
            await interaction.send(payment.check_pay())

    elif interaction.component.custom_id == "close_channel":

        member = interaction.author
        guild = interaction.guild
        required_role_id = config.RoleIdForClose

        required_role = disnake.utils.get(guild.roles, id=required_role_id)
        
        if required_role in member.roles:
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("Для удаления канала нужна роль Администратора!", ephemeral=True)

bot.run(config.TOKEN)    