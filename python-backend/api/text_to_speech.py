from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import IPython.display as ipd
import soundfile as sf
import base64


class tts_fairseq:
    def __init__(self):
        self.models, self.cfg, self.task = load_model_ensemble_and_task_from_hf_hub(
            "facebook/fastspeech2-en-ljspeech",
            arg_overrides={"vocoder": "hifigan", "fp16": False})
        TTSHubInterface.update_cfg_with_data_cfg(self.cfg, self.task.data_cfg)
        self.generator = self.task.build_generator(self.models, self.cfg)

    def predict(self, text="The earth is approximately 900 kilometers from the sun."):
        #sample["speaker"] = sample["speaker"].cuda()
        sample = TTSHubInterface.get_model_input(task, text)
        sample["net_input"]["src_tokens"] = sample["net_input"]["src_tokens"].to(
            "cuda:0")
        sample["net_input"]["src_lengths"] = sample["net_input"]["src_lengths"].to(
            "cuda:0")
        wav, rate = TTSHubInterface.get_prediction(
            self.task, self.models[0].cuda(), self.generator, self.sample)
        ipd.Audio(wav.cpu(), rate=rate)
        sf.write("a.wav", wav.cpu(), rate)
        with open("a.wav", "rb") as f:
            s = base64.b64encode(f.read())
            return s
