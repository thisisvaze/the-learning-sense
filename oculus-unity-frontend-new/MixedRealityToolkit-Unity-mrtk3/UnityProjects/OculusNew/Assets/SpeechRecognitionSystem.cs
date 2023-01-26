using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Windows.Speech;

public class SpeechRecognitionSystem : MonoBehaviour
{
    public string LOG = "SpeechRecognitionManager";
    private DictationRecognizer m_DictationRecognizer;


    private void setupDictationRecognizer()
    {
        m_DictationRecognizer = new DictationRecognizer();

        m_DictationRecognizer.DictationResult += (text, confidence) =>
        {
            EventManager.TriggerEvent(Constants.SPEECH_SENTENCE_SPOKEN, text);
            Debug.LogFormat(LOG + " Dictation result: {0}", text);
        };

        m_DictationRecognizer.DictationHypothesis += (text) =>
        {
            Debug.LogFormat(LOG + " Dictation hypothesis: {0}", text);
        };

        m_DictationRecognizer.DictationComplete += (completionCause) =>
        {
            switch (completionCause)
            {
                case DictationCompletionCause.TimeoutExceeded:
                case DictationCompletionCause.PauseLimitExceeded:
                case DictationCompletionCause.Canceled:
                case DictationCompletionCause.Complete:
                    // Restart required
                    m_DictationRecognizer.Stop();
                    m_DictationRecognizer.Start();
                    break;
                case DictationCompletionCause.UnknownError:
                case DictationCompletionCause.AudioQualityFailure:
                case DictationCompletionCause.MicrophoneUnavailable:
                case DictationCompletionCause.NetworkFailure:
                    // Error
                    m_DictationRecognizer.Stop();
                    break;
            }
        };

        m_DictationRecognizer.DictationError += (error, hresult) =>
        {
            Debug.LogErrorFormat(LOG + " Dictation error: {0}; HResult = {1}.", error, hresult);
        };

        m_DictationRecognizer.Start();
        m_DictationRecognizer.AutoSilenceTimeoutSeconds = Mathf.Infinity;
    }

    // Start is called before the first frame update
    void Start()
    {
        setupDictationRecognizer();
        DontDestroyOnLoad(this);
    }

    // Update is called once per frame
    void Update()
    {

    }
}
