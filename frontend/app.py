import streamlit as st
import requests

# -------------------------
# 1. Page Configuration
# -------------------------

st.set_page_config(
    page_title="SimpleMail AI",
    page_icon="✉️",
    layout="centered"
)

# Backend URL จะกำหนดภายหลังเมื่อ Deploy บน RunPod
API_URL = st.secrets["API_URL"]

# -------------------------
# 2. Website Header
# -------------------------

st.title("✉️ SimpleMail AI")

st.write(
    "ผู้ช่วย AI สำหรับเขียนอีเมลภาษาไทย "
    เพียงพิมพ์ข้อความสั้น ๆ ก็สามารถสร้างอีเมลได้"
)

st.divider()

# -------------------------
# 3. User Input
# -------------------------

user_prompt = st.text_area(
    "ต้องการเขียนอีเมลเกี่ยวกับอะไร?",
    placeholder="เช่น ต้องการขอเลื่อนนัดประชุมกับอาจารย์ เนื่องจากติดธุระส่วนตัว",
    height=150
)

tone = st.selectbox(
    "เลือกระดับภาษา",
    [
        "เป็นทางการ",
        "กึ่งทางการ",
        "ไม่เป็นทางการ"
    ]
)

email_type = st.selectbox(
    "เลือกประเภทอีเมล",
    [
        "ทั่วไป",
        "ติดต่ออาจารย์",
        "สมัครงาน",
        "ติดต่อบริษัท",
        "ขอความอนุเคราะห์"
    ]
)

# -------------------------
# 4. Generate Email
# -------------------------

if st.button("✉️ สร้างอีเมล", use_container_width=True):

    if not user_prompt.strip():

        st.warning("กรุณากรอกข้อความก่อน")

    else:

        with st.spinner("AI กำลังสร้างอีเมล กรุณารอสักครู่..."):

            try:

                response = requests.post(
                    f"{API_URL.rstrip('/')}/generate-email",
                    json={
                        "user_prompt": user_prompt,
                        "tone": tone,
                        "email_type": email_type
                    },
                    timeout=600
                )

                response.raise_for_status()

                result = response.json()["email"]

                st.success("สร้างอีเมลสำเร็จ")

                st.subheader("ผลลัพธ์")

                st.text_area(
                    "อีเมลที่สร้าง",
                    value=result,
                    height=350
                )

                st.download_button(
                    "ดาวน์โหลดอีเมล",
                    data=result,
                    file_name="simplemail_email.txt",
                    mime="text/plain"
                )

            except requests.exceptions.Timeout:

                st.error("ใช้เวลาสร้างอีเมลนานเกินไป กรุณาลองใหม่")

            except requests.exceptions.RequestException as e:

                st.error(f"ไม่สามารถเชื่อมต่อ Backend ได้: {e}")

            except Exception as e:

                st.error(f"เกิดข้อผิดพลาด: {e}")
