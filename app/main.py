import base64
import json
import PIL.Image
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain_core.messages import HumanMessage

# Import our custom modules
from app.agents import llm, create_p2p_guardian_crew
from app.database import get_order_by_id, update_order_status

app = FastAPI(title="Agentic Guard | Deriv P2P API")

# 1. ANALYZE CHAT ENDPOINT
@app.post("/analyze-trade/{order_id}")
async def analyze_trade(order_id: str):
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # In a real demo, this chat would come from a frontend input
    mock_chat = "User: Send me the money on WhatsApp +123456. The app is slow."
    
    # Use real database info for the AI context
    crew = create_p2p_guardian_crew(mock_chat, order.model_dump())
    result = crew.kickoff()

    # Update the DB if the AI detects a risk
    if "whatsapp" in str(result).lower() or "scam" in str(result).lower():
        update_order_status(order_id, status="flagged", risk_score=90, notes=str(result))

    return {"order_id": order_id, "analysis": result, "current_status": get_order_by_id(order_id)}


# 2. VERIFY RECEIPT ENDPOINT (STABILIZED)
@app.post("/verify-evidence/{order_id}")
async def verify_evidence(order_id: str, file: UploadFile = File(...)):
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 1. Convert image to Base64 for Gemini
    content = await file.read()
    image_base64 = base64.b64encode(content).decode("utf-8")

    # 2. Create the Strict Verification Prompt
    prompt_text = f"""
    Analyze this bank receipt against the following Order Data:
    - Expected Amount: {order.amount} {order.currency}
    - Expected Sender Name: {order.buyer_name}

    If the names or amounts do not match exactly, set "match" to false.
    Return ONLY JSON: 
    {{"match": true/false, "reason": "explanation of findings"}}
    """

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
        ]
    )
    
    # 3. Call Gemini and parse the JSON
    response = llm.invoke([message])
    
    try:
        # Clean potential markdown wrappers like ```json
        clean_json = response.content.replace("```json", "").replace("```", "").strip()
        ai_result = json.loads(clean_json)
        is_match = ai_result.get("match", False)
        reason = ai_result.get("reason", "No reason provided.")
    except Exception:
        is_match = False
        reason = f"AI could not parse receipt. Raw output: {response.content[:100]}"

    # 4. Save results to Database
    new_status = "verified" if is_match else "flagged"
    risk = 0 if is_match else 95
    update_order_status(order_id, status=new_status, risk_score=risk, notes=reason)

    return {"status": "processed", "ai_findings": reason, "updated_order": get_order_by_id(order_id)}


# 3. STATUS CHECK (For Frontend)
@app.get("/order/{order_id}")
async def check_status(order_id: str):
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order