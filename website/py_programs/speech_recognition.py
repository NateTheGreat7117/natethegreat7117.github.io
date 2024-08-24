from transformers import WhisperProcessor, WhisperForConditionalGeneration
from torchaudio.transforms import Resample
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
model.config.forced_decoder_ids = None
forced_decoder_ids = processor.get_decoder_prompt_ids(language="english", task="transcribe")

resample = Resample(orig_freq=16000, new_freq=processor.feature_extractor.sampling_rate)


def speech_recognition(waveform):
    input_features = processor(resample(waveform)[0].numpy(), sampling_rate=16000, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
    beam_search_transcript = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    beam_search_result = beam_search_transcript.strip().replace(".", "")
    return beam_search_result