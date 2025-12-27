"""CSS styling for the SEO Content Generator application"""

def get_custom_css() -> str:
    """Return custom CSS for the app with dashboard-aligned colors"""
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1 {
        color: #667eea;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #764ba2;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #667eea;
        font-weight: 600;
        margin-top: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Form inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }
    
    /* Cards & Expanders */
    .stExpander {
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        background: white;
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .stMetric label {
        color: #666;
        font-size: 0.9rem;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #f5f5f5;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #666;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(102, 126, 234, 0.1);
        color: #667eea;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    /* Info/Success/Warning/Error boxes */
    .stInfo {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stSuccess {
        background-color: #e8f5e9;
        border-left: 4px solid #4CAF50;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stWarning {
        background-color: #fff3e0;
        border-left: 4px solid #FF9800;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background-color: #ffebee;
        border-left: 4px solid #F44336;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 2px solid #e0e0e0;
        margin: 2rem 0;
    }
    
    /* Column spacing */
    .stColumn {
        padding: 0 1rem;
    }
    
    /* Form */
    .stForm {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Code blocks */
    code {
        background-color: #f5f5f5;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        color: #667eea;
    }
    
    pre {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
        border-left: 4px solid #667eea;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f9f9f9;
    }
    
    /* Balloons animation enhancement */
    .stApp {
        background-color: #fafafa;
    }
    </style>
    """
