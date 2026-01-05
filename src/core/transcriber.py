"""
Módulo de Transcripción de Audio
Usa Google Gemini para convertir audio a texto
"""

from typing import Optional
import base64
import io
import wave

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class AudioTranscriber:
    """Transcribidor de audio usando Google Gemini"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Inicializa el transcribidor con API Key de Gemini
        
        Args:
            api_key: API Key de Google Gemini
        """
        self.api_key = api_key
        
        if GENAI_AVAILABLE and api_key:
            try:
                genai.configure(api_key=api_key)
                print("✅ Transcribidor de audio (Gemini) inicializado")
            except Exception as e:
                print(f"⚠️ Error inicializando transcribidor: {e}")
    
    def set_api_key(self, api_key: str):
        """Configura una nueva API Key"""
        self.api_key = api_key
        if GENAI_AVAILABLE:
            try:
                genai.configure(api_key=api_key)
                self.client = google.genai
                return True
            except Exception as e:
                print(f"Error configurando transcribidor: {e}")
                return False
        return False
    
    def transcribe_audio(self, audio_bytes: bytes, language: str = "es") -> str:
        """Transcribe audio a texto usando Gemini
        
        Args:
            audio_bytes: Datos de audio en bytes (PCM 16-bit)
            language: Código de idioma (ej: es para español)
        
        Returns:
            Texto transcrito
        """
        if not self.api_key:
            return "❌ Transcribidor no disponible. Configura tu API Key de Gemini."
        
        if not audio_bytes or len(audio_bytes) < 1000:
            return "⚠️ Audio muy corto o vacío"
        
        try:
            # Convertir PCM raw a WAV format
            audio_buffer = io.BytesIO()
            with wave.open(audio_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(16000)  # 16kHz
                wav_file.writeframes(audio_bytes)
            
            wav_audio = audio_buffer.getvalue()
            audio_b64 = base64.standard_b64encode(wav_audio).decode('utf-8')
            
            # Usar Gemini 2.0 Flash para transcribir (soporta audio)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            response = model.generate_content([
                "Transcribe este audio a texto en español. Responde SOLO con el texto transcrito.",
                {
                    "mime_type": "audio/wav",
                    "data": audio_b64
                }
            ])
            
            text = response.text.strip() if response else "⚠️ Sin respuesta"
            
            if text and len(text) > 3:
                print(f"✅ Transcripción completada: {len(text)} caracteres")
                return text
            else:
                return "⚠️ No se detectó audio claro."
        
        except Exception as e:
            print(f"❌ Error en transcripción: {e}")
            return f"❌ Error: {str(e)}"
    
    def transcribe_audio_file(self, file_path: str, language: str = "es-ES") -> str:
        """Transcribe un archivo de audio
        
        Args:
            file_path: Ruta al archivo de audio
            language: Idioma
        
        Returns:
            Texto transcrito
        """
        try:
            with open(file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            
            return self.transcribe_audio(audio_bytes, language)
        except Exception as e:
            return f"❌ Error leyendo archivo: {str(e)}"
