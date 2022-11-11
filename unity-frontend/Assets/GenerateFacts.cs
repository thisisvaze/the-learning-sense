using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NativeWebSocket;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine.Windows.Speech;
using System;
using System.Net;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine.Windows.WebCam;
using TMPro;
using System.Security.Cryptography.X509Certificates;
using System.Security.Cryptography;
using System.Runtime.InteropServices;
using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.Subsystems;
using Microsoft.MixedReality.Toolkit.SpatialManipulation;
using Microsoft.MixedReality.Toolkit.Input;
using UnityEngine.Windows.Speech;
using UnityEngine.UI;
using NativeWebSocket;
using System.Threading;
using System.Threading.Tasks;
public class GenerateFacts : MonoBehaviour
{

    Texture2D targetTexture = null;
    public GameObject quad;
    public Renderer quadRenderer;
    public Texture2D texture = null;
    public bool done = false;
      public GameObject button;
    public GameObject labels;

 [Serializable]
        public class position{
            public string x;
            public string y; 
            public string z;
        }  
    
    public static class JsonHelper
    {
        public static T[] FromJson<T>(string json)
        {
            Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
            return wrapper.Items;
        }
        public static string ToJson<T>(T[] array)
        {
            Wrapper<T> wrapper = new Wrapper<T>();
            wrapper.Items = array;
            return JsonUtility.ToJson(wrapper);
        }
        public static string ToJson<T>(T[] array, bool prettyPrint)
        {
            Wrapper<T> wrapper = new Wrapper<T>();
            wrapper.Items = array;
            return JsonUtility.ToJson(wrapper, prettyPrint);
        }
        [Serializable]
        private class Wrapper<T>
        {
            public T[] Items;
        }
    }
    WebSocket websocket;

    DictationRecognizer m_DictationRecognizer;
    async void setupClientSocket(){
        
    websocket = new WebSocket("ws://localhost:8000/ws");

    websocket.OnOpen += () =>
    {
      Debug.Log("Listening to Hololens Speech");
    };

    websocket.OnError += (e) =>
    {
      Debug.Log("Speech Error! " + e);
    };

    websocket.OnClose += (e) =>
    {
      Debug.Log("Speech Connection closed!");
    };

    websocket.OnMessage += (bytes) =>
    {
      //Debug.Log("OnMessage!");
      //Debug.Log(bytes);

      // getting the message as a string
      var message = System.Text.Encoding.UTF8.GetString(bytes);
      message = message.Replace("'","\"");
      Debug.Log(message);
      handleResponse(message);
     };
      // Keep sending messages at every 0.3s
    //InvokeRepeating("SendWebSocketMessage", 0.0f, 2f);

    // waiting for messages
    await websocket.Connect();
    }

    private void handleResponse(string message){
      //generateLessonItem(message);
      generateFactItem(message);
    }
     
    private void setupDictationRecognizer(){
        m_DictationRecognizer = new DictationRecognizer();

        m_DictationRecognizer.DictationResult += (text, confidence) =>
        // 
        {
         Debug.LogFormat("Dictation result: {0}", text);
   

             
              
           
           //m_Recognitions.text += text + "\n";
            

        };

        m_DictationRecognizer.DictationHypothesis += (text) =>
        {
            Debug.LogFormat("Dictation hypothesis: {0}", text);

          SendWebSocketMessage(text);
    

            
            //  float scale = 0.1f;
            
            //   switch (text)
            // {
            //     case "earth": scale =  0.1f;break;
            //     case "moon": scale = 0.0005f;break;
            //     case "mars": scale = 0.2f;break;
            //     default: scale = 0.1f; break;
            // }
            // generateCustomFromURL(modelMap[text], scale);
           // m_Hypotheses.text += text;
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
            Debug.LogErrorFormat("Dictation error: {0}; HResult = {1}.", error, hresult);
        };

        m_DictationRecognizer.Start();
        m_DictationRecognizer.AutoSilenceTimeoutSeconds = Mathf.Infinity;
    }

    // Start is called before the first frame update
    void Start()
    {
        setupClientSocket();
        setupDictationRecognizer();
    }

    // Update is called once per frame
    void Update()
    {
        #if !UNITY_WEBGL || UNITY_EDITOR
        websocket.DispatchMessageQueue();
        #endif
    }


private void generateFactItem(string message){                                         
                    Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
                    //Vector3 labelFaceRotation = Vector3.Cross(forwardPosition, new Vector3(0,1,0.1f)).normalized;
                    Vector3 finalPosition = Camera.main.transform.position + 0.5f*forwardPosition + new Vector3(0f , 0.05f, 0);
                    Debug.Log(finalPosition);
                    
                    if(done == false){
                        button = (Instantiate(labels, finalPosition, Camera.main.transform.rotation));
                        done = true;
                    }
                    
                   button.GetComponentInChildren<TMP_Text>().text = message;
                        button.active = true;
                        button.transform.position = finalPosition;
                        button.transform.rotation =  Camera.main.transform.rotation;
            

}

    async void SendWebSocketMessage(string text)
    {
        if (websocket.State == WebSocketState.Open)
        {
        // Sending bytes
        //await websocket.Send(new byte[] { 10, 20, 30 });

        // Sending plain text
            await websocket.SendText(text);
            Debug.Log("Speech text sent");
        }
    }

    private async void OnApplicationQuit()
  {
    await websocket.Close();
  }

}
