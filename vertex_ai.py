import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession

# 初期化
project_id = "blueprotocol-408115"
location = "asia-northeast1"
vertexai.init(project=project_id, location=location)

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    """Geminiへメッセージを送信
    引数:
        - chat   (obj): チャットインスタンス
        - prompt (str): 送信用プロンプト
    戻り値:
        - response (str): レスポンスされたテキスト
    """
    response = chat.send_message(prompt).text
    return response

def summary_text(text):
    """文章を要約する
    引数:
        - text (str): 処理するテキスト
    戻り値:
        - res  (str): 要約テキスト
    """
    prompt = """ルールを基に以下の文章を要約してください

    """ + text

    res = get_chat_response(chat, prompt)

    return res

# モデル作成とルールを付与して返答を制限する
model = GenerativeModel("gemini-pro")
chat = model.start_chat()

prompt = """以下のルールをに従ってください
・箇条書きのみを返答
・箇条書きは最大で5点まで"""
chat.send_message(prompt)

