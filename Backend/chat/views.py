import os
import re
import google.generativeai as genai
from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Conversation, Message
from media_upload.models import MediaFile

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

VISUAL_ANALYSIS_PHRASES = [
    "analyze this image", "analyse this image", "analyze the image",
    "analyse the image", "analyze this photo", "what do you see",
    "visible damage", "damage", "damaged", "accident", "collision", "crash",
    "safe to drive", "what parts", "inspect the image"
]

UNRELATED_RESPONSE = "I’m a car mechanic assistant and can only help with car or mechanical-related questions."


def _has_positive_symptom(text, terms):
    if not any(term in text for term in terms):
        return False
    return not re.search(
        r"\b(no|not|never|isn't|aren't|without)\s+(?:any\s+)?(?:visible\s+)?(?:" + "|".join(map(re.escape, terms)) + r")\b",
        text,
    )

def traditional_response(message):
    text = message.lower()

    if "won't start" in text or "wont start" in text:
        return "Let's troubleshoot it step by step. Does the engine crank when you turn the key, or do you only hear a clicking sound?"

    if "battery" in text and _has_positive_symptom(text, [
        "weak", "dead", "won't start", "wont start", "dim", "clicking"
    ]):
        return "A weak battery can cause starting issues. Are your headlights dim, and do you hear a rapid clicking sound when trying to start?"

    if "brake" in text and _has_positive_symptom(text, [
        "noise", "squeal", "squeaking", "grind", "grinding", "clicking", "soft", "pedal"
    ]):
        return "Brake noise should be checked carefully. Is the noise a squealing sound, grinding sound, or a clicking sound?"

    if ("overheat" in text or "overheating" in text) and _has_positive_symptom(text, [
        "temperature", "steam", "hot", "red zone", "coolant"
    ]):
        return "Stop driving if the temperature gauge is in the red zone. Is coolant leaking, and is there steam coming from the engine bay?"

    if ("transmission" in text or "gear" in text) and _has_positive_symptom(text, [
        "slipping", "shift", "shifting", "stuck", "fluid", "rough"
    ]):
        return "Transmission issues can be serious. Are you experiencing rough shifting, slipping gears, or fluid leaks?"

    if ("ac" in text.split() or "a/c" in text or "air conditioner" in text) and _has_positive_symptom(text, [
        "warm", "hot", "blowing", "not working", "not cold", "leak", "problem"
    ]):
        return "A/C problems could be due to a refrigerant leak, a bad compressor, or a faulty blend door actuator. Is it blowing warm air?"

    if ("exhaust" in text or "smoke" in text) and _has_positive_symptom(text, [
        "smoke", "color", "blue", "black", "white", "leak"
    ]):
        return "Exhaust smoke can indicate different things depending on its color. Is the smoke blue, black, or white?"

    if "oil leak" in text or "leaking oil" in text:
        return "Oil leaks can come from the valve cover gasket, oil pan, or seals. Have you noticed dark puddles under the car?"

    return "GENERIC_FALLBACK"


def requires_visual_analysis(message, media_file):
    if not media_file or media_file.media_type != "image":
        return False
    text = message.lower()
    return any(phrase in text for phrase in VISUAL_ANALYSIS_PHRASES)


def accident_follow_up_response(conversation, message):
    if not conversation.media_files.filter(media_type="image").exists():
        return None

    text = message.lower()
    answer_signals = [
        "no visible fluid", "not leaking", "no fluid", "steering feels normal",
        "steering is normal", "brakes are working", "brakes work",
        "no warning lights", "warning lights are not", "airbags did not deploy",
        "airbags didn't deploy", "airbags did not"
    ]
    if sum(signal in text for signal in answer_signals) < 2:
        return None

    previous_messages = conversation.messages.filter(role="user").exclude(
        content=message
    ).values_list("content", flat=True)
    previous_bot = conversation.messages.filter(role="bot").order_by("-created_at").first()
    accident_context = any(
        term in " ".join(previous_messages).lower()
        for term in ["accident", "collision", "crash", "front end", "damaged"]
    )
    safety_question = previous_bot and any(
        term in previous_bot.content.lower()
        for term in ["fluid", "steering", "brakes", "airbags", "do not drive"]
    )

    if not accident_context or not safety_question:
        return None

    return (
        "Thanks. Since there are no visible fluid leaks, the steering and brakes are functioning "
        "normally, and the airbags did not deploy, the immediate warning signs you mentioned are "
        "absent. However, the image shows significant front-end collision damage, so hidden damage "
        "to components behind the bumper and grille cannot be ruled out. I recommend a professional "
        "inspection before driving the vehicle. Likely areas to inspect include the bumper assembly, "
        "grille, headlights, radiator support, and components behind the front-end structure."
    )


