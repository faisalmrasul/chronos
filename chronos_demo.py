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

def create_video_content(campaign):
    """Create video content section"""
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
        st.markdown("#### 📊 আনুমানিক পারফরম্যান্স")
        
        estimated_reach = random.randint(300, 1500)
        estimated_engagement = random.randint(50, 500)
        
        st.metric("আনুমানিক রিচ", f"{estimated_reach}")
        st.metric("আনুমানিক এঙ্গেজমেন্ট", f"{estimated_engagement}")
        
        # Calculate estimated earning
        base_earning = campaign['base_payment'] if estimated_engagement >= campaign['min_engagement'] else 0
        engagement_earning = estimated_engagement * campaign['per_engagement']
        total_estimated = base_earning + engagement_earning
        
        st.metric("আনুমানিক আয়", f"৳{total_estimated:.2f}")
        
        if st.button("✅ ভিডিও সাবমিট করুন", type="primary", use_container_width=True):
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
            
            st.success("✅ ভিডিও সাবমিট করা হয়েছে! পারফরম্যান্স ট্র্যাকিং শুরু হয়েছে।")
            st.balloons()

def create_text_image_content(campaign):
    """Create text+image content section"""
    st.subheader("📝 টেক্সট+ইমেজ কন্টেন্ট তৈরি করুন")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### ১. টেক্সট কন্টেন্ট")
        
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
    
    with col2:
        st.markdown("#### ২. ইমেজ সিলেক্ট করুন")
        
        image_option = st.radio(
            "ইমেজ অপশন",
            ["AI দিয়ে জেনারেট করুন", "আপলোড করুন", "স্টক ইমেজ ব্যবহার করুন"]
        )
        
        if image_option == "AI দিয়ে জেনারেট করুন":
            prompt = st.text_input("AI প্রম্পট লিখুন", f"{campaign['brand']} {campaign['title']}")
            if st.button("🖼️ জেনারেট ইমেজ"):
                st.info("AI ইমেজ জেনারেট হচ্ছে... (ডেমো)")
        
        elif image_option == "আপলোড করুন":
            uploaded_file = st.file_uploader("ছবি আপলোড করুন", type=['jpg', 'png', 'jpeg'])
            if uploaded_file:
                st.image(uploaded_file, caption="আপলোডেড ইমেজ", width=200)
        
        else:
            st.info("স্টক ইমেজ লাইব্রেরি থেকে সিলেক্ট করুন")
        
        # Preview and Submit
        st.markdown("---")
        st.markdown("#### 📊 আনুমানিক পারফরম্যান্স")
        
        estimated_reach = random.randint(200, 1000)
        estimated_engagement = random.randint(40, 300)
        
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

