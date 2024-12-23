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
            "en": {
                "nav": {"home": "Home", "faq": "FAQ"},
                "hero": {
                    "title_highlight": "Create Music",
                    "title_regular": "Like Never Before",
                    "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
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
            "en": {
                "faq_sections": []
            }
        }

def get_faq_data(lang='en'):
    try:
        faq_data = load_faq_data()
        return faq_data.get(lang, faq_data.get('en', {})).get('faq_sections', [])
    except Exception as e:
        app.logger.error(f"Error getting FAQ data: {e}")
        return []

# Load translations
try:
    translations = load_translations()
except Exception as e:
    app.logger.error(f"Error loading initial translations: {e}")
    translations = {
        "en": {
            "nav": {"home": "Home", "faq": "FAQ"},
            "hero": {
                "title_highlight": "Create Music",
                "title_regular": "Like Never Before",
                "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
            }
        }
    }

def get_translations(lang='en'):
    try:
        if lang not in translations:
            return translations.get('en', {
                "nav": {"home": "Home", "faq": "FAQ"},
                "hero": {
                    "title_highlight": "Create Music",
                    "title_regular": "Like Never Before",
                    "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                }
            })
        return translations[lang]
    except Exception as e:
        app.logger.error(f"Error getting translations for {lang}: {e}")
        return {
            "nav": {"home": "Home", "faq": "FAQ"},
            "hero": {
                "title_highlight": "Create Music",
                "title_regular": "Like Never Before",
                "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
            }
        }

@app.route('/')
def home():
    try:
        lang = request.args.get('lang', 'en')
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
                                 "nav": {"home": "Home", "faq": "FAQ"},
                                 "hero": {
                                     "title_highlight": "Create Music",
                                     "title_regular": "Like Never Before",
                                     "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                                 }
                             },
                             current_lang='en')

@app.route('/about')
def about():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/game')
def game():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/introduction')
def introduction():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/faq')
def faq():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/blog')
def blog():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/community')
def community():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/leaderboard')
def leaderboard():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/events')
def events():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/feedback')
def feedback():
    try:
        lang = request.args.get('lang', 'en')
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
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         current_lang='en')

@app.route('/sprunki-lily')
def sprunki_lily():
    try:
        lang = request.args.get('lang', 'en')
        custom_translations = {
            "nav": {
                "home": "Home",
                "about": "About",
                "game": "Game",
                "introduction": "Introduction",
                "contact": "Contact",
                "faq": "FAQ",
                "blog": "Blog",
                "community": "Community",
                "leaderboard": "Leaderboard",
                "events": "Events",
                "feedback": "Feedback",
                "sprunki-lily": "Sprunki Lily"
            },
            "hero": {
                "title_highlight": "Sprunki Lily",
                "title_regular": "New Character Mod",
                "description": "Sprunki new mod adds new characters like Lilac (Lily), and they are so cool"
            },
            "footer": {
                "description": "Experience the joy of music creation with Sprunkr's innovative platform.",
                "copyright": " 2024 Sprunkr. All rights reserved.",
                "links": {
                    "privacy": "Privacy Policy",
                    "terms": "Terms of Service",
                    "contact": "Contact Us"
                }
            }
        }
        return render_template('sprunki-lily.html',
                         title='Sprunki Lily - New Character Mod',
                         translations=custom_translations,
                         current_lang=lang)
    except Exception as e:
        app.logger.error(f"Error in sprunki-lily route: {e}")
        return render_template('sprunki-lily.html',
                         title='Sprunki Lily - New Character Mod',
                         translations={
                             "nav": {
                                "home": "Home",
                                "about": "About",
                                "game": "Game",
                                "introduction": "Introduction",
                                "contact": "Contact",
                                "faq": "FAQ",
                                "blog": "Blog",
                                "community": "Community",
                                "leaderboard": "Leaderboard",
                                "events": "Events",
                                "feedback": "Feedback",
                                "sprunki-lily": "Sprunki Lily"
                             },
                             "hero": {
                                 "title_highlight": "Sprunki Lily",
                                 "title_regular": "New Character Mod",
                                 "description": "Sprunki new mod adds new characters like Lilac (Lily), and they are so cool"
                             },
                             "footer": {
                                 "description": "Experience the joy of music creation with Sprunkr's innovative platform.",
                                 "copyright": " 2024 Sprunkr. All rights reserved.",
                                 "links": {
                                     "privacy": "Privacy Policy",
                                     "terms": "Terms of Service",
                                     "contact": "Contact Us"
                                 }
                             }
                         },
                         current_lang='en')

@app.route('/sprunki-megalovania')
def sprunki_megalovania():
    translations = get_translations('en')
    translations.update({
        'hero': {
            'title_highlight': 'Sprunki Megalovania',
            'title_regular': '',
            'description': 'Have some fun with this Sprunki new mod'
        }
    })
    return render_template('sprunki-megalovania.html', translations=translations)

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/sprunki-spruted')
def sprunki_spruted():
    return render_template('sprunki-spruted.html', translations=translations)

@app.route('/privacy-policy')
def privacy_policy():
    try:
        lang = request.args.get('lang', 'en')
        translations_data = get_translations(lang)
        return render_template('privacy-policy.html', translations=translations_data)
    except Exception as e:
        app.logger.error(f"Error in privacy policy route: {e}")
        return render_template('error.html', error="An error occurred loading the privacy policy page.")

@app.route('/terms-of-service')
def terms_of_service():
    try:
        lang = request.args.get('lang', 'en')
        translations_data = get_translations(lang)
        return render_template('terms-of-service.html', translations=translations_data)
    except Exception as e:
        app.logger.error(f"Error in terms of service route: {e}")
        return render_template('error.html', error="An error occurred loading the terms of service page.")

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
