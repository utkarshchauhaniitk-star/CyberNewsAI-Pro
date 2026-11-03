import asyncio
import edge_tts

VOICE = "en-US-GuyNeural"

async def generate_voice(text, output_file):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )
    await communicate.save(output_file)

def text_to_speech(text, output_file):
    asyncio.run(generate_voice(text, output_file))