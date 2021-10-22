import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print("login succeed")
    print(client.user.name)
    print(client.user.id)
    print("-------------")

    for channel in client.get_all_channels():
        print("----------")
        print("チャンネル名：" + str(channel.name))
        print("チャンネルID：" + str(channel.id))
        print("-------------")


# mainメソッド ----------------------------------------------------------
@client.event
async def on_message(message):
    #print(message.author.roles)
    # 入力したユーザーがボットの場合何も処理しない
    if message.author.bot:
        return

    # コマンドを格納する二次元リスト
    commandsList = {
        0:{"!apex":"0", "!r6s":"1", "!valo":"2"},
        1:{"casual":"0", "c":"0", "unrated":"0", "un":"0",
           "rank":"1", "r":"1", "competitive":"1", "co":"1"}
    }

    # 入力されたコマンドを空白で分割・小文字に変換し、格納する
    inputList = list(map( str.lower, message.content.split() ))
    while len(inputList) < 4:
        inputList.append("None")

    name = message.author.name
    icon = message.author.avatar_url
    rank = inputList[2]
    apexRankList = {"bronze":"ブロンズ", "silver":"シルバー", "gold":"ゴールド", "platinum":"プラチナ", "diamond":"ダイヤモンド", "master":"マスター", "predator":"プレデター",
                "b":"ブロンズ", "s":"シルバー", "g":"ゴールド", "p":"プラチナ", "d":"ダイヤモンド", "m":"マスター", "pr":"プレデター"}

    r6sRankList = {"copper":"コッパー", "bronze":"ブロンズ", "silver":"シルバー", "gold":"ゴールド", "platinum":"プラチナ", "diamond":"ダイヤモンド", "champion":"チャンピオン",
                   "c":"コッパー", "b":"ブロンズ", "s":"シルバー", "g":"ゴールド", "p":"プラチナ", "d":"ダイヤモンド", "ch":"チャンピオン"}

    valoRankList = {"iron":"アイアン", "bronze":"ブロンズ", "silver":"シルバー", "gold":"ゴールド", "platinum":"プラチナ", "diamond":"ダイヤモンド", "immortal":"イモータル", "rediant":"レディアント",
                    "i":"アイアン", "b":"ブロンズ", "s":"シルバー", "g":"ゴールド", "p":"プラチナ", "d":"ダイヤモンド", "im":"イモータル", "r":"レディアント"}

    # メソッドを格納するリスト
    functionList = {"00":await apexCasual(name, icon, rank, apexRankList), "01":await apexRank(name, icon, rank, apexRankList),
                    "10":await r6sCasual(name, icon, rank, r6sRankList), "11":await r6sRank(name, icon, rank, r6sRankList),
                    "20":await valoUnrated(name, icon, rank, valoRankList), "21":await valoCompetitive(name, icon, rank, valoRankList)}

    # 入力されたコマンドから、実行するメソッドの番号を取得する
    functionNumber = await getFunctionNumber(inputList, commandsList)

    if functionNumber is not "False":
        result = functionList[functionNumber]
        room = client.get_channel(result[1])
        await room.send(embed = result[0])
    else:
        print("It command isn't valid.")
# mainメソッド ----------------------------------------------------------


# 入力されたコマンドが有効か判定
async def isValidCommands (list, commands):
    if len(list) >= 2:
        flag = True
        for i in range(2):
            insideList = commands[i]
            flag *= list[i] in insideList.keys()
        return bool(flag)
    else:
        return False

# コマンドに相当する番号を返す
async def getFunctionNumber(list, commands):
    if await isValidCommands(list, commands):
        functionNumber = ""
        for i in range(2):
            insideList = commands[i]
            functionNumber += insideList[list[i]]
        return functionNumber
    else:
        return "False"

async def apexCasual(name, icon, rank, rankList):
    return await gameEmbed("ゲーム募集", "APEX カジュアル募集", 0xff3030, name, icon, "895230460089741323", rank, rankList, 2, 893931666823864330)

async def apexRank(name, icon, rank, rankList):
    return await gameEmbed("ランク募集", "APEX ランク募集", 0xff3030, name, icon, "895230460089741323", rank, rankList, 2, 893931729054740510)

async def r6sCasual(name, icon, rank, rankList):
    return await gameEmbed("ゲーム募集", "R6S カジュアル募集", 0x0080ff, name, icon, "895230662691422208", rank, rankList, 4, 893931666823864330)

async def r6sRank(name, icon, rank, rankList):
    return await gameEmbed("ランク募集", "R6S ランク募集", 0x0080ff, name, icon, "895230662691422208", rank, rankList, 4, 893931729054740510)

async def valoUnrated(name, icon, rank, rankList):
    return await gameEmbed("ゲーム募集", "VALORANT アンレート募集", 0xff5050, name, icon, "895230767200886804", rank, rankList, 4, 893931666823864330)

async def valoCompetitive(name, icon, rank, rankList):
    return await gameEmbed("ランク募集", "VALORANT コンペティティブ募集", 0xff5050, name, icon, "895230767200886804", rank, rankList, 4, 893931729054740510)


async def gameEmbed(title, des, color, name, icon, roleId, rank, rankList, member, roomId):
    embed = discord.Embed(title=title, description=des, color=color)
    embed.set_author(name = name, icon_url = icon)
    embed.add_field(name="----- 募集対象 -----", value="{0}".format("<@&" + roleId + ">"))
    if rank in rankList.keys():
        embed.add_field(name="----- 募集人数 -----", value="{0}人".format(member))
        embed.add_field(name="----- ランク帯 -----", value="{0}".format(rankList[rank]))
    else:
        embed.add_field(name="----- 募集人数 -----", value="{0}人".format(member))
    return [embed, roomId]

client.run(TOKEN)