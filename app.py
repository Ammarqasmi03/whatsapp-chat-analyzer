import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import preprocessor, helper
import plotly.express as px
import plotly.graph_objects as go
import datetime


import streamlit as st

text_color = st.get_option("theme.textColor")
background = st.get_option("theme.backgroundColor")
secondary_bg = st.get_option("theme.secondaryBackgroundColor")

# 1. Page Configuration & Bootstrap Icons CDN
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">',
    unsafe_allow_html=True
)

# 2. Premium UI Design System CSS (Dark Sidebar + Bright SaaS Main Dashboard Layout)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #F0F2F5 !important;
        color: #111B21 !important;
    }
    
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* ---------------- SIDEBAR DESIGN (DARK MAP FROM IMAGE) ---------------- */
    [data-testid="stSidebar"] {
        background-color: #0B141A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .sidebar-title-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 20px 14px 25px 14px;
    }
    .sidebar-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.2;
    }
    
    /* Elegant Radio Nav Menu overrides to look exactly like standard layout menu tabs */
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] {
        gap: 4px;
        padding: 0 8px;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label {
        background: transparent;
        border: none;
        padding: 12px 16px;
        border-radius: 12px;
        color: #AEBAC1 !important;
        transition: all 0.2s ease;
        font-weight: 500;
        width: 100%;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.04) !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stSidebarUserContent"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: rgba(37, 211, 102, 0.1) !important;
        color: #25D366 !important;
        font-weight: 600;
    }

    /* Sidebar Footer Box component matching uploaded image callout box */
    .sidebar-footer-box {
        background: rgba(255, 255, 255, 0.02);
        border: 1px dashed rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin: 30px 14px 10px 14px;
        text-align: center;
    }
    
    /* ---------------- MAIN DASHBOARD WHITE SAAS CARDS ---------------- */
    .kpi-card {
        background: #FFFFFF;
        padding: 22px 24px;
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.02);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015);
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #667781;
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 700;
        color: #111B21;
    }
    .kpi-icon-wrapper {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
    }
    
    .chart-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.02);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015);
        margin-bottom: 24px;
        font-family: 'Inter', sans-serif;
        width: 100%;
        
        
    }
    .chart-card-title {
        font-size: 1.50rem;
        font-weight: 600;
        color: #111B21;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        text-align: center;
    }
    .chart-placeholder-content {
        height: 260px;
        background: #FAFAFA;
        border: 1px dashed #E9EDEF;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #8696A0;
        font-style: italic;
        font-size: 0.95rem;
    }
    
    .control-card {
        background: #FFFFFF;
        padding: 10px 16px;
        border-radius: 14px;
        border: 1px solid rgba(0, 0, 0, 0.02);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015);
        min-height: 50px;
    }
    .step-number-badge {
        background-color: #25D366;
        color: white;
        border-radius: 50%;
        width: 22px;
        height: 22px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 8px;
    }
    .control-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #111B21;
    }
    .control-subtext {
        font-size: 0.78rem;
        color: #667781;
        margin-left: 30px;
        margin-top: -2px;
    }

    /* Premium Button Look */
    div.stButton > button:first-child {
        background: #25D366;
        color: #FFFFFF;
        border: none;
        padding: 14px 24px;
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        height: 54px;
        box-shadow: 0 4px 14px rgba(37, 211, 102, 0.2);
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background: #20BA5A;
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.3);
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)



# 3. Persistent Session State Memory Controls
if "df" not in st.session_state:
    st.session_state.df = None
if "user_list" not in st.session_state:
    st.session_state.user_list = ["Overall"]
if "analysis_generated" not in st.session_state:
    st.session_state.analysis_generated = False
if "selected_user" not in st.session_state:
    st.session_state.selected_user = "Overall"

