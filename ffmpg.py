#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
音声ファイルから音声認識を行い、認識結果のテキストをベクトル化するパイプラインサンプル

使用方法：
    python audio_pipeline.py 入力ファイル名

例：
    python audio_pipeline.py input.mp4

各ライブラリのインストール：
    pip install SpeechRecognition
    pip install sentence-transformers

ffmpegが必要です。OSに合わせてffmpegのインストールをしてください。
"""

import subprocess
import sys
import speech_recognition as sr
from sentence_transformers import SentenceTransformer

def convert_to_wav(input_file: str, output_file: str = 'output.wav'):
    """
    ffmpegを利用して入力ファイルから音声を抽出し、
    16kHz, モノラル, 16bit PCM形式のwavファイルに変換する。
    """
    # -vn: 映像を無視, -ac 1: モノラル, -ar 16000: サンプリングレート16kHz, -sample_fmt s16: 16bit PCM
    cmd = ['ffmpeg', '-i', input_file, '-vn', '-ac', '1', '-ar', '16000', '-sample_fmt', 's16', output_file, '-y']
    try:
        print(f"ffmpegを利用して {input_file} から音声を抽出し、{output_file} に変換中...")
        subprocess.run(cmd, check=True)
        print("変換が完了しました。")
    except subprocess.CalledProcessError as e:
        print("ffmpegによる変換に失敗しました。")
        sys.exit(1)

def recognize_audio(wav_file: str, language: str = "ja-JP") -> str:
    """
    speech_recognitionライブラリを使ってwavファイルから音声認識を行いテキストに変換する。
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_file) as source:
            print(f"{wav_file}を読み込み中...")
            audio_data = recognizer.record(source)
        print("音声認識を実施中...")
        # Google Web Speech APIを利用（API制限等に注意）
        recognized_text = recognizer.recognize_google(audio_data, language=language)
        return recognized_text
    except sr.UnknownValueError:
        print("音声を認識できませんでした。")
        sys.exit(1)
    except sr.RequestError as e:
        print(f"APIへのリクエストに失敗しました: {e}")
        sys.exit(1)

def vectorize_text(text: str):
    """
    Sentence Transformersの事前学習済みモデルを使用してテキストをベクトル化する。
    """
    print("Sentence Transformerを読み込み中...")
    # 日本語にも対応可能な多言語モデルを指定
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("テキストのベクトル化を実施中...")
    embedding = model.encode(text)
    return embedding

def main():
    if len(sys.argv) < 2:
        print("Usage: python audio_pipeline.py <input_audio_or_video_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    wav_file = 'output.wav'

    # 1. ffmpegで音声抽出・変換
    convert_to_wav(input_file, wav_file)

    # 2. 音声認識でテキストに変換
    recognized_text = recognize_audio(wav_file, language="ja-JP")
    print("認識結果:")
    print(recognized_text)

    # 3. テキストのベクトル化
    embedding = vectorize_text(recognized_text)
    print("テキストの埋め込みベクトル:")
    print(embedding)

if __name__ == "__main__":
    main()
