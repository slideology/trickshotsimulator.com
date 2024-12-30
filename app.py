from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, session, g
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

# Language settings
SUPPORTED_LANGUAGES = ['en', 'es']
DEFAULT_LANGUAGE = 'en'

@app.before_request
def before_request():
    # Get language from URL parameter, cookie, or browser settings
    lang = request.args.get('lang')
    if lang not in SUPPORTED_LANGUAGES:
        lang = request.cookies.get('lang')
    if lang not in SUPPORTED_LANGUAGES:
        lang = request.accept_languages.best_match(SUPPORTED_LANGUAGES, default=DEFAULT_LANGUAGE)
    g.lang = lang

# Language route
@app.route('/set-language')
def set_language():
    lang = request.args.get('lang')
    if lang in SUPPORTED_LANGUAGES:
        response = redirect(request.referrer or url_for('home'))
        response.set_cookie('lang', lang, max_age=60*60*24*365)
        return response
    return redirect(request.referrer or url_for('home'))

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
                "nav": {"home": "Home", "guide": "Game Guide", "faq": "FAQ", "play": "Play", "about": "About", "contact": "Contact"},
                "hero": {
                    "title_highlight": "Create Music",
                    "title_regular": "Like Never Before",
                    "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                },
                "game": {
                    "title": "Sprunkr",
                    "subtitle": "Sprunki Online Horror Music Game",
                    "description": "Unleash haunting melodies with our special glitch music system. Stack sounds, witness their digital distortion transformation. Embrace Horror Aesthetics."
                },
                "trending": {
                    "title": "Trending Games",
                    "sprunki_lily": "Sprunki - Lily",
                    "sprunki_megalovania": "Sprunki - Megalovania",
                    "sprunki_spruted": "Sprunki - Spruted"
                }
            })
        return translations[lang]
    except Exception as e:
        app.logger.error(f"Error getting translations for {lang}: {e}")
        return {
            "nav": {"home": "Home", "guide": "Game Guide", "faq": "FAQ", "play": "Play", "about": "About", "contact": "Contact"},
            "hero": {
                "title_highlight": "Create Music",
                "title_regular": "Like Never Before",
                "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
            },
            "game": {
                "title": "Sprunkr",
                "subtitle": "Sprunki Online Horror Music Game",
                "description": "Unleash haunting melodies with our special glitch music system. Stack sounds, witness their digital distortion transformation. Embrace Horror Aesthetics."
            },
            "trending": {
                "title": "Trending Games",
                "sprunki_lily": "Sprunki - Lily",
                "sprunki_megalovania": "Sprunki - Megalovania",
                "sprunki_spruted": "Sprunki - Spruted"
            }
        }

@app.route('/')
def home():
    try:
        trans = get_translations(g.lang)
        return render_template('index.html', 
                         title='Sprunkr - Interactive Music Experience',
                         description='Create amazing music with Sprunkr! Mix beats, compose tunes, and share your musical creations.',
                         translations=trans,
                         current_lang=g.lang)
    except Exception as e:
        app.logger.error(f"Error in home route: {e}")
        return render_template('index.html',
                         title='Sprunkr - Interactive Music Creation Game',
                         translations={
                             "nav": {"home": "Home", "guide": "Game Guide", "faq": "FAQ", "play": "Play", "about": "About", "contact": "Contact"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Sprunkr. Mix beats, create melodies, and share your music with the world."
                             },
                             "game": {
                                 "title": "Sprunkr",
                                 "subtitle": "Sprunki Online Horror Music Game",
                                 "description": "Unleash haunting melodies with our special glitch music system. Stack sounds, witness their digital distortion transformation. Embrace Horror Aesthetics."
                             },
                             "trending": {
                                 "title": "Trending Games",
                                 "sprunki_lily": "Sprunki - Lily",
                                 "sprunki_megalovania": "Sprunki - Megalovania",
                                 "sprunki_spruted": "Sprunki - Spruted"
                             }
                         },
                         current_lang='en')

