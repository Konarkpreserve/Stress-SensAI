import streamlit as st

from api import login, register


def initialize_session():

    if "token" not in st.session_state:

        st.session_state["token"] = None


def login_screen():

    st.markdown(
        """
        <div style="
            max-width:520px;
            margin:auto;
            margin-top:70px;
            background:white;
            padding:40px;
            border-radius:25px;
            box-shadow:0 12px 35px rgba(0,0,0,.15);
            border:1px solid #E5E7EB;
        ">
            <h1 style="text-align:center;">
                🧠 Stress SensAI
            </h1>
            <p style="
                text-align:center;
                color:#6B7280;
                font-size:18px;
            ">
                Personalized Stress Intelligence Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if "page" not in st.session_state:
        st.session_state.page = "login"

    if "message" not in st.session_state:
        st.session_state.message = ""

    if "registered_email" not in st.session_state:
        st.session_state.registered_email = ""

    left, center, right = st.columns([1,2,1])

    with center:

        if st.session_state.message:

            st.success(st.session_state.message)

            st.session_state.message = ""

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "🔑 Login",
                use_container_width=True
            ):
                st.session_state.page = "login"
                st.rerun()

        with c2:

            if st.button(
                "📝 Register",
                use_container_width=True
            ):
                st.session_state.page = "register"
                st.rerun()

        st.markdown("---")

        #login form

        if st.session_state.page == "login":

            with st.form("login_form"):

                email = st.text_input(
                    "📧 Email",
                    value=st.session_state.registered_email,
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "🔒 Password",
                    type="password"
                )

                login_btn = st.form_submit_button(
                    "Login",
                    type="primary",
                    use_container_width=True,
                )

            if login_btn:

                response = login(
                    email,
                    password
                )

                try:
                    result = response.json()
                except Exception:
                    result = {}

                if (
                    response.status_code == 200
                    and
                    "access_token" in result
                ):

                    st.session_state["token"] = result["access_token"]

                    st.session_state.registered_email = ""

                    st.rerun()

                else:

                    st.error(
                        "Invalid Email or Password"
                    )

        #register form

        else:

            with st.form("register_form"):

                name = st.text_input(
                    "👤 Name",
                    placeholder="Enter your name"
                )

                email = st.text_input(
                    "📧 Email",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "🔒 Password",
                    type="password",
                    placeholder="Create password"
                )

                register_btn = st.form_submit_button(
                    "Create Account",
                    use_container_width=True,
                    type="primary"
                )

            if register_btn:

                response = register(
                    name,
                    email,
                    password
                )

                if response.status_code == 200:

                    st.session_state.registered_email = email

                    st.session_state.message = (
                        "✅ Account created successfully! Please login."
                    )

                    st.session_state.page = "login"

                    st.rerun()

                else:

                    try:

                        detail = response.json().get(
                            "detail",
                            "Registration Failed"
                        )

                        st.error(detail)

                    except Exception:

                        st.error(
                            "Registration Failed"
                        )

    st.stop()


def require_login():

    initialize_session()

    if st.session_state["token"] is None:

        login_screen()


def logout_button():

    if st.sidebar.button(

        "🚪 Logout",

        use_container_width=True

    ):

        st.session_state["token"] = None

        st.rerun()


def get_token():

    return st.session_state["token"]