# 4. Premium Image Sidebar Navigation Architecture
with st.sidebar:
    st.markdown("""
        <div class="sidebar-title-container">
            <i class="bi bi-whatsapp" style="font-size: 2.2rem; color: #25D366;"></i>
            <div class="sidebar-title">WhatsApp<br><span style="font-weight:400; font-size:1.15rem; color:#AEBAC1;">Chat Analyzer</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Left Side Nav Router Links
    

    menu_selection = option_menu(
        menu_title=None,  
        options=[
        "Dashboard",
        "Users",
        "Messages",
        "Emoji Analysis",
       
        "Timeline",
        "Activity Heatmap",
        "Word Cloud",
        "About"
        ],
        icons=[
           "speedometer2",
           "people-fill",
           "chat-left-text-fill",
           "emoji-smile-fill",
           "bar-chart-line-fill",
           "grid-3x3-gap-fill",
           "cloud-fill",
           
          "info-circle-fill"
        ],
        menu_icon="whatsapp",
        default_index=0,
        styles={
    #     "container": {
    #         "padding": "0!important",
    #         "background-color": "#0f172a"
    #     },
    #     "icon": {
    #         "color": "#25D366",
    #         "font-size": "18px"
    #     },
    #     "nav-link": {
    #         "font-size": "16px",
    #         "text-align": "left",
    #         "margin": "4px",
    #         "--hover-color": "#1f2937",
    #     },
        "nav-link-selected": {
            "background-color": "#25D366",
            "color": "white",
        }
       }
    )
    
    # Custom Sidebar Footer Upload Graphic component mirroring the bottom of your image
    st.markdown("""
        <div class="sidebar-footer-box">
            <i class="bi bi-cloud-arrow-up" style="font-size: 2rem; color: #25D366; display:block; margin-bottom:8px;"></i>
            <span style="color:#FFFFFF; font-weight:500; font-size:0.85rem; display:block;">Upload your WhatsApp chat</span>
            <span style="color:#667781; font-size:0.75rem; display:block; margin-bottom:12px;">.txt file format</span>
        </div>
    """, unsafe_allow_html=True)

# 5. Dashboard Top Header Title
st.markdown("""
    <div style="text-align: center; margin-bottom: 35px;">
        <h1 style="font-weight: 800; font-size: 2.8rem; color: #111B21; margin-bottom: 5px;">
            <i class="bi bi-whatsapp" style="color: #25D366; margin-right: 10px;"></i>WhatsApp Chat Analyzer
        </h1>
        <p style="color: #667781; font-size: 1.1rem; font-weight: 400; margin-top: 0;">
            Analyze your WhatsApp chats and uncover amazing insights 📊
        </p>
    </div>
""", unsafe_allow_html=True)

# 6. Integrated Step-by-Step Control Inputs Cards
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 1.5, 1.2])

with ctrl_col1:
    st.markdown("""
        <div class="control-card">
            <div><span class="step-number-badge">1</span><span class="control-label">Upload Chat</span></div>
            <div class="control-subtext">Upload your .txt file</div>
        </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload .txt file", type=["txt"], label_visibility="collapsed")

# Automatic background stream parsing on file discovery
if uploaded_file is not None and st.session_state.df is None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    # Real pipeline connector line:
    st.session_state.df = preprocessor.preprocess(data)
    
    # Local mock simulation so layout displays structural data immediately
    # import pandas as pd
    # st.session_state.df = pd.DataFrame({'user': ['Ammar', 'Irfan', 'Ali', 'Saad', 'Hamza', 'group_notification']})
    
    raw_users = st.session_state.df['user'].unique().tolist()
    if 'group_notification' in raw_users:
        raw_users.remove('group_notification')
    raw_users.sort()
    st.session_state.user_list = ["Overall"] + raw_users

with ctrl_col2:
    st.markdown("""
        <div class="control-card">
            <div><span class="step-number-badge">2</span><span class="control-label">Select User</span></div>
            <div class="control-subtext">Choose a user to analyze</div>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.selected_user = st.selectbox(
        "Select user", 
        st.session_state.user_list, 
        index=st.session_state.user_list.index(st.session_state.selected_user) if st.session_state.selected_user in st.session_state.user_list else 0,
        label_visibility="collapsed"
    )

with ctrl_col3:
    st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
    if st.button("🚀 Generate Analysis"):
        st.session_state.analysis_generated = True

st.markdown("<br>", unsafe_allow_html=True)

num_messages, num_words, num_emojis, num_links, active_users_df,_,_= helper.get_user_stats(st.session_state.df, st.session_state.selected_user) if st.session_state.analysis_generated and st.session_state.df is not None else (0, 0, 0, 0, pd.DataFrame(),0,0)


# ==========================================
# PAGE VIEW CONFIGURATION ROUTER
# ==========================================
if "Dashboard" in menu_selection:

    # 5-Column High-End Metric Card Grid
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    def render_kpi_card(col, title, value, icon_class, bg_color, icon_color):
        with col:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <span class="kpi-title">{title}</span>
                        <div class="kpi-icon-wrapper" style="background-color: {bg_color}; color: {icon_color};">
                            <i class="{icon_class}"></i>
                        </div>
                    </div>
                    <div>
                        <div class="kpi-value">{value}</div>
                        <div style="margin-top: 6px; font-size: 0.75rem; color: #A0AEC0;">⚡ Active Metrics Stream</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    render_kpi_card(kpi_col1, "Total Messages", f"{num_messages:,}", "bi bi-chat-dots-fill", "rgba(37, 211, 102, 0.12)", "#128C7E")
    render_kpi_card(kpi_col2, "Total Words", f"{num_words:,}", "bi bi-type", "rgba(59, 130, 246, 0.12)", "#3B82F6")
    render_kpi_card(kpi_col3, "Total Emojis", f"{num_emojis:,}", "bi bi-emoji-laughing-fill", "rgba(168, 85, 247, 0.12)", "#A855F7")
    render_kpi_card(kpi_col4, "Total Links", f"{num_links:,}", "bi bi-link-45deg", "rgba(249, 115, 22, 0.12)", "#F97316")
    render_kpi_card(kpi_col5, "Active Users", f"{active_users_df.shape[0]}", "bi bi-people-fill", "rgba(14, 165, 233, 0.12)", "#0EA5E9")

    
    st.markdown("<br><hr style='border-color: rgba(0,0,0,0.05); margin-bottom: 30px;'>", unsafe_allow_html=True)
    
    # Visualization Row 1: Timelines
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown('<div class="chart-card"><div class="chart-card-title"><i class="bi bi-graph-up-arrow" style="color:#25D366;"></i> Monthly Timeline</div>', unsafe_allow_html=True)
        if st.session_state.analysis_generated and st.session_state.df is not None:
            
            monthly_timeline = helper.monthly_year_timeline(st.session_state.df, st.session_state.selected_user)
            
            fig_hour = px.area(monthly_timeline, x='time', y='messages', labels={"time":"Date","messages":"Number of Messages"})
            fig_hour.update_traces(line=dict(color="#1A8930", width=2), fillcolor='rgba(26, 137, 48, 0.3)')
            fig_hour.update_layout(margin=dict(l=0, r=0, t=5, b=0), height=400,
                               xaxis=dict(showgrid=False, color='#667781'), yaxis=dict(showgrid=False, color='#667781'))
            st.plotly_chart(fig_hour, use_container_width=True, config={'displayModeBar': False})
            
            fig,ax = plt.subplots(figsize=(10,10))
            ax.plot(monthly_timeline['time'], monthly_timeline['messages'],color='green')
            plt.xlabel('Date')
            plt.ylabel('Number of Messages')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
   
            

            # fig = px.line(monthly_timeline, x='time', y='messages',labels={'time': 'Date', 'messages': 'Number of Messages'}, color_discrete_sequence=['#25D366'])
            # st.plotly_chart(fig, use_container_width=True)
           # st.markdown(f"""<div class="chart-placeholder-content">{st.pyplot(fig)}</div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="chart-placeholder-content">Awaiting Analysis Generation...</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row1_col2:
        st.markdown('<div class="chart-card"><div class="chart-card-title"><i class="bi bi-bar-chart-fill" style="color:#25D366;"></i> Daily Timeline</div>', unsafe_allow_html=True)
        if st.session_state.analysis_generated and st.session_state.df is not None:
            daily_timeline = helper.daily_year_timeline(st.session_state.df, st.session_state.selected_user)
            
            fig_hour = px.area(daily_timeline, x='only_date', y='messages',labels={"only_date":"Date","messages":"Number of Messages"})
            fig_hour.update_traces(line=dict(color="#C90338", width=2), fillcolor='rgba(201, 3, 56, 1)')
            fig_hour.update_layout(margin=dict(l=0, r=0, t=5, b=0), height=400,
                               xaxis=dict(showgrid=False, color='#667781'), yaxis=dict(showgrid=False, color='#667781'))
            
            st.plotly_chart(fig_hour, use_container_width=True, config={'displayModeBar': False})
            
            fig,ax = plt.subplots(figsize=(10,10.6))
            ax.plot(daily_timeline['only_date'], daily_timeline['messages'],color='red')
            plt.xlabel('Date')
            plt.ylabel('Number of Messages')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            # fig = px.line(daily_timeline, x='only_date', y='messages',labels={'only_date': 'Date', 'messages': 'Number of Messages'})

            # st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown('<div class="chart-placeholder-content">Awaiting Analysis Generation...</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Active User Graph

    st.markdown("<br><hr style='border-color: rgba(0,0,0,0.05); margin-bottom: 30px;'>", unsafe_allow_html=True)
   
    st.markdown('<div class="chart-card"><div class="chart-card-title">👥 Most Active Users</div>', unsafe_allow_html=True)

    if st.session_state.analysis_generated and st.session_state.df is not None:
        # Top 10 users
        top_users = active_users_df.head(10)

        fig = px.bar(top_users, x="user", y="message_count", color="user", text="message_count", labels={"user": "User", "message_count": "Messages Sent"}, color_discrete_sequence=px.colors.qualitative.Set3)
        
        fig.update_layout(
            margin=dict(l=20, r=20, t=60, b=20),
            height=400,
            xaxis=dict(type='category',showgrid=False,color=text_color),
            yaxis=dict(showgrid=False,gridcolor=secondary_bg,color=text_color),
            font=dict(color=text_color),
            showlegend=True
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.markdown('<div class="chart-placeholder-content" style="height:220px;">No Chart Data</div>', unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(0,0,0,0.05); margin-bottom: 30px;'>", unsafe_allow_html=True)


   
     # Create a 2-column layout for Monthly and Weekly Activity
    row_activity_col1, row_activity_col2 = st.columns(2)


    with row_activity_col1:
        st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-calendar3" style="color: #25D366; font-size: 32px; margin-top: 4px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 24px; font-weight: 700; color: #111B21;">Monthly Activity</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Check if analysis has been generated yet
        if st.session_state.analysis_generated and st.session_state.df is not None:
                try:
                    df_month = st.session_state.df['month_name'].value_counts().reset_index()
                    df_month.columns = ['month_name', 'count']
            
           
                    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                    df_month['month_name'] = pd.Categorical(df_month['month_name'], categories=month_order, ordered=True)
                    df_month = df_month.sort_values('month_name')
            
                    fig_weekly = go.Figure()
                    fig_weekly.add_trace(go.Bar(
                    x=df_month['month_name'],
                    y=df_month['count'],
                    marker_color="#4225D3",
                    marker_line=dict(color="#7C128C", width=1),
                    opacity=0.85
                    ))
            
                    fig_weekly.update_layout(
                    
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=350,
                    xaxis=dict(showgrid=False,color=text_color),
                    yaxis=dict(showgrid=False,gridcolor=secondary_bg,color=text_color),
                    font=dict(color=text_color),
                    showlegend=False,
                    bargap=0.3
                    )
            
                    st.plotly_chart(fig_weekly, use_container_width=True, config={'displayModeBar': False})
                
            
                
            
                except Exception as e:
                    st.markdown('<div class="chart-placeholder-content" style="height: 260px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Mapping chart data columns...</div>', unsafe_allow_html=True)
        else:
        # Fallback view when app freshly boots up
            st.markdown('<div class="chart-placeholder-content" style="height: 260px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting Data Generation...</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# COLUMN 2: WEEKLY ACTIVITY CHART CONTAINER
# =====================================================================
    with row_activity_col2:
            st.markdown("""
                 <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-calendar-week" style="color: #25D366; font-size: 32px; margin-top: 4px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 24px; font-weight: 700; color: #111B21;">Weekly Activity</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
            if st.session_state.analysis_generated and st.session_state.df is not None:
                try:
           
                    df_day = st.session_state.df['day_name'].value_counts().reset_index()
                    df_day.columns = ['day_name', 'count']
            
           
                    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    df_day['day_name'] = pd.Categorical(df_day['day_name'], categories=day_order, ordered=True)
                    df_day = df_day.sort_values('day_name')
            
                    fig_weekly = go.Figure()
                    fig_weekly.add_trace(go.Bar(
                    x=df_day['day_name'],
                    y=df_day['count'],
                    marker_color='#25D366',
                    marker_line=dict(color='#128C7E', width=1),
                    opacity=0.85
                    ))
            
                    fig_weekly.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=350,
                    xaxis=dict(showgrid=False, color='#667781'),
                    yaxis=dict(showgrid=False, color='#667781'),
                    bargap=0.3
              )
            
                    st.plotly_chart(fig_weekly, use_container_width=True, config={'displayModeBar': False})
            
                except Exception as e:
                    st.markdown('<div class="chart-placeholder-content" style="height: 260px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Mapping chart data columns...</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="chart-placeholder-content" style="height: 260px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting Data Generation...</div>', unsafe_allow_html=True)
        
            st.markdown("</div>", unsafe_allow_html=True)

    
elif 'Users' in menu_selection:
      
    active_chatter, most_active_today, avg_messages_per_user, quiet_profiles = helper.get_part_user_stats(st.session_state.df, st.session_state.selected_user) if st.session_state.analysis_generated and st.session_state.df is not None else (0, "N/A", 0, 0)

   

# ==========================================
# PAGE HEADER: USER ANALYTICS TITLE
# ==========================================
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h2 style="font-weight: 700; font-size: 2rem; color: #111B21; margin: 0; display: flex; align-items: center; gap: 10px;">
            <i class="bi bi-people-fill" style="color: #25D366;"></i> User Analytics
        </h2>
        <p style="color: #667781; font-size: 0.95rem; margin: 4px 0 0 0;">
            Deep-dive metrics tracking member activity, engagement profiles, and timeline contributions.
        </p>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# ROW 1: 4-COLUMN KPI CARDS MATRIX
# ==========================================
    card1, card2, card3, card4 = st.columns(4)

    def render_user_kpi(col, title, value, icon_class, bg_color, icon_color):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="background: #FFFFFF; padding: 20px; border-radius: 14px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015);">
                <div class="kpi-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span class="kpi-title" style="font-size: 0.8rem; font-weight: 600; color: #667781; text-transform: uppercase;">{title}</span>
                    <div class="kpi-icon-wrapper" style="width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; background-color: {bg_color}; color: {icon_color};">
                        <i class="{icon_class}"></i>
                    </div>
                </div>
                <div class="kpi-value" style="font-size: 1.8rem; font-weight: 700; color: #111B21;">{value}</div>
            </div>
        """, unsafe_allow_html=True)

# Replace these placeholders with your dynamic variables (e.g., len(user_list))
    render_user_kpi(card1, "Active Chatters", active_chatter, "bi bi-person-check-fill", "rgba(37, 211, 102, 0.12)", "#128C7E")
    render_user_kpi(card2, "Most Active Today", most_active_today, "bi bi-lightning-charge-fill", "rgba(249, 115, 22, 0.12)", "#F97316")
    render_user_kpi(card3, "Avg Messages / User", avg_messages_per_user, "bi bi-calculator", "rgba(59, 130, 246, 0.12)", "#3B82F6")
    render_user_kpi(card4, "Quiet Profiles", quiet_profiles, "bi bi-person-dash", "rgba(100, 116, 139, 0.12)", "#64748B")

    st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# ROW 2: SIDE-BY-SIDE CHARTS
# ==========================================
    col1, col2 = st.columns(2)

# Column 1: User Ranking Container
    with col1:
        st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-graph-up-arrow" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
            <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #111B21;">User Timeline</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
        if st.session_state.analysis_generated and st.session_state.df is not None:
             timeline = helper.daily_year_timeline(st.session_state.df, st.session_state.selected_user)

             fig = px.line(
                 timeline, 
                 x='only_date', 
                 y='messages', 
                 labels={'only_date': 'Date', 'messages': 'Number of Messages'},
                 color_discrete_sequence=["#B325D3"]
                 )
             
             fig.update_traces(mode='lines+markers', line=dict(width=1.5), marker=dict(size=4))
             fig.update_layout(
                    margin=dict(l=20, r=20, t=60, b=20),
                    height=400,
                    showlegend=False,
                    xaxis=dict(showgrid=False, color='#667781'),
                    yaxis=dict(showgrid=False, color='#667781')
                )
             
             st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Column 2: User Contribution Container
    with col2:
        st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-pie-chart-fill" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
           <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #111B21;">User Contribution</h3>
        </div>
    </div>""", unsafe_allow_html=True)
    
        if st.session_state.analysis_generated and st.session_state.df is not None:
            user_contribution = active_users_df.head(10)
            

            fig = px.pie (
                user_contribution,
                names="user",
                values="message_count",
                hole=0.30,                  # Makes it a donut chart
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            fig.update_traces(
                    textposition="inside",
                    textinfo="percent",
                    hovertemplate="<b>%{label}</b><br>Messages: %{value}<br>%{percent}"
                )

            fig.update_layout(
            margin=dict(l=20, r=20, t=60, b=20),
            height=400,
            showlegend=False,
            xaxis=dict(showgrid=False, color='#667781'),
            yaxis=dict(showgrid=False, color='#667781')
             ) 

            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# ROW 3: FULL WIDTH USER TIMELINE
# ==========================================
    st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-trophy-fill" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #111B21;">User Ranking(Top-5)</h3>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.analysis_generated and st.session_state.df is not None:
         # Top 5 users
            
            top_users = active_users_df.head(5)

            fig = px.bar(top_users, x="message_count", y="user",orientation='h', color="user", text="message_count", labels={"user": "User", "message_count": "Messages Sent"},color_discrete_sequence=["#25D366", "#128C7E", "#075E54", "#34B7F1", "#25D366"])

            fig.update_layout(
       
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        xaxis=dict(showgrid=True, color='#667781'),
        yaxis=dict(type='category', showgrid=False, color='#111B21') ,# Forces distinct y-axis categories
        showlegend=True
    )

            st.plotly_chart(fig, use_container_width=True,config={'displayModeBar': False})
    else:
        st.markdown('<div class="chart-placeholder-content" style="height:260px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# ROW 4: DATA TABLE SHEET SUMMARY
# ==========================================
    st.markdown("""
<div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
    <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
        <i class="bi bi-table" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
        <div>
            <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #111B21;">User Statistics (Sheet)</h3>
        </div>
    </div>
""", unsafe_allow_html=True)

    if st.session_state.analysis_generated and st.session_state.df is not None:
    # Render clean structural dataframes seamlessly directly within the layout boundary container
       st.dataframe(helper.all_user_stats_summary(st.session_state.df,st.session_state.selected_user), use_container_width=True)
    else:
       st.markdown('<div class="chart-placeholder-content" style="height:180px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)



elif 'Messages' in menu_selection:
    
    num_msg,_,_,_,_,num_media_msg,num_del_msg = helper.get_user_stats(st.session_state.df,st.session_state.selected_user) if st.session_state.analysis_generated and st.session_state.df is not None else (0,0,0,0,0,0,0)

# ==========================================
# PAGE HEADER: MESSAGES SECTION TITLE
# ==========================================
    st.markdown("""
    <div style="margin-bottom: 25px;">
        <h2 style="font-weight: 700; font-size: 2rem; color: #111B21; margin: 0; display: flex; align-items: center; gap: 10px;">
            <i class="bi bi-chat-left-text-fill" style="color: #25D366;"></i> Messages Analytics
        </h2>
        <p style="color: #667781; font-size: 0.95rem; margin: 4px 0 0 0;">
            Granular text diagnostics exploring structural lengths, media rates, and word distributions.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# ROW 1: 4-COLUMN KPI METRIC CARDS
# ==========================================
    msg_card1, msg_card2, msg_card3 = st.columns(3)

    def render_msg_kpi(col, title, value, icon_class, bg_color, icon_color):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="background: #FFFFFF; padding: 10px; border-radius: 14px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015);">
                <div class="kpi-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span class="kpi-title" style="font-size: 0.8rem; font-weight: 600; color: #667781; text-transform: uppercase;">{title}</span>
                    <div class="kpi-icon-wrapper" style="width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; background-color: {bg_color}; color: {icon_color};">
                        <i class="{icon_class}"></i>
                    </div>
                </div>
                <div class="kpi-value" style="font-size: 1.8rem; font-weight: 700; color: #111B21;">{value}</div>
            </div>
        """, unsafe_allow_html=True)

# Replace these metrics with real extracted properties from your helper tools
    render_msg_kpi(msg_card1, "Total Messages",num_msg , "bi bi-chat-square-quote", "rgba(37, 211, 102, 0.12)", "#128C7E")
    render_msg_kpi(msg_card2, "Media Messages", num_media_msg, "bi bi-image-fill", "rgba(168, 85, 247, 0.12)", "#A855F7")
    render_msg_kpi(msg_card3, "Deleted Messages",num_del_msg , "bi bi-trash3-fill", "rgba(239, 68, 68, 0.12)", "#EF4444")

    st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# ROW 2: SIDE-BY-SIDE VISUALIZATIONS
# ==========================================
    col_v1, col_v2 = st.columns(2)

# Column 1: Message Length Distribution Histogram
    with col_v1:
        st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-bar-chart-line-fill" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #111B21;">Message Length Distribution</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
        if st.session_state.analysis_generated and st.session_state.df is not None:
            try:
                len_df = helper.msg_len_distribution(st.session_state.df, st.session_state.selected_user)

                plt.style.use("default")

                fig, ax = plt.subplots(figsize=(11,11))

                sns.histplot(
                    len_df["word_count"],
                    bins=20,
                    kde=True,
                    color="#B625D3",
                    edgecolor="white",
                    linewidth=1,
                    alpha=0.9,
                    ax=ax
                )

                ax.set_xlabel("Words per Message")
                ax.set_ylabel("Frequency")

                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)

                st.pyplot(fig)
                
            except:
                st.markdown('<div class="chart-placeholder-content" style="height:250px;">Error parsing structural metrics</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Column 2: Word Cloud Component Box
    with col_v2:
        st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-cloud-haze2-fill" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #111B21;">Word Cloud</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
        if st.session_state.analysis_generated and st.session_state.df is not None:
             df_wc = helper.create_wordcloud(st.session_state.df,st.session_state.selected_user)
             fig,ax = plt.subplots()
             fig.patch.set_facecolor('none')
             ax.set_facecolor('none')
             ax.imshow(df_wc, interpolation='bilinear')
             ax.axis("off")
             plt.tight_layout(pad=0)
             st.pyplot(fig, clear_figure=True, use_container_width=True)
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# ROW 3: RECURRENT TERMS ANALYSIS
# ==========================================
    col_v3, col_v4 = st.columns(2)

# Column 1: Most Common Words
    with col_v3:
        st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-filter-square-fill" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #111B21;">Most Common Words</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
        if st.session_state.analysis_generated and st.session_state.df is not None:
            most_common_df = helper.most_common_words(st.session_state.df,st.session_state.selected_user)

            fig,ax = plt.subplots(figsize=(10,10))
            ax.barh(most_common_df[0],most_common_df[1])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            st.pyplot(fig)
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Column 2: Most Used Phrases
    with col_v4:
        st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 16px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-chat-left-quote" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #111B21;">Most Used Phrases</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
        if st.session_state.analysis_generated and st.session_state.df is not None:
            phrases_df = helper.most_used_phase(st.session_state.df,st.session_state.selected_user)

            fig = go.Figure()

            # Add the Sticks (Horizontal line segments)
            for i, row in phrases_df.iterrows():
                fig.add_shape(
                    type="line",
                    x0=0, 
                    y0=row['Phrase'],
                    x1=row['Frequency'], 
                    y1=row['Phrase'],
                    line=dict(color="#CBD5E1", width=3) # Clean, sleek slate-colored stick
                )

            # Add the Candy Heads (Scatter dots marking data points)
            fig.add_trace(go.Scatter(
                x=phrases_df['Frequency'],
                y=phrases_df['Phrase'],
                mode='markers+text',
                marker=dict(
                    color="#0EF1F1",       # Core WhatsApp Green
                    size=15,               # Prominent lollipop diameter
                    line=dict(color='#128C7E', width=2) # Distinct darker rim
                ),
                text=phrases_df['Frequency'],
                textposition="top right",
                textfont=dict(size=13, color="#667781"),
                hoverinfo='text+y'
            ))

            # 3. Clean Layout Tuning for the SaaS UI Look
            fig.update_layout(
                margin=dict(l=10, r=40, t=10, b=10),
                height=500,
                showlegend=False,
                xaxis=dict(
                    showgrid=True, 
                    color='#667781',
                    zeroline=True,
                    zerolinecolor='#E9EDEF'
                ),
                yaxis=dict(
                    type='category', 
                    showgrid=False, 
                    color='#111B21',
                    autorange="reversed" # Ensures top values remain structurally superior
                )
            )

            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)





elif 'Emoji Analysis' in menu_selection:

    total_emojis, uniq_emojis , top_emojis, emojis_df = helper.emojis_stats(st.session_state.df,st.session_state.selected_user) if st.session_state.analysis_generated and st.session_state.df is not None else (0, 0, "N/A", pd.DataFrame())

     
    # ==========================================
    # PAGE HEADER: EMOJI ANALYTICS TITLE
    # ==========================================
    st.markdown("""
        <div style="margin-bottom: 30px;">
            <h2 style="font-weight: 700; font-size: 2.2rem; color: #111B21; margin: 0; display: flex; align-items: center; gap: 12px;">
                <i class="bi bi-emoji-laughing-fill" style="color: #25D366;"></i> Emoji Analytics
            </h2>
            <p style="color: #667781; font-size: 1rem; margin: 6px 0 0 0; font-family: 'Inter', sans-serif;">
                Deep-dive emotional diagnostics tracking layout sentiments, distinct distributions, and individual expression profiles.
            </p>
        </div>
    """, unsafe_allow_html=True)


    # ==========================================
    # ROW 1: 4-COLUMN PREMIUM KPI METRIC CARDS
    # ==========================================
    emoji_col1, emoji_col2, emoji_col3 = st.columns(3)

    def render_emoji_kpi(col, title, value, icon_class, bg_color, icon_color):
        with col:
            st.markdown(f"""
                <div class="kpi-card" style="background: #FFFFFF;padding: 10px;border-radius: 18px;border: 1px solid rgba(0, 0, 0, 0.02);box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);transition: transform 0.2s ease, box-shadow 0.2s ease;margin-bottom: 16px;">
                    <div class="kpi-header" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 5px;">
                        <div>
                             <span class="kpi-title" style="font-size: 0.85rem; font-weight: 700; color: #667781; text-transform: uppercase; tracking-caps: 0.05em;">{title}</span>
                        </div>
                        <div class="kpi-icon-wrapper" style="width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; background: {bg_color}; color: {icon_color};">
                            <i class="{icon_class}"></i>
                        </div>
                    </div>
                    <div class="kpi-value" style="font-size: 2.2rem; font-weight: 800; color: #111B21; line-height: 1.1;">{value}</div>
                </div>""", unsafe_allow_html=True)

    # Simulated static values if fresh load / Real connections fetch values dynamically from helper metrics
    render_emoji_kpi(emoji_col1, "Total Emojis", total_emojis, "bi bi-emoji-smile-fill", "linear-gradient(135deg, rgba(37, 211, 102, 0.15) 0%, rgba(18, 140, 126, 0.05) 100%)", "#128C7E")
    render_emoji_kpi(emoji_col2, "Unique Emojis", uniq_emojis, "bi bi-stars", "linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.05) 100%)", "#3B82F6")
    render_emoji_kpi(emoji_col3, "Top Emoji", top_emojis, "bi bi-trophy-fill", "linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6) 0.05%)", "#F50BDA")
    
    st.markdown("<br>", unsafe_allow_html=True)


    # ==========================================
    # ROW 2: VISUALIZATION GRID (EQUAL WIDTH CARDS)
    # ==========================================
    col_v1, col_v2 = st.columns(2)

    # Left Side Panel Container: Donut Distribution Chart
    with col_v1:
        st.markdown("""
        <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02); margin-bottom: 24px;">
            <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 5px;">
                <i class="bi bi-pie-chart-fill" style="color: #25D366; font-size: 30px; margin-top: 2px;"></i>
                <div>
                    <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700; color: #111B21;">Emoji Distribution(Top-5)</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.analysis_generated and st.session_state.df is not None: # Toggle true/false based on system state
            # Realistic Top 5 Emojis Mock Data Frame
            mock_pie = emojis_df.copy().head()
            
            fig_donut = px.pie(
                mock_pie, values='Count', names='Emoji', hole=0.6,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_donut.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
            fig_donut.update_layout(
                margin=dict(l=10, r=10, t=10, b=10), height=500, showlegend=False
            )
            st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:280px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # Right Side Panel Container: Top Emojis Horizontal Colorful Bar Chart
    with col_v2:
        st.markdown("""
        <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02); margin-bottom: 24px;">
            <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 5px;">
                <i class="bi bi-bar-chart-steps" style="color: #25D366; font-size: 30px; margin-top: 2px;"></i>
                <div>
                    <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700; color: #111B21;">Top Emojis(Top-10)</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.analysis_generated and st.session_state.df is not None:
            # Realistic Top 15 Emojis Dataset
            mock_bar = emojis_df.copy().head(10)
            mock_bar = mock_bar.sort_values(by='Count',ascending=True)
            
            fig_bar = px.bar(
                mock_bar, x='Count', y='Emoji', orientation='h', text='Count',
                color='Count', color_continuous_scale=px.colors.sequential.Bluered_r
            )
            fig_bar.update_layout(
                margin=dict(l=10, r=10, t=10, b=10), height=500, coloraxis_showscale=False,
                xaxis=dict(showgrid=True, color='#667781'),
                yaxis=dict(type='category', color='#111B21')
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:280px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================
    # ROW 3: DETAILED TABLE STATS CONTAINER
    # ==========================================
    st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 5px;">
            <i class="bi bi-clipboard-data-fill" style="color: #25D366; font-size: 30px; margin-top: 2px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700; color: #111B21;">Emoji Statistics</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.analysis_generated and st.session_state.df is not None:
        table_data = helper.emojis_stats_summary(st.session_state.df,st.session_state.selected_user)
        styled_df = table_data.style.set_properties(**{
            'background-color': '#FFFFFF',
            'color': '#111B21',
            'border-color': '#F0F2F5',
            'font-size': '14px',
            'padding': '12px 16px'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#F8F9FA'), ('color', '#667781'), ('font-weight', '700'), ('border-bottom', '2px solid #25D366')]},
            {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#FAFAFA')]},
            {'selector': 'tr:hover', 'props': [('background-color', '#F4F6F8')]}
        ]).format({
            "Emoji Count": "{:,}",
            "Emoji / Message": "{:.2f}",
            "Unique Emojis": "{:,}"
        })
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="chart-placeholder-content" style="height:200px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif 'Timeline' in menu_selection:
    
    first_msg , last_msg , peak_day , active_months = helper.time_stats(st.session_state.df,st.session_state.selected_user) if st.session_state.analysis_generated and st.session_state.df is not None else ("No Date", "No Date", "N/A", 0)

    
    # ==========================================
    # PAGE HEADER: TIMELINE TITLE
    # ==========================================
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h2 style="font-weight: 700; font-size: 2.2rem; color: #111B21; margin: 0; display: flex; align-items: center; gap: 12px;">
            <i class="bi bi-calendar3-trend" style="color: #25D366;"></i> Timeline Analytics
        </h2>
        <p style="color: #667781; font-size: 1rem; margin: 6px 0 0 0; font-family: 'Inter', sans-serif;">
            Track conversation velocity, peak communication periods, and message volume changes over time.
        </p>
    </div>
""", unsafe_allow_html=True)

    
    


    # ==========================================
    # SECTION 1: ROW 1 (PREMIUM KPI CARDS)
    # ==========================================
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    def render_timeline_kpi(col, title, value, icon_class, bg_gradient, icon_color):
        with col:
            st.markdown(f"""
                <div style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0,0,0,0.02); box-shadow: 0 10px 30px rgba(0,0,0,0.015);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 5px;">
                        <div>
                            <span style="font-size: 0.85rem; font-weight: 700; color: #667781; text-transform: uppercase;">{title}</span>
                        </div>
                        <div style="width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; background: {bg_gradient}; color: {icon_color};">
                            <i class="{icon_class}"></i>
                        </div>
                    </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #111B21; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{value}</div>
                </div>
            """, unsafe_allow_html=True)

    render_timeline_kpi(kpi_col1, "First Message", first_msg, "bi bi-play-circle-fill", "linear-gradient(135deg, rgba(37, 211, 102, 0.15) 0%, rgba(18, 140, 126, 0.05) 100%)", "#128C7E")
    render_timeline_kpi(kpi_col2, "Last Message",  last_msg, "bi bi-stop-circle-fill", "linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.05) 100%)", "#3B82F6")
    render_timeline_kpi(kpi_col3, "Peak Activity Day",  peak_day, "bi bi-trophy-fill", "linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.05) 100%)", "#F59E0B")
    render_timeline_kpi(kpi_col4, "Active Months", f"{active_months} Months", "bi bi-calendar-check-fill", "linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(147, 51, 234, 0.05) 100%)", "#A855F7")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # SECTION 2: TOP FILTER BAR (CONTROL PANELS)
    # =========================================
     


    st.markdown("""
        <div class="control-card">
            <div><span class="control-label">📈 View Density Type</span></div>
        </div>
    """, unsafe_allow_html=True)
    timeline_type = st.selectbox("Timeline type", ["Monthly", "Daily", "Hourly", "Yearly"], label_visibility="collapsed")

   
    st.markdown("<br>", unsafe_allow_html=True)



    # ==========================================
    # SECTION 3: LARGE MAIN DYNAMIC TIMELINE CHART
    # ==========================================
    st.markdown(f"""
<div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02); margin-bottom: 24px;">
    <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
        <i class="bi bi-activity" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
        <div>
            <h3 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">Dynamic Chronological Stream ({timeline_type} View)</h3>
            <p style="margin: 2px 0 0 0; color: #667781; font-size: 20px;">Real-time timeline analysis</p>
        </div>
    </div>
""", unsafe_allow_html=True)
    if st.session_state.analysis_generated and st.session_state.df is not None: 
    # Generate Dynamic Plots Based on Selected View
        if timeline_type == "Monthly" :
        # Sample Mock Tracking Data
            df_line = helper.monthly_timeline(st.session_state.df, st.session_state.selected_user)
            fig_main = px.line(df_line, x='month_name', y='messages', markers=True)
            fig_main.update_traces(line=dict(color='#25D366', width=3.5), marker=dict(size=8, color='#128C7E'))
    
        elif timeline_type  == "Daily":
         # Sample Mock Tracking Data
            df_line = helper.daily_timeline(st.session_state.df, st.session_state.selected_user)
            fig_main = px.line(df_line, x='Date', y='messages', markers=True)
            fig_main.update_traces(line=dict(color="#D325D3", width=3.5), marker=dict(size=8, color='#128C7E'))

        elif timeline_type == "Hourly":
            df_area =  helper.hourly_timeline(st.session_state.df, st.session_state.selected_user)
            fig_main = px.area(df_area, x='hour', y='messages')
            fig_main.update_traces(line=dict(color="#0F88EC", width=2), fillcolor='rgba(15, 136, 236, 0.15)')

        else: # Yearly
            df_bar =  helper.yearly_timeline(st.session_state.df, st.session_state.selected_user)
            fig_main = px.bar(df_bar, x='year', y='messages', text_auto=True)
            fig_main.update_traces(marker_color="#A2F705", opacity=0.9, marker_line=dict(width=0))

        fig_main.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), height=500,
        xaxis=dict(showgrid=False, color='#667781'),
        yaxis=dict(showgrid=False, color='#667781')
        )
        st.plotly_chart(fig_main, use_container_width=True, config={'displayModeBar': False})

    else:
        st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================
    # SECTION 4: TWO SIDE-BY-SIDE CHARTS (ROW 2)
    # ==========================================
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-calendar-day" style="color: #25D366; font-size: 26px; margin-top: 2px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">Daily Activity</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
        
        if st.session_state.analysis_generated and st.session_state.df is not None:
            df_day = helper.day_activity(st.session_state.df,st.session_state.selected_user)
            fig_day = px.bar(df_day, x='day_name', y='messages')
            fig_day.update_traces(marker_color="#09E6CC")
            fig_day.update_layout( bargap=0.45, margin=dict(l=0, r=0, t=5, b=0), height=400,
                              xaxis=dict(showgrid=False, color="#E9EDEF"), 
                              yaxis=dict(showgrid=True, color="#F9FBFC"))
            st.plotly_chart(fig_day, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with row2_col2:
        st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-clock-history" style="color: #25D366; font-size: 26px; margin-top: 2px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">Hourly Activity</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)
        
        if st.session_state.analysis_generated and st.session_state.df is not None:

            df_hour = helper.hour_activity(st.session_state.df,st.session_state.selected_user)            
            fig_hour_bar = px.bar(df_hour, x='hour', y='messages')
            fig_hour_bar.update_traces(
              marker_color="#B7FC08", 
              marker_line_width=0,
              hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>"
            )
            fig_hour_bar.update_layout(
              margin=dict(l=0, r=0, t=10, b=0), height=400, bargap=0.4,
              xaxis=dict(showgrid=False, color='#667781', title=None),
              yaxis=dict(showgrid=False, color='#667781', title=None)
            )
            st.plotly_chart(fig_hour_bar, use_container_width=True, config={'displayModeBar': False})
        
           
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================
    # SECTION 5: TWO SIDE-BY-SIDE CHARTS (ROW 3)
    # ==========================================
   

    
    st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
            <i class="bi bi-graph-up" style="color: #25D366; font-size: 26px; margin-top: 2px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">User Trends</h3>
                <p style="margin: 2px 0 0 0; color: #667781; font-size: 20px;">Multi-line comparison traces tracking separate active users</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
        
    if st.session_state.analysis_generated and st.session_state.df is not None:
        df_trends =  helper.user_trend(st.session_state.df,st.session_state.selected_user)
        if df_trends is not None and not df_trends.empty:
            df_trends = df_trends.copy()
            if "user" in df_trends.columns:
                df_trends["user"] = df_trends["user"].astype(str)

        # 1. Initialize Figure & Premium Theme Styles
            plt.rcParams['font.family'] = 'sans-serif'
            fig, ax = plt.subplots(figsize=(18,12))
            fig.patch.set_facecolor('none')  # Transparent figure wrappe
            ax.set_facecolor('none')       # Transparent plot area canvas

        # 2. Build Multi-Line Plot via Seaborn
            sns.lineplot(
            data=df_trends,
            x="Period",
            y="Messages",
            hue="user" if "user" in df_trends.columns else None,
            palette="tab10",
            linewidth=2.5,
            marker="o",
            markersize=6,
            markeredgewidth=1,
            markeredgecolor="#FFFFFF",
            ax=ax
            )

        # 3. Structural Ticks & Custom Clean Grid Configuration
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_color('#E9EDEF')

            ax.grid(axis='y', linestyle='-', linewidth=1, color='#F0F2F5', zorder=0)
            ax.set_axisbelow(True)

        # # Label styling
        # ax.set_xlabel("", fontsize=11, color="#667781", labelpad=10)
        # ax.set_ylabel("Message Volume", fontsize=11, color="#667781", labelpad=10)
        # ax.tick_params(colors='#667781', labelsize=10)

        # 4. Horizontal Top Legend Alignment
            if "user" in df_trends.columns:
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(
                handles, labels,
                loc='lower right',
                bbox_to_anchor=(1.0, 1.02),
                ncol=5,
                frameon=False,
                fontsize=10,
                labelcolor="#111B21"
                )

        # Render out chart container safely
            st.pyplot(fig, clear_figure=True)
    else:
        st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================
    # SECTION 6: TIMELINE SUMMARY DATA FRAME SHEET
    # ==========================================
    st.markdown("""
<div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02); margin-bottom: 24px;">
    <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
        <i class="bi bi-journal-text" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
        <div>
            <h3 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">Timeline Summary</h
        </div>
    </div>
""", unsafe_allow_html=True)

    if st.session_state.analysis_generated and st.session_state.df is not None:
    # Generate Structured Report Sheet
        summary_df = helper.year_month_summary(st.session_state.df,st.session_state.selected_user)

        styled_summary = summary_df.style.set_properties(**{
        'background-color': '#FFFFFF', 'color': '#111B21', 'border-color': '#F0F2F5', 'font-size': '14px', 'padding': '12px'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#F8F9FA'), ('color', '#667781'), ('font-weight', '700'), ('border-bottom', '2px solid #25D366')]},
        {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#FAFAFA')]},
        {'selector': 'tr:hover', 'props': [('background-color', '#F4F6F8')]}
    ]).format({
        "Messages": "{:,}", "Avg / Day": "{:.1f}"
    })

        st.dataframe(styled_summary, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(0,0,0,0.05); margin-bottom: 30px;'>", unsafe_allow_html=True)

elif 'Activity Heatmap' in menu_selection:
    st.markdown("""
    <div style="margin-bottom: 30px;">
        <h2 style="font-weight: 700; font-size: 2.2rem; color: #111B21; margin: 0; display: flex; align-items: center; gap: 12px;">
            <i class="bi bi-grid-3x3-gap-fill" style="color: #25D366;"></i> Activity Heatmap
        </h2>
        <p style="color: #667781; font-size: 1rem; margin: 6px 0 0 0; font-family: 'Inter', sans-serif;">
            Visualize peak engagement windows mapped by days of the week and hourly distribution matrices.
        </p>
    </div>
""", unsafe_allow_html=True)

   
    active_hour = helper.most_active_hour(st.session_state.df,st.session_state.selected_user) if st.session_state.analysis_generated and st.session_state.df is not None else ("N/A")
    # ==========================================
    # ROW 1: DUAL SIDE-BY-SIDE GRAPH BAR PROFILES
    # ==========================================
    graph_col1, graph_col2 = st.columns(2)

    with graph_col1:
        st.markdown(f"""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.015); margin-bottom: 16px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 5px;">
            <i class="bi bi-clock-fill" style="color: #128C7E; font-size: 24px;"></i>
            <div>
                <h4 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">Most Active Hour</h4>
                <span class="kpi-value" style="font-size: 2.2rem; font-weight: 800; color: #111B21; line-height: 1.1;">{active_hour}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
        if st.session_state.analysis_generated and st.session_state.df is not None:
    # Mock data for hours surrounding peak times (e.g., afternoon to night)
            df_active_hours = helper.hour_activity(st.session_state.df,st.session_state.selected_user)
            
            fig_hour_bar = px.bar(df_active_hours, x='hour', y='messages')
            fig_hour_bar.update_traces(
              marker_color="#8C1282", 
              marker_line_width=0,
              hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>"
            )
            fig_hour_bar.update_layout(
              margin=dict(l=0, r=0, t=10, b=0), height=400, bargap=0.4,
              xaxis=dict(showgrid=False, color='#667781', title=None),
              yaxis=dict(showgrid=False, color='#667781', title=None)
            )
            st.plotly_chart(fig_hour_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    active_day = helper.most_active_day(st.session_state.df,st.session_state.selected_user) if st.session_state.analysis_generated and st.session_state.df is not None else ("N/A")

    with graph_col2:
        st.markdown(f"""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.015); margin-bottom: 16px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 5px;">
            <i class="bi bi-calendar-heart-fill" style="color: #25D366; font-size: 24px;"></i>
            <div>
                <h4 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">Most Active Day</h4>
                <span class="kpi-value" style="font-size: 2.2rem; font-weight: 800; color: #111B21; line-height: 1.1;">{active_day}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
        
        if st.session_state.analysis_generated and st.session_state.df is not None:
    # Mock data tracking weekly logs
            df_active_days = helper.day_activity(st.session_state.df,st.session_state.selected_user)
    
            fig_day_bar = px.bar(df_active_days, x='day_name', y='messages')
            fig_day_bar.update_traces(
            marker_color='#25D366', 
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Messages: %{y}<extra></extra>"
            )
            fig_day_bar.update_layout(
            margin=dict(l=0, r=0, t=10, b=0), height=400, bargap=0.45,
            xaxis=dict(showgrid=False, color='#667781', title=None),
            yaxis=dict(showgrid=False, color='#667781', title=None)
            )
            st.plotly_chart(fig_day_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ROW 2: HOURLY HEATMAP MATRIX
# ==========================================
    st.markdown("""
<div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02); margin-bottom: 24px;">
    <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px;">
        <i class="bi bi-alarm" style="color: #25D366; font-size: 26px; margin-top: 2px;"></i>
        <div>
            <h3 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #111B21;">Hourly Activity Heatmap</h3>
        </div>
    </div>
""", unsafe_allow_html=True)

# Generate mock data array representing 24 hours
    if st.session_state.analysis_generated and st.session_state.df is not None:
        df_hourly_heat = helper.hourly_activity_heatmap(st.session_state.df,st.session_state.selected_user)

        fig, ax = plt.subplots(figsize=(16,9))

        sns.heatmap(
            df_hourly_heat,
            cmap="crest",
            linewidths=.5,
            annot=True,
            cbar=True,
            ax=ax
        )

        ax.set_title(
    "⏰ Hourly Activity by Month",
    fontsize=16,
    weight="bold"
          )

        ax.set_xlabel("Hour")
        ax.set_ylabel("Month")

        st.pyplot(fig)
    else:
        st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)
  
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# ROW 3: WEEKLY HEATMAP MATRIX
# ==========================================
    st.markdown("""
<div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.02); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);">
    <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 5px; ">
        <i class="bi bi-alarm" style="color: #25D366; font-size: 26px; margin-top: 2px;"></i>
        <div>
            <h3 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #111B21;">Weekly Activity Heatmap</h3>
        </div>
    </div>
""", unsafe_allow_html=True)

# Generate mock 2D data matrix framework representing 7 days x 24 hours
    if st.session_state.analysis_generated and st.session_state.df is not None:
        df_weekly_heat = helper.weekly_activity_heatmap(st.session_state.df,st.session_state.selected_user)

        fig, ax = plt.subplots(figsize=(16,9))

        sns.heatmap(
            df_weekly_heat,
            cmap="viridis",
            linewidths=.5,
            annot=True,
            cbar=True,
            ax=ax
        )

        ax.set_title(
           "🔥 Weekly Activity Heatmap",
           fontsize=16,
           weight="bold"
        )

        ax.set_xlabel("Hour of Day") 
        ax.set_ylabel("Day of Week")

        st.pyplot(fig)
    else:
        st.markdown('<div class="chart-placeholder-content" style="height:250px; background: #FAFAFA; border: 1px dashed #E9EDEF; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #8696A0; font-style: italic;">Awaiting file upload...</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif 'Word Cloud' in menu_selection:
    # ==========================================
    # PAGE HEADER: WORD CLOUD ANALYSIS
    # ==========================================
    st.markdown("""
        <div style="margin-bottom: 30px;">
            <h2 style="font-weight: 700; font-size: 2.2rem; color: #111B21; margin: 0; display: flex; align-items: center; gap: 12px;">
                <i class="bi bi-cloud-text-fill" style="color: #25D366;"></i> Word Cloud Analysis
            </h2>
            <p style="color: #667781; font-size: 1rem; margin: 6px 0 0 0; font-family: 'Inter', sans-serif;">
                Explore vocabulary matrices, search keyword context vectors, and parse high-frequency text distributions.
            </p>
        </div>
    """, unsafe_allow_html=True)


    # ==========================================
    # ROW 1: INTERACTIVE WORD CLOUD CARD
    # ==========================================
    st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.03); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 5px;">
            <i class="bi bi-cloud-haze2-fill" style="color: #25D366; font-size: 32px;"></i>
            <div>
                <h3 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">Interactive Word Cloud</h3>
                <p style="margin: 2px 0 0 0; color: #667781; font-size: 13px;">Visual representation of the most frequently used words in the selected conversation.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Generate or pass your wordcloud figure here. 
    # For demonstration, we integrate a placeholder asset or text layout inside the padded card wrapper.
    if st.session_state.analysis_generated and st.session_state.df is not None:
        df_wc = helper.create_wordcloud(st.session_state.df, st.session_state.selected_user)

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(fig, clear_figure=True, use_container_width=True)
    else:
        st.markdown('<div style="color: #8696A0; font-style: italic;">Awaiting file parsing matrix...</div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


    # ==========================================
    # ROW 2: WORD SEARCH INSIGHTS MATRIX
    # ==========================================
    st.markdown("""
    <div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.03); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
        <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 5px;">
            <i class="bi bi-search" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
            <div>
            <h3 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">Word Search Insights</h3>
            <p style="margin: 2px 0 0 0; color: #667781; font-size: 13px;">Detailed statistics for the searched word.</p>
        </div>
    </div>
""", unsafe_allow_html=True)
# Central dynamic search bar input block
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_word = st.text_input("Search Keyword Entry", placeholder="Type a word to analyze... (e.g., project)", label_visibility="collapsed")
    with search_col2:
        search_btn = st.button("📊 Scan Word Matrix", use_container_width=True)

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

# Metric layout sub-grid configuration
    m_col1, m_col2, m_col3, m_col4, m_col5= st.columns(5)

    def render_search_metric(col, label, value, icon):
        with col:
            st.markdown(f"""
            <div style="background: #FAFAFA; border: 1px solid #E9EDEF; padding: 18px; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;">
                <div>
                    <span style="font-size: 0.78rem; font-weight: 600; color: #667781; text-transform: uppercase; display: block; margin-bottom: 4px;">{label}</span>
                    <span style="font-size: 1.25rem; font-weight: 700; color: #111B21;">{value}</span>
                </div>
                <div style="font-size: 1.3rem; color: #128C7E; padding-left: 10px;"><i class="{icon}"></i></div>
            </div>
        """, unsafe_allow_html=True)

    total_occurance, first_date,last_date,pct_msg,filterd= helper.search_word_stats(st.session_state.df,st.session_state.selected_user,search_word) if st.session_state.analysis_generated and st.session_state.df is not None else (0, "No Date","No Date", "0.0%", pd.DataFrame())

# Mock dynamic data responses
    target = search_word if search_word else None
    if target is not None:
        target = target.lower()
    if search_btn:
        if filterd.empty:
           st.error(f'🔍 No messages found containing the word "{target}".')
           render_search_metric(m_col1, "Search Word", f'{target}', "bi bi-search")
           render_search_metric(m_col2, "Total Occurrences", 0, "bi bi-bar-chart-fill")
           render_search_metric(m_col3, "First Used", "No Date", "bi bi-calendar-event")
           render_search_metric(m_col4, "Last Used", "No Date", "bi bi-clock-history")
           render_search_metric(m_col5, "Pct of Messages", "0.0%", "bi bi-percent")
        else:
            render_search_metric(m_col1, "Search Word", f'{target}', "bi bi-search")
            render_search_metric(m_col2, "Total Occurrences", f'{total_occurance} Uses', "bi bi-bar-chart-fill")
            render_search_metric(m_col3, "First Used", f'{first_date}', "bi bi-calendar-event")
            render_search_metric(m_col4, "Last Used", f'{last_date}', "bi bi-clock-history")
            render_search_metric(m_col5, "Pct of Messages", f'{pct_msg}%', "bi bi-percent")
    else:
        render_search_metric(m_col1, "Search Word", f'{target}', "bi bi-search")
        render_search_metric(m_col2, "Total Occurrences", 0, "bi bi-bar-chart-fill")
        render_search_metric(m_col3, "First Used", "No Date", "bi bi-calendar-event")
        render_search_metric(m_col4, "Last Used", "No Date", "bi bi-clock-history")
        render_search_metric(m_col5, "Pct of Messages", "0.0%", "bi bi-percent")
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# ROW 3: WORD FREQUENCY STATISTICS TABLE
# ==========================================
    st.markdown("""
<div class="chart-card" style="background: #FFFFFF; padding: 10px; border-radius: 18px; border: 1px solid rgba(0, 0, 0, 0.03); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.015); margin-bottom: 24px;">
    <div class="chart-card-title" style="display: flex; align-items: flex-start; gap: 14px; margin-bottom: 5px;">
        <i class="bi bi-clipboard2-data-fill" style="color: #25D366; font-size: 28px; margin-top: 2px;"></i>
        <div>
            <h3 style="margin: 0; font-size: 1.50rem; font-weight: 700; color: #111B21;">Word Frequency Statistics</h3>
        </div>
    </div>
""", unsafe_allow_html=True)

# Constructing structural word metric DataFrame table sheet
    table_word_data = helper.most_common_word_stats(st.session_state.df,st.session_state.selected_user) if st.session_state.analysis_generated and st.session_state.df is not None else (pd.DataFrame())


# Formatting data frame elements safely with custom row styling properties
    styled_word_matrix = table_word_data.style.set_properties(**{
    'background-color': '#FFFFFF',
    'color': '#111B21',
    'border-color': '#F0F2F5',
    'font-size': '14px',
    'padding': '14px 18px'
}).set_table_styles([
    {'selector': 'th', 'props': [('background-color', '#F8F9FA'), ('color', '#667781'), ('font-weight', '700'), ('border-bottom', '2px solid #25D366')]},
    {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#FAFAFA')]},
    {'selector': 'tr:hover', 'props': [('background-color', '#F4F6F8')]}
]).format({
    "Frequency": "{:,}",
    "Percentage": "{:.1f}%",
    "Users": "{:,}",
    "Average per Month": "{:.1f}"
})

    st.dataframe(styled_word_matrix, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:

# ==========================================
# PAGE CONFIG & PREMIUM BRANDING STYLES
# ==========================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700&display=swap');
    
    /* Global Overrides */
    .about-body {
        font-family: 'Inter', sans-serif;
        color: #111B21;
    }
    
    /* Card Container Base Styling */
    .saas-card {
        background: #FFFFFF;
        padding: 28px;
        border-radius: 18px;
        border: 1px solid rgba(0, 0, 0, 0.03);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.015);
        margin-bottom: 24px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .saas-card:hover {
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.03);
    }
    
    /* Header Typography */
    .card-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.3rem;
        color: #111B21;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .card-subtitle {
        color: #667781;
        font-size: 0.85rem;
        margin: 4px 0 20px 0;
    }
    
    /* Tech Badges */
    .tech-badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        background: #FAFAFA;
        border: 1px solid #E9EDEF;
        color: #111B21;
    }
    
    /* Info Row Items */
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #F0F2F5;
        font-size: 0.9rem;
    }
    .info-row:last-child {
        border-bottom: none;
    }
    .info-label {
        color: #667781;
        font-weight: 500;
    }
    .info-value {
        color: #111B21;
        font-weight: 600;
    }
    
    /* Social Anchor Buttons */
    .social-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 10px;
        font-size: 0.85rem;
        text-decoration: none;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        background: #FAFAFA;
        color: #111B21;
        border: 1px solid #E9EDEF;
        transition: all 0.2s ease;
    }
    .social-btn:hover {
        background: #25D366;
        color: #FFFFFF;
        border-color: #25D366;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# APP HEADER
# ==========================================
    header_col1, header_col2 = st.columns([4, 1])

    with header_col1:
        st.markdown("""
        <div style="margin-bottom: 30px;">
            <h2 style="font-weight: 800; font-size: 2.3rem; color: #111B21; margin: 0; display: flex; align-items: center; gap: 14px;">
                <i class="bi bi-info-circle-fill" style="color: #25D366;"></i> About Chat Analyzer
            </h2>
            <p style="color: #667781; font-size: 1.05rem; margin: 8px 0 0 0; font-family: 'Inter', sans-serif; line-height: 1.5;">
                An end-to-end data analytics dashboard that transforms exported WhatsApp chats into meaningful insights using Python, NLP, and interactive visualizations.
            </p>
        </div>
    """, unsafe_allow_html=True)

    with header_col2:
        st.markdown("""
        <div style="display: flex; justify-content: flex-end; align-items: center; height: 100%;">
            <div style="width: 80px; height: 80px; background: rgba(37, 211, 102, 0.1); border-radius: 22px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: #25D366;">
                <i class="bi bi-bar-chart-line-fill"></i>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# ROW 1: TWO EQUAL-WIDTH CARDS
# ==========================================
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("""
        <div class="saas-card", style="min-height: 480px;">
            <h3 class="card-title"><i class="bi bi-info-circle-fill" style="color: #25D366;"></i> Project Information</h3>
            <p class="card-subtitle">Architecture structural release and profile logs</p>
            <div class="info-row"><span class="info-label">Project Name</span><span class="info-value">WhatsApp Chat Analyzer</span></div>
            <div class="info-row"><span class="info-label">Version</span><span class="info-value">v1.0</span></div>
            <div class="info-row"><span class="info-label">Release Year</span><span class="info-value">2026</span></div>
            <div class="info-row"><span class="info-label">Category</span><span class="info-value">Data Analytics & NLP</span></div>
            <div class="info-row"><span class="info-label">License</span><span class="info-value">MIT License</span></div>
            <div class="info-row"><span class="info-label">Status</span><span class="info-value" style="color:#25D366; background:rgba(37,211,102,0.1); padding:2px 8px; border-radius:12px; font-size:0.8rem;">Production Ready</span></div>
        </div>
    """, unsafe_allow_html=True)

    with row1_col2:
        st.markdown("""
        <div class="saas-card", style="min-height: 480px;">
            <h3 class="card-title"><i class="bi bi-person-circle" style="color: #25D366;"></i> Developer</h3>
            <p class="card-subtitle">Maintainer and engineering lead profiles</p>
            <div style="display: flex; gap: 16px; align-items: center; margin-bottom: 16px;">
                <div style="width: 64px; height: 64px; background: #25D366; color:#FFFFFF; border-radius: 50%; display:flex; align-items:center; justify-content:center; font-size:1.8rem; font-weight:700; box-shadow: 0 4px 12px rgba(37,211,102,0.2);">
                    AG
                </div>
                <div>
                    <h4 style="margin:0; font-size:1.15rem; font-weight:700; color:#111B21;">Ammar Gour</h4>
                    <span style="font-size:0.82rem; color:#667781; font-weight:500;">AI & Machine Learning Enthusiast</span>
                </div>
            </div>
            <p style="font-size: 0.85rem; color:#667781; margin:0 0 12px 0; line-height:1.5;">
                <b>Education:</b> Master of Computer Applications (MCA)<br>
                <b>Specialization:</b> Machine Learning • Data Science • NLP
            </p>
            <p style="font-size: 0.85rem; color:#667781; margin:0 0 20px 0; line-height:1.5; font-style:italic;">
                "Passionate about building AI-powered applications, data visualization dashboards, and end-to-end machine learning projects using Python and modern analytics tools."
            </p>
            <div>
                <a href="https://ammarqasmi03.github.io/my-portfilio/" class="social-btn"><i class="bi bi-globe"></i> Portfolio</a>
                <a href="https://github.com/Ammarqasmi03/whatsapp-chat-analyzer/" class="social-btn"><i class="bi bi-github"></i> GitHub</a>
                <a href="https://www.linkedin.com/in/ammar-qasmi-082266289/" class="social-btn"><i class="bi bi-linkedin"></i> LinkedIn</a>
                <a href="amjadammar786786@gmail.com" class="social-btn"><i class="bi bi-envelope"></i> Email</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
       


# ==========================================
# ROW 2: TECH STACK & DEVELOPER PROFILE
# ==========================================
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("""
        <div class="saas-card" style="min-height: 400px;">
            <h3 class="card-title"><i class="bi bi-cpu-fill" style="color: #25D366;"></i> Tech Stack</h3>
            <p class="card-subtitle">Core frameworks driving data ingestion and visualizations</p>
            <div style="margin-top: 15px;">
                <span class="tech-badge" style="border-left: 3px solid #3776AB;">Python</span>
                <span class="tech-badge" style="border-left: 3px solid #150458;">Pandas</span>
                <span class="tech-badge" style="border-left: 3px solid #013243;">NumPy</span>
                <span class="tech-badge" style="border-left: 3px solid #FF4B4B;">Streamlit</span>
                <span class="tech-badge" style="border-left: 3px solid #111B21;">Regex</span>
                <span class="tech-badge" style="border-left: 3px solid #1F425F;">Matplotlib</span>
                <span class="tech-badge" style="border-left: 3px solid #3776AB;">Plotly</span>
                <span class="tech-badge" style="border-left: 3px solid #4C72B0;">Seaborn</span>
                <span class="tech-badge" style="border-left: 3px solid #F05032;">Sklearn</span>
                <span class="tech-badge" style="border-left: 3px solid #307CA1;">NLTK</span>
                <span class="tech-badge" style="border-left: 3px solid #25D366;">WordCloud</span>
                <span class="tech-badge" style="border-left: 3px solid #FFDE57;">Emoji</span>
                <span class="tech-badge" style="border-left: 3px solid #181717;">GitHub</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    with row2_col2:
        st.markdown("""
        <div class="saas-card" style="min-height: 400px;">
            <h3 class="card-title"><i class="bi bi-stars" style="color: #25D366;"></i> Core Features</h3>
            <p class="card-subtitle">Functional capabilities integrated within this engine</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.88rem; color: #111B21; font-weight: 500;">
                <div><i class="bi bi-check-circle-fill" style="color:#25D366; margin-right:6px;"></i> Interactive Dashboard</div>
                <div><i class="bi bi-check-circle-fill" style="color:#25D366; margin-right:6px;"></i> User Analytics</div>
                <div><i class="bi bi-check-circle-fill" style="color:#25D366; margin-right:6px;"></i> Message Analytics</div>
                <div><i class="bi bi-check-circle-fill" style="color:#25D366; margin-right:6px;"></i> Emoji Analysis</div>
                <div><i class="bi bi-check-circle-fill" style="color:#25D366; margin-right:6px;"></i> Timeline Analysis</div>
                <div><i class="bi bi-check-circle-fill" style="color:#25D366; margin-right:6px;"></i> Activity Heatmaps</div>
                <div><i class="bi bi-check-circle-fill" style="color:#25D366; margin-right:6px;"></i> Word Cloud Engine</div>
                <div><i class="bi bi-check-circle-fill" style="color:#25D366; margin-right:6px;"></i> Search Insights</div>
                <div><i class="bi bi-check-circle-fill" style="color:#25D366; margin-right:6px;"></i> Export Ready Charts</div>
            </div>
        </div>
    """, unsafe_allow_html=True) 


# ==========================================
# ROW 3: PROJECT HIGHLIGHTS (GRADIENT CARDS)
# ==========================================
    st.markdown("""
    <div class="saas-card" style="padding-bottom: 28px;">
        <h3 class="card-title" style="margin-bottom: 4px;"><i class="bi bi-rocket-takeoff-fill" style="color: #25D366;"></i> Project Highlights</h3>
        <p class="card-subtitle" style="margin-bottom: 24px;">Quantitative structural scale and component density metrics</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
            <div style="background: linear-gradient(135deg, rgba(37, 211, 102, 0.12) 0%, rgba(18, 140, 126, 0.04) 100%); padding: 20px; border-radius: 14px; border: 1px solid rgba(37,211,102,0.1); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="display:block; font-size:0.8rem; font-weight:700; color:#667781; text-transform:uppercase;">Python Files</span>
                    <span style="font-size:1.8rem; font-weight:800; color:#111B21;">15+</span>
                </div>
                <div style="font-size:1.6rem; color:#128C7E;"><i class="bi bi-filetype-py"></i></div>
            </div>
            <div style="background: linear-gradient(135deg, rgba(52, 183, 241, 0.12) 0%, rgba(30, 124, 161, 0.04) 100%); padding: 20px; border-radius: 14px; border: 1px solid rgba(52,183,241,0.1); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="display:block; font-size:0.8rem; font-weight:700; color:#667781; text-transform:uppercase;">Visualizations</span>
                    <span style="font-size:1.8rem; font-weight:800; color:#111B21;">20+</span>
                </div>
                <div style="font-size:1.6rem; color:#34B7F1;"><i class="bi bi-pie-chart-fill"></i></div>
            </div>
            <div style="background: linear-gradient(135deg, rgba(168, 85, 247, 0.12) 0%, rgba(147, 51, 234, 0.04) 100%); padding: 20px; border-radius: 14px; border: 1px solid rgba(168,85,247,0.1); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="display:block; font-size:0.8rem; font-weight:700; color:#667781; text-transform:uppercase;">NLP Features</span>
                    <span style="font-size:1.8rem; font-weight:800; color:#111B21;">10+</span>
                </div>
                <div style="font-size:1.6rem; color:#A855F7;"><i class="bi bi-translate"></i></div>
            </div>
            <div style="background: linear-gradient(135deg, rgba(255, 46, 147, 0.12) 0%, rgba(219, 10, 111, 0.04) 100%); padding: 20px; border-radius: 14px; border: 1px solid rgba(255,46,147,0.1); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="display:block; font-size:0.8rem; font-weight:700; color:#667781; text-transform:uppercase;">Dashboard Pages</span>
                    <span style="font-size:1.8rem; font-weight:800; color:#111B21;">8+</span>
                </div>
                <div style="font-size:1.6rem; color:#FF2E93;"><i class="bi bi-layers-half"></i></div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# FOOTER ARCHITECTURE
# ==========================================
    st.markdown("""
    <hr style="border: none; border-top: 1px solid #E9EDEF; margin: 40px 0 20px 0;">
    <div style="text-align: center; font-family: 'Inter', sans-serif; color: #8696A0; font-size: 0.85rem; padding-bottom: 20px;">
        <p style="margin: 0 0 8px 0;">Made with ❤️ using Python & Streamlit</p>
        <p style="margin: 0 0 15px 0; font-weight: 600; color: #667781;">Developed by Ammar Gour</p>
        <div style="display: flex; justify-content: center; gap: 16px; font-size: 1.2rem;">
            <a href="https://ammarqasmi03.github.io/my-portfilio/" style="color: #8696A0; transition: color 0.2s;" onmouseover="this.style.color='#25D366'" onmouseout="this.style.color='#8696A0'"><i class="bi bi-globe"></i></a>
            <a href="https://github.com/Ammarqasmi03/whatsapp-chat-analyzer/" style="color: #8696A0; transition: color 0.2s;" onmouseover="this.style.color='#111B21'" onmouseout="this.style.color='#8696A0'"><i class="bi bi-github"></i></a>
            <a href="https://www.linkedin.com/in/ammar-qasmi-082266289/" style="color: #8696A0; transition: color 0.2s;" onmouseover="this.style.color='#0A66C2'" onmouseout="this.style.color='#8696A0'"><i class="bi bi-linkedin"></i></a>
        </div>
    </div>
""", unsafe_allow_html=True)

# 8. Premium Bottom Quote Banner Footer Section
st.markdown("""
    <div style="background: linear-gradient(90deg, #E9EDEF 0%, #FFFFFF 100%); padding: 16px; border-radius: 12px; text-align: center; margin-top: 10px; border-left: 5px solid #25D366; box-shadow: 0 4px 12px rgba(0,0,0,0.01);">
        <span style="font-style: italic; color: #667781; font-weight: 500;">"Data speaks when words can't. Let's analyze your conversations!"</span>
    </div>
""", unsafe_allow_html=True)



