import speech_recognition as sr

# Recognizerのインスタンス作成
r = sr.Recognizer()

# マイクを使用して連続認識を実行
with sr.Microphone() as source:
    # 背景ノイズに合わせて調整（最初に一度調整を実施）
    print("背景ノイズの調整を行っています。しばらくお待ちください...")
    r.adjust_for_ambient_noise(source)
    print("連続音声認識を開始します。Ctrl+Cで終了できます。")

    while True:
        try:
            print("\n音声入力待ち...")
            audio = r.listen(source)
            try:
                # Google Web Speech API を利用して音声をテキストに変換（日本語）
                text = r.recognize_google(audio, language="ja-JP")
                print("認識結果:", text)
            except sr.UnknownValueError:
                print("認識できませんでした。もう一度お試しください。")
            except sr.RequestError as e:
                print("認識サービスへのリクエストに失敗しました。エラー:", e)
        except KeyboardInterrupt:
            print("\nプログラムを終了します。")
            break
