# prompts.py
# --- This file defines the prompt templates for our AI agents ---

# Template for Critic Agent
CRITIC_PROMPT_TEMPLATE = """
                        Analyze the following content for cultural sensitivity and localization risks.

                        Context:
                        - Country: {country}
                        - Platform: {platform}
                        - Language: {language}
                        - Religion: {religion}
                        - Sensitive Contributors: {sensitive_contributors}
                        - Image Analysis: {image_analysis}
                        - Image Hint: {image_hint}
                        Content:
                        {content}

                        Instructions:
                        - Identify any cultural, religious, political, linguistic, or emotional sensitivity risks.
                        - Evaluate the tone, word choice, color references, and use of images or metaphors.
                        - Highlight risks related to audience perception, emotional resonance, brand trust, and local expectations.
                        - Pay attention to color symbolism, gestures, emoji usage, and expression styles across cultures.
                        - Suggest specific revision methods to improve cultural fit, emotional connection, and platform performance.
                        - Estimate the CTR impact and content risk mitigation effect if adjustments are made.
                        - Carefully review the content and image analysis findings to identify any cultural risks.
                    """

# Template for Rewriter Agent
REWRITE_PROMPT_TEMPLATE = """
                        Based on the following cultural critique, rewrite the original content.

                        Requirements:
                        - Maintain the original meaning and marketing purpose.
                        - Fully integrate the critique's suggestions into the rewritten text.
                        - Adjust emotional tone, cultural references, color mentions, and imagery according to the audience's cultural and emotional norms.
                        - Ensure clear, sensitive, and appropriate expressions across languages and regions.
                        - If necessary, modify metaphors, humor, idioms, or symbols to suit local audience expectations.

                        Critique:
                        {critique}

                        Original Content and background:
                        {content}
                        """
