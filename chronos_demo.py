There's a syntax error in the code. The string isn't properly closed. Let me provide the complete, corrected code:

```python
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Chronos Bazaar - Brand Marketplace",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Hind Siliguri', sans-serif;
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
    
    .bangla-text {
        font-size: 1.1rem;
        line-height: 1.8;
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

# Brand Database
BRANDS = {
    'প্রাণ ফুডস': {
        'logo': '🥘',
        'color': '#FF6B6B',
        'category': 'ফুড এন্ড বেভারেজ',
        'rating': 4.8,
        'campaigns': [
            {
                'id': 'pran1',
                'title': 'প্রাণ জুস প্রমোশন',
                'description': 'নতুন প্রাণ ম্যাঙ্গো জুসের প্রমোশনাল কন্টেন্ট তৈরি করুন',
                'content_type': 'video',
                'base_payment': 150,
                'target_reach': 1000,
                'per_engagement': 0.5,
                'min_engagement': 200,
                'deadline': '১৫ ডিসেম্বর',
                'status': 'active',
                'created_content': None
            },
            {
                'id': 'pran2',
                'title': 'প্রাণ নুডলস রেসিপি',
                'description': 'প্রাণ নুডলস দিয়ে সহজ রেসিপি ভিডিও তৈরি করুন',
                'content_type': 'text_image',
                'base_payment': 100,
                'target_reach': 500,
                'per_engagement': 0.3,
                'min_engagement': 150,
                'deadline': '২০ ডিসেম্বর',
                'status': 'active',
                'created_content': None
            }
        ]
    },
    'আকিজ গ্রুপ': {
        'logo': '👔',
        'color': '#3b82f6',
        'category': 'ফ্যাশন এন্ড টেক্সটাইল',
        'rating': 4.6,
        'campaigns': [
            {
                'id': 'akij1',
                'title': 'আকিজ ফুটওয়্যার লঞ্চ',
                'description': 'নতুন আকিজ জুতা কালেকশনের স্ট্যাটিক পোস্ট তৈরি করুন',
                'content_type': 'static_post',
                'base_payment': 120,
                'target_reach': 800,
                'per_engagement': 0.4,
                'min_engagement': 200,
                'deadline': '১২ ডিসেম্বর',
                'status': 'active',
                'created_content': None
            }
        ]
    },
    'ড্যানিশ ডেইরি': {
        'logo': '🥛',
        'color': '#10b981',
        'category': 'ডেইরি প্রোডাক্ট',
        'rating': 4.7,
        'campaigns': [
            {
                'id': 'danish1',
                'title': 'ড্যানিশ মিল্ক হেলথ ক্যাম্পেইন',
                'description': 'ড্যানিশ মিল্কের স্বাস্থ্য উপকারিতা নিয়ে ভিডিও তৈরি করুন',
                'content_type': 'video',
                'base_payment': 180,
                'target_reach': 1200,
                'per_engagement': 0.6,
                'min_engagement': 300,
                'deadline': '১৮ ডিসেম্বর',
                'status': 'active',
                'created_content': None
            }
        ]
    },
    'বেস্টার্ন কম্পিউটার': {
        'logo': '💻',
        'color': '#8b5cf6',
        'category': 'ইলেকট্রনিক্স',
        'rating': 4.5,
        'campaigns': [
            {
                'id': 'bestern1',
                'title': 'বেস্টার্ন ল্যাপটপ রিভিউ',
                'description': 'বেস্টার্ন ল্যাপটপের হ্যান্ডস-অন রিভিউ ভিডিও তৈরি করুন',
                'content_type': 'video',
                'base_payment': 200,
                'target_reach': 1500,
                'per_engagement': 0.7,
                'min_engagement': 400,
                'deadline': '২৫ ডিসেম্বর',
                'status': 'active',
                'created_content': None
            }
        ]
    },
    'লিজেন্ড ফার্মাসিউটিক্যাল': {
        'logo': '💊',
        'color': '#f59e0b',
        'category': 'ফার্মাসিউটিক্যাল',
        'rating': 4.9,
        'campaigns': [
            {
                'id': 'legend1',
                'title': 'লিজেন্ড ভিটামিন সচেতনতা',
                'description': 'স্বাস্থ্য সচেতনতা বিষয়ক টেক্সট+ইমেজ কন্টেন্ট তৈরি করুন',
                'content_type': 'text_image',
                'base_payment': 90,
                'target_reach': 600,
                'per_engagement': 0.35,
                'min_engagement': 180,
                'deadline': '১০ ডিসেম্বর',
                'status': 'active',
                'created_content': None
            }
        ]
    }
}

def get_content_type_name(content_type):
    """Convert content type code to readable name"""
    names = {
        'static_post': 'স্ট্যাটিক পোস্ট',
        'video': 'ভিডিও',
        'text_image': 'টেক্সট+ইমেজ'
    }
    return names.get(content_type, content_type)

def generate_ai_content(brand, title):
    """Generate AI content for brand campaigns"""
    templates = {
        'প্রাণ ফুডস': {
            'headline': f'{brand} - {title}',
            'body': 'বিশেষ অফার! সীমিত সময়ের জন্য সবচেয়ে ভালো দামে পাচ্ছেন। আজই অর্ডার করুন!',
            'hashtags': f'#{brand.replace(" ", "")} #বাংলাদেশ #অফার #স্পেশাল'
        },
        'আকিজ গ্রুপ': {
            'headline': f'{brand} এর নতুন কালেকশন',
            'body': 'নতুন ডিজাইনের সাথে উপস্থিত! স্টাইলিশ এবং আরামদায়ক, আপনার জন্য বিশেষ দাম।',
            'hashtags': f'#{brand.replace(" ", "")} #ফ্যাশন #নতুনকালেকশন #বাংলাদেশ'
        },
        'ড্যানিশ ডেইরি': {
            'headline': f'{brand} - পুষ্টির উৎস',
            'body': '১০০% বিশুদ্ধ ও পুষ্টিকর। পরিবারের স্বাস্থ্যের জন্য সেরা পছন্দ।',
            'hashtags': f'#{brand.replace(" ", "")} #স্বাস্থ্য #পুষ্টি #ডেইরি'
        }
    }
    
    return templates.get(brand, {
        'headline': f'{brand} - {title}',
        'body': 'বিশেষ অফার! সীমিত সময়ের জন্য বিশেষ দাম। আজই কিনুন!',
        'hashtags': f'#{brand.replace(" ", "")} #অফার #বাংলাদেশ #স্পেশাল'
    })

def generate_video_script(brand, title):
    """Generate video script for brand campaigns"""
    scripts = {
        'প্রাণ ফুডস': f'আজ আমরা দেখবো {brand} এর নতুন প্রোডাক্ট। স্বাদের সাথে স্বাস্থ্যের পরিপূর্ণ সংমিশ্রণ।',
        'আকিজ গ্রুপ': f'{brand} এর নতুন কালেকশন নিয়ে আজকের ভিডিও। স্টাইলিশ ডিজাইন আর আরামদায়ক ফিট।',
        'ড্যানিশ ডেইরি': f'{brand} - বিশুদ্ধতার প্রতিশ্রুতি। পরিবারের প্রতিটি সদস্যের জন্য পুষ্টির উৎস।'
    }
    
    return scripts.get(brand, f'{brand} এর {title} সম্পর্কে আজকের বিশেষ ভিডিও।')

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>💰</h1>", unsafe_allow_html=True)
        st.title("Chronos Bazaar")
        
        menu = st.radio(
            "নেভিগেশন মেনু",
            ["🏠 ড্যাশবোর্ড", "🏢 ব্র্যান্ড মার্কেটপ্লেস", "🎨 কন্টেন্ট তৈরি", "📊 আমার ক্যাম্পেইন", "💰 আয় ও উত্তোলন"]
        )
        
        st.markdown("---")
        
        # Quick Stats
        st.subheader("📊 আমার স্ট্যাটস")
        st.metric("বর্তমান ব্যালেন্স", f"৳{st.session_state.balance}")
        st.metric("সক্রিয় ক্যাম্পেইন", len(st.session_state.active_campaigns))
        st.metric("সম্পন্ন ক্যাম্পেইন", len(st.session_state.completed_campaigns))
        
        st.markdown("---")
        
        # Quick Actions
        if st.button("🔄 নতুন ক্যাম্পেইন খুঁজুন", use_container_width=True):
            st.session_state.show_marketplace = True

    # Main Content
    if menu == "🏠 ড্যাশবোর্ড":
        show_dashboard()
    elif menu == "🏢 ব্র্যান্ড মার্কেটপ্লেস":
        show_marketplace()
    elif menu == "🎨 কন্টেন্ট তৈরি":
        create_content()
    elif menu == "📊 আমার ক্যাম্পেইন":
        show_my_campaigns()
    elif menu == "💰 আয় ও উত্তোলন":
        show_earnings()

def show_dashboard():
    st.title("💰 Chronos Bazaar - ব্র্যান্ড মার্কেটপ্লেস")
    
    # Welcome Card
    st.markdown(f"""
    <div class="earning-card">
        <h2>স্বাগতম! আপনার আয়ের সুযোগের ড্যাশবোর্ড</h2>
        <p class="bangla-text">ব্র্যান্ডগুলোর জন্য কন্টেন্ট তৈরি করুন, টার্গেট রিচ পূরণ করুন এবং অর্থ উপার্জন করুন!</p>
        <h3>বর্তমান ব্যালেন্স: ৳{st.session_state.balance}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        active_earning = sum([c.get('estimated_earning', 0) for c in st.session_state.active_campaigns])
        st.metric("সক্রিয় ক্যাম্পেইন আয়", f"৳{active_earning}", "সম্ভাব্য")
    
    with col2:
        completed_earning = sum([c.get('paid_amount', 0) for c in st.session_state.completed_campaigns])
        st.metric("সম্পন্ন ক্যাম্পেইন আয়", f"৳{completed_earning}", "প্রাপ্ত")
    
    with col3:
        total_content = len(st.session_state.content_created)
        st.metric("তৈরি কন্টেন্ট", total_content)
    
    st.markdown("---")
    
    # Recommended Campaigns
    st.subheader("🔥 সুপারিশকৃত ক্যাম্পেইন")
    
    # Show 3 random campaigns
    all_campaigns = []
    for brand_name, brand_data in BRANDS.items():
        for campaign in brand_data['campaigns']:
            if campaign['status'] == 'active':
                all_campaigns.append({
                    'brand': brand_name,
                    'brand_logo': brand_data['logo'],
                    'brand_color': brand_data['color'],
                    **campaign
                })
    
    if all_campaigns:
        rec_campaigns = random.sample(all_campaigns, min(3, len(all_campaigns)))
        
        for campaign in rec_campaigns:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div class="brand-card" style="border-left-color: {campaign['brand_color']};">
                    <h3>{campaign['brand_logo']} {campaign['brand']} - {campaign['title']}</h3>
                    <p>{campaign['description']}</p>
                    <p><strong>কন্টেন্ট টাইপ:</strong> {get_content_type_name(campaign['content_type'])}</p>
                    <p><strong>বেস পেমেন্ট:</strong> ৳{campaign['base_payment']}</p>
                    <span class="reach-badge">লক্ষ্য রিচ: {campaign['target_reach']}</span>
                    <span class="reach-badge">ন্যূনতম এঙ্গেজমেন্ট: {campaign['min_engagement']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("গ্রহণ করুন", key=f"accept_{campaign['id']}", use_container_width=True):
                    # Add to active campaigns
                    st.session_state.active_campaigns.append({
                        'campaign_id': campaign['id'],
                        'brand': campaign['brand'],
                        'title': campaign['title'],
                        'content_type': campaign['content_type'],
                        'base_payment': campaign['base_payment'],
                        'target_reach': campaign['target_reach'],
                        'min_engagement': campaign['min_engagement'],
                        'per_engagement': campaign['per_engagement'],
                        'accepted_date': datetime.now().strftime("%d %b %Y"),
                        'status': 'content_pending',
                        'created_content': None,
                        'current_reach': 0,
                        'current_engagement': 0,
                        'estimated_earning': 0
                    })
                    st.success(f"✅ '{campaign['title']}' ক্যাম্পেইন গ্রহণ করা হয়েছে!")
                    st.rerun()
    else:
        st.info("বর্তমানে কোনো সক্রিয় ক্যাম্পেইন নেই")

def show_marketplace():
    st.title("🏢 ব্র্যান্ড মার্কেটপ্লেস")
    
    # Search and Filter
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("ব্র্যান্ড/ক্যাম্পেইন সার্চ করুন", "")
    
    with col2:
        content_filter = st.selectbox(
            "কন্টেন্ট টাইপ ফিল্টার",
            ["সবগুলো", "ভিডিও", "স্ট্যাটিক পোস্ট", "টেক্সট+ইমেজ"]
        )
    
    with col3:
        payment_filter = st.selectbox(
            "পেমেন্ট ফিল্টার",
            ["সবগুলো", "৳১০০ এর নিচে", "৳১০০-৳১৫০", "৳১৫০ এর উপরে"]
        )
    
    st.markdown("---")
    
    # Display Brands
    for brand_name, brand_data in BRANDS.items():
        st.markdown(f"""
        <div style="
            background: {brand_data['color']}20;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border-left: 5px solid {brand_data['color']};
        ">
            <h2>{brand_data['logo']} {brand_name}</h2>
            <p><strong>ক্যাটাগরি:</strong> {brand_data['category']} | <strong>রেটিং:</strong> {brand_data['rating']} ⭐</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show campaigns for this brand
        for campaign in brand_data['campaigns']:
            if campaign['status'] == 'active':
                # Apply filters
                if content_filter != "সবগুলো" and content_filter != get_content_type_name(campaign['content_type']):
                    continue
                
                if payment_filter == "৳১০০ এর নিচে" and campaign['base_payment'] >= 100:
                    continue
                elif payment_filter == "৳১০০-৳১৫০" and (campaign['base_payment'] < 100 or campaign['base_payment'] > 150):
                    continue
                elif payment_filter == "৳১৫০ এর উপরে" and campaign['base_payment'] <= 150:
                    continue
                
                if search_query and search_query.lower() not in f"{brand_name} {campaign['title']}".lower():
                    continue
                
                display_campaign_card(brand_name, brand_data, campaign)

def display_campaign_card(brand_name, brand_data, campaign):
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="campaign-card">
            <h3>{campaign['title']}</h3>
            <p>{campaign['description']}</p>
            
            <div style="display: flex; gap: 20px; margin-top: 15px;">
                <div>
                    <strong>কন্টেন্ট টাইপ:</strong><br>
                    {get_content_type_name(campaign['content_type'])}
                </div>
                <div>
                    <strong>বেস পেমেন্ট:</strong><br>
                    ৳{campaign['base_payment']}
                </div>
                <div>
                    <strong>লক্ষ্য রিচ:</strong><br>
                    {campaign['target_reach']}
                </div>
                <div>
                    <strong>ন্যূনতম এঙ্গেজমেন্ট:</strong><br>
                    {campaign['min_engagement']}
                </div>
            </div>
            
            <div style="margin-top: 15px;">
                <strong>পেমেন্ট স্ট্রাকচার:</strong><br>
                • বেস পেমেন্ট: ৳{campaign['base_payment']}<br>
                • প্রতি এঙ্গেজমেন্ট: ৳{campaign['per_engagement']}<br>
                • সর্বোচ্চ আয়: ৳{campaign['base_payment'] + (campaign['target_reach'] * campaign['per_engagement'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📅 ডেডলাইন")
        st.markdown(f"**{campaign['deadline']}**")
        
        st.markdown("#### ⏱️ সময় বাকি")
        days_left = random.randint(3, 14)
        st.markdown(f"**{days_left} দিন**")
    
    with col3:
        # Check if already accepted
        already_accepted = any(
            c['campaign_id'] == campaign['id'] 
            for c in st.session_state.active_campaigns + st.session_state.completed_campaigns
        )
        
        if not already_accepted:
            if st.button("✅ ক্যাম্পেইন গ্রহণ করুন", key=f"accept_{campaign['id']}", use_container_width=True):
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
                st.success(f"✅ '{campaign['title']}' ক্যাম্পেইন গ্রহণ করা হয়েছে!")
                st.rerun()
        else:
            st.info("⏳ ইতিমধ্যে গ্রহণ করা হয়েছে")
        
        # Quick Stats
        st.markdown("---")
        st.markdown("#### 📊 পরিসংখ্যান")
        st.markdown(f"""
        <small>
        • গ্রহণ করেছে: {random.randint(50, 200)} জন<br>
        • সফল হয়েছে: {random.randint(30, 80)} জন<br>
        • গড় আয়: ৳{campaign['base_payment'] + random.randint(20, 80)}
        </small>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

def create_content():
    st.title("🎨 কন্টেন্ট তৈরি করুন")
    
    if not st.session_state.active_campaigns:
        st.info("📭 আপনি এখনো কোনো ক্যাম্পেইন গ্রহণ করেননি। প্রথমে ব্র্যান্ড মার্কেটপ্লেস থেকে ক্যাম্পেইন গ্রহণ করুন।")
        if st.button("🏢 ব্র্যান্ড মার্কেটপ্লেস দেখুন"):
            st.session_state.current_menu = "marketplace"
            st.rerun()
        return
    
    # Select campaign to create content for
    pending_campaigns = [c for c in st.session_state.active_campaigns if c['status'] == 'content_pending']
    
    if not pending_campaigns:
        st.success("✅ আপনার সব ক্যাম্পেইনের জন্য কন্টেন্ট তৈরি করা হয়েছে!")
        return
    
    campaign_options = {f"{c['brand']} - {c['title']}": c for c in pending_campaigns}
    selected_campaign_name = st.selectbox(
        "কন্টেন্ট তৈরি করার জন্য ক্যাম্পেইন সিলেক্ট করুন",
        list(campaign_options.keys())
    )
    
    selected_campaign = campaign_options[selected_campaign_name]
    
    st.markdown(f"""
    <div class="brand-card" style="border-left-color: {BRANDS[selected_campaign['brand']]['color']};">
        <h3>{BRANDS[selected_campaign['brand']]['logo']} {selected_campaign['brand']}</h3>
        <h4>{selected_campaign['title']}</h4>
        <p><strong>কন্টেন্ট টাইপ:</strong> {get_content_type_name(selected_campaign['content_type'])}</p>
        <p><strong>বেস পেমেন্ট:</strong> ৳{selected_campaign['base_payment']}</p>
        <p><strong>লক্ষ্য:</strong> {selected_campaign['target_reach']} রিচ, {selected_campaign['min_engagement']} এঙ্গেজমেন্ট</p>
        <p><strong>ডেডলাইন:</strong> {selected_campaign.get('deadline', '১৫ ডিসেম্বর')}</p>
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
    st.subheader("🖼️ স্ট্যাটিক পোস্ট তৈরি করুন")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Image Upload or Generation
        st.markdown("#### ১. ইমেজ তৈরি/আপলোড করুন")
        image_option = st.radio(
            "ইমেজ অপশন",
            ["AI দিয়ে জেনারেট করুন", "আপলোড করুন", "টেমপ্লেট ব্যবহার করুন"]
        )
        
        if image_option == "AI দিয়ে জেনারেট করুন":
            prompt = st.text_area("AI প্রম্পট লিখুন", 
                                 f"{campaign['brand']} এর {campaign['title']} এর জন্য আকর্ষণীয় সোশ্যাল মিডিয়া পোস্ট")
            if st.button("🖼️ AI ইমেজ জেনারেট করুন"):
                st.info("AI ইমেজ জেনারেট হচ্ছে... (ডেমো)")
                # Mock image generation
                st.image("https://via.placeholder.com/600x400/3b82f6/ffffff?text=AI+Generated+Post", 
                        caption="AI জেনারেটেড ইমেজ")
        
        elif image_option == "আপলোড করুন":
            uploaded_file = st.file_uploader("ছবি আপলোড করুন", type=['jpg', 'png', 'jpeg'])
            if uploaded_file:
                st.image(uploaded_file, caption="আপলোডেড ইমেজ")
        
        else:  # Template
            template = st.selectbox("টেমপ্লেট সিলেক্ট করুন", ["ডিজাইন ১", "ডিজাইন ২", "ডিজাইন ৩"])
            st.image(f"https://via.placeholder.com/600x400/{BRANDS[campaign['brand']]['color'][1:]}/ffffff?text={campaign['brand']}+{template}", 
                    caption=f"{template} টেমপ্লেট")
    
    with col2:
        st.markdown("#### ২. টেক্সট কন্টেন্ট")
        
        # AI Text Generation
        if st.button("🤖 AI টেক্সট জেনারেট করুন"):
            generated_text = generate_ai_content(campaign['brand'], campaign['title'])
            st.session_state.generated_text = generated_text
        
        if 'generated_text' in st.session_state:
            headline = st.text_input("হেডলাইন", st.session_state.generated_text['headline'])
            body = st.text_area("বডি টেক্সট", st.session_state.generated_text['body'], height=150)
            hashtags = st.text_input("হ্যাশট্যাগ", st.session_state.generated_text['hashtags'])
        else:
            headline = st.text_input("হেডলাইন", f"{campaign['brand']} - {campaign['title']}")
            body = st.text_area("বডি টেক্সট", "বিশেষ অফার! সীমিত সময়ের জন্য...", height=150)
            hashtags = st.text_input("হ্যাশট্যাগ", f"#{campaign['brand'].replace(' ', '')} #অফার #বাংলাদেশ")
        
        st.markdown("#### ৩. প্ল্যাটফর্ম")
        platforms = st.multiselect(
            "পোস্ট করার প্ল্যাটফর্ম",
            ["Facebook", "Instagram", "Twitter", "LinkedIn"],
            default=["Facebook", "Instagram"]
        )
    
    st.markdown("---")
    
    # Preview and Submit
    st.subheader("👁️ পোস্ট প্রিভিউ")
    
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
                    background: {BRANDS[campaign['brand']]['color']};
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1.5rem;
                    margin-right: 10px;
                ">{BRANDS[campaign['brand']]['logo']}</div>
                <div>
                    <strong>আপনার পেজ</strong><br>
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
                🖼️ পোস্ট ইমেজ
            </div>
            
            <p><small>{hashtags}</small></p>
            
            <div style="display: flex; gap: 20px; color: #6b7280; margin-top: 15px;">
                <span>❤️ লাইক</span>
                <span>💬 কমেন্ট</span>
                <span>🔄 শেয়ার</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with preview_col2:
        st.markdown("#### 📊 আনুমানিক পারফরম্যান্স")
        
        estimated_reach = random.randint(300, 1200)
        estimated_engagement = random.randint(50, 400)
        
        st.metric("আনুমানিক রিচ", f"{estimated_reach}")
        st.metric("আনুমানিক এঙ্গেজমেন্ট", f"{estimated_engagement}")
        
        # Calculate estimated earning
        base_earning = campaign['base_payment'] if estimated_engagement >= campaign['min_engagement'] else 0
        engagement_earning = estimated_engagement * campaign['per_engagement']
        total_estimated = base_earning + engagement_earning
        
        st.metric("আনুমানিক আয়", f"৳{total_estimated:.2f}")
        
        if st.button("✅ কন্টেন্ট সাবমিট করুন", type="primary", use_container_width=True):
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
            
            st.success("✅ কন্টেন্ট সাবমিট করা হয়েছে! পারফরম্যান্স ট্র্যাকিং শুরু হয়েছে।")
            st.balloons()

def create_video_content(campaign):
    st.subheader("🎥 ভিডিও কন্টেন্ট তৈরি করুন")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### ১. ভিডিও স্ক্রিপ্ট")
        
        if st.button("🤖 AI স্ক্রিপ্ট জেনারেট করুন"):
            script = generate_video_script(campaign['brand'], campaign['title'])
            st.session_state.video_script = script
        
        if 'video_script' in st.session_state:
            script_text = st.text_area("স্ক্রিপ্ট", st.session_state.video_script, height=200)
        else:
            script_text = st.text_area("স্ক্রিপ্ট", f"{campaign['brand']} এর {campaign['title']} সম্পর্কে ভিডিও স্ক্রিপ্ট...", height=200)
        
        st.markdown("#### ২. ভিডিও সেটিংস")
        
        duration = st.slider("ভিডিও দৈর্ঘ্য (সেকেন্ড)", 15, 60, 30)
        aspect_ratio = st.selectbox("অ্যাসপেক্ট রেশিও", ["9:16 (Reels/TikTok)", "1:1 (Instagram)", "16:9 (YouTube)"])
        music = st.selectbox("ব্যাকগ্রাউন্ড মিউজিক", ["Upbeat", "Calm", "Trending", "No Music"])
        voiceover = st.selectbox("ভয়েসওভার", ["পুরুষ (বাংলা)", "মহিলা (বাংলা)", "ইংরেজি", "No Voiceover"])
    
    with col2:
        st.markdown("#### ৩. মিডিয়া আপলোড")
        
        uploaded_files = st.file_uploader(
            "ছবি/ভিডিও ক্লিপ আপলোড করুন",
            type=['jpg', 'png', 'mp4', 'mov'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"{len(uploaded_files)} টি ফাইল আপলোড হয়েছে")
        
        st.markdown("#### ৪. AI ভিডিও জেনারেশন")
        
        if st.button("🎬 AI ভিডিও জেনারেট করুন"):
            st.info("AI ভিডিও জেনারেট হচ্ছে... (ডেমো)")
            # Mock video generation
            st.markdown("""
This is some markdown text
With multiple lines
Now properly closed with triple quotes
""")
            <div style="
                "background-color: #f0f0f0; padding: 10px;">Content</div>';
                height: 300px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 1.5rem;
                margin:
