import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Chronos Bazaar - Content Creator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Bangla support
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Hind Siliguri', sans-serif;
    }
    
    .content-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #3b82f6;
    }
    
    .video-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
    }
    
    .ai-badge {
        background: #10b981;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 5px;
    }
    
    .post-preview {
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        padding: 20px;
        background: #f9fafb;
        margin: 15px 0;
    }
    
    .social-media-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }
    
    .bangla-text {
        font-size: 1.1rem;
        line-height: 1.8;
        text-align: right;
    }
    
    .platform-facebook { background: #1877F2; color: white; }
    .platform-instagram { background: #E4405F; color: white; }
    .platform-tiktok { background: #000000; color: white; }
    .platform-youtube { background: #FF0000; color: white; }
</style>
""", unsafe_allow_html=True)

# Initialize session state for content
if 'created_content' not in st.session_state:
    st.session_state.created_content = []
if 'balance' not in st.session_state:
    st.session_state.balance = 2565

def load_templates():
    return {
        'restaurant': {
            'name': 'রেস্টুরেন্ট টেমপ্লেট',
            'colors': ['#FF6B6B', '#4ECDC4', '#FFD166'],
            'fonts': ['Hind Siliguri', 'Kalpurush'],
            'elements': ['food_image', 'price_tag', 'discount_badge']
        },
        'fashion': {
            'name': 'ফ্যাশন বুটিক টেমপ্লেট',
            'colors': ['#FF6B6B', '#118AB2', '#EF476F'],
            'fonts': ['Hind Siliguri', 'Siyam Rupali'],
            'elements': ['model_pose', 'new_arrival', 'price_slash']
        },
        'electronics': {
            'name': 'ইলেকট্রনিক্স দোকান',
            'colors': ['#06D6A0', '#118AB2', '#073B4C'],
            'fonts': ['Hind Siliguri', 'AdorshoLipi'],
            'elements': ['product_3d', 'tech_specs', 'warranty_badge']
        }
    }

def main():
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🎨</h1>", unsafe_allow_html=True)
        st.title("Chronos Bazaar")
        
        menu = st.radio(
            "নেভিগেশন মেনু",
            ["🏠 ড্যাশবোর্ড", "📝 টেক্সট তৈরি", "🖼️ ইমেজ তৈরি", "🎥 ভিডিও তৈরি", "📊 পারফরম্যান্স", "💰 আয়"]
        )
        
        st.markdown("---")
        
        # Quick Stats
        st.subheader("📈 আজকের স্ট্যাটস")
        st.metric("তৈরি কন্টেন্ট", f"{len(st.session_state.created_content)}")
        st.metric("আজকের আয়", "৳225")
        st.metric("ব্যালেন্স", f"৳{st.session_state.balance}")
        
        st.markdown("---")
        
        # Quick Actions
        if st.button("🔄 নতুন আইডিয়া জেনারেট", use_container_width=True):
            st.session_state.generate_idea = True
        
        if st.button("⚡ দ্রুত পোস্ট তৈরি", use_container_width=True):
            st.session_state.quick_post = True

    # Main Content Area
    if menu == "🏠 ড্যাশবোর্ড":
        show_dashboard()
    elif menu == "📝 টেক্সট তৈরি":
        create_text_content()
    elif menu == "🖼️ ইমেজ তৈরি":
        create_image_content()
    elif menu == "🎥 ভিডিও তৈরি":
        create_video_content()
    elif menu == "📊 পারফরম্যান্স":
        show_performance()
    elif menu == "💰 আয়":
        show_earnings()

def show_dashboard():
    st.title("🎯 Chronos Bazaar - AI কন্টেন্ট ক্রিয়েটর")
    
    # Welcome Message
    st.markdown("""
    <div class="content-card">
        <h2>স্বাগতম! আপনার AI কন্টেন্ট এসিস্ট্যান্ট</h2>
        <p class="bangla-text">এক ক্লিকে টেক্সট, ইমেজ এবং ভিডিও কন্টেন্ট তৈরি করুন। শুধু আপনার ব্যবসার ধরন বলুন, বাকিটা আমরা করব!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Create Section
    st.subheader("🚀 দ্রুত শুরু করুন")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 টেক্সট কন্টেন্ট তৈরি", use_container_width=True):
            st.session_state.current_tab = "text"
            st.rerun()
        st.markdown("<p style='text-align: center;'>অটো বাংলা ক্যাপশন, হ্যাশট্যাগ</p>", unsafe_allow_html=True)
    
    with col2:
        if st.button("🖼️ গ্রাফিক্স ডিজাইন তৈরি", use_container_width=True):
            st.session_state.current_tab = "image"
            st.rerun()
        st.markdown("<p style='text-align: center;'>সোশ্যাল মিডিয়া পোস্ট, ব্যানার</p>", unsafe_allow_html=True)
    
    with col3:
        if st.button("🎥 শর্ট ভিডিও তৈরি", use_container_width=True):
            st.session_state.current_tab = "video"
            st.rerun()
        st.markdown("<p style='text-align: center;'>TikTok/Reels, প্রোডাক্ট ডেমো</p>", unsafe_allow_html=True)
    
    # Recent Content
    st.subheader("🔄 সাম্প্রতিক তৈরি কন্টেন্ট")
    
    if st.session_state.created_content:
        for i, content in enumerate(st.session_state.created_content[-3:]):
            with st.expander(f"{i+1}. {content['type'].upper()} - {content.get('business', 'কন্টেন্ট')}"):
                st.write(f"**টাইপ:** {content['type']}")
                st.write(f"**তৈরির সময়:** {content['created_at']}")
                st.write(f"**আয়:** ৳{content['earning']}")
    else:
        st.info("এখনো কোনো কন্টেন্ট তৈরি করা হয়নি। উপরের বাটন ক্লিক করে শুরু করুন!")

def create_text_content():
    st.title("📝 AI টেক্সট কন্টেন্ট জেনারেটর")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        business_type = st.selectbox(
            "আপনার ব্যবসার ধরন",
            ["রেস্টুরেন্ট/ক্যাফে", "ফ্যাশন/কাপড়", "ইলেকট্রনিক্স", "পাঠশালা/টিউশন", "স্বাস্থ্য/বিউটি", "অন্যান্য"]
        )
        
        content_type = st.selectbox(
            "কন্টেন্ট টাইপ",
            ["সোশ্যাল মিডিয়া পোস্ট", "প্রোডাক্ট ডেসক্রিপশন", "গ্রাহক রিভিউ রেসপন্স", 
             "বিশেষ অফার ঘোষণা", "ফেস্টিভ্যাল গ্রিটিং", "কোম্পানি আপডেট"]
        )
        
        tone = st.select_slider(
            "টোন সিলেক্ট করুন",
            options=["অফিশিয়াল", "বন্ধুত্বপূর্ণ", "উত্সাহপূর্ণ", "পেশাদার", "মজাদার"]
        )
        
        keywords = st.text_input("কীওয়ার্ডস (কমা দিয়ে আলাদা করুন)", "বিশেষ অফার, ছাড়, নতুন প্রোডাক্ট")
    
    with col2:
        st.markdown("""
        <div style="background:#f0f9ff; padding:20px; border-radius:10px; margin-top:20px;">
            <h4>⚡ AI সুপারিশ:</h4>
            <p>• ঈদের জন্য বিশেষ পোস্ট</p>
            <p>• গ্রাহকদের সাথে ইন্টারেক্টিভ কন্টেন্ট</p>
            <p>• ভিডিও ক্যাপশন অটো জেনারেট</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Generate Button
    if st.button("🤖 AI দিয়ে কন্টেন্ট জেনারেট করুন", type="primary", use_container_width=True):
        with st.spinner("AI আপনার কন্টেন্ট তৈরি করছে..."):
            # Simulate AI generation
            generated_content = generate_ai_text(business_type, content_type, tone, keywords)
            
            # Display generated content
            st.markdown("### ✅ তৈরি হয়েছে!")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### 📄 জেনারেটেড কন্টেন্ট:")
                st.markdown(f"""
                <div class="post-preview">
                    <h4>{generated_content['headline']}</h4>
                    <p>{generated_content['body']}</p>
                    <p><strong>হ্যাশট্যাগ:</strong> {generated_content['hashtags']}</p>
                    <p><strong>টোন:</strong> {tone}</p>
                    <p><strong>শব্দ সংখ্যা:</strong> {generated_content['word_count']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### 📱 প্ল্যাটফর্ম:")
                platforms = st.multiselect(
                    "শেয়ার করার জন্য",
                    ["Facebook", "Instagram", "TikTok", "WhatsApp", "YouTube"],
                    default=["Facebook", "Instagram"]
                )
                
                if st.button("💾 সেভ করুন", use_container_width=True):
                    content_item = {
                        'type': 'text',
                        'business': business_type,
                        'content': generated_content,
                        'platforms': platforms,
                        'created_at': datetime.now().strftime("%d %b %Y, %I:%M %p"),
                        'earning': 25
                    }
                    st.session_state.created_content.append(content_item)
                    st.session_state.balance += 25
                    st.success(f"✅ কন্টেন্ট সেভ করা হয়েছে! আয় যোগ হয়েছে: ৳25")

def create_image_content():
    st.title("🖼️ AI ইমেজ ডিজাইন জেনারেটর")
    
    # Template Selection
    st.markdown("### ১. টেমপ্লেট সিলেক্ট করুন")
    
    templates = load_templates()
    template_cols = st.columns(3)
    
    selected_template = 'restaurant'  # Default
    
    for i, (key, template) in enumerate(templates.items()):
        with template_cols[i]:
            if st.button(f"🎨 {template['name']}", key=f"template_{key}", use_container_width=True):
                selected_template = key
    
    selected = templates[selected_template]
    
    st.markdown(f"### ২. '{selected['name']}' টেমপ্লেট কাস্টোমাইজ করুন")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text Inputs
        headline = st.text_input("হেডলাইন", "বিশেষ অফার!")
        subheading = st.text_input("সাবহেডিং", "শুধু এই সপ্তাহে")
        offer_text = st.text_input("অফার টেক্সট", "৫০% ছাড়")
        button_text = st.text_input("বাটন টেক্সট", "অর্ডার করুন")
        
        # Upload image
        uploaded_file = st.file_uploader("আপনার প্রোডাক্ট/লোগো ছবি আপলোড করুন", 
                                       type=['png', 'jpg', 'jpeg'])
    
    with col2:
        # Color Customization
        st.markdown("#### 🎨 কালার সেটিংস")
        bg_color = st.color_picker("ব্যাকগ্রাউন্ড কালার", selected['colors'][0])
        text_color = st.color_picker("টেক্সট কালার", "#FFFFFF")
        button_color = st.color_picker("বাটন কালার", selected['colors'][1])
        
        # Font Selection
        font = st.selectbox("ফন্ট সিলেক্ট করুন", selected['fonts'])
    
    st.markdown("---")
    
    # Generate Image Button
    if st.button("🖼️ AI ইমেজ ডিজাইন তৈরি করুন", type="primary", use_container_width=True):
        st.markdown("### 🎨 আপনার ডিজাইন প্রিভিউ")
        
        # Create a mock image design
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Mock design visualization
            st.markdown(f"""
            <div style="
                background: {bg_color};
                border-radius: 15px;
                padding: 30px;
                color: {text_color};
                height: 400px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            ">
                <div>
                    <h1 style="font-size: 2.5rem; margin: 0;">{headline}</h1>
                    <h2 style="font-size: 1.5rem; margin: 10px 0 30px 0;">{subheading}</h2>
                </div>
                
                <div style="
                    background: rgba(255,255,255,0.2);
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                ">
                    <h3 style="font-size: 3rem; margin: 0;">{offer_text}</h3>
                    <p style="font-size: 1.2rem;">সকল প্রোডাক্টে</p>
                </div>
                
                <button style="
                    background: {button_color};
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 50px;
                    font-size: 1.2rem;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 30px;
                ">{button_text}</button>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📱 সোশ্যাল মিডিয়া সাইজ")
            sizes = st.multiselect(
                "সিলেক্ট সাইজ",
                ["Facebook Post (1200×630)", "Instagram Square (1080×1080)", 
                 "Instagram Story (1080×1920)", "Twitter Post (1200×675)"],
                default=["Facebook Post (1200×630)"]
            )
        
        with col3:
            st.markdown("#### 💰 আয়ের সুযোগ")
            earning = 50 if len(sizes) > 1 else 30
            st.metric("এই ডিজাইনের আয়", f"৳{earning}")
            
            if st.button("💾 ডিজাইন সেভ করুন", use_container_width=True):
                content_item = {
                    'type': 'image',
                    'template': selected['name'],
                    'design': {
                        'headline': headline,
                        'subheading': subheading,
                        'offer': offer_text,
                        'colors': [bg_color, text_color, button_color],
                        'font': font
                    },
                    'sizes': sizes,
                    'created_at': datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    'earning': earning
                }
                st.session_state.created_content.append(content_item)
                st.session_state.balance += earning
                st.success(f"✅ ডিজাইন সেভ করা হয়েছে! আয় যোগ হয়েছে: ৳{earning}")

def create_video_content():
    st.title("🎥 AI ভিডিও কন্টেন্ট জেনারেটর")
    
    st.markdown("""
    <div class="video-card">
        <h3>🚀 ১৫ সেকেন্ডের মধ্যে ভিডিও তৈরি করুন</h3>
        <p>AI আপনার স্ক্রিপ্ট লিখবে, ভয়েসওভার তৈরি করবে এবং ভিডিও এডিট করবে!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Video Creation Steps
    steps = st.columns(4)
    steps[0].markdown("### 1️⃣")
    steps[0].markdown("**টপিক সিলেক্ট**")
    steps[1].markdown("### 2️⃣")
    steps[1].markdown("**স্ক্রিপ্ট জেনারেট**")
    steps[2].markdown("### 3️⃣")
    steps[2].markdown("**মিডিয়া অ্যাড**")
    steps[3].markdown("### 4️⃣")
    steps[3].markdown("**ভিডিও রেন্ডার**")
    
    st.markdown("---")
    
    # Video Topic Selection
    topic = st.selectbox(
        "ভিডিও টপিক সিলেক্ট করুন",
        ["প্রোডাক্ট ডেমো", "গ্রাহক টেস্টিমোনিয়াল", "হাউ-টু টিউটোরিয়াল", 
         "বিশেষ অফার", "কোম্পানি স্টোরি", "ইভেন্ট কভারেজ"]
    )
    
    # Video Style
    style = st.selectbox(
        "ভিডিও স্টাইল",
        ["TikTok/Reels Style", "YouTube Shorts", "Instagram Story", 
         "Facebook Video", "Professional Promo"]
    )
    
    # Duration
    duration = st.slider("ভিডিও ডিউরেশন (সেকেন্ড)", 10, 60, 15)
    
    # Media Upload
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📸 ছবি/ভিডিও আপলোড")
        media_files = st.file_uploader(
            "আপলোড করুন (ছবি/ভিডিও)",
            type=['jpg', 'png', 'mp4', 'mov'],
            accept_multiple_files=True
        )
        
        if media_files:
            st.success(f"{len(media_files)} টি ফাইল আপলোড হয়েছে")
    
    with col2:
        st.markdown("#### 🎵 ব্যাকগ্রাউন্ড মিউজিক")
        music_options = ["Upbeat Energetic", "Calm Background", "Trending TikTok", "No Music"]
        music = st.selectbox("মিউজিক সিলেক্ট করুন", music_options)
        
        st.markdown("#### 🗣️ ভয়েসওভার")
        voice = st.selectbox("ভয়েস টাইপ", ["পুরুষ (বাংলা)", "মহিলা (বাংলা)", "ইংরেজি"])
        auto_caption = st.checkbox("অটো বাংলা ক্যাপশন", value=True)
    
    # Generate Video Button
    if st.button("🎬 AI ভিডিও তৈরি করুন", type="primary", use_container_width=True):
        with st.spinner("AI আপনার ভিডিও তৈরি করছে..."):
            # Simulate video processing
            progress_bar = st.progress(0)
            
            for i in range(100):
                progress_bar.progress(i + 1)
            
            st.markdown("### 🎉 আপনার ভিডিও তৈরি হয়েছে!")
            
            # Mock video player
            st.markdown(f"""
            <div style="
                background: #000;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                margin: 20px 0;
            ">
                <div style="
                    width: 100%;
                    height: 400px;
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 2rem;
                ">
                    ▶️ AI Generated Video
                </div>
                <div style="color: white; margin-top: 15px;">
                    <span>⏱️ {duration}s</span>
                    <span style="margin: 0 20px;">🎵 {music}</span>
                    <span>🗣️ {voice}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Video details and earnings
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 ভিডিও ডিটেইলস")
                details = {
                    "টপিক": topic,
                    "স্টাইল": style,
                    "ডিউরেশন": f"{duration} সেকেন্ড",
                    "মিডিয়া ফাইল": len(media_files) if media_files else 0,
                    "ক্যাপশন": "হ্যাঁ" if auto_caption else "না"
                }
                
                for key, value in details.items():
                    st.write(f"**{key}:** {value}")
            
            with col2:
                st.markdown("#### 💰 আয়ের সুযোগ")
                video_earning = 75 + (len(media_files) * 5 if media_files else 0)
                st.metric("এই ভিডিওর আয়", f"৳{video_earning}")
                
                platforms = st.multiselect(
                    "প্ল্যাটফর্ম সিলেক্ট করুন",
                    ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook Video"],
                    default=["TikTok", "Instagram Reels"]
                )
                
                if st.button("💾 ভিডিও সেভ করুন", use_container_width=True):
                    content_item = {
                        'type': 'video',
                        'topic': topic,
                        'style': style,
                        'duration': duration,
                        'platforms': platforms,
                        'created_at': datetime.now().strftime("%d %b %Y, %I:%M %p"),
                        'earning': video_earning
                    }
                    st.session_state.created_content.append(content_item)
                    st.session_state.balance += video_earning
                    st.success(f"✅ ভিডিও সেভ করা হয়েছে! আয় যোগ হয়েছে: ৳{video_earning}")

def generate_ai_text(business_type, content_type, tone, keywords):
    """Generate AI text content based on inputs"""
    templates = {
        "রেস্টুরেন্ট/ক্যাফে": {
            "headline": ["বিশেষ অফার!", "নতুন মেনু আইটেম", "গ্রাহকদের জন্য বিশেষ উপহার"],
            "body": [
                "আমাদের রেস্টুরেন্টে আজ বিশেষ অফার চলছে! সকল আইটেমে ৩০% ছাড়। শুধু আজকের জন্য।",
                "নতুন মেনু আইটেম যোগ করা হয়েছে। আসুন স্বাদ নিয়ে দেখুন!",
                "আজ রাতের ডিনারে বিশেষ উপহার পাবেন। আসুন পরিবার নিয়ে আমাদের রেস্টুরেন্টে।"
            ]
        },
        "ফ্যাশন/কাপড়": {
            "headline": ["নতুন কালেকশন!", "সিজন সেল", "বিশেষ ছাড়"],
            "body": [
                "নতুন কালেকশনের কাপড় এসেছে দোকানে। আজই দেখতে আসুন।",
                "সিজন শেষের সেল চলছে। সকল প্রোডাক্টে ৫০% পর্যন্ত ছাড়।",
                "সপ্তাহব্যাপী বিশেষ অফার। শুধু স্টোর ভিজিটরদের জন্য।"
            ]
        },
        "ইলেকট্রনিক্স": {
            "headline": ["নতুন প্রোডাক্ট লঞ্চ!", "ফ্ল্যাশ সেল", "ওয়ারেন্টি অফার"],
            "body": [
                "নতুন স্মার্টফোন এসেছে। প্রি-অর্ডার শুরু হয়েছে!",
                "ফ্ল্যাশ সেল! শুধু আজ ১০টা থেকে ৫টা পর্যন্ত।",
                "বিশেষ ওয়ারেন্টি অফার সাথে বিনামূল্যে ডেলিভারি।"
            ]
        }
    }
    
    # Get template based on business type
    biz_template = templates.get(business_type, templates["রেস্টুরেন্ট/ক্যাফে"])
    
    # Generate content
    content = {
        'headline': random.choice(biz_template['headline']),
        'body': random.choice(biz_template['body']),
        'hashtags': "#বিশেষঅফার #বাংলাদেশ #দোকান #সেল " + " ".join([f"#{kw.strip()}" for kw in keywords.split(",")[:3]]),
        'word_count': random.randint(50, 150)
    }
    
    return content

def show_performance():
    st.title("📊 কন্টেন্ট পারফরম্যান্স")
    
    if not st.session_state.created_content:
        st.info("এখনো কোনো কন্টেন্ট তৈরি করা হয়নি!")
        return
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_earning = sum([c['earning'] for c in st.session_state.created_content])
    col1.metric("মোট আয়", f"৳{total_earning}")
    col2.metric("মোট কন্টেন্ট", len(st.session_state.created_content))
    
    # Content type distribution
    content_types = {}
    for content in st.session_state.created_content:
        content_types[content['type']] = content_types.get(content['type'], 0) + 1
    
    col3.metric("টেক্সট কন্টেন্ট", content_types.get('text', 0))
    col4.metric("ভিডিও কন্টেন্ট", content_types.get('video', 0))
    
    # Performance chart
    st.markdown("---")
    st.subheader("📈 আয়ের ট্রেন্ড")
    
    # Create sample data for chart
    dates = [(datetime.now() - timedelta(days=i)).strftime('%d %b') for i in range(7, -1, -1)]
    earnings = [random.randint(100, 300) for _ in range(8)]
    
    chart_data = pd.DataFrame({
        'দিন': dates,
        'আয় (৳)': earnings
    })
    
    st.line_chart(chart_data.set_index('দিন'))
    
    # Content list
    st.markdown("---")
    st.subheader("📋 সব কন্টেন্ট")
    
    for i, content in enumerate(st.session_state.created_content):
        with st.expander(f"{i+1}. {content['type'].upper()} - ৳{content['earning']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**বিজনেস:** {content.get('business', content.get('topic', 'N/A'))}")
                st.write(f"**তৈরির সময়:** {content['created_at']}")
                st.write(f"**প্ল্যাটফর্ম:** {', '.join(content.get('platforms', ['N/A']))}")
            with col2:
                st.metric("আয়", f"৳{content['earning']}")

def show_earnings():
    st.title("💰 আপনার আয়ের বিশদ")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="content-card">
            <h2>মোট আয়: ৳{st.session_state.balance}</h2>
            <p>এই মাসে: ৳{st.session_state.balance + 1000}</p>
            <p>গত মাসে: ৳{st.session_state.balance - 500}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Earning breakdown
        st.subheader("📊 আয়ের ব্রেকডাউন")
        
        if st.session_state.created_content:
            earning_data = pd.DataFrame({
                'কন্টেন্ট টাইপ': [c['type'] for c in st.session_state.created_content],
                'আয়': [c['earning'] for c in st.session_state.created_content],
                'তারিখ': [c['created_at'] for c in st.session_state.created_content]
            })
            
            st.dataframe(earning_data, use_container_width=True)
        
        # Withdrawal section
        st.subheader("💸 bKash উত্তোলন")
        
        bkash_number = st.text_input("bKash নম্বর", "01XXXXXXXXX")
        amount = st.number_input("টাকার পরিমাণ", 
                               min_value=100, 
                               max_value=st.session_state.balance,
                               value=min(500, st.session_state.balance))
        
        if st.button("✅ bKash-এ পাঠান", type="primary", use_container_width=True):
            if bkash_number and len(bkash_number) == 11:
                st.session_state.balance -= amount
                st.success(f"✅ ৳{amount} {bkash_number} নম্বরে পাঠানো হয়েছে!")
                st.balloons()
            else:
                st.error("❌ সঠিক bKash নম্বর দিন")
    
    with col2:
        st.subheader("🏆 শীর্ষ উপার্জনকারী")
        
        top_earners = [
            {"name": "রাজু (ঢাকা)", "earning": 15250, "business": "চা দোকান"},
            {"name": "সুমি (চট্টগ্রাম)", "earning": 12750, "business": "কাপড়ের দোকান"},
            {"name": "করিম (সিলেট)", "earning": 11200, "business": "রেস্টুরেন্ট"},
            {"name": "আপনি", "earning": st.session_state.balance, "business": "আপনার দোকান"}
        ]
        
        for earner in top_earners:
            st.markdown(f"""
            <div style="
                background: white;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            ">
                <b>{earner['name']}</b><br>
                <small>{earner['business']}</small><br>
                <b style="color: #10b981;">৳{earner['earning']}</b>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
