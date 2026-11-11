import re
import torch

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer


# ==================================
# 1. Model Configuration
# ==================================

MODEL_NAME = "openthaigpt/openthaigpt-thaillm-8b-instruct-v0.7.2-research-preview"

print("Loading OpenThaiGPT model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)

model.eval()

print("Model loaded successfully!")


# ==================================
# 2. FastAPI Configuration
# ==================================

app = FastAPI(
    title="SimpleMail AI",
    description="AI Email Writing Assistant using OpenThaiGPT",
    version="1.0.0"
)


# ==================================
# 3. Request Schema
# ==================================

class EmailRequest(BaseModel):
    user_prompt: str
    tone: str = "เป็นทางการ"
    email_type: str = "ทั่วไป"


# ==================================
# 4. Generate Email Function
# ==================================

def generate_email(user_prompt, tone, email_type):

    system_prompt = f"""
คุณคือผู้ช่วยเขียนอีเมลภาษาไทย
มีหน้าที่เปลี่ยนข้อความสั้น ๆ ของผู้ใช้ให้เป็นอีเมลที่สมบูรณ์

ประเภทอีเมล: {email_type}
ระดับภาษา: {tone}

ข้อกำหนด:
1. ใช้ภาษาไทยที่ถูกต้อง อ่านง่าย และเป็นธรรมชาติ
2. เขียนให้เหมาะสมกับผู้รับและประเภทอีเมล
3. หากเป็นการติดต่ออาจารย์ ให้ใช้คำขึ้นต้นว่า "เรียน อาจารย์"
4. ไม่แต่งเติมข้อมูลที่ผู้ใช้ไม่ได้ระบุ
5. จัดรูปแบบให้ประกอบด้วยหัวข้ออีเมล คำขึ้นต้น เนื้อหา และคำลงท้าย
6. แสดงเฉพาะอีเมลฉบับสมบูรณ์ ไม่ต้องอธิบายขั้นตอนการคิด
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = tokenizer(
        [text],
        return_tensors="pt"
    ).to(model.device)

    with torch.inference_mode():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=512,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    output_ids = generated_ids[0][model_inputs.input_ids.shape[1]:]

    result = tokenizer.decode(
        output_ids,
        skip_special_tokens=True
    )

    # Remove thinking tags if present
    result = re.sub(
        r"<think>.*?</think>",
        "",
        result,
        flags=re.DOTALL
    )

    return result.strip()


# ==================================
# 5. API Endpoints
# ==================================

@app.get("/")
def home():
    return {
        "message": "Welcome to SimpleMail AI",
        "status": "running",
        "model": MODEL_NAME
    }


@app.post("/generate-email")
def create_email(request: EmailRequest):

    if not request.user_prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="กรุณาระบุข้อความที่ต้องการเขียนอีเมล"
        )

    try:
        result = generate_email(
            user_prompt=request.user_prompt,
            tone=request.tone,
            email_type=request.email_type
        )

        return {
            "success": True,
            "email": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