@app.route('/about')
def about():
    try:
        trans = get_translations(g.lang)
        return render_template('about.html', 
                         title='About Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
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
        trans = get_translations(g.lang)
        return render_template('game.html',
                         title='Play Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
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
        trans = get_translations(g.lang)
        return render_template('introduction.html',
                         title='Game Guide - Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
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
        trans = get_translations(g.lang)
        if request.method == 'POST':
            return send_message()
        return render_template('contact.html',
                         title='Contact Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
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
        trans = get_translations(g.lang)
        return render_template('faq.html',
                         title='FAQ - Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
    except Exception as e:
        app.logger.error(f"Error in faq route: {e}")
        return render_template('faq.html',
                         title='FAQ - Sprunkr',
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
        trans = get_translations(g.lang)
        return render_template('blog.html',
                         title='Blog - Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
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
        trans = get_translations(g.lang)
        return render_template('community.html',
                         title='Community - Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
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
        trans = get_translations(g.lang)
        return render_template('leaderboard.html',
                         title='Leaderboard - Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
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
        trans = get_translations(g.lang)
        return render_template('events.html',
                         title='Events - Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
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
        trans = get_translations(g.lang)
        return render_template('feedback.html',
                         title='Feedback - Sprunkr',
                         translations=trans,
                         current_lang=g.lang)
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
                         current_lang=g.lang)
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

@app.route('/sprunki-sprunkr')
def sprunki_sprunkr():
    return render_template('sprunki-sprunkr.html', translations=translations)

@app.route('/sprunki-spruted')
def sprunki_spruted():
    try:
        trans = get_translations(g.lang)
        return render_template('sprunki-spruted.html', translations=trans, current_page='spruted')
    except Exception as e:
        app.logger.error(f"Error in spruted route: {str(e)}")
        return render_template('sprunki-spruted.html', translations=get_default_translations(), current_page='spruted')

@app.route('/sprunki-banana')
def sprunki_banana():
    try:
        trans = get_translations(g.lang)
        return render_template('sprunki-banana.html', translations=trans, current_page='banana')
    except Exception as e:
        app.logger.error(f"Error in banana route: {str(e)}")
        return render_template('sprunki-banana.html', translations=get_default_translations(), current_page='banana')

@app.route('/sprunki-ketchup')
def sprunki_ketchup():
    try:
        trans = get_translations(g.lang)
        return render_template('sprunki-ketchup.html', translations=trans, current_page='ketchup')
    except Exception as e:
        app.logger.error(f"Error in ketchup route: {str(e)}")
        return render_template('sprunki-ketchup.html', translations=get_default_translations(), current_page='ketchup')

@app.route('/sprunki-parodybox')
def sprunki_parodybox():
    try:
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
                "sprunki-parodybox": "Sprunki Parodybox"
            },
            "hero": {
                "title_highlight": "Sprunki Parodybox",
                "title_regular": " All new Characters Mod",
                "description": "Sprunki Parodybox is a Spine-Chilling Music Creation Experience. Similar to Incredibox, yet with a Distinctively Eerie Horror Twist, Try it!"
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
        return render_template('sprunki-parodybox.html',
                         title='Play Sprunki Parodybox Characters Mod of Sprunki on Sprunkr Online in 2025',
                         translations=custom_translations,
                         current_lang=g.lang)
    except Exception as e:
        app.logger.error(f"Error in sprunki-parodybox route: {e}")
        return render_template('sprunki-parodybox.html',
                         title='Play Sprunki Parodybox Characters Mod of Sprunki on Sprunkr Online in 2025',
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
                                "sprunki-parodybox": "Sprunki Parodybox"
                             },
                             "hero": {
                                 "title_highlight": "Sprunki Parodybox",
                                 "title_regular": "All new Characters Mod",
                                 "description": "Sprunki Parodybox is a Spine-Chilling Music Creation Experience. Similar to Incredibox, yet with a Distinctively Eerie Horror Twist, Try it!"
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
@app.route('/sprunki-pyramixed')
def sprunki_pyramixed():
    try:
        trans = get_translations(g.lang)
        return render_template('sprunki-pyramixed.html',
                         title='Sprunki Pyramixed New Horror Characters Mod of Sprunki in 2025',
                         description='Sprunki Pyramixed is A Whole new Horror Mode of Sprunki, And Maybe The Best Horror Version, Try It!',
                         translations=trans,
                         current_lang=g.lang)
    except Exception as e:
        app.logger.error(f"Error in sprunki-pyramixed: {e}")
        return render_template('sprunki-pyramixed.html',
                         title='Sprunki Pyramixed New Horror Characters Mod of Sprunki in 2025',
                         translations=get_default_translations(),
                         current_lang='en')
@app.route('/sprunki-retake-but-human')
def sprunki_retake_but_human():
    try:
        trans = get_translations(g.lang)
        return render_template('sprunki-retake-but-human.html',
                         title='Sprunki Retake But Human All Characters Mod For the Sprunki Play Online in 2025',
                         description='Sprunki Retake But Human: A Mesmerizing Mod That Transforms Sprunki\'s Animated Characters into Lifelike Humans, Offering a Fresh and Captivating Experience.',
                         translations=trans,
                         current_lang=g.lang)
    except Exception as e:
        app.logger.error(f"Error in sprunki-retake-but-human route: {e}")
        return render_template('sprunki-retake-but-human.html',
                         title='Sprunki Retake But Human All Characters Mod',
                         translations=get_default_translations(),
                         current_lang='en')

@app.route('/privacy-policy')
def privacy_policy():
    try:
        translations_data = get_translations(g.lang)
        return render_template('privacy-policy.html', translations=translations_data)
    except Exception as e:
        app.logger.error(f"Error in privacy policy route: {e}")
        return render_template('error.html', error="An error occurred loading the privacy policy page.")

@app.route('/terms-of-service')
def terms_of_service():
    try:
        translations_data = get_translations(g.lang)
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
