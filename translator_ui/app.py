from flask import Flask, render_template, request
from source.utils import call_fast_api, transliterate
app = Flask(__name__)

video_editor_port = 7082
video_editor_port = 8000
search_service_port = 8000
video_editor_host = 'localhost'
video_editor_host = 'webservice_videoeditor'
search_service_host = 'service_search'

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
    lang_in = request.form.get("language")
    if lang_in == 'en':
        source_language = 'en'
        target_language = 'bg'
    elif lang_in == 'bg':
        source_language = 'bg'
        target_language = 'en'
        
    print(lang_in)
    data = {
        "user_id": "user1234",
        "text": str(qry),
        "source_language": source_language,
        "target_language": target_language,
        "path_to_gcp_creds": "../gcp_creds.json"
    }

    result_translate = call_fast_api(data, endpoint = 'translate_gcp/', port=video_editor_port, action='POST', host = video_editor_host)
    
    if lang_in == 'en':
        image_search_qry = str(qry)
        voice_qry_text = result_translate['translated_text']
        voice_qry_voice = "bg-bg-Standard-A"
        reverse_translit = False
    elif lang_in == 'bg':
        image_search_qry = str(result_translate['translated_text'])
        voice_qry_text = result_translate['translated_text']
        voice_qry_voice = "en-GB-Wavenet-D"
        reverse_translit = True

    data = {
        "user_id": "user1234",
        "search_query": image_search_qry,
        "search_domains": [
            "Google_image"
        ],
        "response_size_each_domain": 5
    }
    result_search = call_fast_api(data, endpoint = 'search_request/', port=search_service_port, action='POST', host = search_service_host)
           
    data = {
        "user_id": "user1234",
        "text": voice_qry_text,
        "voice_name": voice_qry_voice,
        "output_path": "../data/speaker",
        "path_to_gcp_creds": "../gcp_creds.json"
    }
    result_tts = call_fast_api(data, endpoint = 'tts_gcp/', port=video_editor_port, action='POST', host = video_editor_host)
    if (int(result_translate.get('success_code',0))==200) & (int(result_tts.get('success_code',0))==200):
        
        #page_config = result_tts
        page_config['text'] = result_translate['text']
        page_config['translated_text'] = result_translate['translated_text']
        page_config['translit_text'] = transliterate(result_translate['translated_text'], reverse=reverse_translit)
        page_config['file_name'] = result_tts['file_name']
        page_config['images'] = [r["thumbnail"] for r in result_search['search_response']]

        page_config['show_results'] = True
    return render_template('home.html',page_config = page_config)

if __name__ == "__main__":

    app.run('0.0.0.0', port=9090, debug=True, use_reloader=True, use_debugger=True, )