import speech_recognition as sr

# Recognizerのインスタンスを作成
r = sr.Recognizer()

# マイクから音声を取得するための設定
with sr.Microphone() as source:
    print("背景ノイズの調整を行います...")
    r.adjust_for_ambient_noise(source)  # 周囲の雑音レベルに合わせて調整
    print("話してください...")
    audio = r.listen(source)  # マイクから音声を取得

try:
    # Google Web Speech API を利用して音声を認識 (日本語設定: ja-JP)
    text = r.recognize_google(audio, language="ja-JP")
    print("音声認識結果:", text)
except sr.UnknownValueError:
    print("音声を認識できませんでした。")
except sr.RequestError as e:
    print("Google Speech Recognitionサービスへのリクエストに失敗しました; {0}".format(e))
