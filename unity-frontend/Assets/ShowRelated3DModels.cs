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
public class ShowRelated3DModels : MonoBehaviour
{

    IDictionary<string,string> modelMap = null;
    bool plantCellShown = false;
    GameObject empty;
    GLTFast.GltfAsset gltf; 
    Texture2D targetTexture = null;
    public GameObject quad;
    public Renderer quadRenderer;
    public Texture2D texture = null;
    public float delta_x = 0, delta_y = 0, delta_z = 0;

      public GameObject[] buttons = new GameObject[10];
    public GameObject labels;

       [Serializable]
    public class LabelInfo
    {
        public string name;
        public string x;
        public string y;
        public string z;
    }

 [Serializable]
        public class position{
            public string x;
            public string y; 
            public string z;
        }  
  [Serializable]
        public class info{
            public position position;
            public string content; 
        }  
  [Serializable]
        public class lesson_objects{
          public string type;
          public info info;
        }
 
     [Serializable]
    public class LessonItem
    {
        public lesson_objects[] lesson_objects;
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
        
    websocket = new WebSocket("http://localhost:8000/");

    websocket.OnOpen += () =>
    {
      Debug.Log("Connection open");
    };

    websocket.OnError += (e) =>
    {
      Debug.Log("Connection Error! " + e);
    };

    websocket.OnClose += (e) =>
    {
      Debug.Log("Connection closed!");
    };

    websocket.OnMessage += (bytes) =>
    {
     // Debug.Log("OnMessage!");
      //Debug.Log(bytes);

      // getting the message as a string
      var message = System.Text.Encoding.UTF8.GetString(bytes);
      message = message.Replace("'","\"");
      //Debug.Log(message);
      handleResponse(message);
     };
      // Keep sending messages at every 0.3s
    //InvokeRepeating("SendWebSocketMessage", 0.0f, 2f);

    // waiting for messages
    await websocket.Connect();
    }

        void generateCustomFromURL(string url, float scale)
    {
        Debug.Log("Generate planets GLTF");
        ImportGLTF(url, scale);
    }

    void ImportGLTF(string filepath, float scale) {
        var empty = new GameObject(); 
        gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = filepath;

        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward*0.5f;
        Vector3 finalPosition = Camera.main.transform.position + forwardPosition;
        gltf.transform.localPosition = finalPosition;
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        empty.transform.localScale = new Vector3(scale, scale, scale);
        // empty.AddComponent<BoxCollider>();
        // empty.AddComponent<BoundsControl>();
        // empty.AddComponent<ObjectManipulator>();
        // empty.AddComponent<ConstraintManager>();
        
        Debug.Log("Generatated");
    }

    private void handleResponse(string message){
      showMultipleObjectLabels(message);
    }
     
    private void setupDictationRecognizer(){
        m_DictationRecognizer = new DictationRecognizer();

        m_DictationRecognizer.DictationResult += (text, confidence) =>
        // 
        {
        //     if(text.Length>0){
            
        //    StartCoroutine(GetWolframResults(text));
               
        //     }

         Debug.LogFormat("Dictation result: {0}", text);
            if(text =="tell me"){

             
              // SendWebSocketMessage(text);

            }
           

           // m_Recognitions.text += text + "\n";
            

        };

        m_DictationRecognizer.DictationHypothesis += (text) =>
        {
            Debug.LogFormat("Dictation hypothesis: {0}", text);


             
             // SendWebSocketMessage(text);

            
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
  SendWebSocketMessage("connected");
        modelMap = new Dictionary<string, string>(){
	{"plant_cell",   Application.dataPath + "/Resources/plant_cell.glb"},
    {"earth",   Application.dataPath + "/Resources/earth.glb"},
    {"mars",   Application.dataPath + "/Resources/mars.glb"},
    {"saturn",   Application.dataPath + "/Resources/saturn.glb"}
      };
        // quad = GameObject.CreatePrimitive(PrimitiveType.Quad);
        // quadRenderer = quad.GetComponent<Renderer>() as Renderer;
        // quadRenderer.material = new Material(Shader.Find("Unlit/Texture"));
        // quad.transform.parent = this.transform;
        setupClientSocket();
        //setupDictationRecognizer();

        // for(int i=0; i<1; i++){
        //   buttons[i] = (Instantiate(labels, Camera.main.transform.position, Camera.main.transform.rotation) as GameObject);
        
        // }

        empty = new GameObject(); 
        gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = Application.dataPath + "/Resources/doughnut.glb";
        var scale = 0.3f;
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        empty.transform.localScale = new Vector3(scale, scale, scale);
        // empty.AddComponent<BoxCollider>();
        // empty.AddComponent<BoundsControl>();
        // empty.AddComponent<ObjectManipulator>();
        // empty.AddComponent<ConstraintManager>();
    }

    // Update is called once per frame
    void Update()
    {
        #if !UNITY_WEBGL || UNITY_EDITOR
        websocket.DispatchMessageQueue();
        #endif
    }

    
private void showMultipleObjectLabels(string objectInfoLabelJson){

      LabelInfo[] info = JsonHelper.FromJson<LabelInfo>(objectInfoLabelJson); 
            if (info.Length > 0) {
                //Debug.Log(info[0].name);
                    
                    //Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
                    //Vector3 labdateelFaceRotation = Vector3.Cross(forwardPosition, new Vector3(0,1,0.1)).normalized;
                    try
                    {
                      LabelInfo labelInfo = info[0];
                      Vector3 finalPosition = 
                    //Camera.main.transform.position + 
                    new Vector3((float.Parse(labelInfo.x))+delta_x , (float.Parse(labelInfo.y))+ delta_y, (float.Parse(labelInfo.z))+delta_z);
                    //Debug.Log(finalPosition);
                    //
                    //buttons[0].transform.position = finalPosition;
                    //buttons[0].transform.rotation =  Camera.main.transform.rotation;
                    //buttons[0].GetComponentInChildren<TMP_Text>().text = labelInfo.name;
                    empty.transform.localPosition = finalPosition;
                    }
                    catch (System.Exception)
                    {
                      
                      throw;
                    }
                    

            }
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
