import flet as ft
import requests
import speech_recognition as sr
from deep_translator import MyMemoryTranslator
from gtts import gTTS
import os

def main(page: ft.Page):
    page.title = "Y Dictionary Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    title = ft.Text("Y Dictionary Pro", size=26, weight=ft.FontWeight.BOLD, color="blue")
    status_text = ft.Text("", size=14, color="orange")
    word_input = ft.TextField(
        label="اكتب، تكلم، أو اختر صورة...",
        multiline=True,
        min_lines=2,
        max_lines=4,
        text_align=ft.TextAlign.CENTER,
        width=340
    )
    result_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # --- 1. النطق الصوتي باللهجة البريطانية ---
    def speak_british(e):
        if result_text.value.strip() != "":
            status_text.value = "جاري تجهيز النطق البريطاني..."
            page.update()
            try:
                tts = gTTS(text=result_text.value, lang='en', tld='co.uk')
                audio_path = os.path.join(os.getcwd(), "british_voice.mp3")
                tts.save(audio_path)
                page.launch_url(f"file://{audio_path}")
                status_text.value = ""
            except Exception as ex:
                status_text.value = "تعذر تشغيل الصوت على هذا الجهاز"
            page.update()

    btn_speak = ft.IconButton(
        icon=ft.Icons.VOLUME_UP,
        icon_color="blue",
        icon_size=32,
        tooltip="استمع للنطق البريطاني",
        visible=False,
        on_click=speak_british
    )

    # --- 2. دوال الترجمة ---
    def translate_to_gb(e):
        if word_input.value.strip() != "":
            status_text.value = "جاري الترجمة..."
            btn_speak.visible = False
            page.update()
            try:
                res = MyMemoryTranslator(source='ar-SA', target='en-GB').translate(word_input.value)
                result_text.value = res
                result_text.color = "blue"
                btn_speak.visible = True
                status_text.value = ""
            except:
                result_text.value = "تأكد من الاتصال بالإنترنت"
                result_text.color = "red"
            page.update()

    def translate_to_ar(e):
        if word_input.value.strip() != "":
            status_text.value = "جاري الترجمة..."
            btn_speak.visible = False
            page.update()
            try:
                res = MyMemoryTranslator(source='en-GB', target='ar-SA').translate(word_input.value)
                result_text.value = res
                result_text.color = "green"
                status_text.value = ""
            except:
                result_text.value = "تأكد من الاتصال بالإنترنت"
                result_text.color = "red"
            page.update()

    # --- 3. التصوير واستخراج النص من الصور (OCR) ---
    def on_image_picked(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            status_text.value = "جاري قراءة النص من الصورة..."
            page.update()
            try:
                with open(file_path, 'rb') as f:
                    response = requests.post(
                        'https://ocr.space',
                        files={'filename': f},
                        data={'apikey': 'helloworld', 'language': 'eng'}
                    )
                data = response.json()
                extracted_text = data['ParsedResults'][0]['ParsedText']
                if extracted_text.strip():
                    word_input.value = extracted_text.strip()
                    status_text.value = "تم استخراج النص! اضغط ترجمة."
                else:
                    status_text.value = "لم يتم العثور على نص واضح في الصورة."
            except Exception as ex:
                status_text.value = "فشل في قراءة الصورة، تأكد من الإنترنت."
            page.update()

    file_picker = ft.FilePicker(on_result=on_image_picked)
    page.overlay.append(file_picker)

    # --- 4. الميكروفون وتحويل الصوت لنص ---
    is_recording = False
    audio_rec = ft.AudioRecorder(
        audio_encoder=ft.AudioEncoder.WAV,
    )
    page.overlay.append(audio_rec)
    wav_path = os.path.join(os.getcwd(), "voice_input.wav")

    def toggle_mic(e):
        nonlocal is_recording
        if not is_recording:
            is_recording = True
            btn_mic.icon_color = "red"
            status_text.value = "جاري الاستماع... تحدث الآن ثم اضغط لإيقاف"
            page.update()
            audio_rec.start_recording(wav_path)
        else:
            is_recording = False
            btn_mic.icon_color = "blue"
            status_text.value = "جاري تحويل صوتك إلى نص..."
            page.update()
            audio_rec.stop_recording()
            
            try:
                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_path) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="ar-EG")
                    word_input.value = text
                    status_text.value = "تم تحويل الصوت بنجاح!"
            except:
                status_text.value = "لم أتمكن من فهم الصوت، حاول مرة أخرى."
            page.update()

    btn_camera = ft.IconButton(
        icon=ft.Icons.CAMERA_ALT,
        icon_color="blue",
        icon_size=30,
        tooltip="استخراج نص من صورة",
        on_click=lambda _: file_picker.pick_files(file_type=ft.FilePickerFileType.IMAGE)
    )
    btn_mic = ft.IconButton(
        icon=ft.Icons.MIC,
        icon_color="blue",
        icon_size=30,
        tooltip="تحدث للكتابة",
        on_click=toggle_mic
    )

    btn_gb = ft.Button("إلى إنجليزي بريطاني", on_click=translate_to_gb, bgcolor="blue", color="white")
    btn_ar = ft.Button("إلى العربية", on_click=translate_to_ar, bgcolor="green", color="white")

    page.add(
        title,
        ft.Row([btn_camera, btn_mic], alignment=ft.MainAxisAlignment.CENTER),
        word_input,
        status_text,
        ft.Row([btn_gb, btn_ar], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20, color="transparent"),
        result_text,
        btn_speak
    )

ft.run(main)
