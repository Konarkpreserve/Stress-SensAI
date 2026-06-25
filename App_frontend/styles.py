def load_css():

    return """
<style>

/* ============================================
BACKGROUND
============================================ */

.stApp{

    background:linear-gradient(
        135deg,
        #f5f7f6,
        #eef7ff
    );

}

/* ============================================
HEADINGS
============================================ */

h1,h2,h3,h4,h5,h6{

    color:#1f2937;

    font-family:'Segoe UI',sans-serif;

}

p,span,label{

    color:#374151;

    font-family:'Segoe UI',sans-serif;

}

/* =========
MAIN
========= */

.main{

animation:fadein .5s ease;

}

@keyframes fadein{

from{

opacity:0;

transform:translateY(10px);

}

to{

opacity:1;

transform:none;

}

}


/* ===========================================
HERO CARD
=========================================== */

.hero-card{

background:linear-gradient(
135deg,
#60A5FA,
#86EFAC
);

padding:35px;

border-radius:28px;

box-shadow:0 18px 45px rgba(0,0,0,.12);

margin-bottom:25px;

color:white;

transition:.25s;

}

.hero-card:hover{

transform:translateY(-3px);

}

/* ============================================
LOGIN CARD
============================================ */

.login-card{

    background:white;

    border-radius:24px;

    padding:40px;

    box-shadow:0 14px 40px rgba(0,0,0,.10);

    border:1px solid #E5E7EB;

}

.login-title{

    text-align:center;

    font-size:34px;

    font-weight:700;

}

.login-subtitle{

    text-align:center;

    color:#6B7280;

    margin-top:5px;

    margin-bottom:30px;

    font-size:17px;

}

/* ============================================
METRIC CARD
============================================ */

.metric-card{

    background:white;

    border-radius:20px;

    padding:24px;

    box-shadow:0 10px 25px rgba(0,0,0,.07);

    transition:.25s;

    border:1px solid #E5E7EB;

}

.metric-card:hover{

    transform:translateY(-5px);

    box-shadow:0 15px 35px rgba(0,0,0,.10);

}

/* ============================================
BLUE CARD
============================================ */

.metric-card-blue{

    background:linear-gradient(

        135deg,

        #E0F2FE,

        #DBEAFE

    );

    border-radius:20px;

    padding:24px;

    box-shadow:0 10px 25px rgba(0,0,0,.08);

    transition:.25s;

}

.metric-card-blue:hover{

    transform:translateY(-5px);

}

/* ============================================
GREEN CARD
============================================ */

.metric-card-green{

    background:linear-gradient(

        135deg,

        #ECFDF5,

        #D1FAE5

    );

    border-radius:20px;

    padding:24px;

    box-shadow:0 10px 25px rgba(0,0,0,.08);

}

/* ============================================
RECOMMENDATION
============================================ */

.recommend-card{

    background:white;

    border-left:8px solid #3B82F6;

    border-radius:18px;

    padding:25px;

    box-shadow:0 8px 20px rgba(0,0,0,.07);

}

/* ============================================
ACTION CARD
============================================ */

.action-card{

    background:white;

    border-left:8px solid #22C55E;

    border-radius:18px;

    padding:22px;

    box-shadow:0 8px 18px rgba(0,0,0,.06);

    margin-bottom:16px;

}

/* ============================================
WELLNESS CARD
============================================ */

.wellness-card{
    background:linear-gradient(
        135deg,
        #ECFEFF,
        #ECFDF5
    );
    border-radius:22px;
    padding:30px;
    text-align:center;
    box-shadow:0 10px 22px rgba(0,0,0,.08);
}

.metric-card,
.metric-card-blue,
.metric-card-green,
.wellness-card,
.recommend-card,
.action-card{

transition:.3s ease;

}

.metric-card:hover,
.metric-card-blue:hover,
.metric-card-green:hover,
.wellness-card:hover,
.recommend-card:hover,
.action-card:hover{

transform:translateY(-6px);

box-shadow:0 20px 40px rgba(0,0,0,.12);

}

.metric-card h4,
.metric-card-blue h4,
.metric-card-green h4{

margin-bottom:12px;

font-weight:700;

}

/* ============================================
SIDEBAR
============================================ */

[data-testid="stSidebar"]{

    background:#ECFDF5;
    padding-top:25px;

    border-right:1px solid #D1FAE5;

}

[data-testid="stSidebar"] *{

    color:#111827;

}

[data-testid="stAlert"]{

border-radius:18px;

}

/* ======
TABLE
======== */

thead tr th{

background:#E0F2FE !important;

color:#111827 !important;

font-weight:700;

}

/* ============================================
BUTTON
============================================ */

.stButton>button{

    width:100%;

    height:52px;

    border:none;

    border-radius:14px;

    background:linear-gradient(

        90deg,

        #60A5FA,

        #86EFAC

    );

    color:#1F2937;

    font-size:16px;

    font-weight:700;

    transition:.25s;

}

.stButton>button:hover{

    transform:translateY(-2px);

    box-shadow:0 10px 20px rgba(0,0,0,.10);

}

/* ============================================
DOWNLOAD BUTTON
============================================ */

.stDownloadButton>button{

    width:100%;

    height:52px;

    border:none;

    border-radius:14px;

    background:linear-gradient(

        90deg,

        #60A5FA,

        #86EFAC

    );

    color:#1F2937;

    font-weight:700;

    transition:.25s;

}

.stDownloadButton>button:hover{

    transform:translateY(-2px);

}

/* ============================================
TEXT INPUT
============================================ */

.stTextInput input{

    border-radius:12px;

    border:1px solid #CBD5E1;

    height:46px;

}

/* ============================================
NUMBER INPUT
============================================ */

.stNumberInput input{

    border-radius:12px;

}

/* ============================================
SELECT BOX
============================================ */

.stSelectbox div[data-baseweb="select"]{

    border-radius:12px;

}

/* ============================================
DATAFRAME
============================================ */

[data-testid="stDataFrame"]{

    border-radius:18px;

    overflow:hidden;

    border:1px solid #E5E7EB;

}

/* ============================================
METRICS
============================================ */

[data-testid="metric-container"]{

    background:white;

    padding:18px;

    border-radius:18px;

    box-shadow:0 8px 18px rgba(0,0,0,.06);

}

/* ============================================
PROGRESS BAR
============================================ */

.stProgress>div>div{

    background:#3B82F6;

}

/* ============================================
EXPANDER
============================================ */

.streamlit-expanderHeader{

    font-weight:700;

}

/* ============================================
SLIDER
============================================ */

.stSlider{

    padding-top:10px;

}

/* ============================================
SUCCESS
============================================ */

div[data-baseweb="notification"]{

    border-radius:14px;

}

/* ============================================
SCROLLBAR
============================================ */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-thumb{

    background:#CBD5E1;

    border-radius:20px;

}

/* ============================================
DIVIDER
============================================ */

hr{

    border:none;

    border-top:1px solid #E5E7EB;

}

/* ============================================
SIDEBAR Z INDEX
============================================ */

div[data-baseweb="select"]{

    z-index:9999 !important;

}

div[data-baseweb="popover"]{

    z-index:9999 !important;

}

section[data-testid="stSidebar"]{

    z-index:10000 !important;

}

section[data-testid="stSidebar"] *{

    z-index:10000 !important;

}

</style>
"""