# Centralized translation dictionary for UI labels
TRANSLATIONS = {
    'en': {
        'app_title': 'Smart Government Scheme System',
        'home': 'Home',
        'profile': 'My Profile',
        'dashboard': 'Dashboard',
        'schemes': 'All Schemes',
        'welcome_title': 'Welcome to the Smart Scheme Finder',
        'welcome_subtitle': 'Discover government schemes, subsidies, and scholarships you are eligible for.',
        'start_now': 'Start Profile Check',
        'eligible_schemes': 'Eligible Schemes',
        'not_eligible_schemes': 'Not Eligible Schemes',
        'why_eligible': 'Why you are eligible:',
        'reasons': 'Reasons:',
        'select_language': 'Language',
        'view_details': 'View Details',
        'official_website': 'Visit Official Website',
        'back_to_schemes': 'Back to All Schemes',
        'footer_text': 'Smart Government Scheme Eligibility & Recommendation System'
    },
    'hi': {
        'app_title': 'स्मार्ट सरकारी योजना प्रणाली',
        'home': 'मुख्य पृष्ठ',
        'profile': 'मेरी प्रोफाइल',
        'dashboard': 'डैशबोर्ड',
        'schemes': 'सभी योजनाएं',
        'welcome_title': 'स्मार्ट योजना खोजक में आपका स्वागत है',
        'welcome_subtitle': 'अपने लिए योग्य सरकारी योजनाओं, सब्सिडी और छात्रवृत्तियों की खोज करें।',
        'start_now': 'प्रोफाइल शुरू करें',
        'eligible_schemes': 'पात्र योजनाएं',
        'not_eligible_schemes': 'अपात्र योजनाएं',
        'why_eligible': 'आप पात्र क्यों हैं:',
        'reasons': 'कारण:',
        'select_language': 'भाषा चुनें',
        'view_details': 'विवरण देखें',
        'official_website': 'आधिकारिक वेबसाइट पर जाएं',
        'back_to_schemes': 'सभी योजनाओं पर वापस जाएं',
        'footer_text': 'स्मार्ट सरकारी योजना पात्रता और अनुशंसा प्रणाली'
    },
    'mr': {
        'app_title': 'स्मार्ट शासकीय योजना प्रणाली',
        'home': 'मुख्य पृष्ठ',
        'profile': 'माझी प्रोफाइल',
        'dashboard': 'डॅशबोर्ड',
        'schemes': 'सर्व योजना',
        'welcome_title': 'स्मार्ट योजना शोधकमध्ये आपले स्वागत आहे',
        'welcome_subtitle': 'तुमच्यासाठी पात्र असलेल्या सरकारी योजना, अनुदाने आणि शिष्यवृत्ती शोधा.',
        'start_now': 'प्रोफाइल सुरू करा',
        'eligible_schemes': 'पात्र योजना',
        'not_eligible_schemes': 'अपात्र योजना',
        'why_eligible': 'तुम्ही पात्र का आहात:',
        'reasons': 'कारणे:',
        'select_language': 'भाषा निवडा',
        'view_details': 'तपशील पहा',
        'official_website': 'अधिकृत संकेतस्थळाला भेट द्या',
        'back_to_schemes': 'सर्व योजनांकडे परत जा',
        'footer_text': 'स्मार्ट शासकीय योजना पात्रता आणि शिफारस प्रणाली'
    }
}

def translate(key, lang='en'):
    """Looks up a translation key for the specified language. Falls back to English if missing."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    return lang_dict.get(key, TRANSLATIONS['en'].get(key, key))