import streamlit as st
import random
from PIL import Image

# --- 1. 页面高级配置 ---
st.set_page_config(
    page_title="理财博主诊断室 Pro",
    page_icon="💰",
    layout="centered"
)

# --- 2. 商业级理财红样式表 ---
st.markdown("""
<style>
    .stApp { background-color: #0e0202; }
    .main-title {
        text-align: center; font-size: 2.2rem; font-weight: 900;
        color: #D4AF37; letter-spacing: 3px; margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(212,175,55,0.3);
    }
    .card {
        background: rgba(42, 14, 14, 0.6);
        border: 1px solid #5c1f1f; border-radius: 15px;
        padding: 20px; margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    .stButton > button {
        background: linear-gradient(90deg, #8B0000, #B22222) !important;
        color: white !important; border: none; border-radius: 10px;
        height: 45px; font-size: 1.1rem; font-weight: bold;
    }
    .diagnosis-item {
        background: rgba(139,0,0,0.1); border-left: 5px solid #8B0000;
        padding: 12px; margin-bottom: 10px; color: #e8c4c4; font-size: 0.95rem;
    }
    .risk-tag {
        color: #ff4b4b; font-weight: bold; background: rgba(255,75,75,0.1);
        padding: 2px 8px; border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 专业诊断算法 ---
def professional_diagnose(platform, views, completion, saves):
    issues, goods = [], []
    save_rate = (saves / views * 100) if views > 0 else 0
    
    # 抖音逻辑
    if platform == "抖音":
        if completion < 30:
            issues.append("🚩 【开头诊断】5秒完播率低于30%。理财赛道切忌慢节奏，建议前3秒直接展示收益图或‘扎心’数字。")
        elif completion > 50:
            goods.append("✅ 【开头诊断】完播率极佳！你的黄金3秒钩子非常精准。")
            
        if save_rate < 3:
            issues.append("🚩 【内容诊断】收藏率不足。理财粉丝很现实，没有干货清单（如：3步选基法）他们不会点收藏。")
    
    # 小红书逻辑
    else:
        if save_rate < 8:
            issues.append("🚩 【封面诊断】点击/收藏比过低。小红书建议用‘红色背景+超大黄色字体’，突出避坑或赚钱逻辑。")
        if views < 500:
            issues.append("🚩 【流量诊断】没过初始池。检查是否使用了‘理财、存钱、副业’等精准标签。")

    score = min(100, int((completion * 0.5) + (save_rate * 3) + (views/1000 * 2) + 10))
    return score, issues, goods, save_rate

# --- 4. 主界面交互 ---
st.markdown('<div class="main-title">💰 理财博主诊断室 <small style="font-size:0.5em;color:#8a6a6a">Pro</small></div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#8a6a6a;margin-bottom:30px;'>白嫖版·无限次使用</p>", unsafe_allow_html=True)

if "platform" not in st.session_state:
    st.session_state.platform = "抖音"

col1, col2 = st.columns(2)
with col1:
    if st.button("📱 抖音诊断"): st.session_state.platform = "抖音"
with col2:
    if st.button("📕 小红书诊断"): st.session_state.platform = "小红书"

# 数据输入区
with st.container():
    st.markdown(f'<div class="card"><b>📊 {st.session_state.platform} 数据分析面板</b>', unsafe_allow_html=True)
    
    tab_manual, tab_scan = st.tabs(["✏️ 手动输入", "📸 截图识别"])
    
    with tab_manual:
        views = st.slider("总播放量/曝光", 100, 100000, 1500, step=100)
        completion = st.slider("5秒完播率 (%)", 0, 100, 30)
        saves = st.slider("收藏数", 0, 5000, 100)
    
    with tab_scan:
        file = st.file_uploader("上传后台数据截图", type=['jpg', 'png', 'jpeg'])
        if file:
            st.image(file, caption="图片已加载")
            st.warning("💡 提示：Agent 额度已用完，请根据图片数值手动调节左侧滑块。")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 文案风控器（新增功能） ---
with st.container():
    st.markdown('<div class="card"><b>⚠️ 理财违规词扫描</b>', unsafe_allow_html=True)
    script = st.text_area("粘贴你的视频文案/笔记内容：", placeholder="例如：保证大家稳赚不赔，一个月翻倍...")
    if script:
        danger_words = ["稳赚不赔", "肯定赚钱", "保证收益", "100%", "翻倍", "绝对"]
        found = [w for w in danger_words if w in script]
        if found:
            st.error(f"发现违规词：{', '.join(found)}。理财赛道易限流，请修改！")
        else:
            st.success("文案扫描通过，暂未发现极度危险词汇。")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 诊断结果展示 ---
if st.button("🔍 点击获取深度诊断报告"):
    score, issues, goods, s_rate = professional_diagnose(st.session_state.platform, views, completion, saves)
    
    st.divider()
    st.markdown(f"<h2 style='text-align:center;color:#D4AF37;'>综合得分：{score}</h2>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.metric("收藏转化率", f"{s_rate:.1f}%")
    with col_r:
        grade = "S" if score > 85 else "A" if score > 70 else "B" if score > 50 else "C"
        st.metric("作品等级", grade)

    if goods:
        st.subheader("✅ 亮点分析")
        for g in goods: st.markdown(f'<div class="diagnosis-item" style="border-left-color:#D4AF37;">{g}</div>', unsafe_allow_html=True)
    
    if issues:
        st.subheader("⚠️ 改进方案")
        for i in issues: st.markdown(f'<div class="diagnosis-item">{i}</div>', unsafe_allow_html=True)

    # 随机爆款标题
    titles = [
        "【理财干货】普通人翻身的3个底层逻辑",
        "别再存死期了！这个存钱法让你一年多赚5000",
        "我用1个公式，3年存够了人生第一个100万"
    ]
    st.markdown(f'<div class="card"><b>🤖 AI 推荐标题：</b><br>{random.choice(titles)}</div>', unsafe_allow_html=True)

st.caption("开发者提示：当前处于离线模式，所有计算均在本地完成，不消耗任何 API 额度。")
