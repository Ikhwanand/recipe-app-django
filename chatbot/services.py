from django.conf import settings
from .models import ChatMessage
from recipes.models import Recipe
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

class ChatbotService:
    def __init__(self):
        self.endpoint = "https://models.inference.ai.azure.com"
        self.model_name = "Phi-3-mini-4k-instruct"
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(settings.GITHUB_TOKEN),
        )

    def get_recipe_context(self):
        # Get all recipes to provide context
        recipes = Recipe.objects.filter(is_published=True)
        recipe_context = []
        for recipe in recipes:
            total_time = recipe.prep_time + recipe.cook_time
            recipe_context.append({
                'title': recipe.title,
                'description': recipe.description,
                'ingredients': recipe.ingredients,
                'prep_time': recipe.prep_time,
                'cook_time': recipe.cook_time,
                'total_time': total_time,
                'difficulty': recipe.difficulty,
                'servings': recipe.servings,
            })
        return recipe_context

    def format_context(self, recipe_context):
        # Format recipe context into a clear text format
        context = "Available recipes:\n"
        for recipe in recipe_context:
            context += f"- {recipe['title']}\n"
            context += f"  Description: {recipe['description']}\n"
            context += f"  Ingredients: {recipe['ingredients']}\n"
            context += f"  Preparation time: {recipe['prep_time']} minutes\n"
            context += f"  Cooking time: {recipe['cook_time']} minutes\n"
            context += f"  Total time: {recipe['total_time']} minutes\n"
            context += f"  Difficulty: {recipe['difficulty']}\n"
            context += f"  Servings: {recipe['servings']}\n\n"
        return context

    def get_chat_response(self, session, user_message):
        try:
            # Get recipe context
            recipe_context = self.get_recipe_context()
            formatted_context = self.format_context(recipe_context)

            # Get previous messages from the session
            previous_messages = list(ChatMessage.objects.filter(session=session).order_by('timestamp'))
            
            # Get last 4 messages if available
            recent_messages = previous_messages[-4:] if len(previous_messages) >= 4 else previous_messages
            
            # Prepare messages for the model
            messages = [
                SystemMessage(content=f"""You are a helpful cooking assistant named Chef AI. Your personality traits are:
                - Friendly and enthusiastic about cooking
                - Patient and encouraging with beginners
                - Knowledgeable about recipes and cooking techniques
                - Always ready to provide cooking tips and suggestions

                Here are the available recipes in our database:
                {formatted_context}
                
                When recommending recipes:
                - Always use recipes from the database above
                - Be specific and mention actual recipe names
                - Include preparation time, cooking time, difficulty, and servings
                - Provide helpful tips for preparation when relevant
                - Be encouraging and supportive"""),
            ]

            # Add conversation history
            for msg in recent_messages:
                if msg.role == 'user':
                    messages.append(UserMessage(content=msg.content))
                else:
                    messages.append(AssistantMessage(content=msg.content))

            # Add current user message
            messages.append(UserMessage(content=user_message))

            # Get response from the model
            response = self.client.complete(
                messages=messages,
                temperature=0.7,
                top_p=0.95,
                max_tokens=1000,
                model=self.model_name
            )

            assistant_message = response.choices[0].message.content

            # Save user message
            ChatMessage.objects.create(
                session=session,
                role='user',
                content=user_message
            )

            # Save assistant message
            ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=assistant_message
            )

            return assistant_message

        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Please try again later. Error: {str(e)}"
