using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NativeWebSocket;
using SimpleJSON;
using Newtonsoft.Json;
public class WebSocketConnectionClient : MonoBehaviour
{
    public string LOG = "WebSocketConnectionClient";
    WebSocket websocket;

    // Start is called before the first frame update
    async void Start()
    {
        websocket = new WebSocket(Constants.WEB_SOCKET_URL);

        websocket.OnOpen += () =>
        {
            Debug.Log("Connection open!");
        };

        websocket.OnError += (e) =>
        {
            Debug.Log("Error! " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("Connection closed!");
        };

        websocket.OnMessage += (bytes) =>
        {
            Debug.Log("OnMessage!");
            var message = System.Text.Encoding.UTF8.GetString(bytes);
            message = message.Replace("'", "\"");
            Debug.Log("Message:" + message);
            JSONNode jsonResponse = JSONArray.Parse(message);
            Debug.Log(Constants.DATA_TYPE + jsonResponse[Constants.DATA_TYPE]);
            EventManager.TriggerEvent(jsonResponse[Constants.DATA_TYPE], message);
        };

        // Keep sending messages at every 0.3s
        //InvokeRepeating("SendWebSocketMessage", 0.0f, 0.3f);

        // waiting for messages
        await websocket.Connect();
    }

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
            // Sending plain text
            await websocket.SendText(text);
        }
    }

    private async void OnApplicationQuit()
    {
        await websocket.Close();
    }

    void OnEnable()
    {
        //markers[0] = (Instantiate(labelType, Camera.main.transform.position, Camera.main.transform.rotation) as GameObject);
        EventManager.StartListening(Constants.SPEECH_SENTENCE_SPOKEN, OnSentenceSpoken);
        EventManager.StartListening(Constants.BUTTON_PRESSED, OnInputRecieved);
        EventManager.StartListening(Constants.INITIATE_LESSON_REQUEST, OnLessonInitiateRequestRecieved);
        EventManager.StartListening(Constants.REQUEST_ENV_INFO_UPDATE, OnEnvironmentInfoRequested);
    }

    void OnDisable()
    {
        EventManager.StopListening(Constants.SPEECH_SENTENCE_SPOKEN, OnSentenceSpoken);
        EventManager.StopListening(Constants.BUTTON_PRESSED, OnInputRecieved);
        EventManager.StartListening(Constants.REQUEST_ENV_INFO_UPDATE, OnEnvironmentInfoRequested);
    }
    private void OnLessonInitiateRequestRecieved(string message)
    {
        Debug.Log(LOG + " Sending  " + message + "to server");
        Dictionary<string, string> dict = new Dictionary<string, string>();
        dict.Add(Constants.DATA_TYPE, Constants.INITIATE_LESSON_REQUEST);
        dict.Add(Constants.DATA_VALUE, message);
        string send_this = JsonConvert.SerializeObject(dict);
        SendWebSocketMessage(send_this);
    }
    private void OnEnvironmentInfoRequested(string message)
    {
        Debug.Log(LOG + " Sending  " + message + "to server");
        Dictionary<string, string> dict = new Dictionary<string, string>();
        dict.Add(Constants.DATA_TYPE, Constants.REQUEST_ENV_INFO_UPDATE);
        dict.Add(Constants.DATA_VALUE, message);
        string send_this = JsonConvert.SerializeObject(dict);
        SendWebSocketMessage(send_this);
    }
    private void OnSentenceSpoken(string message)
    {
        Debug.Log(LOG + " Sending  " + message + "to server");
        Dictionary<string, string> dict = new Dictionary<string, string>();
        dict.Add(Constants.DATA_TYPE, Constants.SPEECH_SENTENCE_SPOKEN);
        dict.Add(Constants.DATA_VALUE, message);
        string send_this = JsonConvert.SerializeObject(dict);
        SendWebSocketMessage(send_this);
    }

    private void OnInputRecieved(string message)
    {
        Debug.Log(LOG + " Sending  " + message + "to server");
        Dictionary<string, string> dict = new Dictionary<string, string>();
        dict.Add(Constants.DATA_TYPE, Constants.BUTTON_PRESSED);
        dict.Add(Constants.DATA_VALUE, message);
        string send_this = JsonConvert.SerializeObject(dict);
        SendWebSocketMessage(send_this);
    }
}
