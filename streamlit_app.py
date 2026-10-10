import os
import streamlit as st

from rag import ask_question
from document_manager import build_vector_database


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Evidence-RAG",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "document_name" not in st.session_state:
    st.session_state.document_name = "No document uploaded"

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

if "question" not in st.session_state:
    st.session_state.question = ""

if "answer" not in st.session_state:
    st.session_state.answer = None

if "sources" not in st.session_state:
    st.session_state.sources = []

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

if "processed_file" not in st.session_state:
    st.session_state.processed_file = ""

if "document_info" not in st.session_state:
    st.session_state.document_info = None


# ============================================================
# PROFESSIONAL LINEAR-STYLE THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       DESIGN VARIABLES
       ======================================================== */

    :root {
        --background: #050506;
        --surface: #0a0a0d;
        --surface-light: rgba(255,255,255,0.045);

        --text: #EDEDEF;
        --muted: #8A8F98;
        --subtle: #666B75;

        --blue: #5E6AD2;
        --blue-light: #7B83FF;
        --blue-glow: rgba(94,106,210,0.30);

        --border: rgba(255,255,255,0.08);
        --border-hover: rgba(255,255,255,0.15);
    }


    /* ========================================================
       MAIN BACKGROUND
       ======================================================== */

    .stApp {

        background:
            radial-gradient(
                ellipse at 50% -15%,
                rgba(94,106,210,0.18) 0%,
                rgba(94,106,210,0.06) 30%,
                transparent 60%
            ),
            radial-gradient(
                ellipse at 0% 80%,
                rgba(120,70,180,0.08) 0%,
                transparent 45%
            ),
            #050506 !important;

        color: var(--text) !important;

        min-height: 100vh;

        overflow-x: hidden;
    }


    /* ========================================================
       SUBTLE BACKGROUND GRID
       ======================================================== */

    [data-testid="stAppViewContainer"] {

        background-image:
            linear-gradient(
                rgba(255,255,255,0.015) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(255,255,255,0.015) 1px,
                transparent 1px
            );

        background-size: 64px 64px;
    }


    /* ========================================================
       AMBIENT LIGHT
       ======================================================== */

    .stApp::before {

        content: "";

        position: fixed;

        width: 850px;
        height: 600px;

        top: -300px;
        left: 50%;

        transform: translateX(-50%);

        background:
            radial-gradient(
                circle,
                rgba(94,106,210,0.18) 0%,
                rgba(94,106,210,0.06) 35%,
                transparent 70%
            );

        filter: blur(90px);

        pointer-events: none;

        z-index: 0;

        animation: ambientMove 10s ease-in-out infinite;
    }


    @keyframes ambientMove {

        0%,
        100% {
            transform:
                translateX(-50%)
                translateY(0);
        }

        50% {
            transform:
                translateX(-50%)
                translateY(-18px);
        }
    }


    /* ========================================================
       FLOATING STAR FIELD
       ======================================================== */

    .stApp::after {

        content:
            "✦   ·       ✧        ·       ✦
             ·       ✧       ·        ·
             ✧          ·        ✦
             ·     ✦         ·       ✧
             ✦        ·       ✧       ·
             ·       ✧       ·       ✦
             ✧     ·        ✦        ·
             ·        ✦       ·       ✧
             ✦      ·       ✧       ·";

        position: fixed;

        top: 0;
        left: 0;

        width: 100%;
        height: 100%;

        pointer-events: none;

        z-index: 1;

        white-space: pre;

        word-spacing: 45px;

        line-height: 105px;

        font-size: 7px;

        color: rgba(123,131,255,0.30);

        text-shadow:
            0 0 5px rgba(123,131,255,0.40),
            0 0 13px rgba(94,106,210,0.20);

        opacity: 0.65;

        animation:
            starsFloat 18s ease-in-out infinite;
    }


    /* ========================================================
       SECOND STAR LAYER
       ======================================================== */

    [data-testid="stAppViewContainer"]::after {

        content:
            "·       ✧          ·        ✦
             ✦          ·        ✧
             ·        ✦             ·
             ✧       ·       ✦
             ·   ✦          ·       ✧
             ✧          ·       ✦
             ·       ✧        ·";

        position: fixed;

        top: -60px;
        left: 12%;

        width: 100%;
        height: 120%;

        pointer-events: none;

        z-index: 1;

        white-space: pre;

        word-spacing: 65px;

        line-height: 145px;

        font-size: 5px;

        color: rgba(160,168,255,0.20);

        text-shadow:
            0 0 7px rgba(123,131,255,0.30);

        opacity: 0.55;

        animation:
            starsDrift 25s ease-in-out infinite;
    }


    /* ========================================================
       STAR ANIMATION
       ======================================================== */

    @keyframes starsFloat {

        0% {

            transform:
                translateY(0px)
                translateX(0px);

            opacity: 0.45;
        }

        25% {

            transform:
                translateY(-15px)
                translateX(8px);

            opacity: 0.65;
        }

        50% {

            transform:
                translateY(-5px)
                translateX(-8px);

            opacity: 0.50;
        }

        75% {

            transform:
                translateY(-20px)
                translateX(5px);

            opacity: 0.70;
        }

        100% {

            transform:
                translateY(0px)
                translateX(0px);

            opacity: 0.45;
        }
    }


    @keyframes starsDrift {

        0%,
        100% {

            transform:
                translateY(0px)
                translateX(0px);

            opacity: 0.25;
        }

        50% {

            transform:
                translateY(-25px)
                translateX(15px);

            opacity: 0.55;
        }
    }


    /* ========================================================
       MAIN CONTAINER
       ======================================================== */

    .main .block-container {

        max-width: 1120px;

        padding-top: 55px;
        padding-bottom: 100px;

        position: relative;

        z-index: 2;
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    .main .block-container p {

        color: var(--muted) !important;

        line-height: 1.7;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1,
    h2,
    h3,
    h4 {

        font-family:
            Inter,
            "Geist Sans",
            system-ui,
            sans-serif;

        color: var(--text) !important;

        letter-spacing: -0.035em;
    }


    h2 {

        font-size: 29px !important;

        font-weight: 600 !important;
    }


    h3 {

        font-size: 20px !important;

        font-weight: 600 !important;
    }


    /* ========================================================
       HERO LABEL
       ======================================================== */

    .hero-label {

        text-align: center;

        font-family:
            ui-monospace,
            SFMono-Regular,
            Menlo,
            Monaco,
            Consolas,
            monospace;

        font-size: 10px;

        letter-spacing: 0.18em;

        text-transform: uppercase;

        color: #8A8F98;

        margin-bottom: 18px;
    }


    .hero-label span {

        color: var(--blue-light);
    }


    /* ========================================================
       HERO TITLE
       ======================================================== */

    .hero-title {

        text-align: center;

        font-family:
            Inter,
            "Geist Sans",
            system-ui,
            sans-serif;

        font-size: 68px;

        line-height: 1;

        font-weight: 700;

        letter-spacing: -0.055em;

        margin: 0 auto 22px auto;

        background:
            linear-gradient(
                90deg,
                #7B83FF 0%,
                #5E6AD2 25%,
                #A1A7FF 50%,
                #5E6AD2 75%,
                #7B83FF 100%
            );

        background-size: 220% auto;

        -webkit-background-clip: text;

        background-clip: text;

        -webkit-text-fill-color: transparent;

        filter:
            drop-shadow(
                0 0 16px
                rgba(94,106,210,0.35)
            )
            drop-shadow(
                0 0 42px
                rgba(94,106,210,0.12)
            );

        position: relative;

        z-index: 3;

        animation:
            heroFloat 5s ease-in-out infinite,
            heroShimmer 7s linear infinite;
    }


    /* ========================================================
       HERO FLOAT
       ======================================================== */

    @keyframes heroFloat {

        0%,
        100% {
            transform: translateY(0px);
        }

        50% {
            transform: translateY(-8px);
        }
    }


    /* ========================================================
       HERO SHIMMER
       ======================================================== */

    @keyframes heroShimmer {

        0% {
            background-position: 0% center;
        }

        50% {
            background-position: 100% center;
        }

        100% {
            background-position: 0% center;
        }
    }


    /* ========================================================
       HERO DESCRIPTION
       ======================================================== */

    .hero-description {

        max-width: 720px;

        margin: 0 auto 55px auto;

        text-align: center;

        font-size: 17px;

        line-height: 1.7;

        color: #8A8F98 !important;
    }


    /* ========================================================
       SECTION LABEL
       ======================================================== */

    .section-label {

        font-family:
            ui-monospace,
            SFMono-Regular,
            Menlo,
            Monaco,
            Consolas,
            monospace;

        font-size: 10px;

        letter-spacing: 0.16em;

        text-transform: uppercase;

        color: #8A8F98;

        margin-top: 35px;

        margin-bottom: 10px;
    }


    .section-label::before {

        content: "●";

        color: var(--blue);

        margin-right: 8px;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {

        background:
            linear-gradient(
                180deg,
                rgba(255,255,255,0.055),
                rgba(255,255,255,0.025)
            ) !important;

        border:
            1px solid var(--border) !important;

        border-radius: 14px !important;

        padding: 16px !important;

        box-shadow:
            0 0 0 1px rgba(255,255,255,0.015),
            0 10px 40px rgba(0,0,0,0.35) !important;
    }


    [data-testid="stFileUploader"] section {

        background: transparent !important;

        border: none !important;
    }


    [data-testid="stFileUploader"] button {

        background:
            rgba(255,255,255,0.06) !important;

        color: #EDEDEF !important;

        border:
            1px solid rgba(255,255,255,0.10) !important;

        border-radius: 8px !important;
    }


    [data-testid="stFileUploader"] button:hover {

        border-color:
            rgba(94,106,210,0.55) !important;

        background:
            rgba(94,106,210,0.10) !important;
    }


    [data-testid="stFileUploader"] small {

        color: #8A8F98 !important;
    }


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    div[data-testid="stTextInput"] label {

        color: #8A8F98 !important;

        font-family:
            ui-monospace,
            SFMono-Regular,
            Menlo,
            monospace !important;

        font-size: 10px !important;

        letter-spacing: 0.10em !important;

        text-transform: uppercase;
    }


    div[data-testid="stTextInput"] input {

        background:
            rgba(255,255,255,0.045) !important;

        color: #EDEDEF !important;

        border:
            1px solid rgba(255,255,255,0.10) !important;

        border-radius: 9px !important;

        height: 54px !important;

        font-size: 16px !important;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.03),
            0 3px 20px rgba(0,0,0,0.25) !important;
    }


    div[data-testid="stTextInput"] input::placeholder {

        color: #666B75 !important;

        opacity: 1 !important;
    }


    div[data-testid="stTextInput"] input:focus {

        border-color:
            rgba(94,106,210,0.75) !important;

        box-shadow:
            0 0 0 2px
            rgba(94,106,210,0.18),
            0 0 30px
            rgba(94,106,210,0.08) !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {

        min-height: 44px !important;

        border-radius: 8px !important;

        background:
            rgba(255,255,255,0.045) !important;

        color: #EDEDEF !important;

        border:
            1px solid rgba(255,255,255,0.08) !important;

        font-weight: 600 !important;

        transition:
            transform 180ms ease,
            background 180ms ease,
            border-color 180ms ease,
            box-shadow 180ms ease !important;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        background:
            rgba(255,255,255,0.075) !important;

        border-color:
            rgba(255,255,255,0.15) !important;

        box-shadow:
            0 8px 28px rgba(0,0,0,0.35) !important;
    }


    .stButton > button:active {

        transform: scale(0.98);
    }


    /* ========================================================
       PRIMARY BUTTON
       ======================================================== */

    .stButton > button[kind="primary"] {

        background:
            linear-gradient(
                135deg,
                #5E6AD2,
                #6872D9
            ) !important;

        color: #ffffff !important;

        border:
            1px solid
            rgba(120,130,230,0.65) !important;

        box-shadow:
            0 0 0 1px
            rgba(94,106,210,0.35),
            0 5px 18px
            rgba(94,106,210,0.25),
            inset 0 1px 0
            rgba(255,255,255,0.20) !important;
    }


    .stButton > button[kind="primary"]:hover {

        background:
            linear-gradient(
                135deg,
                #6872D9,
                #7780E5
            ) !important;

        box-shadow:
            0 0 0 1px
            rgba(94,106,210,0.50),
            0 10px 32px
            rgba(94,106,210,0.35),
            inset 0 1px 0
            rgba(255,255,255,0.25) !important;
    }


    /* ========================================================
       ALERTS / ANSWER
       ======================================================== */

    [data-testid="stAlert"] {

        background:
            rgba(255,255,255,0.045) !important;

        color: #EDEDEF !important;

        border:
            1px solid rgba(255,255,255,0.08) !important;

        border-radius: 12px !important;

        box-shadow:
            0 8px 35px rgba(0,0,0,0.28) !important;
    }


    [data-testid="stAlert"] p {

        color: #EDEDEF !important;

        line-height: 1.75 !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {

        background:
            rgba(255,255,255,0.035) !important;

        border:
            1px solid rgba(255,255,255,0.07) !important;

        border-radius: 12px !important;

        transition:
            background 180ms ease,
            border-color 180ms ease !important;
    }


    [data-testid="stExpander"]:hover {

        background:
            rgba(255,255,255,0.055) !important;

        border-color:
            rgba(255,255,255,0.13) !important;
    }


    [data-testid="stExpander"] summary {

        color: #EDEDEF !important;
    }


    [data-testid="stExpander"] summary p {

        color: #EDEDEF !important;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {

        background:
            linear-gradient(
                180deg,
                rgba(255,255,255,0.055),
                rgba(255,255,255,0.025)
            ) !important;

        border:
            1px solid rgba(255,255,255,0.07) !important;

        border-radius: 14px !important;

        padding: 20px !important;

        box-shadow:
            0 8px 35px rgba(0,0,0,0.30) !important;
    }


    [data-testid="stMetricLabel"] {

        color: #8A8F98 !important;
    }


    [data-testid="stMetricValue"] {

        color: #6872D9 !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border-color:
            rgba(255,255,255,0.07) !important;

        margin-top: 35px !important;

        margin-bottom: 35px !important;
    }


    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar {
        width: 8px;
    }


    ::-webkit-scrollbar-track {
        background: #050506;
    }


    ::-webkit-scrollbar-thumb {

        background:
            rgba(255,255,255,0.12);

        border-radius: 10px;
    }


    ::-webkit-scrollbar-thumb:hover {

        background:
            rgba(94,106,210,0.50);
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .main .block-container {

            padding-top: 35px;

            padding-left: 18px;

            padding-right: 18px;
        }


        .hero-title {

            font-size: 44px;
        }


        .hero-description {

            font-size: 15px;

            margin-bottom: 40px;
        }
    }


    /* ========================================================
       REDUCED MOTION
       ======================================================== */

    @media (prefers-reduced-motion: reduce) {

        .stApp::before,
        .stApp::after,
        [data-testid="stAppViewContainer"]::after {

            animation: none !important;
        }

        .hero-title {

            animation: none !important;
        }

        .stButton > button {

            transition: none !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-label">
        DOCUMENT INTELLIGENCE
        &nbsp;•&nbsp;
        LOCAL RAG
        &nbsp;•&nbsp;
        <span>EVIDENCE-GROUNDED</span>
    </div>

    <div class="hero-title">
        Evidence-RAG
    </div>

    <div class="hero-description">
        Transform your documents into reliable,
        evidence-grounded answers using local retrieval
        and a local language model.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DOCUMENT SECTION
# ============================================================

st.markdown(
    '<div class="section-label">Document</div>',
    unsafe_allow_html=True
)

st.header("Upload your document")

st.write(
    "Upload a PDF to create a searchable knowledge base."
)


uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"],
    help="Upload the PDF you want to use with Evidence-RAG."
)


# ============================================================
# PROCESS PDF
# ============================================================

if uploaded_file is not None:

    upload_directory = "data/uploads"

    os.makedirs(
        upload_directory,
        exist_ok=True
    )

    pdf_path = os.path.join(
        upload_directory,
        uploaded_file.name
    )


    # Save uploaded document

    with open(
        pdf_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )


    # Process only when a NEW document is uploaded

    if (
        st.session_state.processed_file
        != uploaded_file.name
    ):

        with st.spinner(
            "Processing document and creating embeddings..."
        ):

            try:

                info = build_vector_database(
                    pdf_path
                )

                st.session_state.document_name = (
                    uploaded_file.name
                )

                st.session_state.document_ready = True

                st.session_state.processed_file = (
                    uploaded_file.name
                )

                st.session_state.document_info = info

                st.session_state.answer = None

                st.session_state.sources = []

                st.session_state.evaluation = None

                st.success(
                    "Document processed successfully."
                )

            except Exception as error:

                st.session_state.document_ready = False

                st.error(
                    f"Document processing failed: {error}"
                )


# ============================================================
# CURRENT DOCUMENT
# ============================================================

if st.session_state.document_ready:

    st.markdown(
        f"""
        <div style="
            margin-top:20px;
            padding:14px 18px;
            border-radius:10px;
            background:rgba(34,197,94,0.08);
            border:1px solid rgba(34,197,94,0.20);
            color:#B8F3C7;
            font-size:14px;
        ">
            ◈ &nbsp;
            <b>{st.session_state.document_name}</b>
            &nbsp; • &nbsp;
            Ready
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# QUESTION SECTION
# ============================================================

st.markdown(
    '<div class="section-label">Question</div>',
    unsafe_allow_html=True
)

st.header("Ask your document")

st.write(
    "Ask anything that can be answered from the uploaded document."
)


question = st.text_input(
    "Your question",
    value=st.session_state.question,
    placeholder="Example: What payment methods are supported?"
)


# ============================================================
# QUESTION BUTTONS
# ============================================================

ask_col, clear_col = st.columns([5, 1])


with ask_col:

    ask_button = st.button(
        "🔎 Ask Question",
        type="primary",
        use_container_width=True
    )


with clear_col:

    clear_button = st.button(
        "Clear",
        use_container_width=True
    )


# ============================================================
# CLEAR BUTTON
# ============================================================

if clear_button:

    st.session_state.question = ""

    st.session_state.answer = None

    st.session_state.sources = []

    st.session_state.evaluation = None

    st.rerun()


# ============================================================
# ASK QUESTION
# ============================================================

if ask_button:

    if not st.session_state.document_ready:

        st.warning(
            "Please upload a PDF document first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        st.session_state.question = question

        with st.spinner(
            "Searching the document and generating an evidence-grounded answer..."
        ):

            try:

                result = ask_question(
                    question,
                    top_k=3
                )

                st.session_state.answer = (
                    result.get(
                        "answer",
                        ""
                    )
                )

                st.session_state.sources = (
                    result.get(
                        "sources",
                        []
                    )
                )

            except Exception as error:

                st.error(
                    f"Unable to answer the question: {error}"
                )


# ============================================================
# ANSWER
# ============================================================

if st.session_state.answer:

    st.markdown(
        '<div class="section-label">Answer</div>',
        unsafe_allow_html=True
    )

    st.header("Evidence-Grounded Answer")

    st.markdown(
        f"""
        <div style="
            margin-top:15px;
            padding:24px;
            border-radius:14px;
            background:
                linear-gradient(
                    180deg,
                    rgba(255,255,255,0.055),
                    rgba(255,255,255,0.025)
                );
            border:1px solid rgba(255,255,255,0.08);
            box-shadow:
                0 10px 40px rgba(0,0,0,0.30);
        ">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state.answer
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# RETRIEVED EVIDENCE
# ============================================================

if st.session_state.sources:

    st.markdown(
        '<div class="section-label">Evidence</div>',
        unsafe_allow_html=True
    )

    st.header("Retrieved Evidence")

    st.write(
        "Document sections retrieved and used to generate the answer."
    )


    for index, source in enumerate(
        st.session_state.sources
    ):

        page = source.get(
            "page",
            source.get(
                "page_number",
                "Unknown"
            )
        )

        text = source.get(
            "text",
            ""
        )

        with st.expander(
            f"Source {index + 1} • Page {page}"
        ):

            st.write(text)


# ============================================================
# RETRIEVAL EVALUATION
# ============================================================

st.markdown(
    '<div class="section-label">Evaluation</div>',
    unsafe_allow_html=True
)

st.header("Retrieval Performance")

st.write(
    "Measure how accurately the retrieval system finds relevant document pages."
)


run_evaluation = st.button(
    "Run Retrieval Evaluation"
)


if run_evaluation:

    try:

        from evaluation_report import evaluate

        with st.spinner(
            "Running retrieval evaluation..."
        ):

            metrics = evaluate()

        st.session_state.evaluation = metrics

    except ImportError:

        st.warning(
            "evaluation_report.py is not available."
        )

    except Exception as error:

        st.error(
            f"Evaluation failed: {error}"
        )


# ============================================================
# EVALUATION RESULTS
# ============================================================

if st.session_state.evaluation:

    metrics = st.session_state.evaluation

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Recall@1",
            f"{metrics.get('recall_at_1', 0):.2f}%"
        )


    with col2:

        st.metric(
            "Recall@3",
            f"{metrics.get('recall_at_3', 0):.2f}%"
        )


    with col3:

        st.metric(
            "MRR",
            f"{metrics.get('mrr', 0):.3f}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <hr>

    <div style="
        text-align:center;
        color:#666B75;
        font-size:11px;
        padding:15px 0 30px 0;
    ">
        Evidence-RAG
        &nbsp;•&nbsp;
        Local Retrieval-Augmented Generation
        &nbsp;•&nbsp;
        ChromaDB
        &nbsp;•&nbsp;
        Sentence Transformers
        &nbsp;•&nbsp;
        Llama 3.2 3B
    </div>
    """,
    unsafe_allow_html=True
)