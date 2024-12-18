from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import json
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'sprunkr-secret-key-2023')

# Set up logging
app.logger.setLevel(logging.DEBUG)  # Change to DEBUG level
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

def load_translations():
    translations_path = os.path.join(app.static_folder, 'data', 'translations.json')
    try:
        with open(translations_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading translations: {e}")
        return {
            "zh": {
                "nav": {"home": "首页", "faq": "常见问题"},
                "hero": {
                    "title_highlight": "创作音乐",
                    "title_regular": "前所未有的体验",
                    "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                }
            }
        }

def load_faq_data():
    faq_path = os.path.join(app.static_folder, 'data', 'faq.json')
    try:
        with open(faq_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading FAQ data: {e}")
        return {
            "zh": {
                "faq_sections": []
            }
        }

def get_faq_data(lang='zh'):
    try:
        faq_data = load_faq_data()
        return faq_data.get(lang, faq_data.get('zh', {})).get('faq_sections', [])
    except Exception as e:
        app.logger.error(f"Error getting FAQ data: {e}")
        return []

# Load translations with error handling
try:
    translations = load_translations()
except Exception as e:
    app.logger.error(f"Error loading initial translations: {e}")
    translations = {}

def get_translations(lang='zh'):
    try:
        return translations.get(lang, translations.get('zh', {
            "nav": {"home": "首页", "faq": "常见问题"},
            "hero": {
                "title_highlight": "创作音乐",
                "title_regular": "前所未有的体验",
                "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
            }
        }))
    except Exception as e:
        app.logger.error(f"Error getting translations: {e}")
        return {
            "nav": {"home": "首页", "faq": "常见问题"},
            "hero": {
                "title_highlight": "创作音乐",
                "title_regular": "前所未有的体验",
                "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
            }
        }

@app.route('/')
def home():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        try:
            faq_data = load_faq_data()
            return render_template('index.html', 
                             title='Sprunkr - Interactive Music Experience',
                             description='Create amazing music with Sprunkr! Mix beats, compose tunes, and share your musical creations.',
                             faq_data=faq_data,
                             translations=trans,
                             current_lang=lang)
        except Exception as e:
            app.logger.error(f"Error in home route: {str(e)}")
            return render_template('index.html', 
                             title='Sprunkr - Interactive Music Experience',
                             description='Create amazing music with Sprunkr! Mix beats, compose tunes, and share your musical creations.',
                             faq_data={"faq_sections": []},
                             translations=trans,
                             current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in home route: {e}")
        return render_template('index.html',
                             title='Sprunkr - Interactive Music Creation Game',
                             translations={
                                 "nav": {"home": "首页", "faq": "常见问题"},
                                 "hero": {
                                     "title_highlight": "创作音乐",
                                     "title_regular": "前所未有的体验",
                                     "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                                 }
                             },
                             current_lang='zh')

@app.route('/about')
def about():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        return render_template('about.html', 
                         title='About Sprunkr',
                         translations=trans,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in about route: {e}")
        return render_template('about.html',
                         title='About Sprunkr',
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

@app.route('/game')
def game():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        return render_template('game.html',
                         title='Play Sprunkr',
                         translations=trans,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in game route: {e}")
        return render_template('game.html',
                         title='Play Sprunkr',
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

@app.route('/introduction')
def introduction():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        return render_template('introduction.html',
                         title='Game Guide - Sprunkr',
                         translations=trans,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in introduction route: {e}")
        return render_template('introduction.html',
                         title='Game Guide - Sprunkr',
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        if request.method == 'POST':
            return send_message()
        return render_template('contact.html',
                         title='Contact Sprunkr',
                         translations=trans,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in contact route: {e}")
        return render_template('contact.html',
                         title='Contact Sprunkr',
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

@app.route('/faq')
def faq():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        try:
            faq_sections = get_faq_data(lang)
            return render_template('faq.html',
                             title='FAQ - Sprunkr',
                             faq_data={'faq_sections': faq_sections},
                             translations=trans,
                             current_lang=lang)
        except Exception as e:
            app.logger.error(f"Error in faq route: {str(e)}")
            return render_template('faq.html',
                             title='FAQ - Sprunkr',
                             faq_data={"faq_sections": []},
                             translations=trans,
                             current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in faq route: {e}")
        return render_template('faq.html',
                         title='FAQ - Sprunkr',
                         faq_data={"faq_sections": []},
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/blog')
def blog():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        return render_template('blog.html',
                         title='Blog - Sprunkr',
                         translations=trans,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in blog route: {e}")
        return render_template('blog.html',
                         title='Blog - Sprunkr',
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

@app.route('/community')
def community():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        return render_template('community.html',
                         title='Community - Sprunkr',
                         translations=trans,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in community route: {e}")
        return render_template('community.html',
                         title='Community - Sprunkr',
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

@app.route('/leaderboard')
def leaderboard():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        return render_template('leaderboard.html',
                         title='Leaderboard - Sprunkr',
                         translations=trans,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in leaderboard route: {e}")
        return render_template('leaderboard.html',
                         title='Leaderboard - Sprunkr',
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

@app.route('/events')
def events():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        return render_template('events.html',
                         title='Events - Sprunkr',
                         translations=trans,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in events route: {e}")
        return render_template('events.html',
                         title='Events - Sprunkr',
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

@app.route('/feedback')
def feedback():
    try:
        lang = request.args.get('lang', 'zh')
        trans = get_translations(lang)
        return render_template('feedback.html',
                         title='Feedback - Sprunkr',
                         translations=trans,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in feedback route: {e}")
        return render_template('feedback.html',
                         title='Feedback - Sprunkr',
                         translations={
                             "nav": {"home": "首页", "faq": "常见问题"},
                             "hero": {
                                 "title_highlight": "创作音乐",
                                 "title_regular": "前所未有的体验",
                                 "description": "用 Sprunkr 将您的音乐创意变为现实。混音节拍，创作旋律，与世界分享您的音乐。"
                             }
                         },
                         current_lang='zh')

def send_message():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([name, email, subject, message]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('contact'))
        
        try:
            email_user = os.getenv('EMAIL_USER')
            email_password = os.getenv('EMAIL_PASSWORD')
            
            if not email_user or not email_password:
                flash('Email configuration is not set up', 'error')
                return redirect(url_for('contact'))
            
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_user  # Send to yourself
            msg['Subject'] = f"Sprunkr: {subject} - from {name}"
            
            body = f"""
            Name: {name}
            Email: {email}
            Subject: {subject}
            Message: {message}
            """
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
            server.quit()
            
            flash('Thank you for your message! We will get back to you soon.', 'success')
        except Exception as e:
            app.logger.error(f"Error sending message: {str(e)}")
            flash('Sorry, there was a problem sending your message. Please try again later.', 'error')
    except Exception as e:
        app.logger.error(f"Error in send_message: {e}")
        flash('Sorry, there was a problem sending your message. Please try again later.', 'error')
    
    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
