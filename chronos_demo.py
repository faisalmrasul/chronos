import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="CollabNet – Global Creator Collaboration Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .brand-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 5px solid;
        border-left-color: #3b82f6;
    }
    
    .campaign-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    
    .earning-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
    }
    
    .status-active { color: #10b981; font-weight: bold; }
    .status-pending { color: #f59e0b; font-weight: bold; }
    .status-completed { color: #6b7280; font-weight: bold; }
    
    .reach-badge {
        background: #3b82f6;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 5px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
    }
    
    .currency-selector {
        background: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'balance' not in st.session_state:
    st.session_state.balance = 1250
if 'active_campaigns' not in st.session_state:
    st.session_state.active_campaigns = []
if 'completed_campaigns' not in st.session_state:
    st.session_state.completed_campaigns = []
if 'content_created' not in st.session_state:
    st.session_state.content_created = []
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'currency' not in st.session_state:
    st.session_state.currency = 'USD'
if 'region' not in st.session_state:
    st.session_state.region = 'Global'
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Currency configurations
CURRENCIES = {
    'USD': {'symbol': '$', 'rate': 1.0, 'name': 'US Dollar'},
    'EUR': {'symbol': '€', 'rate': 0.92, 'name': 'Euro'},
    'GBP': {'symbol': '£', 'rate': 0.78, 'name': 'British Pound'},
    'BDT': {'symbol': '৳', 'rate': 110.0, 'name': 'Bangladeshi Taka'},
    'INR': {'symbol': '₹', 'rate': 83.0, 'name': 'Indian Rupee'},
    'JPY': {'symbol': '¥', 'rate': 148.0, 'name': 'Japanese Yen'},
    'AUD': {'symbol': 'A$', 'rate': 1.52, 'name': 'Australian Dollar'},
    'CAD': {'symbol': 'C$', 'rate': 1.35, 'name': 'Canadian Dollar'},
    'SGD': {'symbol': 'S$', 'rate': 1.34, 'name': 'Singapore Dollar'},
    'AED': {'symbol': 'د.إ', 'rate': 3.67, 'name': 'UAE Dirham'}
}

# Languages supported
LANGUAGES = {
    'en': {'name': 'English', 'flag': '🇬🇧'},
    'bn': {'name': 'বাংলা', 'flag': '🇧🇩'},
    'hi': {'name': 'हिन्दी', 'flag': '🇮🇳'},
    'es': {'name': 'Español', 'flag': '🇪🇸'},
    'fr': {'name': 'Français', 'flag': '🇫🇷'},
    'de': {'name': 'Deutsch', 'flag': '🇩🇪'},
    'ja': {'name': '日本語', 'flag': '🇯🇵'},
    'zh': {'name': '中文', 'flag': '🇨🇳'},
    'ar': {'name': 'العربية', 'flag': '🇸🇦'},
    'pt': {'name': 'Português', 'flag': '🇧🇷'}
}

# Language translations
TRANSLATIONS = {
    'en': {
        'app_name': 'CollabNet',
        'tagline': 'Global Creator Collaboration Platform',
        'balance': 'Balance',
        'active_campaigns': 'Active Campaigns',
        'completed_campaigns': 'Completed Campaigns',
        'total_earnings': 'Total Earnings',
        'quick_actions': 'Quick Actions',
        'browse_brands': 'Browse Brands',
        'create_content': 'Create Content',
        'view_performance': 'View Performance',
        'recent_activity': 'Recent Activity',
        'no_active_campaigns': 'No active or completed campaigns yet.',
        'brand_marketplace': 'Brand Marketplace',
        'search_brand': 'Search brand/campaign',
        'content_type_filter': 'Content Type Filter',
        'payment_filter': 'Payment Filter',
        'all': 'All',
        'video': 'Video',
        'static_post': 'Static Post',
        'text_image': 'Text+Image',
        'under_100': 'Under 100',
        'between_100_150': '100-150',
        'above_150': 'Above 150',
        'deadline': 'Deadline',
        'days_left': 'Days Left',
        'accept_campaign': 'Accept Campaign',
        'already_accepted': 'Already Accepted',
        'create_content_for': 'Create Content For',
        'ai_generate': 'AI Generate',
        'upload': 'Upload',
        'use_template': 'Use Template',
        'preview': 'Preview',
        'submit_content': 'Submit Content',
        'estimated_performance': 'Estimated Performance',
        'estimated_reach': 'Estimated Reach',
        'estimated_engagement': 'Estimated Engagement',
        'estimated_earning': 'Estimated Earning',
        'performance_tracking': 'Performance Tracking',
        'time_filter': 'Time Filter',
        'campaign_filter': 'Campaign Filter',
        'all_time': 'All Time',
        'last_7_days': 'Last 7 Days',
        'last_30_days': 'Last 30 Days',
        'this_month': 'This Month',
        'all_campaigns': 'All Campaigns',
        'performance_metrics': 'Performance Metrics',
        'total_reach': 'Total Reach',
        'total_engagement': 'Total Engagement',
        'total_campaigns': 'Total Campaigns',
        'campaign_performance': 'Campaign Performance',
        'brand': 'Brand',
        'campaign': 'Campaign',
        'status': 'Status',
        'reach': 'Reach',
        'engagement': 'Engagement',
        'start_date': 'Start Date'
    },
    'bn': {
        'app_name': 'কল্যাবনেট',
        'tagline': 'গ্লোবাল ক্রিয়েটর সহযোগিতা প্ল্যাটফর্ম',
        'balance': 'ব্যালেন্স',
        'active_campaigns': 'সক্রিয় ক্যাম্পেইন',
        'completed_campaigns': 'সম্পন্ন ক্যাম্পেইন',
        'total_earnings': 'মোট আয়',
        'quick_actions': 'দ্রুত একশন',
        'browse_brands': 'ব্র্যান্ড ব্রাউজ করুন',
        'create_content': 'কন্টেন্ট তৈরি করুন',
        'view_performance': 'পারফরম্যান্স দেখুন',
        'recent_activity': 'সাম্প্রতিক কার্যকলাপ',
        'no_active_campaigns': 'কোনো সক্রিয় বা সম্পন্ন ক্যাম্পেইন নেই।',
        'brand_marketplace': 'ব্র্যান্ড মার্কেটপ্লেস',
        'search_brand': 'ব্র্যান্ড/ক্যাম্পেইন সার্চ করুন',
        'content_type_filter': 'কন্টেন্ট টাইপ ফিল্টার',
        'payment_filter': 'পেমেন্ট ফিল্টার',
        'all': 'সবগুলো',
        'video': 'ভিডিও',
        'static_post': 'স্ট্যাটিক পোস্ট',
        'text_image': 'টেক্সট+ইমেজ',
        'under_100': '১০০ এর নিচে',
        'between_100_150': '১০০-১৫০',
        'above_150': '১৫০ এর উপরে',
        'deadline': 'ডেডলাইন',
        'days_left': 'দিন বাকি',
        'accept_campaign': 'ক্যাম্পেইন গ্রহণ করুন',
        'already_accepted': 'ইতিমধ্যে গ্রহণ করা হয়েছে',
        'create_content_for': 'কন্টেন্ট তৈরি করার জন্য',
        'ai_generate': 'AI জেনারেট করুন',
        'upload': 'আপলোড করুন',
        'use_template': 'টেমপ্লেট ব্যবহার করুন',
        'preview': 'প্রিভিউ',
        'submit_content': 'কন্টেন্ট সাবমিট করুন',
        'estimated_performance': 'আনুমানিক পারফরম্যান্স',
        'estimated_reach': 'আনুমানিক রিচ',
        'estimated_engagement': 'আনুমানিক এঙ্গেজমেন্ট',
        'estimated_earning': 'আনুমানিক আয়',
        'performance_tracking': 'পারফরম্যান্স ট্র্যাকিং',
        'time_filter': 'সময় ফিল্টার',
        'campaign_filter': 'ক্যাম্পেইন ফিল্টার',
        'all_time': 'সব সময়',
        'last_7_days': 'সর্বশেষ ৭ দিন',
        'last_30_days': 'সর্বশেষ ৩০ দিন',
        'this_month': 'এই মাস',
        'all_campaigns': 'সব ক্যাম্পেইন',
        'performance_metrics': 'পারফরম্যান্স মেট্রিক্স',
        'total_reach': 'মোট রিচ',
        'total_engagement': 'মোট এঙ্গেজমেন্ট',
        'total_campaigns': 'মোট ক্যাম্পেইন',
        'campaign_performance': 'ক্যাম্পেইন পারফরম্যান্স',
        'brand': 'ব্র্যান্ড',
        'campaign': 'ক্যাম্পেইন',
        'status': 'স্ট্যাটাস',
        'reach': 'রিচ',
        'engagement': 'এঙ্গেজমেন্ট',
        'start_date': 'শুরু তারিখ'
    }
}

# Global Brand Database
BRANDS = {
    'Global': {
        'Nike': {
            'logo': '🏃',
            'color': '#FF6B6B',
            'category': 'Sports & Fitness',
            'rating': 4.8,
            'campaigns': [
                {
                    'id': 'nike1',
                    'title': 'Nike Run Club Campaign',
                    'description': 'Create engaging content for Nike Run Club community',
                    'content_type': 'video',
                    'base_payment': 250,
                    'target_reach': 2000,
                    'per_engagement': 0.8,
                    'min_engagement': 500,
                    'deadline': '15 December',
                    'status': 'active',
                    'created_content': None
                }
            ]
        },
        'Apple': {
            'logo': '🍎',
            'color': '#3b82f6',
            'category': 'Technology',
            'rating': 4.9,
            'campaigns': [
                {
                    'id': 'apple1',
                    'title': 'iPhone Creator Challenge',
                    'description': 'Showcase your creativity with iPhone photography',
                    'content_type': 'static_post',
                    'base_payment': 300,
                    'target_reach': 2500,
                    'per_engagement': 1.0,
                    'min_engagement': 600,
                    'deadline': '20 December',
                    'status': 'active',
                    'created_content': None
                }
            ]
        },
        'Spotify': {
            'logo': '🎵',
            'color': '#10b981',
            'category': 'Music & Entertainment',
            'rating': 4.7,
            'campaigns': [
                {
                    'id': 'spotify1',
                    'title': 'Spotify Wrapped Campaign',
                    'description': 'Create content celebrating your Spotify Wrapped',
                    'content_type': 'text_image',
                    'base_payment': 200,
                    'target_reach': 1800,
                    'per_engagement': 0.6,
                    'min_engagement': 400,
                    'deadline': '10 December',
                    'status': 'active',
                    'created_content': None
                }
            ]
        }
    },
    'Asia': {
        'Samsung': {
            'logo': '📱',
            'color': '#8b5cf6',
            'category': 'Electronics',
            'rating': 4.6,
            'campaigns': [
                {
                    'id': 'samsung1',
                    'title': 'Galaxy S24 Ultra Review',
                    'description': 'Create hands-on review content for Galaxy S24 Ultra',
                    'content_type': 'video',
                    'base_payment': 280,
                    'target_reach': 2200,
                    'per_engagement': 0.9,
                    'min_engagement': 550,
                    'deadline': '25 December',
                    'status': 'active',
                    'created_content': None
                }
            ]
        },
        'Shopee': {
            'logo': '🛍️',
            'color': '#f59e0b',
            'category': 'E-Commerce',
            'rating': 4.4,
            'campaigns': [
                {
                    'id': 'shopee1',
                    'title': 'Shopee 12.12 Campaign',
                    'description': 'Create promotional content for 12.12 Sale',
                    'content_type': 'text_image',
                    'base_payment': 180,
                    'target_reach': 1500,
                    'per_engagement': 0.5,
                    'min_engagement': 350,
                    'deadline': '12 December',
                    'status': 'active',
                    'created_content': None
                }
            ]
        }
    },
    'Europe': {
        'Adidas': {
            'logo': '👟',
            'color': '#FF6B6B',
            'category': 'Sports & Fitness',
            'rating': 4.7,
            'campaigns': [
                {
                    'id': 'adidas1',
                    'title': 'Adidas Originals Campaign',
                    'description': 'Create style content for Adidas Originals',
                    'content_type': 'static_post',
                    'base_payment': 260,
                    'target_reach': 2000,
                    'per_engagement': 0.75,
                    'min_engagement': 500,
                    'deadline': '18 December',
                    'status': 'active',
                    'created_content': None
                }
            ]
        },
        "L'Oreal": {
            'logo': '💄',
            'color': '#ec4899',
            'category': 'Beauty & Cosmetics',
            'rating': 4.8,
            'campaigns': [
                {
                    'id': 'loreal1',
                    'title': "L'Oreal Beauty Influencer Campaign",
                    'description': "Create beauty content featuring L'Oreal products",
                    'content_type': 'video',
                    'base_payment': 320,
                    'target_reach': 2500,
                    'per_engagement': 1.0,
                    'min_engagement': 600,
                    'deadline': '22 December',
                    'status': 'active',
                    'created_content': None
                }
            ]
        }
    },
    'Americas': {
        'Amazon': {
            'logo': '📦',
            'color': '#f59e0b',
            'category': 'E-Commerce',
            'rating': 4.5,
            'campaigns': [
                {
                    'id': 'amazon1',
                    'title': 'Amazon Holiday Gift Guide',
                    'description': 'Create holiday gift guide content with Amazon products',
                    'content_type': 'text_image',
                    'base_payment': 220,
                    'target_reach': 2000,
                    'per_engagement': 0.7,
                    'min_engagement': 450,
                    'deadline': '20 December',
                    'status': 'active',
                    'created_content': None
                }
            ]
        },
        'Netflix': {
            'logo': '📺',
            'color': '#e50914',
            'category': 'Entertainment',
            'rating': 4.9,
            'campaigns': [
                {
                    'id': 'netflix1',
                    'title': 'Netflix Original Series Review',
                    'description': 'Create content reviewing new Netflix Originals',
                    'content_type': 'video',
                    'base_payment': 350,
                    'target_reach': 2800,
                    'per_engagement': 1.2,
                    'min_engagement': 700,
                    'deadline': '28 December',
                    'status': 'active',
                    'created_content': None
                }
            ]
        }
    }
}

def get_currency_symbol():
    """Get current currency symbol"""
    return CURRENCIES.get(st.session_state.currency, CURRENCIES['USD'])['symbol']

def format_currency(amount):
    """Format amount in selected currency"""
    symbol = get_currency_symbol()
    rate = CURRENCIES.get(st.session_state.currency, CURRENCIES['USD'])['rate']
    converted = amount * rate
    return f"{symbol}{converted:.2f}"

def t(key):
    """Get translation for current language"""
    lang = st.session_state.language
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    return TRANSLATIONS['en'].get(key, key)

def get_content_type_name(content_type):
    """Convert content type code to readable name"""
    names = {
        'static_post': t('static_post'),
        'video': t('video'),
        'text_image': t('text_image')
    }
    return names.get(content_type, content_type)

def generate_ai_content(brand, title, language='en'):
    """Generate AI content based on brand and language"""
    templates = {
        'en': {
            'headline': f'{brand} - {title}',
            'body': 'Special offer! Limited time deal. Order now!',
            'hashtags': f'#{brand.replace(" ", "")} #SpecialOffer #Deal #LimitedTime'
        },
        'bn': {
            'headline': f'{brand} - {title}',
            'body': 'বিশেষ অফার! সীমিত সময়ের জন্য সবচেয়ে ভালো দামে পাচ্ছেন। আজই অর্ডার করুন!',
            'hashtags': f'#{brand.replace(" ", "")} #বিশেষঅফার #ডিল #সীমিতসময়'
        },
        'hi': {
            'headline': f'{brand} - {title}',
            'body': 'विशेष ऑफर! सीमित समय के लिए। आज ही ऑर्डर करें!',
            'hashtags': f'#{brand.replace(" ", "")} #स्पेशलऑफर #डील #लिमिटेडटाइम'
        }
    }
    
    return templates.get(language, templates['en'])

def generate_video_script(brand, title, language='en'):
    """Generate video script in different languages"""
    scripts = {
        'en': f'Today we\'re exploring {brand}\'s new product. Perfect combination of taste and health.',
        'bn': f'আজ আমরা দেখবো {brand} এর নতুন প্রোডাক্ট। স্বাদের সাথে স্বাস্থ্যের পরিপূর্ণ সংমিশ্রণ।',
        'hi': f'आज हम {brand} के नए उत्पाद की खोज कर रहे हैं। स्वाद और स्वास्थ्य का परिपूर्ण संयोजन।'
    }
    return scripts.get(language, scripts['en'])

def add_notification(message, type='info'):
    """Add notification to session state"""
    st.session_state.notifications.append({
        'message': message,
        'type': type,
        'time': datetime.now().strftime("%H:%M")
    })

def show_dashboard():
    """Show main dashboard"""
    st.markdown(f"""
    <div class="main-header">
        <h1>💰 {t('app_name')} - {t('tagline')}</h1>
        <p>{t('recent_activity')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="earning-card">
            <h3>{t('balance')}</h3>
            <h2>{format_currency(st.session_state.balance)}</h2>
            <p>{t('total_earnings')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_count = len([c for c in st.session_state.active_campaigns if c['status'] != 'completed'])
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 20px; border-radius: 15px;">
            <h3>{t('active_campaigns')}</h3>
            <h2>{active_count}</h2>
            <p>{t('quick_actions')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        completed_count = len(st.session_state.completed_campaigns)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; padding: 20px; border-radius: 15px;">
            <h3>{t('completed_campaigns')}</h3>
            <h2>{completed_count}</h2>
            <p>{t('total_campaigns')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_earning = sum(c.get('estimated_earning', 0) for c in st.session_state.completed_campaigns)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 20px; border-radius: 15px;">
            <h3>{t('total_earnings')}</h3>
            <h2>{format_currency(total_earning)}</h2>
            <p>{t('estimated_earning')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader(f"⚡ {t('quick_actions')}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🏢 {t('browse_brands')}", use_container_width=True):
            st.session_state.page = "marketplace"
            st.rerun()
    
    with col2:
        if st.button(f"🎨 {t('create_content')}", use_container_width=True):
            st.session_state.page = "create_content"
            st.rerun()
    
    with col3:
        if st.button(f"📊 {t('view_performance')}", use_container_width=True):
            st.session_state.page = "performance"
            st.rerun()
    
    st.markdown("---")
    
    # Recent Activity
    st.subheader(f"📝 {t('recent_activity')}")
    
    if not st.session_state.active_campaigns and not st.session_state.completed_campaigns:
        st.info(f"ℹ️ {t('no_active_campaigns')}")
    
    else:
        # Show active campaigns
        if st.session_state.active_campaigns:
            st.markdown(f"#### 🎯 {t('active_campaigns')}")
            for campaign in st.session_state.active_campaigns[-3:]:
                status_text = "Content needed" if campaign['status'] == 'content_pending' else "Posted"
                status_color = "#f59e0b" if campaign['status'] == 'content_pending' else "#10b981"
                
                st.markdown(f"""
                <div style="
                    background: white;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid {status_color};
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                ">
                    <h4>{campaign['brand']} - {campaign['title']}</h4>
                    <p><strong>{t('status')}:</strong> <span style="color: {status_color}">{status_text}</span></p>
                    <p><strong>{t('estimated_earning')}:</strong> {format_currency(campaign.get('estimated_earning', 0))}</p>
                    <p><strong>{t('deadline')}:</strong> {campaign.get('deadline', '15 December')}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Show completed campaigns
        if st.session_state.completed_campaigns:
            st.markdown(f"#### ✅ {t('completed_campaigns')}")
            for campaign in st.session_state.completed_campaigns[-3:]:
                st.markdown(f"""
                <div style="
                    background: white;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #10b981;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                ">
                    <h4>{campaign['brand']} - {campaign['title']}</h4>
                    <p><strong>{t('estimated_earning')}:</strong> {format_currency(campaign.get('actual_earning', campaign.get('estimated_earning', 0)))}</p>
                    <p><strong>{t('reach')}:</strong> {campaign.get('actual_reach', 0)}</p>
                    <p><strong>{t('status')}:</strong> {campaign.get('completed_date', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)

def show_marketplace():
    """Show brand marketplace with global brands"""
    st.title(f"🏢 {t('brand_marketplace')}")
    
    # Region and Language Settings
    col1, col2, col3 = st.columns(3)
    
    with col1:
        region_filter = st.selectbox(
            "🌍 Region Filter",
            ["Global", "Asia", "Europe", "Americas", "All Regions"]
        )
    
    with col2:
        search_query = st.text_input(f"🔍 {t('search_brand')}", "")
    
    with col3:
        content_filter = st.selectbox(
            f"📱 {t('content_type_filter')}",
            [t('all'), t('video'), t('static_post'), t('text_image')]
        )
    
    st.markdown("---")
    
    # Display Brands based on region
    for region, brands in BRANDS.items():
        if region_filter != "All Regions" and region_filter != region:
            continue
            
        st.subheader(f"🌍 {region}")
        
        for brand_name, brand_data in brands.items():
            # Apply search filter
            if search_query and search_query.lower() not in f"{brand_name} {brand_data['category']}".lower():
                continue
                
            st.markdown(f"""
            <div style="
                background: {brand_data['color']}20;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                border-left: 5px solid {brand_data['color']};
            ">
                <h2>{brand_data['logo']} {brand_name}</h2>
                <p><strong>{t('brand')}:</strong> {brand_data['category']} | <strong>Rating:</strong> {brand_data['rating']} ⭐</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show campaigns for this brand
            for campaign in brand_data['campaigns']:
                if campaign['status'] == 'active':
                    # Apply content type filter
                    content_type_name = get_content_type_name(campaign['content_type'])
                    if content_filter != t('all') and content_filter != content_type_name:
                        continue
                    
                    display_campaign_card(brand_name, brand_data, campaign)

def display_campaign_card(brand_name, brand_data, campaign):
    """Display individual campaign card with multi-currency support"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        max_earning = campaign['base_payment'] + (campaign['target_reach'] * campaign['per_engagement'])
        st.markdown(f"""
        <div class="campaign-card">
            <h3>{campaign['title']}</h3>
            <p>{campaign['description']}</p>
            
            <div style="display: flex; gap: 20px; margin-top: 15px; flex-wrap: wrap;">
                <div>
                    <strong>{t('content_type_filter')}:</strong><br>
                    {get_content_type_name(campaign['content_type'])}
                </div>
                <div>
                    <strong>{t('estimated_earning')}:</strong><br>
                    {format_currency(campaign['base_payment'])}
                </div>
                <div>
                    <strong>{t('reach')}:</strong><br>
                    {campaign['target_reach']}
                </div>
                <div>
                    <strong>Min Engagement:</strong><br>
                    {campaign['min_engagement']}
                </div>
            </div>
            
            <div style="margin-top: 15px;">
                <strong>Payment Structure:</strong><br>
                • Base: {format_currency(campaign['base_payment'])}<br>
                • Per Engagement: {format_currency(campaign['per_engagement'])}<br>
                • Max Earning: {format_currency(max_earning)}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"#### 📅 {t('deadline')}")
        st.markdown(f"**{campaign['deadline']}**")
        
        st.markdown(f"#### ⏱️ {t('days_left')}")
        days_left = random.randint(3, 14)
        st.markdown(f"**{days_left} {t('days_left')}**")
    
    with col3:
        # Check if already accepted
        already_accepted = any(
            c['campaign_id'] == campaign['id'] 
            for c in st.session_state.active_campaigns + st.session_state.completed_campaigns
        )
        
        if not already_accepted:
            if st.button(f"✅ {t('accept_campaign')}", key=f"accept_{campaign['id']}", use_container_width=True):
                # Add to active campaigns
                st.session_state.active_campaigns.append({
                    'campaign_id': campaign['id'],
                    'brand': brand_name,
                    'title': campaign['title'],
                    'content_type': campaign['content_type'],
                    'base_payment': campaign['base_payment'],
                    'target_reach': campaign['target_reach'],
                    'min_engagement': campaign['min_engagement'],
                    'per_engagement': campaign['per_engagement'],
                    'deadline': campaign['deadline'],
                    'accepted_date': datetime.now().strftime("%d %b %Y"),
                    'status': 'content_pending',
                    'created_content': None,
                    'current_reach': 0,
                    'current_engagement': 0,
                    'estimated_earning': 0
                })
                add_notification(f"✅ '{campaign['title']}' campaign accepted!", 'success')
                st.success(f"✅ '{campaign['title']}' {t('accept_campaign')}!")
                time.sleep(1)
                st.rerun()
        else:
            st.info(f"⏳ {t('already_accepted')}")
        
        # Quick Stats
        st.markdown("---")
        st.markdown("#### 📊 Stats")
        st.markdown(f"""
        <small>
        • Accepted: {random.randint(50, 200)} creators<br>
        • Successful: {random.randint(30, 80)} creators<br>
        • Avg Earning: {format_currency(campaign['base_payment'] + random.randint(20, 80))}
        </small>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

def create_content():
    """Create content for campaigns"""
    st.title(f"🎨 {t('create_content')}")
    
    if not st.session_state.active_campaigns:
        st.info(f"📭 {t('no_active_campaigns')}")
        if st.button(f"🏢 {t('browse_brands')}"):
            st.session_state.page = "marketplace"
            st.rerun()
        return
    
    # Select campaign to create content for
    pending_campaigns = [c for c in st.session_state.active_campaigns if c['status'] == 'content_pending']
    
    if not pending_campaigns:
        st.success("✅ All your campaigns have content created!")
        return
    
    campaign_options = {f"{c['brand']} - {c['title']}": c for c in pending_campaigns}
    selected_campaign_name = st.selectbox(
        f"{t('create_content_for')}:",
        list(campaign_options.keys())
    )
    
    selected_campaign = campaign_options[selected_campaign_name]
    
    # Get brand data (handle case where brand might not exist in BRANDS)
    brand_color = '#3b82f6'
    brand_logo = '🏢'
    for region in BRANDS.values():
        if selected_campaign['brand'] in region:
            brand_color = region[selected_campaign['brand']]['color']
            brand_logo = region[selected_campaign['brand']]['logo']
            break
    
    st.markdown(f"""
    <div class="brand-card" style="border-left-color: {brand_color};">
        <h3>{brand_logo} {selected_campaign['brand']}</h3>
        <h4>{selected_campaign['title']}</h4>
        <p><strong>{t('content_type_filter')}:</strong> {get_content_type_name(selected_campaign['content_type'])}</p>
        <p><strong>{t('estimated_earning')}:</strong> {format_currency(selected_campaign['base_payment'])}</p>
        <p><strong>{t('reach')}:</strong> {selected_campaign['target_reach']} | <strong>Min Engagement:</strong> {selected_campaign['min_engagement']}</p>
        <p><strong>{t('deadline')}:</strong> {selected_campaign.get('deadline', '15 December')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Content Creation Based on Type
    content_type = selected_campaign['content_type']
    
    if content_type == 'static_post':
        create_static_post_content(selected_campaign)
    elif content_type == 'video':
        create_video_content(selected_campaign)
    elif content_type == 'text_image':
        create_text_image_content(selected_campaign)

def create_static_post_content(campaign):
    """Create static post content"""
    st.subheader("🖼️ Create Static Post")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 1. Create/Upload Image")
        image_option = st.radio(
            "Image Option",
            ["AI Generate", "Upload", "Use Template"]
        )
        
        if image_option == "AI Generate":
            prompt = st.text_area("AI Prompt", 
                                 f"{campaign['brand']} - {campaign['title']} - Engaging social media post")
            if st.button("🖼️ Generate AI Image"):
                st.info("AI Image generating... (Demo)")
                st.image("https://via.placeholder.com/600x400/3b82f6/ffffff?text=AI+Generated+Post", 
                        caption="AI Generated Image")
        
        elif image_option == "Upload":
            uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
            if uploaded_file:
                st.image(uploaded_file, caption="Uploaded Image")
        
        else:  # Template
            template = st.selectbox("Select Template", ["Design 1", "Design 2", "Design 3"])
            st.image(f"https://via.placeholder.com/600x400/3b82f6/ffffff?text={campaign['brand']}+{template}", 
                    caption=f"{template} Template")
    
    with col2:
        st.markdown("#### 2. Text Content")
        
        # AI Text Generation
        if st.button("🤖 Generate AI Text"):
            generated_text = generate_ai_content(campaign['brand'], campaign['title'], st.session_state.language)
            st.session_state.generated_text = generated_text
        
        if 'generated_text' in st.session_state:
            headline = st.text_input("Headline", st.session_state.generated_text['headline'])
            body = st.text_area("Body Text", st.session_state.generated_text['body'], height=150)
            hashtags = st.text_input("Hashtags", st.session_state.generated_text['hashtags'])
        else:
            headline = st.text_input("Headline", f"{campaign['brand']} - {campaign['title']}")
            body = st.text_area("Body Text", "Special offer! Limited time deal...", height=150)
            hashtags = st.text_input("Hashtags", f"#{campaign['brand'].replace(' ', '')} #Deal #SpecialOffer")
        
        st.markdown("#### 3. Platforms")
        platforms = st.multiselect(
            "Post to Platforms",
            ["Facebook", "Instagram", "Twitter/X", "LinkedIn", "TikTok", "YouTube"],
            default=["Facebook", "Instagram"]
        )
    
    st.markdown("---")
    
    # Preview and Submit
    st.subheader("👁️ Post Preview")
    
    preview_col1, preview_col2 = st.columns([2, 1])
    
    with preview_col1:
        st.markdown(f"""
        <div style="
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            padding: 20px;
            background: white;
            margin: 10px 0;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: #3b82f6;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1.5rem;
                    margin-right: 10px;
                ">👤</div>
                <div>
                    <strong>Your Page</strong><br>
                    <small>Sponsored • Just now</small>
                </div>
            </div>
            
            <p><strong>{headline}</strong></p>
            <p>{body}</p>
            
            <div style="
                background: #f3f4f6;
                height: 300px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #6b7280;
                margin: 15px 0;
            ">
                🖼️ Post Image
            </div>
            
            <p><small>{hashtags}</small></p>
            
            <div style="display: flex; gap: 20px; color: #6b7280; margin-top: 15px;">
                <span>❤️ Like</span>
                <span>💬 Comment</span>
                <span>🔄 Share</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with preview_col2:
        st.markdown("#### 📊 Estimated Performance")
        
        estimated_reach = random.randint(300, 1200)
        estimated_engagement = random.randint(50, 400)
        
        st.metric("Estimated Reach", f"{estimated_reach}")
        st.metric("Estimated Engagement", f"{estimated_engagement}")
        
        # Calculate estimated earning
        base_earning = campaign['base_payment'] if estimated_engagement >= campaign['min_engagement'] else 0
        engagement_earning = estimated_engagement * campaign['per_engagement']
        total_estimated = base_earning + engagement_earning
        
        st.metric("Estimated Earning", f"{format_currency(total_estimated)}")
        
        if st.button("✅ Submit Content", type="primary", use_container_width=True):
            # Update campaign
            for i, c in enumerate(st.session_state.active_campaigns):
                if c['campaign_id'] == campaign['campaign_id']:
                    st.session_state.active_campaigns[i]['status'] = 'posted'
                    st.session_state.active_campaigns[i]['created_content'] = {
                        'headline': headline,
                        'body': body,
                        'hashtags': hashtags,
                        'platforms': platforms,
                        'created_date': datetime.now().strftime("%d %b %Y, %I:%M %p")
                    }
                    st.session_state.active_campaigns[i]['current_reach'] = estimated_reach
                    st.session_state.active_campaigns[i]['current_engagement'] = estimated_engagement
                    st.session_state.active_campaigns[i]['estimated_earning'] = total_estimated
            
            # Add to content created
            st.session_state.content_created.append({
                'campaign_id': campaign['campaign_id'],
                'brand': campaign['brand'],
                'title': campaign['title'],
                'content_type': campaign['content_type'],
                'content': {'headline': headline, 'body': body, 'hashtags': hashtags},
                'created_date': datetime.now().strftime("%d %b %Y, %I:%M %p"),
                'estimated_earning': total_estimated
            })
            
            add_notification(f"✅ '{campaign['title']}' content submitted!", 'success')
            st.success("✅ Content submitted! Performance tracking started.")
            st.balloons()
            time.sleep(2)
            st.rerun()

def create_video_content(campaign):
    """Create video content section"""
    st.subheader("🎥 Create Video Content")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 1. Video Script")
        
        if st.button("🤖 Generate AI Script"):
            script = generate_video_script(campaign['brand'], campaign['title'], st.session_state.language)
            st.session_state.video_script = script
        
        if 'video_script' in st.session_state:
            script_text = st.text_area("Script", st.session_state.video_script, height=200)
        else:
            script_text = st.text_area("Script", f"Video script for {campaign['brand']}'s {campaign['title']}...", height=200)
        
        st.markdown("#### 2. Video Settings")
        
        duration = st.slider("Video Duration (seconds)", 15, 60, 30)
        aspect_ratio = st.selectbox("Aspect Ratio", ["9:16 (Reels/TikTok)", "1:1 (Instagram)", "16:9 (YouTube)"])
        music = st.selectbox("Background Music", ["Upbeat", "Calm", "Trending", "No Music"])
        voiceover = st.selectbox("Voiceover", ["Male (English)", "Female (English)", "Male (Local)", "Female (Local)", "No Voiceover"])
    
    with col2:
        st.markdown("#### 3. Media Upload")
        
        uploaded_files = st.file_uploader(
            "Upload Images/Videos",
            type=['jpg', 'png', 'mp4', 'mov'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"{len(uploaded_files)} files uploaded")
        
        st.markdown("#### 4. AI Video Generation")
        
        if st.button("🎬 Generate AI Video"):
            st.info("AI Video generating... (Demo)")
            st.markdown("""
            <div style="
                background: linear-gradient(45deg, #667eea, #764ba2);
                height: 300px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 1.5rem;
                margin: 15px 0;
            ">
                🎥 AI Generated Video Preview
            </div>
            """, unsafe_allow_html=True)
        
        # Preview and Submit
        st.markdown("---")
        st.markdown("#### 📊 Estimated Performance")
        
        estimated_reach = random.randint(300, 1500)
        estimated_engagement = random.randint(50, 500)
        
        st.metric("Estimated Reach", f"{estimated_reach}")
        st.metric("Estimated Engagement", f"{estimated_engagement}")
        
        # Calculate estimated earning
        base_earning = campaign['base_payment'] if estimated_engagement >= campaign['min_engagement'] else 0
        engagement_earning = estimated_engagement * campaign['per_engagement']
        total_estimated = base_earning + engagement_earning
        
        st.metric("Estimated Earning", f"{format_currency(total_estimated)}")
        
        if st.button("✅ Submit Video", type="primary", use_container_width=True):
            # Update campaign
            for i, c in enumerate(st.session_state.active_campaigns):
                if c['campaign_id'] == campaign['campaign_id']:
                    st.session_state.active_campaigns[i]['status'] = 'posted'
                    st.session_state.active_campaigns[i]['created_content'] = {
                        'script': script_text,
                        'duration': duration,
                        'aspect_ratio': aspect_ratio,
                        'music': music,
                        'voiceover': voiceover,
                        'created_date': datetime.now().strftime("%d %b %Y, %I:%M %p")
                    }
                    st.session_state.active_campaigns[i]['current_reach'] = estimated_reach
                    st.session_state.active_campaigns[i]['current_engagement'] = estimated_engagement
                    st.session_state.active_campaigns[i]['estimated_earning'] = total_estimated
            
            # Add to content created
            st.session_state.content_created.append({
                'campaign_id': campaign['campaign_id'],
                'brand': campaign['brand'],
                'title': campaign['title'],
                'content_type': campaign['content_type'],
                'content': {'script': script_text, 'duration': duration},
                'created_date': datetime.now().strftime("%d %b %Y, %I:%M %p"),
                'estimated_earning': total_estimated
            })
            
            add_notification(f"✅ '{campaign['title']}' video submitted!", 'success')
            st.success("✅ Video submitted! Performance tracking started.")
            st.balloons()
            time.sleep(2)
            st.rerun()

def create_text_image_content(campaign):
    """Create text+image content section"""
    st.subheader("📝 Create Text+Image Content")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 1. Text Content")
        
        if st.button("🤖 Generate AI Text"):
            generated_text = generate_ai_content(campaign['brand'], campaign['title'], st.session_state.language)
            st.session_state.generated_text = generated_text
        
        if 'generated_text' in st.session_state:
            headline = st.text_input("Headline", st.session_state.generated_text['headline'])
            body = st.text_area("Body Text", st.session_state.generated_text['body'], height=150)
            hashtags = st.text_input("Hashtags", st.session_state.generated_text['hashtags'])
        else:
            headline = st.text_input("Headline", f"{campaign['brand']} - {campaign['title']}")
            body = st.text_area("Body Text", "Special offer! Limited time deal...", height=150)
            hashtags = st.text_input("Hashtags", f"#{campaign['brand'].replace(' ', '')} #Deal #SpecialOffer")
    
    with col2:
        st.markdown("#### 2. Select Image")
        
        image_option = st.radio(
            "Image Option",
            ["AI Generate", "Upload", "Use Stock Image"]
        )
        
        if image_option == "AI Generate":
            prompt = st.text_input("AI Prompt", f"{campaign['brand']} {campaign['title']}")
            if st.button("🖼️ Generate Image"):
                st.info("AI Image generating... (Demo)")
        
        elif image_option == "Upload":
            uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
            if uploaded_file:
                st.image(uploaded_file, caption="Uploaded Image", width=200)
        
        else:
            st.info("Select from stock image library")
        
        # Preview and Submit
        st.markdown("---")
        st.markdown("#### 📊 Estimated Performance")
        
        estimated_reach = random.randint(200, 1000)
        estimated_engagement = random.randint(40, 300)
        
        st.metric("Estimated Reach", f"{estimated_reach}")
        st.metric("Estimated Engagement", f"{estimated_engagement}")
        
        # Calculate estimated earning
        base_earning = campaign['base_payment'] if estimated_engagement >= campaign['min_engagement'] else 0
        engagement_earning = estimated_engagement * campaign['per_engagement']
        total_estimated = base_earning + engagement_earning
        
        st.metric("Estimated Earning", f"{format_currency(total_estimated)}")
        
        if st.button("✅ Submit Content", type="primary", use_container_width=True):
            # Update campaign
            for i, c in enumerate(st.session_state.active_campaigns):
                if c['campaign_id'] == campaign['campaign_id']:
                    st.session_state.active_campaigns[i]['status'] = 'posted'
                    st.session_state.active_campaigns[i]['created_content'] = {
                        'headline': headline,
                        'body': body,
                        'hashtags': hashtags,
                        'image_option': image_option,
                        'created_date': datetime.now().strftime("%d %b %Y, %I:%M %p")
                    }
                    st.session_state.active_campaigns[i]['current_reach'] = estimated_reach
                    st.session_state.active_campaigns[i]['current_engagement'] = estimated_engagement
                    st.session_state.active_campaigns[i]['estimated_earning'] = total_estimated
            
            # Add to content created
            st.session_state.content_created.append({
                'campaign_id': campaign['campaign_id'],
                'brand': campaign['brand'],
                'title': campaign['title'],
                'content_type': campaign['content_type'],
                'content': {'headline': headline, 'body': body, 'hashtags': hashtags},
                'created_date': datetime.now().strftime("%d %b %Y, %I:%M %p"),
                'estimated_earning': total_estimated
            })
            
            add_notification(f"✅ '{campaign['title']}' content submitted!", 'success')
            st.success("✅ Content submitted! Performance tracking started.")
            st.balloons()
            time.sleep(2)
            st.rerun()

def show_performance():
    """Show performance tracking"""
    st.title(f"📊 {t('performance_tracking')}")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        time_filter = st.selectbox(
            f"⏰ {t('time_filter')}", 
            [t('all_time'), t('last_7_days'), t('last_30_days'), t('this_month')]
        )
    with col2:
        campaign_filter = st.selectbox(
            f"🎯 {t('campaign_filter')}",
            [t('all_campaigns')] + [c['title'] for c in st.session_state.active_campaigns + st.session_state.completed_campaigns]
        )
    
    st.markdown("---")
    
    # Performance Metrics
    st.subheader(f"📈 {t('performance_metrics')}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_reach = sum(c.get('current_reach', 0) for c in st.session_state.active_campaigns + st.session_state.completed_campaigns)
    total_engagement = sum(c.get('current_engagement', 0) for c in st.session_state.active_campaigns + st.session_state.completed_campaigns)
    total_earning = sum(c.get('estimated_earning', 0) for c in st.session_state.completed_campaigns) + \
                   sum(c.get('estimated_earning', 0) for c in st.session_state.active_campaigns if c['status'] == 'posted')
    campaign_count = len(st.session_state.active_campaigns) + len(st.session_state.completed_campaigns)
    
    with col1:
        st.metric(t('total_reach'), f"{total_reach}")
    with col2:
        st.metric(t('total_engagement'), f"{total_engagement}")
    with col3:
        st.metric(t('total_earnings'), f"{format_currency(total_earning)}")
    with col4:
        st.metric(t('total_campaigns'), f"{campaign_count}")
    
    st.markdown("---")
    
    # Detailed Campaign Performance
    st.subheader(f"🎯 {t('campaign_performance')}")
    
    if not st.session_state.active_campaigns and not st.session_state.completed_campaigns:
        st.info(f"📭 {t('no_active_campaigns')}")
    else:
        # Create performance table
        performance_data = []
        
        for campaign in st.session_state.active_campaigns + st.session_state.completed_campaigns:
            if campaign_filter != t('all_campaigns') and campaign['title'] != campaign_filter:
                continue
            
            performance_data.append({
                t('brand'): campaign['brand'],
                t('campaign'): campaign['title'],
                t('status'): 'Completed' if campaign in st.session_state.completed_campaigns else 'Active',
                t('reach'): campaign.get('current_reach', 0),
                t('engagement'): campaign.get('current_engagement', 0),
                t('estimated_earning'): format_currency(campaign.get('estimated_earning', 0)),
                t('start_date'): campaign.get('accepted_date', 'N/A')
            })
        
        if performance_data:
            st.dataframe(pd.DataFrame(performance_data), use_container_width=True)
        else:
            st.info("No campaigns match the selected filter.")

def show_notifications():
    """Show notifications panel"""
    st.sidebar.markdown("### 🔔 Notifications")
    
    if not st.session_state.notifications:
        st.sidebar.info("No notifications")
    else:
        for notif in reversed(st.session_state.notifications[-5:]):
            color = "#10b981" if notif['type'] == 'success' else "#3b82f6"
            st.sidebar.markdown(f"""
            <div style="
                background: {color}10;
                border-left: 3px solid {color};
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                font-size: 0.9rem;
            ">
                <div style="display: flex; justify-content: space-between;">
                    <span>{notif['message']}</span>
                    <small>{notif['time']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if st.sidebar.button("Clear Notifications"):
        st.session_state.notifications = []
        st.rerun()

def main():
    # Initialize page state
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
    
    # Sidebar Navigation
    st.sidebar.image("https://via.placeholder.com/150x50/667eea/ffffff?text=CollabNet", use_column_width=True)
    
    st.sidebar.markdown("---")
    
    # Language and Currency Settings
    st.sidebar.markdown("### 🌍 Settings")
    
    # Language selector
    lang_options = {f"{LANGUAGES[code]['flag']} {LANGUAGES[code]['name']}": code for code in LANGUAGES}
    selected_lang = st.sidebar.selectbox(
        "Language",
        list(lang_options.keys()),
        index=list(lang_options.values()).index(st.session_state.language) if st.session_state.language in lang_options.values() else 0
    )
    st.session_state.language = lang_options[selected_lang]
    
    # Currency selector
    currency_options = {f"{CURRENCIES[code]['symbol']} {CURRENCIES[code]['name']}": code for code in CURRENCIES}
    selected_currency = st.sidebar.selectbox(
        "Currency",
        list(currency_options.keys()),
        index=list(currency_options.values()).index(st.session_state.currency) if st.session_state.currency in currency_options.values() else 0
    )
    st.session_state.currency = currency_options[selected_currency]
    
    st.sidebar.markdown("---")
    st.sidebar.title("📱 Navigation")
    
    # Navigation buttons
    if st.sidebar.button(f"📊 {t('dashboard')}", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
    
    if st.sidebar.button(f"🏢 {t('browse_brands')}", use_container_width=True):
        st.session_state.page = "marketplace"
        st.rerun()
    
    if st.sidebar.button(f"🎨 {t('create_content')}", use_container_width=True):
        st.session_state.page = "create_content"
        st.rerun()
    
    if st.sidebar.button(f"📊 {t('view_performance')}", use_container_width=True):
        st.session_state.page = "performance"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Show notifications in sidebar
    show_notifications()
    
    st.sidebar.markdown("---")
    
    # User info
    st.sidebar.markdown("### 👤 Your Info")
    st.sidebar.markdown(f"**{t('balance')}:** {format_currency(st.session_state.balance)}")
    st.sidebar.markdown(f"**{t('active_campaigns')}:** {len([c for c in st.session_state.active_campaigns if c['status'] != 'completed'])}")
    
    if st.sidebar.button("💰 Withdraw"):
        if st.session_state.balance > 0:
            st.sidebar.success(f"{format_currency(st.session_state.balance)} withdrawn successfully!")
            st.session_state.balance = 0
            add_notification("✅ Withdrawal successful!", 'success')
        else:
            st.sidebar.warning("Insufficient balance for withdrawal")
    
    st.sidebar.markdown("---")
    
    # Page selection
    if st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "marketplace":
        show_marketplace()
    elif st.session_state.page == "create_content":
        create_content()
    elif st.session_state.page == "performance":
        show_performance()

if __name__ == "__main__":
    main()
