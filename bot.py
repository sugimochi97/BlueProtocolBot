import discord
from discord.ext import commands, tasks
from get_news import get_news_texts
from vertex_ai import summary_text

token = ""

# 初期化
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@tasks.loop(seconds=1)
async def send_news():
    """一日ごとにニュースをチェックして新規ニュースがあれば送信
    引数： なし
    戻り値: なし
    """
    # 送信するチャンネルを取得
    channel_id = None
    channel = client.get_channel(channel_id)
    # ニュース文を取得
    news_list, title_list, urls = get_news_texts()
    # ニュース文を要約しながら送信
    if news_list:
        await channel.send("# 新規ニュース！")
    else:
        print("新規ニュースなし")

    for i in range(len(news_list)):
        summary = summary_text(news_list[i])
        output = f"## 【{title_list[i]}】\n{urls[i]}\n□ 概要\n" + summary
        await channel.send(output)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    send_news.start()

client.run(token)