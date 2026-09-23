import os
import json
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Diagnosis
from .serializers import DiagnosisSerializer
from chat.models import Conversation

def generate_diagnosis(problem):
    text = problem.lower()

    if any(term in text for term in ["accident", "collision", "crash", "front end", "front-end"]):
        return {
            "diagnosis": "Significant visible front-end collision damage is present, but hidden damage cannot be ruled out from an image alone.",
            "recommendation": "Arrange a professional inspection before driving. Check the bumper assembly, grille, headlights, radiator support, steering, suspension, fluid lines, and airbag system; tow the vehicle if structural or safety-system damage is suspected.",
            "severity": "high"
        }

    if "battery" in text:
        return {
            "diagnosis": "The symptoms may indicate a weak battery or charging-system issue.",
            "recommendation": "Test the battery voltage and alternator output.",
            "severity": "medium"
        }

    if "brake" in text and ("grinding" in text or "grind" in text):
        return {
            "diagnosis": "Grinding from the brakes can indicate severe brake pad wear or rotor damage.",
            "recommendation": "Avoid unnecessary driving and have the braking system inspected immediately.",
            "severity": "high"
        }

    if "overheat" in text or "overheating" in text:
        return {
            "diagnosis": "The vehicle may have a cooling-system issue.",
            "recommendation": "Stop driving if the temperature is in the red zone and inspect coolant levels/leaks.",
            "severity": "high"
        }

    return "GENERIC"

def ai_diagnosis(problem):
    system_prompt = (
        "You are an expert car mechanic. Given a car problem description, "
        "provide a JSON response with keys: 'diagnosis', 'recommendation', and 'severity'. "
        "Severity must be one of: 'low', 'medium', 'high'. "
        "Output ONLY valid JSON."
    )
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-3.6-flash"
        )
        prompt = f"Instructions: {system_prompt}\n\nProblem: {problem}"
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean up if markdown blocks exist
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        data = json.loads(text.strip())
        return {
            "diagnosis": data.get("diagnosis", "Unable to determine precise diagnosis."),
            "recommendation": data.get("recommendation", "A mechanic inspection is recommended."),
            "severity": data.get("severity", "medium").lower()
        }
    except Exception as e:
        print(f"Gemini API error in diagnosis: {e}")
        return {
            "diagnosis": "More information is required to identify the likely cause.",
            "recommendation": "A mechanic inspection is recommended.",
            "severity": "medium"
        }


class DiagnosisAPIView(APIView):
    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        problem = request.data.get("problem")

        if not conversation_id or not problem:
            return Response(
                {"error": "conversation_id and problem are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        result = generate_diagnosis(problem)
        if result == "GENERIC":
            result = ai_diagnosis(problem)
            
        if result["severity"] not in ["low", "medium", "high"]:
            result["severity"] = "medium"

        diagnosis = Diagnosis.objects.create(
            conversation=conversation,
            problem=problem,
            diagnosis=result["diagnosis"],
            recommendation=result["recommendation"],
            severity=result["severity"]
        )

        serializer = DiagnosisSerializer(diagnosis)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )