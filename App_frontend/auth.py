import streamlit as st

from api import login


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

    left, center, right = st.columns([1,2,1])

    with center:

        email = st.text_input(

            "📧 Email",

            placeholder="example@gmail.com"

        )

        password = st.text_input(

            "🔒 Password",

            type="password",

            placeholder="Enter Password"

        )

        st.markdown("<br>",unsafe_allow_html=True)

        if st.button(

            "Login",

            use_container_width=True

        ):

            response = login(

                email,

                password

            )

            result = response.json()

            if (

                response.status_code==200

                and

                "access_token" in result

            ):

                st.session_state["token"] = result["access_token"]

                st.success(

                    "Login Successful"

                )

                st.rerun()

            else:

                st.error(

                    "Invalid Email or Password"

                )

        st.markdown(
            """
            <br>

            <center>

            🔒 Secure AI Powered Platform

            </center>

            """,
            unsafe_allow_html=True
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