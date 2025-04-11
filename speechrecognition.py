import lmstudio as lms
import speech_recognition as sr
import datetime

# LM Studioのモデルを読み込みます（モデル名は環境に合わせて変更してください）
model = lms.llm("llama-3.2-1b-instruct")

# Recognizerのインスタンス生成
r = sr.Recognizer()

# 認識したテキストを保持するリスト
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

                # 認識したテキストをLM Studio APIに渡して返答を取得する
                result = model.respond(text)
                print("LM Studioの返答:", result)

            except sr.UnknownValueError:
                print("音声を認識できませんでした。")
            except sr.RequestError as e:
                print("サービスへのリクエストに失敗しました。エラー:", e)
    except KeyboardInterrupt:
        print("\nCtrl+C が押されました。認識を停止し、テキストをファイルに保存します。")

# 認識したテキストがある場合、タイムスタンプ付きでファイルに保存する
if recognized_texts:
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"recognized_text_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for line in recognized_texts:
            f.write(line + "\n")
    print("認識したテキストを保存しました:", filename)
else:
    print("認識したテキストはありませんでした。")
