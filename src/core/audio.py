"""
Módulo de Captura de Audio
Captura micrófono y transcribe en tiempo real
"""

import threading
from typing import Callable, Optional
import time

try:
    import sounddevice as sd
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

class AudioCapture:
    """Gestor de captura de audio con detección de silencio"""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1, silence_threshold: float = 0.08, silence_duration: float = 2.0):
        """Inicializa el capturador de audio
        
        Args:
            sample_rate: Tasa de muestreo (Hz)
            channels: Número de canales
            silence_threshold: Umbral de amplitud para detectar silencio (0-1)
            silence_duration: Segundos de silencio antes de considerar pausa (default: 2s)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.audio_data = []
        self.stream = None
        self.audio_buffer = []
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.silence_timer = 0.0
        self.last_sound_time = time.time()
        self.on_silence_detected = None  # Callback cuando detecta silencio
    
    def start_recording(self, callback: Optional[Callable] = None, on_silence: Optional[Callable] = None) -> bool:
        """Inicia la grabación de audio
        
        Args:
            callback: Función a llamar con cada chunk de audio
            on_silence: Función a llamar cuando detecta pausa/silencio
        """
        if not AUDIO_AVAILABLE:
            print("❌ Librerías de audio no disponibles")
            return False
        
        self.is_recording = True
        self.audio_data = []
        self.audio_buffer = []
        self.silence_timer = 0.0
        self.last_sound_time = time.time()
        self.on_silence_detected = on_silence
        
        def audio_callback(indata, frames, time_info, status):
            if status:
                print(f"⚠️ Audio status: {status}")
            
            # Agregar datos
            audio_chunk = indata.copy().flatten()
            self.audio_buffer.append(audio_chunk)
            self.audio_data.append(indata.copy())
            
            # Detectar nivel de audio (amplitud RMS)
            rms_level = np.sqrt(np.mean(audio_chunk ** 2))
            
            # Si hay sonido, resetear contador de silencio
            if rms_level > self.silence_threshold:
                self.last_sound_time = time.time()
                self.silence_timer = 0.0
            else:
                # Calcular tiempo en silencio
                elapsed_silence = time.time() - self.last_sound_time
                
                # Si pasó el umbral de silencio, disparar callback
                if elapsed_silence > self.silence_duration and self.on_silence_detected:
                    self.on_silence_detected()
            
            # Callback opcional
            if callback:
                callback(indata.copy())
        
        try:
            # Iniciar stream
            self.stream = sd.InputStream(
                channels=self.channels,
                samplerate=self.sample_rate,
                callback=audio_callback,
                blocksize=4096
            )
            self.stream.start()
            print("✅ Grabación iniciada (detectando silencio en pausa)")
            return True
        except Exception as e:
            print(f"❌ Error iniciando grabación: {e}")
            return False
    
    def stop_recording(self) -> bytes:
        """Detiene la grabación y retorna los datos"""
        if not self.is_recording:
            return b""
        
        self.is_recording = False
        
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
            
            # Combinar datos de audio
            if self.audio_data:
                audio_array = np.concatenate(self.audio_data)
                # Convertir a bytes (formato PCM 16-bit)
                audio_bytes = (audio_array * 32767).astype(np.int16).tobytes()
                print(f"✅ Grabación detenida ({len(audio_bytes)} bytes)")
                return audio_bytes
            
            return b""
        except Exception as e:
            print(f"❌ Error deteniendo grabación: {e}")
            return b""
    
    def get_microphones(self) -> list:
        """Obtiene lista de micrófonos disponibles"""
        if not AUDIO_AVAILABLE:
            return []
        
        try:
            devices = sd.query_devices()
            return [d for d in devices if d['max_input_channels'] > 0]
        except:
            return []
    
    def simulate_recording(self, text: str) -> bool:
        """Simula una grabación leyendo texto (para testing)"""
        self.is_recording = True
        self.audio_data = []
        print(f"✅ Simulando grabación: {text}")
        return True
    
    def get_audio_duration(self) -> float:
        """Obtiene duración del audio en segundos"""
        if not self.audio_buffer:
            return 0.0
        
        total_samples = sum(len(chunk) for chunk in self.audio_buffer)
        return total_samples / self.sample_rate