def show_my_campaigns():
    """Show user's active and completed campaigns"""
    st.title("📊 আমার ক্যাম্পেইন")
    
    # Tabs for active and completed campaigns
    tab1, tab2, tab3 = st.tabs(["🚀 সক্রিয় ক্যাম্পেইন", "✅ সম্পন্ন ক্যাম্পেইন", "🖼️ তৈরি করা কন্টেন্ট"])
    
    with tab1:
        if not st.session_state.active_campaigns:
            st.info("📭 আপনার কোনো সক্রিয় ক্যাম্পেইন নেই। ব্র্যান্ড মার্কেটপ্লেস থেকে নতুন ক্যাম্পেইন গ্রহণ করুন।")
        else:
            for campaign in st.session_state.active_campaigns:
                status_color = {
                    'content_pending': '#f59e0b',
                    'posted': '#3b82f6',
                    'under_review': '#8b5cf6'
                }.get(campaign['status'], '#6b7280')
                
                status_text = {
                    'content_pending': 'কন্টেন্ট অপেক্ষমান',
                    'posted': 'পোস্ট করা হয়েছে',
                    'under_review': 'রিভিউ চলছে'
                }.get(campaign['status'], campaign['status'])
                
                st.markdown(f"""
                <div class="brand-card" style="border-left-color: {status_color};">
                    <h3>{BRANDS[campaign['brand']]['logo']} {campaign['brand']} - {campaign['title']}</h3>
                    <p><strong>স্ট্যাটাস:</strong> <span style="color: {status_color};">{status_text}</span></p>
                    <p><strong>গ্রহণ করেছেন:</strong> {campaign['accepted_date']}</p>
                    
                    <div style="display: flex; gap: 20px; margin-top: 15px;">
                        <div>
                            <strong>বর্তমান রিচ:</strong><br>
                            {campaign['current_reach']} / {campaign['target_reach']}
                        </div>
                        <div>
                            <strong>বর্তমান এঙ্গেজমেন্ট:</strong><br>
                            {campaign['current_engagement']} / {campaign['min_engagement']}
                        </div>
                        <div>
                            <strong>আনুমানিক আয়:</strong><br>
                            ৳{campaign['estimated_earning']:.2f}
                        </div>
                    </div>
                    
                    {f'<p><strong>কন্টেন্ট তৈরি করেছেন:</strong> {campaign["created_content"]["created_date"]}</p>' if campaign.get('created_content') else ''}
                    
                    <div style="margin-top: 15px;">
                        <div style="background: #f3f4f6; height: 10px; border-radius: 5px; overflow: hidden;">
                            <div style="
                                background: #10b981; 
                                height: 100%; 
                                width: {min(100, (campaign['current_reach'] / campaign['target_reach']) * 100)}%;
                            "></div>
                        </div>
                        <small>রিচ টার্গেট: {min(100, (campaign['current_reach'] / campaign['target_reach']) * 100):.1f}%</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        if not st.session_state.completed_campaigns:
            st.info("📭 আপনার কোনো সম্পন্ন ক্যাম্পেইন নেই।")
        else:
            total_earned = 0
            for campaign in st.session_state.completed_campaigns:
                total_earned += campaign.get('paid_amount', 0)
                
                st.markdown(f"""
                <div class="brand-card" style="border-left-color: #10b981;">
                    <h3>{BRANDS[campaign['brand']]['logo']} {campaign['brand']} - {campaign['title']}</h3>
                    <p><strong>স্ট্যাটাস:</strong> <span class="status-completed">সম্পন্ন</span></p>
                    <p><strong>প্রাপ্ত পরিমাণ:</strong> ৳{campaign.get('paid_amount', 0)}</p>
                    <p><strong>সম্পন্ন তারিখ:</strong> {campaign.get('completed_date', 'N/A')}</p>
                    
                    <div style="display: flex; gap: 20px; margin-top: 15px;">
                        <div>
                            <strong>চূড়ান্ত রিচ:</strong><br>
                            {campaign.get('final_reach', 0)}
                        </div>
                        <div>
                            <strong>চূড়ান্ত এঙ্গেজমেন্ট:</strong><br>
                            {campaign.get('final_engagement', 0)}
                        </div>
                        <div>
                            <strong>পেমেন্ট স্ট্যাটাস:</strong><br>
                            {campaign.get('payment_status', 'প্রক্রিয়াধীন')}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if total_earned > 0:
                st.markdown(f"""
                <div class="earning-card">
                    <h3>মোট উপার্জন: ৳{total_earned}</h3>
                    <p>সকল সম্পন্ন ক্যাম্পেইন থেকে আপনার মোট আয়</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        if not st.session_state.content_created:
            st.info("📭 আপনি এখনো কোনো কন্টেন্ট তৈরি করেননি।")
        else:
            for content in st.session_state.content_created:
                st.markdown(f"""
                <div class="brand-card">
                    <h3>{BRANDS[content['brand']]['logo']} {content['brand']} - {content['title']}</h3>
                    <p><strong>কন্টেন্ট টাইপ:</strong> {get_content_type_name(content['content_type'])}</p>
                    <p><strong>তৈরির তারিখ:</strong> {content['created_date']}</p>
                    <p><strong>আনুমানিক আয়:</strong> ৳{content.get('estimated_earning', 0):.2f}</p>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 10px; margin-top: 10px;">
                        <p><strong>কন্টেন্ট প্রিভিউ:</strong></p>
                        <p>{content['content'].get('headline', 'N/A')}</p>
                        <p><small>{content['content'].get('body', 'N/A')[:100]}...</small></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def show_earnings():
    """Show earnings and withdrawal section"""
    st.title("💰 আয় ও উত্তোলন")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="earning-card">
            <h2>আপনার ব্যালেন্স</h2>
            <h1>৳{st.session_state.balance}</h1>
            <p>উত্তোলনযোগ্য ব্যালেন্স</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Transaction History
        st.subheader("📋 লেনদেনের হিসাব")
        
        # Mock transaction data
        transactions = [
            {'date': '১০ ডিসেম্বর ২০২৩', 'description': 'প্রাণ ফুডস ক্যাম্পেইন', 'amount': 320, 'type': 'credit'},
            {'date': '৮ ডিসেম্বর ২০২৩', 'description': 'আকিজ গ্রুপ ক্যাম্পেইন', 'amount': 280, 'type': 'credit'},
            {'date': '৫ ডিসেম্বর ২০২৩', 'description': 'উত্তোলন', 'amount': 500, 'type': 'debit'},
            {'date': '১ ডিসেম্বর ২০২৩', 'description': 'ড্যানিশ ডেইরি ক্যাম্পেইন', 'amount': 450, 'type': 'credit'},
        ]
        
        for tx in transactions:
            color = "#10b981" if tx['type'] == 'credit' else "#ef4444"
            symbol = "+" if tx['type'] == 'credit' else "-"
            
            st.markdown(f"""
            <div style="
                padding: 15px;
                border-bottom: 1px solid #e5e7eb;
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div>
                    <strong>{tx['description']}</strong><br>
                    <small>{tx['date']}</small>
                </div>
                <div style="color: {color}; font-weight: bold;">
                    {symbol}৳{tx['amount']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💳 উত্তোলন করুন")
        
        withdrawal_method = st.selectbox(
            "উত্তোলনের মাধ্যম",
            ["বিকাশ", "নগদ", "রকেট", "ব্যাংক ট্রান্সফার"]
        )
        
        withdrawal_amount = st.number_input(
            "উত্তোলনের পরিমাণ",
            min_value=100,
            max_value=st.session_state.balance,
            value=min(500, st.session_state.balance),
            step=100
        )
        
        account_number = st.text_input(f"{withdrawal_method} নম্বর")
        
        if st.button("💰 উত্তোলন রিকোয়েস্ট করুন", use_container_width=True, type="primary"):
            if withdrawal_amount > st.session_state.balance:
                st.error("❌ আপনার ব্যালেন্স পর্যাপ্ত নয়")
            elif not account_number:
                st.error("❌ অ্যাকাউন্ট নম্বর দিন")
            else:
                st.session_state.balance -= withdrawal_amount
                st.success(f"✅ {withdrawal_amount} টাকা উত্তোলনের রিকোয়েস্ট গ্রহণ করা হয়েছে")
                st.info(f"💰 আপনার নতুন ব্যালেন্স: ৳{st.session_state.balance}")
                st.rerun()
        
        st.markdown("---")
        
        st.subheader("📊 উপার্জনের পরিসংখ্যান")
        
        total_campaigns = len(st.session_state.completed_campaigns) + len(st.session_state.active_campaigns)
        success_rate = (len(st.session_state.completed_campaigns) / total_campaigns * 100) if total_campaigns > 0 else 0
        
        st.metric("মোট ক্যাম্পেইন", total_campaigns)
        st.metric("সফলতার হার", f"{success_rate:.1f}%")
        st.metric("গড় আয় প্রতি ক্যাম্পেইন", f"৳{st.session_state.balance / total_campaigns:.2f}" if total_campaigns > 0 else "৳0")

def main():
    """Main application function"""
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
    """Show main dashboard"""
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
                   