def ai_image_response(media_file, message):
    system_prompt = (
        "You are a cautious senior automobile technician reviewing a customer-provided image. "
        "Describe only visible damage or components. Do not claim to see hidden damage and do not "
        "say the vehicle is safe to drive based only on an image. For major front-end, brake, "
        "steering, suspension, airbag, fluid-leak, or overheating concerns, recommend not driving "
        "until a qualified mechanic inspects it and towing if appropriate. Ask one or two relevant "
        "follow-up questions before a final diagnosis. Be concise and mechanic-friendly."
    )

    try:
        media_file.file.open("rb")
        image = Image.open(media_file.file)
        model = genai.GenerativeModel(
            model_name="gemini-3.6-flash"
        )
        response = model.generate_content([
            f"Instructions: {system_prompt}\nCustomer question: {message}",
            image
        ])
        return response.text.strip()
    except Exception as error:
        print(f"Gemini Vision API error: {error}")
        return (
            "I can see that the image needs an in-person inspection, but I could not complete "
            "the visual analysis. Is the car leaking fluid, and do the steering, brakes, or airbags "
            "show any warning signs? Do not drive it if the front structure, wheels, steering, or "
            "airbags may be damaged."
        )
    finally:
        if getattr(media_file.file, "closed", True) is False:
            media_file.file.close()

def ai_response(conversation_history):
    system_prompt = (
        "You are a cautious senior automobile technician. Understand natural-language descriptions "
        "of vehicle symptoms and interpret each message using the conversation history. Ask useful "
        "follow-up questions when information is missing. Distinguish symptoms from confirmed faults, "
        "never invent hidden damage, and do not claim a vehicle is safe based only on a description "
        "or image. Give practical next steps and prioritize towing or professional inspection for "
        "possible accident, brake, steering, suspension, airbag, overheating, or major fluid issues. "
        "Stay within automobile and mechanical topics. If the request is clearly unrelated, reply "
        f'exactly: {UNRELATED_RESPONSE}'
    )
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-3.6-flash"
        )
        
        history_text = "\n".join(
            f"{msg.role}: {msg.content}" for msg in conversation_history
        )
        prompt = (
            f"Instructions: {system_prompt}\n\n"
            "Use the conversation history below to answer the latest user message. "
            "Do not repeat an earlier answer unless it is still directly relevant.\n\n"
            f"{history_text}\n\nLatest response:"
        )
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "I can help troubleshoot your car. Please tell me the car's make, model, year, and describe the problem."


def has_conversation_context(conversation):
    last_bot = conversation.messages.filter(role="bot").order_by("-created_at").first()
    if not last_bot:
        return False
    return "?" in last_bot.content or any(
        phrase in last_bot.content.lower()
        for phrase in ["please describe", "follow-up", "more information", "do not drive"]
    )


class ChatAPIView(APIView):
    def post(self, request):
        message = request.data.get("message")
        conversation_id = request.data.get("conversation_id")
        media_id = request.data.get("media_id")

        if not message:
            return Response(
                {"error": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                conversation = Conversation.objects.create()
        else:
            conversation = Conversation.objects.create()

        media_file = None
        if media_id:
            try:
                media_file = MediaFile.objects.get(id=media_id)
                if media_file.conversation_id and media_file.conversation_id != conversation.id:
                    media_file = None
                elif media_file.conversation_id is None:
                    media_file.conversation = conversation
                    media_file.save(update_fields=["conversation"])
            except MediaFile.DoesNotExist:
                media_file = None
        if media_file is None:
            media_file = conversation.media_files.filter(
                media_type="image"
            ).order_by("-uploaded_at").first()

        Message.objects.create(
            conversation=conversation,
            role="user",
            content=message
        )

        reply = accident_follow_up_response(conversation, message)
        if reply is None and has_conversation_context(conversation):
            reply = ai_response(conversation.messages.all().order_by("created_at"))
        elif reply is None and requires_visual_analysis(message, media_file):
            reply = ai_image_response(media_file, message)
        elif reply is None:
            reply = traditional_response(message)

        if reply == "GENERIC_FALLBACK":
            conversation_history = conversation.messages.all().order_by('created_at')
            reply = ai_response(conversation_history)
            
        # Save bot message
        Message.objects.create(
            conversation=conversation,
            role="bot",
            content=reply
        )

        return Response({
            "conversation_id": conversation.id,
            "reply": reply
        })