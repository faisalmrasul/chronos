import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import time
import json

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="CollabNet - Global Creator Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 10px;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: transform 0.3s ease;
        border: 1px solid #f0f0f0;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .stat-card .stat-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .stat-card .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    
    .stat-card .stat-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 5px;
    }
    
    .campaign-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .brand-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid;
        transition: transform 0.3s ease;
    }
    
    .brand-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .action-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 3px;
    }
    
    .badge-success { background: #10b981; color: white; }
    .badge-warning { background: #f59e0b; color: white; }
    .badge-info { background: #3b82f6; color: white; }
    .badge-danger { background: #ef4444; color: white; }
    
    .notification-item {
        background: #f8f9fa;
        padding: 12px 15px;
        border-radius: 10px;
        margin: 8px 0;
        border-left: 4px solid;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .notification-item .time {
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    .sidebar-section {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #e5e7eb, transparent);
        margin: 20px 0;
    }
    
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
        .stat-card .stat-value { font-size: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'balance': 1250.0,
        'active_campaigns': [],
        'completed_campaigns': [],
        'content_created': [],
        'notifications': [],
        'currency': 'USD',
        'language': 'en',
        'page': 'dashboard',
        'user_name': 'Creator',
        'user_level': 'Pro',
        'total_earned': 0.0,
        'campaign_history': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==================== CONFIGURATIONS ====================
CURRENCIES = {
    'USD': {'symbol': '$', 'rate': 1.0, 'name': 'US Dollar', 'emoji': '💵'},
    'EUR': {'symbol': '€', 'rate': 0.92, 'name': 'Euro', 'emoji': '💶'},
    'GBP': {'symbol': '£', 'rate': 0.78, 'name': 'British Pound', 'emoji': '💷'},
    'BDT': {'symbol': '৳', 'rate': 110.0, 'name': 'Bangladeshi Taka', 'emoji': '🇧🇩'},
    'INR': {'symbol': '₹', 'rate': 83.0, 'name': 'Indian Rupee', 'emoji': '🇮🇳'},
    'JPY': {'symbol': '¥', 'rate': 148.0, 'name': 'Japanese Yen', 'emoji': '💴'},
    'AUD': {'symbol': 'A$', 'rate': 1.52, 'name': 'Australian Dollar', 'emoji': '🇦🇺'},
    'CAD': {'symbol': 'C$', 'rate': 1.35, 'name': 'Canadian Dollar', 'emoji': '🇨🇦'},
    'SGD': {'symbol': 'S$', 'rate': 1.34, 'name': 'Singapore Dollar', 'emoji': '🇸🇬'},
    'AED': {'symbol': 'د.إ', 'rate': 3.67, 'name': 'UAE Dirham', 'emoji': '🇦🇪'},
    'BRL': {'symbol': 'R$', 'rate': 4.95, 'name': 'Brazilian Real', 'emoji': '🇧🇷'},
    'MXN': {'symbol': 'MX$', 'rate': 16.8, 'name': 'Mexican Peso', 'emoji': '🇲🇽'},
    'KRW': {'symbol': '₩', 'rate': 1320, 'name': 'South Korean Won', 'emoji': '🇰🇷'},
    'TRY': {'symbol': '₺', 'rate': 28.5, 'name': 'Turkish Lira', 'emoji': '🇹🇷'},
    'ZAR': {'symbol': 'R', 'rate': 18.5, 'name': 'South African Rand', 'emoji': '🇿🇦'},
}

LANGUAGES = {
    'en': {'name': 'English', 'flag': '🇬🇧', 'code': 'en'},
    'es': {'name': 'Español', 'flag': '🇪🇸', 'code': 'es'},
    'fr': {'name': 'Français', 'flag': '🇫🇷', 'code': 'fr'},
    'de': {'name': 'Deutsch', 'flag': '🇩🇪', 'code': 'de'},
    'ja': {'name': '日本語', 'flag': '🇯🇵', 'code': 'ja'},
    'zh': {'name': '中文', 'flag': '🇨🇳', 'code': 'zh'},
    'ar': {'name': 'العربية', 'flag': '🇸🇦', 'code': 'ar'},
    'hi': {'name': 'हिन्दी', 'flag': '🇮🇳', 'code': 'hi'},
    'bn': {'name': 'বাংলা', 'flag': '🇧🇩', 'code': 'bn'},
    'pt': {'name': 'Português', 'flag': '🇧🇷', 'code': 'pt'},
    'ru': {'name': 'Русский', 'flag': '🇷🇺', 'code': 'ru'},
    'it': {'name': 'Italiano', 'flag': '🇮🇹', 'code': 'it'},
}

# ==================== WORLDWIDE BRAND DATABASE ====================
BRANDS = {
    'Technology': {
        'Apple': {'logo': '🍎', 'color': '#555555', 'rating': 4.9},
        'Google': {'logo': '🔍', 'color': '#4285f4', 'rating': 4.8},
        'Microsoft': {'logo': '💻', 'color': '#00a4ef', 'rating': 4.7},
        'Samsung': {'logo': '📱', 'color': '#1428a0', 'rating': 4.6},
        'Sony': {'logo': '🎮', 'color': '#000000', 'rating': 4.7},
        'Dell': {'logo': '🖥️', 'color': '#007db8', 'rating': 4.5},
        'HP': {'logo': '🖨️', 'color': '#0096d6', 'rating': 4.4},
        'Lenovo': {'logo': '💻', 'color': '#e2231a', 'rating': 4.3},
        'Asus': {'logo': '🔧', 'color': '#0068b4', 'rating': 4.5},
        'Intel': {'logo': '💠', 'color': '#0071c5', 'rating': 4.6},
    },
    'Fashion & Beauty': {
        'Nike': {'logo': '🏃', 'color': '#FF6B6B', 'rating': 4.8},
        'Adidas': {'logo': '👟', 'color': '#000000', 'rating': 4.7},
        'L\'Oreal': {'logo': '💄', 'color': '#ec4899', 'rating': 4.8},
        'Gucci': {'logo': '👝', 'color': '#d4af37', 'rating': 4.9},
        'Prada': {'logo': '👜', 'color': '#000000', 'rating': 4.8},
        'Zara': {'logo': '👗', 'color': '#8b4513', 'rating': 4.5},
        'H&M': {'logo': '👔', 'color': '#e50010', 'rating': 4.4},
        'Uniqlo': {'logo': '👕', 'color': '#c41e3a', 'rating': 4.5},
        'Levi\'s': {'logo': '👖', 'color': '#1a3a5c', 'rating': 4.6},
        'Puma': {'logo': '🐆', 'color': '#000000', 'rating': 4.5},
    },
    'Food & Beverage': {
        'Coca-Cola': {'logo': '🥤', 'color': '#f40000', 'rating': 4.7},
        'Pepsi': {'logo': '🥤', 'color': '#004b93', 'rating': 4.6},
        'Starbucks': {'logo': '☕', 'color': '#006241', 'rating': 4.8},
        'McDonald\'s': {'logo': '🍔', 'color': '#da291c', 'rating': 4.5},
        'KFC': {'logo': '🍗', 'color': '#9c1a1a', 'rating': 4.4},
        'Burger King': {'logo': '👑', 'color': '#d62326', 'rating': 4.3},
        'Dominos': {'logo': '🍕', 'color': '#006491', 'rating': 4.3},
        'Nestle': {'logo': '🍫', 'color': '#d71921', 'rating': 4.6},
        'Unilever': {'logo': '🧴', 'color': '#1f75fe', 'rating': 4.5},
        'Danone': {'logo': '🥛', 'color': '#0093d0', 'rating': 4.6},
    },
    'Automotive': {
        'Tesla': {'logo': '🚗', 'color': '#e82127', 'rating': 4.9},
        'Toyota': {'logo': '🚙', 'color': '#eb0a1e', 'rating': 4.7},
        'BMW': {'logo': '🏎️', 'color': '#0066b1', 'rating': 4.8},
        'Mercedes': {'logo': '⭐', 'color': '#00adef', 'rating': 4.8},
        'Ford': {'logo': '🚘', 'color': '#003478', 'rating': 4.5},
        'Honda': {'logo': '🏍️', 'color': '#cc0000', 'rating': 4.6},
        'Volkswagen': {'logo': '🚐', 'color': '#001e50', 'rating': 4.5},
        'Hyundai': {'logo': '🚗', 'color': '#002c5f', 'rating': 4.4},
        'Nissan': {'logo': '🚘', 'color': '#c3002f', 'rating': 4.4},
        'Audi': {'logo': '🚗', 'color': '#bb0a1e', 'rating': 4.7},
    },
    'Entertainment': {
        'Netflix': {'logo': '📺', 'color': '#e50914', 'rating': 4.9},
        'Disney': {'logo': '🏰', 'color': '#113ccf', 'rating': 4.8},
        'Spotify': {'logo': '🎵', 'color': '#1db954', 'rating': 4.7},
        'YouTube': {'logo': '▶️', 'color': '#ff0000', 'rating': 4.8},
        'Amazon Prime': {'logo': '📦', 'color': '#00a8e1', 'rating': 4.6},
        'HBO': {'logo': '🎬', 'color': '#000000', 'rating': 4.7},
        'TikTok': {'logo': '🎵', 'color': '#000000', 'rating': 4.5},
        'Instagram': {'logo': '📸', 'color': '#e4405f', 'rating': 4.6},
        'Snapchat': {'logo': '👻', 'color': '#fffc00', 'rating': 4.3},
        'Twitch': {'logo': '🎮', 'color': '#6441a5', 'rating': 4.5},
    },
    'Finance': {
        'PayPal': {'logo': '💳', 'color': '#003087', 'rating': 4.6},
        'Mastercard': {'logo': '💳', 'color': '#eb001b', 'rating': 4.7},
        'Visa': {'logo': '💳', 'color': '#1a1f71', 'rating': 4.7},
        'Stripe': {'logo': '💳', 'color': '#635bff', 'rating': 4.8},
        'Square': {'logo': '💳', 'color': '#00a8e1', 'rating': 4.5},
        'Revolut': {'logo': '💳', 'color': '#1a1a1a', 'rating': 4.4},
        'Wise': {'logo': '💳', 'color': '#00b3b3', 'rating': 4.5},
    }
}

# ==================== GENERATE CAMPAIGNS ====================
def generate_campaigns():
    """Generate sample campaigns for all brands"""
    campaigns = []
    campaign_id = 1
    
    categories = list(BRANDS.keys())
    
    for category in categories:
        for brand_name, brand_data in BRANDS[category].items():
            # Generate 1-2 campaigns per brand
            num_campaigns = random.randint(1, 2)
            
            content_types = ['video', 'static_post', 'text_image']
            
            for i in range(num_campaigns):
                content_type = random.choice(content_types)
                
                # Campaign titles based on content type
                titles = {
                    'video': [f'{brand_name} Product Showcase', f'{brand_name} Review', f'{brand_name} Tutorial'],
                    'static_post': [f'{brand_name} Announcement', f'{brand_name} Promotion', f'{brand_name} Brand Story'],
                    'text_image': [f'{brand_name} Lifestyle Post', f'{brand_name} Campaign', f'{brand_name} Special Offer']
                }
                
                campaign = {
                    'id': f'camp_{campaign_id}',
                    'brand': brand_name,
                    'category': category,
                    'title': random.choice(titles[content_type]),
                    'description': f'Create engaging {content_type.replace("_", " ")} content for {brand_name}',
                    'content_type': content_type,
                    'base_payment': random.randint(100, 500),
                    'target_reach': random.randint(1000, 5000),
                    'per_engagement': round(random.uniform(0.3, 1.5), 2),
                    'min_engagement': random.randint(100, 500),
                    'deadline': (datetime.now() + timedelta(days=random.randint(7, 30))).strftime("%d %b %Y"),
                    'status': 'active',
                    'created_content': None,
                    'brand_logo': brand_data['logo'],
                    'brand_color': brand_data['color'],
                    'rating': brand_data['rating']
                }
                campaigns.append(campaign)
                campaign_id += 1
    
    return campaigns

# Generate campaigns once
ALL_CAMPAIGNS = generate_campaigns()

# ==================== HELPER FUNCTIONS ====================
def get_currency_symbol():
    """Get current currency symbol"""
    return CURRENCIES.get(st.session_state.currency, CURRENCIES['USD'])['symbol']

def get_currency_emoji():
    """Get current currency emoji"""
    return CURRENCIES.get(st.session_state.currency, CURRENCIES['USD'])['emoji']

def format_currency(amount):
    """Format amount in selected currency with proper symbol"""
    symbol = get_currency_symbol()
    rate = CURRENCIES.get(st.session_state.currency, CURRENCIES['USD'])['rate']
    converted = amount * rate
    return f"{symbol}{converted:,.2f}"

def get_language_flag():
    """Get flag emoji for current language"""
    return LANGUAGES.get(st.session_state.language, LANGUAGES['en'])['flag']

def get_content_type_name(content_type):
    """Convert content type code to display name"""
    names = {
        'video': '🎥 Video',
        'static_post': '🖼️ Static Post',
        'text_image': '📝 Text + Image'
    }
    return names.get(content_type, content_type)

def generate_ai_content(brand, title):
    """Generate AI content suggestions"""
    templates = {
        'headline': f'🔥 {brand} - {title}',
        'body': f'🌟 Discover the amazing {title} from {brand}! Limited time offer. Don\'t miss out on this incredible deal. #MustHave',
        'hashtags': f'#{brand.replace(" ", "")} #Trending #Viral #{title.replace(" ", "")} #DealOfTheDay',
        'cta': '👉 Click the link in bio to learn more!'
    }
    return templates

def generate_video_script(brand, title):
    """Generate video script"""
    return f"""
    🎬 VIDEO SCRIPT: {brand} - {title}
    
    [HOOK - 0-3 seconds]
    "Hey everyone! Welcome back to the channel!"
    
    [INTRO - 3-10 seconds]
    "Today we're checking out {brand}'s latest {title}. This is something you don't want to miss!"
    
    [MAIN CONTENT - 10-45 seconds]
    "Let me show you why {brand} is changing the game with this incredible product. 
    The quality is outstanding, and the features are exactly what you need."
    
    [CALL TO ACTION - 45-60 seconds]
    "Make sure to check the link in description to get yours! Don't forget to like and subscribe!"
    """

def add_notification(message, type='info'):
    """Add notification to session state"""
    st.session_state.notifications.insert(0, {
        'message': message,
        'type': type,
        'time': datetime.now().strftime("%I:%M %p"),
        'date': datetime.now().strftime("%b %d")
    })
    # Keep only last 50 notifications
    st.session_state.notifications = st.session_state.notifications[:50]

def get_brand_color(brand_name):
    """Get brand color from database"""
    for category in BRANDS.values():
        if brand_name in category:
            return category[brand_name]['color']
    return '#667eea'

def get_brand_logo(brand_name):
    """Get brand logo from database"""
    for category in BRANDS.values():
        if brand_name in category:
            return category[brand_name]['logo']
    return '🏢'

def get_campaign_by_id(campaign_id):
    """Get campaign by ID"""
    for campaign in ALL_CAMPAIGNS:
        if campaign['id'] == campaign_id:
            return campaign
    return None

# ==================== DASHBOARD ====================
def show_dashboard():
    """Main Dashboard View"""
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🌍 CollabNet</h1>
        <p>Connect with brands worldwide • Create amazing content • Earn globally</p>
        <div style="display: flex; gap: 10px; margin-top: 15px; flex-wrap: wrap;">
            <span class="badge badge-info">👋 Welcome, {st.session_state.user_name}</span>
            <span class="badge badge-success">⭐ {st.session_state.user_level} Creator</span>
            <span class="badge badge-warning">{get_currency_emoji()} {st.session_state.currency}</span>
            <span class="badge badge-info">{get_language_flag()} {LANGUAGES[st.session_state.language]['name']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    
    active_count = len([c for c in st.session_state.active_campaigns if c.get('status') != 'completed'])
    completed_count = len(st.session_state.completed_campaigns)
    total_earned = sum(c.get('estimated_earning', 0) for c in st.session_state.completed_campaigns)
    total_reach = sum(c.get('current_reach', 0) for c in st.session_state.active_campaigns + st.session_state.completed_campaigns)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-value">{format_currency(st.session_state.balance)}</div>
            <div class="stat-label">Available Balance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-value">{active_count}</div>
            <div class="stat-label">Active Campaigns</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-value">{completed_count}</div>
            <div class="stat-label">Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">📈</div>
            <div class="stat-value">{format_currency(total_earned)}</div>
            <div class="stat-label">Total Earned</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏢 Find Brands & Campaigns", use_container_width=True, type="primary"):
            st.session_state.page = "marketplace"
            st.rerun()
    
    with col2:
        if st.button("🎨 Create Content", use_container_width=True, type="secondary"):
            st.session_state.page = "create"
            st.rerun()
    
    with col3:
        if st.button("📊 View Analytics", use_container_width=True, type="secondary"):
            st.session_state.page = "analytics"
            st.rerun()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Recent Activity
    st.subheader("📝 Recent Activity")
    
    if not st.session_state.active_campaigns and not st.session_state.completed_campaigns:
        st.info("👋 Welcome to CollabNet! Start by browsing brands and accepting your first campaign.")
        if st.button("🚀 Get Started - Browse Campaigns"):
            st.session_state.page = "marketplace"
            st.rerun()
    else:
        # Active campaigns
        if st.session_state.active_campaigns:
            st.markdown("#### 🎯 Your Active Campaigns")
            for campaign in st.session_state.active_campaigns[:3]:
                status = campaign.get('status', 'pending')
                status_text = "⏳ Pending" if status == 'content_pending' else "✅ Posted"
                status_color = "#f59e0b" if status == 'content_pending' else "#10b981"
                
                with st.container():
                    st.markdown(f"""
                    <div style="background: white; border-radius: 12px; padding: 18px; margin: 10px 0; border-left: 4px solid {status_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                            <div>
                                <strong>{campaign.get('brand', 'Brand')}</strong> - {campaign.get('title', 'Campaign')}
                                <span class="badge { 'badge-warning' if status == 'content_pending' else 'badge-success' }">{status_text}</span>
                            </div>
                            <div>
                                <span style="font-size: 0.9rem; color: #6b7280;">
                                    💰 {format_currency(campaign.get('estimated_earning', 0))}
                                </span>
                            </div>
                        </div>
                        <div style="display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap; font-size: 0.9rem; color: #6b7280;">
                            <span>📅 Deadline: {campaign.get('deadline', 'N/A')}</span>
                            <span>📊 Type: {get_content_type_name(campaign.get('content_type', ''))}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Completed campaigns
        if st.session_state.completed_campaigns:
            st.markdown("#### ✅ Recently Completed")
            for campaign in st.session_state.completed_campaigns[:2]:
                with st.container():
                    st.markdown(f"""
                    <div style="background: #f8fafc; border-radius: 12px; padding: 15px; margin: 8px 0; border-left: 4px solid #10b981;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                            <div>
                                <strong>{campaign.get('brand', 'Brand')}</strong> - {campaign.get('title', 'Campaign')}
                                <span class="badge badge-success">✅ Done</span>
                            </div>
                            <div>
                                <span style="font-weight: 600; color: #10b981;">Earned: {format_currency(campaign.get('estimated_earning', 0))}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ==================== MARKETPLACE ====================
def show_marketplace():
    """Brand Marketplace View"""
    
    st.title("🏢 Global Brand Marketplace")
    st.caption("Discover and connect with brands from around the world")
    
    # Filters
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search Brands", placeholder="Search by brand or category...")
    
    with col2:
        category_filter = st.selectbox(
            "📂 Category",
            ["All Categories"] + list(BRANDS.keys())
        )
    
    with col3:
        content_filter = st.selectbox(
            "📱 Content Type",
            ["All Types", "Video", "Static Post", "Text + Image"]
        )
    
    with col4:
        price_filter = st.selectbox(
            "💰 Budget",
            ["All", "Under $200", "$200-$500", "Above $500"]
        )
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Display campaigns
    filtered_campaigns = []
    
    for campaign in ALL_CAMPAIGNS:
        if campaign['status'] != 'active':
            continue
        
        # Apply filters
        if search_query and search_query.lower() not in campaign['brand'].lower() and search_query.lower() not in campaign['category'].lower():
            continue
        
        if category_filter != "All Categories" and campaign['category'] != category_filter:
            continue
        
        content_map = {"Video": "video", "Static Post": "static_post", "Text + Image": "text_image"}
        if content_filter != "All Types" and campaign['content_type'] != content_map.get(content_filter):
            continue
        
        # Check if already accepted
        already_accepted = any(
            c.get('campaign_id') == campaign['id'] 
            for c in st.session_state.active_campaigns + st.session_state.completed_campaigns
        )
        
        if already_accepted:
            continue
        
        filtered_campaigns.append(campaign)
    
    # Show results
    if not filtered_campaigns:
        st.info("🔍 No campaigns match your filters. Try adjusting your search criteria.")
        return
    
    st.write(f"**{len(filtered_campaigns)}** campaigns available")
    
    # Display campaigns in grid
    for campaign in filtered_campaigns:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                brand_color = campaign.get('brand_color', '#667eea')
                brand_logo = campaign.get('brand_logo', '🏢')
                
                max_earning = campaign['base_payment'] + (campaign['target_reach'] * campaign['per_engagement'])
                
                st.markdown(f"""
                <div class="campaign-card" style="background: linear-gradient(135deg, {brand_color}80 0%, {brand_color}40 100%);">
                    <div style="display: flex; align-items: center; gap: 15px; flex-wrap: wrap;">
                        <div style="font-size: 3rem;">{brand_logo}</div>
                        <div>
                            <h3 style="margin: 0; color: white;">{campaign['brand']}</h3>
                            <p style="margin: 5px 0; color: rgba(255,255,255,0.9);">{campaign['category']}</p>
                        </div>
                        <div style="margin-left: auto;">
                            <span class="badge badge-info">⭐ {campaign['rating']}</span>
                        </div>
                    </div>
                    
                    <h4 style="margin-top: 15px; color: white;">{campaign['title']}</h4>
                    <p style="color: rgba(255,255,255,0.9);">{campaign['description']}</p>
                    
                    <div style="display: flex; gap: 20px; margin-top: 15px; flex-wrap: wrap; color: rgba(255,255,255,0.9);">
                        <div>
                            <strong>📱 Content</strong><br>
                            {get_content_type_name(campaign['content_type'])}
                        </div>
                        <div>
                            <strong>💰 Base Pay</strong><br>
                            {format_currency(campaign['base_payment'])}
                        </div>
                        <div>
                            <strong>🎯 Target Reach</strong><br>
                            {campaign['target_reach']:,}
                        </div>
                        <div>
                            <strong>⚡ Min Engagement</strong><br>
                            {campaign['min_engagement']}
                        </div>
                    </div>
                    
                    <div style="margin-top: 15px; padding: 12px; background: rgba(255,255,255,0.15); border-radius: 10px; color: white;">
                        <strong>💰 Payment Structure:</strong><br>
                        Base {format_currency(campaign['base_payment'])} + {format_currency(campaign['per_engagement'])} per engagement<br>
                        <strong>Max Earning: {format_currency(max_earning)}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                    <p style="margin: 0; font-weight: 600;">📅 Deadline</p>
                    <p style="margin: 5px 0; font-size: 1.1rem;">{campaign['deadline']}</p>
                    <p style="margin: 10px 0 0 0; font-size: 0.9rem; color: #6b7280;">
                        ⏱️ {random.randint(5, 20)} days left
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button(f"✅ Apply Now", key=f"apply_{campaign['id']}", use_container_width=True, type="primary"):
                    # Add to active campaigns
                    campaign_copy = campaign.copy()
                    campaign_copy['accepted_date'] = datetime.now().strftime("%d %b %Y")
                    campaign_copy['status'] = 'content_pending'
                    campaign_copy['current_reach'] = 0
                    campaign_copy['current_engagement'] = 0
                    campaign_copy['estimated_earning'] = 0
                    
                    st.session_state.active_campaigns.append(campaign_copy)
                    
                    add_notification(f"✅ Applied to {campaign['brand']} - {campaign['title']}", 'success')
                    st.success(f"✅ Successfully applied to {campaign['brand']} campaign!")
                    time.sleep(1)
                    st.rerun()
                
                # Show stats
                st.markdown(f"""
                <div style="background: white; padding: 12px; border-radius: 10px; margin-top: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                    <p style="margin: 0; font-size: 0.85rem; color: #6b7280;">
                        📊 {random.randint(50, 200)} creators applied<br>
                        ⭐ {random.randint(80, 95)}% satisfaction rate
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ==================== CONTENT CREATION ====================
def show_content_creation():
    """Content Creation View"""
    
    st.title("🎨 Create Content")
    st.caption("Use AI-powered tools to create amazing content for your campaigns")
    
    # Get campaigns that need content
    pending_campaigns = [c for c in st.session_state.active_campaigns if c.get('status') == 'content_pending']
    
    if not pending_campaigns:
        st.success("🎉 You've created content for all your active campaigns!")
        st.info("💡 Apply to new campaigns from the marketplace to create more content.")
        
        if st.button("🏢 Browse Marketplace", type="primary"):
            st.session_state.page = "marketplace"
            st.rerun()
        return
    
    # Select campaign
    campaign_options = {f"{c['brand']} - {c['title']}": c for c in pending_campaigns}
    selected_key = st.selectbox(
        "📋 Select Campaign to work on",
        list(campaign_options.keys())
    )
    
    campaign = campaign_options[selected_key]
    
    # Display campaign info
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 20px; margin: 15px 0; border-left: 5px solid {get_brand_color(campaign['brand'])}; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
        <div style="display: flex; align-items: center; gap: 15px; flex-wrap: wrap;">
            <div style="font-size: 3rem;">{get_brand_logo(campaign['brand'])}</div>
            <div>
                <h3 style="margin: 0;">{campaign['brand']}</h3>
                <p style="margin: 5px 0; color: #6b7280;">{campaign['title']}</p>
            </div>
            <div style="margin-left: auto;">
                <span class="badge badge-info">{get_content_type_name(campaign['content_type'])}</span>
                <span class="badge badge-warning">💰 {format_currency(campaign['base_payment'])}</span>
            </div>
        </div>
        <div style="display: flex; gap: 20px; margin-top: 15px; flex-wrap: wrap; font-size: 0.9rem; color: #6b7280;">
            <span>🎯 Target Reach: {campaign['target_reach']:,}</span>
            <span>⚡ Min Engagement: {campaign['min_engagement']}</span>
            <span>📅 Deadline: {campaign['deadline']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Content creation based on type
    content_type = campaign['content_type']
    
    if content_type == 'video':
        create_video_content(campaign)
    elif content_type == 'static_post':
        create_static_content(campaign)
    elif content_type == 'text_image':
        create_text_image_content(campaign)

def create_video_content(campaign):
    """Video content creation form"""
    st.subheader("🎥 Create Video Content")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Script generation
        st.markdown("#### 📝 Video Script")
        
        if st.button("🤖 Generate AI Script", use_container_width=True):
            script = generate_video_script(campaign['brand'], campaign['title'])
            st.session_state['script'] = script
        
        default_script = generate_video_script(campaign['brand'], campaign['title'])
        script = st.text_area(
            "Your Script",
            value=st.session_state.get('script', default_script),
            height=250,
            help="Write your video script here or use AI to generate one"
        )
        
        # Video settings
        st.markdown("#### ⚙️ Video Settings")
        
        col_a, col_b = st.columns(2)
        with col_a:
            duration = st.slider("Duration (seconds)", 15, 120, 45)
            aspect_ratio = st.selectbox(
                "Aspect Ratio",
                ["9:16 (Vertical)", "16:9 (Horizontal)", "1:1 (Square)"]
            )
        with col_b:
            music = st.selectbox(
                "Background Music",
                ["Upbeat", "Calm", "Energetic", "Corporate", "No Music"]
            )
            voiceover = st.selectbox(
                "Voiceover Style",
                ["Professional", "Casual", "Enthusiastic", "No Voiceover"]
            )
    
    with col2:
        st.markdown("#### 📁 Media Upload")
        
        uploaded_files = st.file_uploader(
            "Upload B-Roll or Clips",
            type=['mp4', 'mov', 'jpg', 'png'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} files uploaded")
            for file in uploaded_files:
                st.markdown(f"• {file.name}")
        
        st.markdown("#### 🎬 AI Video Generation")
        
        if st.button("🎬 Generate AI Video", use_container_width=True):
            with st.spinner("AI is generating your video..."):
                time.sleep(2)
                st.success("✅ Video generated successfully!")
                st.video("https://sample-videos.com/video321/mp4/240/big_buck_bunny_240p_1mb.mp4")
    
    # Preview & Submit
    st.markdown("---")
    st.subheader("📊 Estimated Performance")
    
    col1, col2, col3 = st.columns(3)
    
    estimated_reach = random.randint(campaign['target_reach'] - 500, campaign['target_reach'] + 1000)
    estimated_engagement = random.randint(campaign['min_engagement'], campaign['min_engagement'] * 2)
    
    base_earning = campaign['base_payment'] if estimated_engagement >= campaign['min_engagement'] else 0
    engagement_earning = estimated_engagement * campaign['per_engagement']
    total_estimated = base_earning + engagement_earning
    
    with col1:
        st.metric("📊 Estimated Reach", f"{estimated_reach:,}")
    with col2:
        st.metric("💬 Estimated Engagement", f"{estimated_engagement:,}")
    with col3:
        st.metric("💰 Estimated Earnings", format_currency(total_estimated))
    
    if st.button("✅ Submit Video Content", type="primary", use_container_width=True):
        # Update campaign
        for i, c in enumerate(st.session_state.active_campaigns):
            if c['id'] == campaign['id']:
                st.session_state.active_campaigns[i]['status'] = 'posted'
                st.session_state.active_campaigns[i]['created_content'] = {
                    'type': 'video',
                    'script': script,
                    'duration': duration,
                    'aspect_ratio': aspect_ratio,
                    'music': music,
                    'voiceover': voiceover,
                    'submitted_at': datetime.now().strftime("%d %b %Y, %I:%M %p")
                }
                st.session_state.active_campaigns[i]['current_reach'] = estimated_reach
                st.session_state.active_campaigns[i]['current_engagement'] = estimated_engagement
                st.session_state.active_campaigns[i]['estimated_earning'] = total_estimated
        
        add_notification(f"✅ Video content submitted for {campaign['brand']} - {campaign['title']}", 'success')
        st.success("🎉 Video content submitted successfully!")
        st.balloons()
        time.sleep(2)
        st.rerun()

def create_static_content(campaign):
    """Static post content creation form"""
    st.subheader("🖼️ Create Static Post")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Image
        st.markdown("#### 🖼️ Image")
        
        image_option = st.radio(
            "Choose Image Source",
            ["🎨 AI Generate", "📤 Upload Image", "📁 Use Template"]
        )
        
        if image_option == "🎨 AI Generate":
            prompt = st.text_input("Describe the image you want", placeholder="e.g., Product showcase with vibrant colors")
            if st.button("Generate Image", use_container_width=True):
                with st.spinner("AI is generating image..."):
                    time.sleep(2)
                    st.image("https://via.placeholder.com/600x400/667eea/ffffff?text=AI+Generated+Image", caption="AI Generated Image")
        
        elif image_option == "📤 Upload Image":
            uploaded_file = st.file_uploader("Upload your image", type=['jpg', 'png', 'jpeg', 'webp'])
            if uploaded_file:
                st.image(uploaded_file, caption="Uploaded Image")
        
        else:  # Template
            template = st.selectbox("Choose Template", ["Modern", "Classic", "Vibrant", "Minimal"])
            st.image(f"https://via.placeholder.com/600x400/667eea/ffffff?text={template}+Template", caption=f"{template} Template")
        
        # Text Content
        st.markdown("#### 📝 Text Content")
        
        if st.button("🤖 Generate AI Text", use_container_width=True):
            ai_content = generate_ai_content(campaign['brand'], campaign['title'])
            st.session_state['ai_text'] = ai_content
        
        ai_content = generate_ai_content(campaign['brand'], campaign['title'])
        default_text = st.session_state.get('ai_text', ai_content)
        
        headline = st.text_input("Headline", default_text['headline'])
        body = st.text_area("Body Text", default_text['body'], height=120)
        hashtags = st.text_input("Hashtags", default_text['hashtags'])
        cta = st.text_input("Call to Action", default_text['cta'])
    
    with col2:
        st.markdown("#### 📱 Platform Selection")
        platforms = st.multiselect(
            "Select platforms to post on",
            ["Facebook", "Instagram", "Twitter/X", "LinkedIn", "TikTok", "Pinterest"],
            default=["Facebook", "Instagram"]
        )
        
        st.markdown("#### ⏰ Post Timing")
        post_now = st.checkbox("Post immediately after approval", value=True)
        if not post_now:
            schedule_time = st.time_input("Schedule time", value=datetime.now().time())
            schedule_date = st.date_input("Schedule date", value=datetime.now().date())
    
    # Preview
    st.markdown("---")
    st.subheader("👁️ Post Preview")
    
    st.markdown(f"""
    <div style="background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px; max-width: 500px; margin: 0 auto;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: {get_brand_color(campaign['brand'])}; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; color: white;">
                {get_brand_logo(campaign['brand'])}
            </div>
            <div>
                <strong>{campaign['brand']}</strong>
                <div style="font-size: 0.8rem; color: #6b7280;">Sponsored • Just now</div>
            </div>
        </div>
        
        <h4 style="margin: 10px 0;">{headline}</h4>
        <p>{body}</p>
        
        <div style="background: #f3f4f6; height: 250px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #6b7280; margin: 15px 0;">
            🖼️ Image Placeholder
        </div>
        
        <p style="color: #3b82f6;">{hashtags}</p>
        <p style="color: #10b981; font-weight: 600;">{cta}</p>
        
        <div style="display: flex; gap: 20px; margin-top: 15px; color: #6b7280; font-size: 0.9rem;">
            <span>❤️ Like</span>
            <span>💬 Comment</span>
            <span>↗️ Share</span>
        </div>
        
        <div style="margin-top: 10px; display: flex; gap: 5px; flex-wrap: wrap;">
            {''.join([f'<span class="badge badge-info">{p}</span>' for p in platforms])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Performance Estimates
    st.markdown("---")
    st.subheader("📊 Estimated Performance")
    
    col1, col2, col3 = st.columns(3)
    
    estimated_reach = random.randint(campaign['target_reach'] - 300, campaign['target_reach'] + 800)
    estimated_engagement = random.randint(campaign['min_engagement'] - 50, campaign['min_engagement'] * 2)
    
    base_earning = campaign['base_payment'] if estimated_engagement >= campaign['min_engagement'] else 0
    engagement_earning = estimated_engagement * campaign['per_engagement']
    total_estimated = base_earning + engagement_earning
    
    with col1:
        st.metric("📊 Estimated Reach", f"{estimated_reach:,}")
    with col2:
        st.metric("💬 Estimated Engagement", f"{estimated_engagement:,}")
    with col3:
        st.metric("💰 Estimated Earnings", format_currency(total_estimated))
    
    if st.button("✅ Submit Post", type="primary", use_container_width=True):
        # Update campaign
        for i, c in enumerate(st.session_state.active_campaigns):
            if c['id'] == campaign['id']:
                st.session_state.active_campaigns[i]['status'] = 'posted'
                st.session_state.active_campaigns[i]['created_content'] = {
                    'type': 'static_post',
                    'headline': headline,
                    'body': body,
                    'hashtags': hashtags,
                    'cta': cta,
                    'platforms': platforms,
                    'submitted_at': datetime.now().strftime("%d %b %Y, %I:%M %p")
                }
                st.session_state.active_campaigns[i]['current_reach'] = estimated_reach
                st.session_state.active_campaigns[i]['current_engagement'] = estimated_engagement
                st.session_state.active_campaigns[i]['estimated_earning'] = total_estimated
        
        add_notification(f"✅ Post submitted for {campaign['brand']} - {campaign['title']}", 'success')
        st.success("🎉 Post submitted successfully!")
        st.balloons()
        time.sleep(2)
        st.rerun()

def create_text_image_content(campaign):
    """Text + Image content creation form"""
    st.subheader("📝 Create Text + Image Content")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text Content
        st.markdown("#### 📝 Text Content")
        
        if st.button("🤖 Generate AI Text", use_container_width=True):
            ai_content = generate_ai_content(campaign['brand'], campaign['title'])
            st.session_state['ai_text'] = ai_content
        
        ai_content = generate_ai_content(campaign['brand'], campaign['title'])
        default_text = st.session_state.get('ai_text', ai_content)
        
        headline = st.text_input("Headline", default_text['headline'])
        body = st.text_area("Body Text", default_text['body'], height=120)
        hashtags = st.text_input("Hashtags", default_text['hashtags'])
        
        # Image
        st.markdown("#### 🖼️ Image")
        image_option = st.radio(
            "Choose Image Source",
            ["🎨 AI Generate", "📤 Upload Image", "📁 Stock Images"],
            horizontal=True
        )
        
        if image_option == "🎨 AI Generate":
            prompt = st.text_input("Image description")
            if st.button("Generate", use_container_width=True):
                st.image("https://via.placeholder.com/400x300/667eea/ffffff?text=AI+Image")
        
        elif image_option == "📤 Upload Image":
            uploaded = st.file_uploader("Upload image", type=['jpg', 'png', 'jpeg'])
            if uploaded:
                st.image(uploaded, width=300)
        
        else:
            stock_categories = ["Nature", "Tech", "Business", "Lifestyle"]
            selected = st.selectbox("Stock Category", stock_categories)
            st.image(f"https://via.placeholder.com/400x300/667eea/ffffff?text={selected}+Stock", width=300)
    
    with col2:
        st.markdown("#### 📱 Platform & Settings")
        platforms = st.multiselect(
            "Platforms",
            ["Facebook", "Instagram", "Twitter/X", "LinkedIn"],
            default=["Facebook", "Instagram"]
        )
        
        engagement_goal = st.number_input(
            "Engagement Goal",
            min_value=100,
            max_value=1000,
            value=campaign['min_engagement']
        )
        
        st.markdown("#### 🎯 Content Tips")
        st.info(f"""
        💡 Tips for {campaign['brand']}:
        • Use high-quality visuals
        • Keep text concise and engaging
        • Include relevant hashtags
        • Add a clear call to action
        • Tag the brand if allowed
        """)
    
    # Preview
    st.markdown("---")
    st.subheader("👁️ Preview")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: white; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px;">
            <h4>{headline}</h4>
            <p>{body}</p>
            <div style="background: #f3f4f6; height: 200px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #6b7280; margin: 10px 0;">
                🖼️ Image
            </div>
            <p style="color: #3b82f6;">{hashtags}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Estimated Performance
        st.markdown("#### 📊 Estimated Performance")
        
        estimated_reach = random.randint(campaign['target_reach'] - 200, campaign['target_reach'] + 500)
        estimated_engagement = random.randint(campaign['min_engagement'] - 30, campaign['min_engagement'] * 2)
        
        base_earning = campaign['base_payment'] if estimated_engagement >= campaign['min_engagement'] else 0
        engagement_earning = estimated_engagement * campaign['per_engagement']
        total_estimated = base_earning + engagement_earning
        
        st.metric("Estimated Reach", f"{estimated_reach:,}")
        st.metric("Estimated Engagement", f"{estimated_engagement:,}")
        st.metric("Estimated Earnings", format_currency(total_estimated))
        
        if st.button("✅ Submit Content", type="primary", use_container_width=True):
            # Update campaign
            for i, c in enumerate(st.session_state.active_campaigns):
                if c['id'] == campaign['id']:
                    st.session_state.active_campaigns[i]['status'] = 'posted'
                    st.session_state.active_campaigns[i]['created_content'] = {
                        'type': 'text_image',
                        'headline': headline,
                        'body': body,
                        'hashtags': hashtags,
                        'platforms': platforms,
                        'submitted_at': datetime.now().strftime("%d %b %Y, %I:%M %p")
                    }
                    st.session_state.active_campaigns[i]['current_reach'] = estimated_reach
                    st.session_state.active_campaigns[i]['current_engagement'] = estimated_engagement
                    st.session_state.active_campaigns[i]['estimated_earning'] = total_estimated
            
            add_notification(f"✅ Content submitted for {campaign['brand']} - {campaign['title']}", 'success')
            st.success("🎉 Content submitted successfully!")
            st.balloons()
            time.sleep(2)
            st.rerun()

# ==================== ANALYTICS ====================
def show_analytics():
    """Analytics Dashboard"""
    
    st.title("📊 Analytics Dashboard")
    st.caption("Track your performance and earnings across all campaigns")
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    total_earned = sum(c.get('estimated_earning', 0) for c in st.session_state.completed_campaigns)
    total_active = len([c for c in st.session_state.active_campaigns if c.get('status') != 'completed'])
    total_completed = len(st.session_state.completed_campaigns)
    total_reach = sum(c.get('current_reach', 0) for c in st.session_state.active_campaigns + st.session_state.completed_campaigns)
    
    with col1:
        st.metric("💰 Total Earned", format_currency(total_earned), delta="+12%")
    with col2:
        st.metric("🎯 Active Campaigns", total_active)
    with col3:
        st.metric("✅ Completed", total_completed)
    with col4:
        st.metric("📊 Total Reach", f"{total_reach:,}")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Earnings Trend")
        
        # Generate sample earnings data
        if st.session_state.completed_campaigns:
            dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
            earnings = [random.randint(0, 200) for _ in range(30)]
            
            chart_data = pd.DataFrame({
                'Date': dates,
                'Earnings': earnings
            })
            st.line_chart(chart_data, x='Date', y='Earnings')
        else:
            st.info("Complete campaigns to see earnings trends")
    
    with col2:
        st.subheader("🎯 Campaign Performance")
        
        if st.session_state.completed_campaigns:
            campaign_data = pd.DataFrame([
                {
                    'Campaign': c['title'][:20],
                    'Reach': c.get('current_reach', 0),
                    'Engagement': c.get('current_engagement', 0)
                }
                for c in st.session_state.completed_campaigns[-5:]
            ])
            st.bar_chart(campaign_data.set_index('Campaign'))
        else:
            st.info("Complete campaigns to see performance data")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Campaign List
    st.subheader("📋 All Campaigns")
    
    all_campaigns = st.session_state.active_campaigns + st.session_state.completed_campaigns
    
    if all_campaigns:
        df = pd.DataFrame([
            {
                'Brand': c['brand'],
                'Campaign': c['title'],
                'Status': '✅ Completed' if c in st.session_state.completed_campaigns else '🔄 Active',
                'Earnings': format_currency(c.get('estimated_earning', 0)),
                'Reach': c.get('current_reach', 0),
                'Engagement': c.get('current_engagement', 0)
            }
            for c in all_campaigns
        ])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No campaigns yet. Start by applying to campaigns in the marketplace!")

# ==================== NOTIFICATIONS ====================
def show_notifications():
    """Display notifications in sidebar"""
    st.sidebar.markdown("### 🔔 Notifications")
    
    if not st.session_state.notifications:
        st.sidebar.info("No notifications")
    else:
        for notif in st.session_state.notifications[:5]:
            color = "#10b981" if notif['type'] == 'success' else "#3b82f6" if notif['type'] == 'info' else "#f59e0b"
            st.sidebar.markdown(f"""
            <div class="notification-item" style="border-left-color: {color};">
                <span>{notif['message']}</span>
                <span class="time">{notif['time']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if len(st.session_state.notifications) > 5:
            st.sidebar.caption(f"+ {len(st.session_state.notifications) - 5} more")
    
    if st.sidebar.button("Clear All", use_container_width=True):
        st.session_state.notifications = []
        st.rerun()

# ==================== SIDEBAR ====================
def render_sidebar():
    """Render sidebar with settings and navigation"""
    
    with st.sidebar:
        # Logo / Header
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-size: 3rem;">🌍</div>
            <h2 style="margin: 5px 0; color: #667eea;">CollabNet</h2>
            <p style="font-size: 0.85rem; color: #6b7280;">Global Creator Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        
        nav_options = {
            "📊 Dashboard": "dashboard",
            "🏢 Marketplace": "marketplace",
            "🎨 Create Content": "create",
            "📊 Analytics": "analytics"
        }
        
        for label, page in nav_options.items():
            if st.button(label, key=f"nav_{page}", use_container_width=True, 
                        type="primary" if st.session_state.page == page else "secondary"):
                st.session_state.page = page
                st.rerun()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Settings
        st.markdown("### 🌍 Settings")
        
        # Language
        lang_options = [f"{LANGUAGES[code]['flag']} {LANGUAGES[code]['name']}" for code in LANGUAGES]
        lang_codes = list(LANGUAGES.keys())
        current_lang_index = lang_codes.index(st.session_state.language) if st.session_state.language in lang_codes else 0
        
        selected_lang = st.selectbox(
            "Language",
            lang_options,
            index=current_lang_index
        )
        selected_code = lang_codes[lang_options.index(selected_lang)]
        if selected_code != st.session_state.language:
            st.session_state.language = selected_code
            st.rerun()
        
        # Currency
        currency_options = [f"{CURRENCIES[code]['emoji']} {CURRENCIES[code]['name']} ({CURRENCIES[code]['symbol']})" 
                           for code in CURRENCIES]
        currency_codes = list(CURRENCIES.keys())
        current_currency_index = currency_codes.index(st.session_state.currency) if st.session_state.currency in currency_codes else 0
        
        selected_currency = st.selectbox(
            "Currency",
            currency_options,
            index=current_currency_index
        )
        selected_currency_code = currency_codes[currency_options.index(selected_currency)]
        if selected_currency_code != st.session_state.currency:
            st.session_state.currency = selected_currency_code
            st.rerun()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # User Info
        st.markdown("### 👤 Profile")
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div><strong>{st.session_state.user_name}</strong></div>
                    <div style="font-size: 0.85rem; color: #6b7280;">⭐ {st.session_state.user_level}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.2rem; font-weight: 600; color: #10b981;">
                        {format_currency(st.session_state.balance)}
                    </div>
                    <div style="font-size: 0.8rem; color: #6b7280;">Balance</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💰 Withdraw", use_container_width=True):
            if st.session_state.balance > 0:
                st.session_state.balance = 0
                add_notification(f"✅ Withdrew {format_currency(st.session_state.balance)}", 'success')
                st.success("Withdrawal successful!")
                st.rerun()
            else:
                st.warning("No balance to withdraw")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Notifications
        show_notifications()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; color: #6b7280;">
            🌍 CollabNet v2.0<br>
            Connect • Create • Earn
        </div>
        """, unsafe_allow_html=True)

# ==================== MAIN APP ====================
def main():
    """Main application entry point"""
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    if st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "marketplace":
        show_marketplace()
    elif st.session_state.page == "create":
        show_content_creation()
    elif st.session_state.page == "analytics":
        show_analytics()

if __name__ == "__main__":
    main()
