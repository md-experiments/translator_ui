from flask import Flask, render_template, request
from source.utils import call_fast_api, transliterate
app = Flask(__name__)

video_editor_port = 7082
video_editor_port = 8000
video_editor_host = 'localhost'
video_editor_host = 'webservice_videoeditor'

@app.route("/")
def home():
    page_config = {
        'show_results':False
    }
    return render_template('home.html',page_config = page_config)

@app.route("/transition_google_english", methods=['POST'])
def translate_from_english():
    page_config = {
        'show_results':False
    }
    qry = request.form.get("query")
    data = {
        "user_id": "user1234",
        "text": str(qry),
        "source_language": "en",
        "target_language": "bg",
        "path_to_gcp_creds": "../gcp_creds.json"
    }

    result_translate = call_fast_api(data, endpoint = 'translate_gcp/', port=video_editor_port, action='POST', host = video_editor_host)
    data = {
        "user_id": "user1234",
        "text": result_translate['translated_text'],
        "voice_name": "bg-bg-Standard-A",
        "output_path": "../data/speaker",
        "path_to_gcp_creds": "../gcp_creds.json"
    }
    result_tts = call_fast_api(data, endpoint = 'tts_gcp/', port=video_editor_port, action='POST', host = video_editor_host)
    if (int(result_translate.get('success_code',0))==200) & (int(result_tts.get('success_code',0))==200):
        
        #page_config = result_tts
        page_config['text'] = result_translate['text']
        page_config['translated_text'] = result_translate['translated_text']
        page_config['translit_text'] = transliterate(result_translate['translated_text'])
        page_config['file_name'] = result_tts['file_name']

        page_config['show_results'] = True
    return render_template('home.html',page_config = page_config)

if __name__ == "__main__":

    app.run('0.0.0.0', port=9090, debug=True, use_reloader=True, use_debugger=True, )