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
public class ShowLesson : MonoBehaviour
{

    IDictionary<string, string> modelMap = null;
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
    public bool lessonGenerated = false;
    [Serializable]
    public class LabelInfo
    {
        public string name;
        public string x;
        public string y;
        public string z;
    }

    [Serializable]
    public class position
    {
        public string x;
        public string y;
        public string z;
    }
    [Serializable]
    public class info
    {
        public position position;
        public string content;
    }
    [Serializable]
    public class lesson_objects
    {
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
    async void setupClientSocket()
    {

        websocket = new WebSocket("ws://localhost:8000/ws");

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
            Debug.Log("OnMessage!");
            //Debug.Log(bytes);

            // getting the message as a string
            var message = System.Text.Encoding.UTF8.GetString(bytes);
            message = message.Replace("'", "\"");
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

    void ImportGLTF(string filepath, float scale)
    {
        var empty = new GameObject();
        gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = filepath;

        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward * 0.5f;
        Vector3 finalPosition = Camera.main.transform.position + forwardPosition;
        gltf.transform.localPosition = finalPosition;
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        empty.transform.localScale = new Vector3(scale, scale, scale);
        empty.AddComponent<BoxCollider>();
        empty.AddComponent<BoundsControl>();
        empty.AddComponent<ObjectManipulator>();
        empty.AddComponent<ConstraintManager>();

        Debug.Log("Generatated");
    }

    private void handleResponse(string message)
    {
        if (lessonGenerated == false)
        {
            generateLessonItem(message);
        }

        lessonGenerated = true;
    }

    private void setupDictationRecognizer()
    {
        m_DictationRecognizer = new DictationRecognizer();

        m_DictationRecognizer.DictationResult += (text, confidence) =>
        // 
        {
            //     if(text.Length>0){

            //    StartCoroutine(GetWolframResults(text));

            //     }

            Debug.LogFormat("Dictation result: {0}", text);
            if (text.Contains("what"))
            {


                //SendWebSocketMessage(text);

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
        //SendWebSocketMessage("connected");
        modelMap = new Dictionary<string, string>(){
        {"cylinder",   Application.dataPath + "/Resources/cylinder.glb"},
        {"plant_cell",   Application.dataPath + "/Resources/plant_cell.glb"},
        {"earth",   Application.dataPath + "/Resources/earth.glb"},
        {"mars",   Application.dataPath + "/Resources/mars.glb"},
        {"saturn",   Application.dataPath + "/Resources/saturn.glb"}
        };
        setupClientSocket();

        SendWebSocketMessage("connected");

    }

    // Update is called once per frame
    void Update()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        websocket.DispatchMessageQueue();
#endif
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

    private void generateLessonItem(string message)
    {

        LessonItem[] info = JsonHelper.FromJson<LessonItem>(message);
        if (info.Length > 0)
        {
            Debug.Log(info[0]);
            Debug.Log(info[0].lesson_objects[0].info);
            Debug.Log(info[0].lesson_objects[0].info.position.y);


            //buttons = new GameObject[10];

            //int i = 0;

            foreach (lesson_objects lesson_object in info[0].lesson_objects)
            {
                if (lesson_object.type == "text")
                {
                    //Vector3 cameraRelative = cam.TransformPoint((float.Parse(labelInfo.x) - 0.5f) / 3 , (float.Parse(labelInfo.y) - 0.5f )/ 3 , 1.5f);
                    //
                    Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
                    //Vector3 labelFaceRotation = Vector3.Cross(forwardPosition, new Vector3(0,1,0.1)).normalized;
                    Vector3 finalPosition = Camera.main.transform.position + 0.8f * forwardPosition + new Vector3((float.Parse(lesson_object.info.position.x) - 0.5f), (0.53f - float.Parse(lesson_object.info.position.y)), 0);
                    //Debug.Log(finalPosition);
                    //
                    // if(buttons[i] != null){
                    //     buttons[i].active = true;
                    //     buttons[i].transform.position = finalPosition;
                    //     buttons[i].transform.rotation =  Camera.main.transform.rotation;
                    // }
                    // else{

                    //     buttons[i] = (Instantiate(labels, finalPosition, Camera.main.transform.rotation));
                    // }

                    GetComponentInChildren<TMP_Text>().text = lesson_object.info.content;
                    this.transform.position = finalPosition;
                    //i++;
                }
                if (lesson_object.type == "media")
                {
                    //Vector3 cameraRelative = cam.TransformPoint((float.Parse(labelInfo.x) - 0.5f) / 3 , (float.Parse(labelInfo.y) - 0.5f )/ 3 , 1.5f);
                    //
                    Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
                    //Vector3 labelFaceRotation = Vector3.Cross(forwardPosition, new Vector3(0,1,0.1)).normalized;
                    Vector3 finalPosition = Camera.main.transform.position + new Vector3(float.Parse(lesson_object.info.position.x), float.Parse(lesson_object.info.position.y), float.Parse(lesson_object.info.position.z));
                    //Debug.Log(finalPosition);
                    //
                    // if(buttons[i] != null){
                    //     buttons[i].active = true;
                    //     buttons[i].transform.position = finalPosition;
                    //     buttons[i].transform.rotation =  Camera.main.transform.rotation;
                    // }
                    // else{

                    //     buttons[i] = (Instantiate(labels, finalPosition, Camera.main.transform.rotation));
                    // }


                    // StartCoroutine(RetrieveImageandSetContent(lesson_object.info.content));


                    //GetComponentInChildren<TMP_Text>().text = lesson_object.info.content;
                    //i++;
                }

            }

            // for(int j = info.Length ; j<10; j++){
            //     if(buttons[j] != null){
            //         buttons[j].active = false;
            //     }

            // }
        }

    }
}

