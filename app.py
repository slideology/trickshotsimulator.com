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
        return {}

def load_faq_data():
    faq_path = os.path.join(app.static_folder, 'data', 'faq.json')
    try:
        with open(faq_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading FAQ data: {e}")
        return {}

def get_faq_data(lang='zh'):
    faq_data = load_faq_data()
    return faq_data.get(lang, faq_data.get('zh', {})).get('faq_sections', [])

# Load translations
translations = load_translations()

def get_translations(lang='zh'):
    return translations.get(lang, translations['zh'])

@app.route('/')
def home():
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

@app.route('/about')
def about():
    lang = request.args.get('lang', 'zh')
    trans = get_translations(lang)
    return render_template('about.html', 
                         title='About Sprunkr',
                         translations=trans,
                         current_lang=lang)

@app.route('/game')
def game():
    lang = request.args.get('lang', 'zh')
    trans = get_translations(lang)
    return render_template('game.html',
                         title='Play Sprunkr',
                         translations=trans,
                         current_lang=lang)

@app.route('/introduction')
def introduction():
    lang = request.args.get('lang', 'zh')
    trans = get_translations(lang)
    return render_template('introduction.html',
                         title='Game Guide - Sprunkr',
                         translations=trans,
                         current_lang=lang)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    lang = request.args.get('lang', 'zh')
    trans = get_translations(lang)
    if request.method == 'POST':
        return send_message()
    return render_template('contact.html',
                         title='Contact Sprunkr',
                         translations=trans,
                         current_lang=lang)

@app.route('/faq')
def faq():
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

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/blog')
def blog():
    lang = request.args.get('lang', 'zh')
    trans = get_translations(lang)
    return render_template('blog.html',
                         title='Blog - Sprunkr',
                         translations=trans,
                         current_lang=lang)

@app.route('/community')
def community():
    lang = request.args.get('lang', 'zh')
    trans = get_translations(lang)
    return render_template('community.html',
                         title='Community - Sprunkr',
                         translations=trans,
                         current_lang=lang)

@app.route('/leaderboard')
def leaderboard():
    lang = request.args.get('lang', 'zh')
    trans = get_translations(lang)
    return render_template('leaderboard.html',
                         title='Leaderboard - Sprunkr',
                         translations=trans,
                         current_lang=lang)

@app.route('/events')
def events():
    lang = request.args.get('lang', 'zh')
    trans = get_translations(lang)
    return render_template('events.html',
                         title='Events - Sprunkr',
                         translations=trans,
                         current_lang=lang)

@app.route('/feedback')
def feedback():
    lang = request.args.get('lang', 'zh')
    trans = get_translations(lang)
    return render_template('feedback.html',
                         title='Feedback - Sprunkr',
                         translations=trans,
                         current_lang=lang)

def send_message():
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
    
    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
