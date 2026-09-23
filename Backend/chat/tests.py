from unittest.mock import patch

from django.test import TestCase

from .models import Conversation, Message
from .views import has_conversation_context, traditional_response


class ChatRoutingTests(TestCase):
	def test_incidental_brake_word_does_not_trigger_brake_rule(self):
		response = traditional_response("The brakes are working normally.")

		self.assertEqual(response, "GENERIC_FALLBACK")

	def test_high_confidence_brake_noise_uses_rule(self):
		response = traditional_response("The brakes are grinding loudly.")

		self.assertIn("Brake noise", response)

	def test_unknown_problem_uses_gemini_fallback_path(self):
		with patch("chat.views.ai_response", return_value="Please describe when the burning smell occurs.") as ai:
			response = self.client.post(
				"/api/chat/",
				{"message": "There is a burning smell after driving for 20 minutes."},
				content_type="application/json",
			)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()["reply"], "Please describe when the burning smell occurs.")
		ai.assert_called_once()

	def test_previous_question_marks_conversation_as_contextual(self):
		conversation = Conversation.objects.create()
		Message.objects.create(
			conversation=conversation,
			role="bot",
			content="Are there any fluid leaks?",
		)

		self.assertTrue(has_conversation_context(conversation))
