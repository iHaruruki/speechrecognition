import speech_recognition as sr
import datetime

# Recognizerのインスタンスを生成
r = sr.Recognizer()

# 認識したテキストを保存するリスト
recognized_texts = []

with sr.Microphone() as source:
    print("背景ノイズの調整中です。少々お待ちください...")
    r.adjust_for_ambient_noise(source)
    print("音声認識を開始します。Ctrl+C を押すと終了し、これまでのテキストをファイルに保存します。")

    try:
        while True:
            print("\nListening...")
            audio = r.listen(source)
            try:
                # Google Web Speech API を利用して日本語で認識
                text = r.recognize_google(audio, language="ja-JP")
                print("認識結果:", text)
                recognized_texts.append(text)
            except sr.UnknownValueError:
                print("音声を認識できませんでした。")
            except sr.RequestError as e:
                print("サービスへのリクエストに失敗しました。エラー:", e)
    except KeyboardInterrupt:
        print("\nCtrl+C が押されました。認識を停止し、テキストをファイルに保存します。")

# 認識したテキストがある場合にファイルへ保存
if recognized_texts:
    # タイムスタンプを使ってファイル名を生成
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"recognized_text_{timestamp}.txt"

    # テキストファイルとして保存（UTF-8エンコーディング）
    with open(filename, "w", encoding="utf-8") as f:
        for line in recognized_texts:
            f.write(line + "\n")
    print("認識したテキストを保存しました:", filename)
else:
    print("認識したテキストがありませんでした。")
