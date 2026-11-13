import flet as ft
from deep_translator import GoogleTranslator, MyMemoryTranslator

def main(page: ft.Page):
    page.title = "Y Dictionary"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    title = ft.Text("Y Dictionary 🇬🇧", size=28, weight=ft.FontWeight.BOLD, color="blue")
    word_input = ft.TextField(label="اكتب الكلمة أو الجملة هنا", text_align=ft.TextAlign.CENTER, width=320)
    result_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    def translate_to_gb(e):
        if word_input.value.strip() != "":
            result_text.value = "جاري الترجمة..."
            result_text.color = "orange"
            page.update()
            try:
                res = MyMemoryTranslator(source='ar-SA', target='en-GB').translate(word_input.value)
                result_text.value = res
                result_text.color = "blue"
            except:
                result_text.value = "تأكد من الاتصال بالإنترنت"
                result_text.color = "red"
            page.update()

    def translate_to_ar(e):
        if word_input.value.strip() != "":
            result_text.value = "جاري الترجمة..."
            result_text.color = "orange"
            page.update()
            try:
                res = MyMemoryTranslator(source='en-GB', target='ar-SA').translate(word_input.value)
                result_text.value = res
                result_text.color = "green"
            except:
                result_text.value = "تأكد من الاتصال بالإنترنت"
                result_text.color = "red"
            page.update()

    btn_gb = ft.Button("إلى إنجليزي بريطاني 🇬🇧", on_click=translate_to_gb, bgcolor="blue", color="white")
    btn_ar = ft.Button("إلى العربية 🇪🇬", on_click=translate_to_ar, bgcolor="green", color="white")

    page.add(
        title,
        ft.Divider(height=20, color="transparent"),
        word_input,
        ft.Row([btn_gb, btn_ar], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20, color="transparent"),
        result_text
    )

ft.run(main)