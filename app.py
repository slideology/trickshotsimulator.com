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

def get_faqs_for_page(page_name):
    faqs_data = {
        'banana': [
            {
                'question': 'What is Sprunki Banana?',
                'answer': 'Sprunki Banana is a unique mod featuring banana-themed characters and tropical soundscapes in the Sprunki universe.'
            },
            {
                'question': 'What makes Banana mod special?',
                'answer': 'The Banana mod brings a fun and tropical twist to Sprunki, with unique sound effects and cheerful character designs.'
            }
        ],
        'garnold': [
            {
                'question': 'Who is Garnold in Sprunki?',
                'answer': 'Garnold (Gold) is one of the main characters in Sprunki, known for his distinctive golden appearance and unique sound effects.'
            },
            {
                'question': 'What are Garnold\'s special features?',
                'answer': 'Garnold brings unique golden-themed sound effects and visual elements to the game, creating a premium music experience.'
            }
        ],
        'ketchup': [
            {
                'question': 'What is Sprunki Ketchup mod?',
                'answer': 'Sprunki Ketchup is a creative mod that adds a fun food-themed twist to the game with unique characters and sounds.'
            },
            {
                'question': 'What makes Ketchup mod unique?',
                'answer': 'The Ketchup mod features food-inspired characters and sound effects, creating a playful and appetizing musical experience.'
            }
        ],
        'lily': [
            {
                'question': 'Who is Lily in Sprunki?',
                'answer': 'Lily is a beloved character in the Sprunki universe, bringing a unique blend of floral themes and melodic sounds.'
            },
            {
                'question': 'What are Lily\'s special features?',
                'answer': 'Lily\'s mod includes nature-inspired sounds and visual elements, creating a peaceful and harmonious musical atmosphere.'
            }
        ],
        'megalovania': [
            {
                'question': 'What is Sprunki Megalovania?',
                'answer': 'Sprunki Megalovania is an epic crossover mod that brings the iconic Undertale track into the Sprunki universe.'
            },
            {
                'question': 'How does Megalovania mod work?',
                'answer': 'This mod allows players to create remixes and variations of the famous Megalovania theme using Sprunki\'s unique sound system.'
            }
        ],
        'parodybox': [
            {
                'question': 'What is Sprunki Mod?',
                'answer': 'Sprunki Mod is a fan-made adaptation of the <strong>Incredibox game</strong>, featuring unique characters, sounds, and themes that enhance the music-mixing experience.'
            },
            {
                'question': 'What is Sprunki Game?',
                'answer': 'Sprunki Game is a modified version of <strong>Incredibox</strong>, allowing players to create custom music tracks using creative characters and unique soundscapes.'
            },
            {
                'question': 'How do I download Sprunki Incredibox?',
                'answer': 'You can download Sprunki Incredibox from its <strong>official website</strong>, <strong>Google Play Store</strong>, <strong>Apple App Store</strong>, or as an APK for Android.'
            }
        ],
        'pyramixed': [
            {
                'question': 'What is PyraMixed?',
                'answer': 'PyraMixed is a unique version that combines pyramid-themed elements with music creation, offering a distinctive visual and audio experience.'
            },
            {
                'question': 'What makes PyraMixed special?',
                'answer': 'PyraMixed features Egyptian-inspired characters, desert soundscapes, and mystical themes that create an immersive musical journey.'
            }
        ],
        'retake-but-human': [
            {
                'question': 'What is Retake But Human mod?',
                'answer': 'Retake But Human is a unique mod that reimagines Sprunki characters with a more humanized approach.'
            },
            {
                'question': 'What makes this mod different?',
                'answer': 'This mod offers a fresh perspective on familiar characters, with human-like characteristics while maintaining the core Sprunki experience.'
            }
        ],
        'sprunkr': [
            {
                'question': 'What is Sprunkr?',
                'answer': 'Sprunkr is the main platform for all Sprunki mods and games, offering a unique horror-themed music creation experience.'
            },
            {
                'question': 'What can I do on Sprunkr?',
                'answer': 'On Sprunkr, you can play various Sprunki mods, create music, share your creations, and join a community of music enthusiasts.'
            }
        ],
        'spruted': [
            {
                'question': 'What is Sprunki Spruted?',
                'answer': 'Sprunki Spruted is a nature-themed mod that brings plant and growth elements into the Sprunki universe.'
            },
            {
                'question': 'What features does Spruted offer?',
                'answer': 'Spruted includes plant-themed characters, natural sound effects, and growth-inspired visual elements for a unique musical experience.'
            }
        ]
    }
    
    conclusions = {
        'banana': 'Experience the tropical vibes of Sprunki Banana, where fun meets music in a unique banana-themed adventure.',
        'garnold': 'Garnold brings a golden touch to the Sprunki universe, offering players a premium music creation experience.',
        'ketchup': 'Dive into the tasty world of Sprunki Ketchup, where food and music come together in perfect harmony.',
        'lily': 'Join Lily in creating beautiful, nature-inspired musical compositions in this peaceful corner of the Sprunki universe.',
        'megalovania': 'Experience the epic fusion of Undertale\'s Megalovania with Sprunki\'s unique sound system.',
        'parodybox': '<strong>Sprunki Incredibox</strong> game offers an immersive and creative musical experience where you can mix beats, experiment with sounds, and share your creations with a thriving community.',
        'pyramixed': 'PyraMixed brings a unique blend of ancient Egyptian themes and modern music creation, offering players an unforgettable experience in rhythm and sound design.',
        'retake-but-human': 'Explore the humanized version of your favorite Sprunki characters while creating amazing music in this unique mod.',
        'sprunkr': 'Join the Sprunkr community today and discover endless possibilities in music creation with our collection of unique Sprunki mods.',
        'spruted': 'Grow your musical creativity with Sprunki Spruted, where nature and music blend into a unique artistic experience.'
    }
    
    return {
        'faqs': faqs_data.get(page_name, []),
        'conclusion': conclusions.get(page_name, '')
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
    faq_data = get_faqs_for_page('lily')
    return render_template('sprunki-lily.html',
                         page_title='Sprunki Lily',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-megalovania')
def sprunki_megalovania():
    faq_data = get_faqs_for_page('megalovania')
    return render_template('sprunki-megalovania.html',
                         page_title='Sprunki Megalovania',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/sprunki-sprunkr')
def sprunki_sprunkr():
    faq_data = get_faqs_for_page('sprunkr')
    return render_template('sprunki-sprunkr.html',
                         page_title='Sprunkr',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-spruted')
def sprunki_spruted():
    faq_data = get_faqs_for_page('spruted')
    return render_template('sprunki-spruted.html',
                         page_title='Sprunki Spruted',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-banana')
def sprunki_banana():
    faq_data = get_faqs_for_page('banana')
    return render_template('sprunki-banana.html',
                         page_title='Sprunki Banana',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-garnold')
def sprunki_garnold():
    faq_data = get_faqs_for_page('garnold')
    return render_template('sprunki-garnold.html',
                         page_title='Sprunki Garnold',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-ketchup')
def sprunki_ketchup():
    faq_data = get_faqs_for_page('ketchup')
    return render_template('sprunki-ketchup.html',
                         page_title='Sprunki Ketchup',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-retake-but-human')
def sprunki_retake_but_human():
    faq_data = get_faqs_for_page('retake-but-human')
    return render_template('sprunki-retake-but-human.html',
                         page_title='Sprunki Retake But Human',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-parodybox')
def sprunki_parodybox():
    faq_data = get_faqs_for_page('parodybox')
    return render_template('sprunki-parodybox.html',
                         page_title='Sprunki ParodyBox',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-pyramixed')
def sprunki_pyramixed():
    faq_data = get_faqs_for_page('pyramixed')
    return render_template('sprunki-pyramixed.html',
                         page_title='Sprunki PyraMixed',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

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
