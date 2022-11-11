using System;
using System.Collections.Generic;
using SocketIOClient;
using UnityEngine;
using UnityEngine.UI;
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
using SimpleJSON;
public class SocketConnectionClient : MonoBehaviour
{


    public string LOG = "SocketConnectionClient";

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


    public SocketIOUnity socket;
    // Start is called before the first frame update
    void Start()
    {
        //TODO: check the Uri if Valid.
        var uri = new Uri(Constants.SOCKET_URL);
        socket = new SocketIOUnity(uri, new SocketIOOptions
        {
            Path = "/ws/socket.io",
            Transport = SocketIOClient.Transport.TransportProtocol.WebSocket
        });
        ///// reserved socketio events
        socket.OnConnected += (sender, e) =>
        {
            Debug.Log("Socket connected with Server");
        };
        // socket.OnPing += (sender, e) =>
        // {
        //     Debug.Log("Ping");
        // };
        // socket.OnPong += (sender, e) =>
        // {
        //     Debug.Log("Pong: " + e.TotalMilliseconds);
        // };


        socket.OnDisconnected += (sender, e) =>
        {
            Debug.Log("Socket disconnected with Server " + e);
            Debug.Log("Trying to reconnect...");
            socket.Connect();
        };
        socket.OnReconnectAttempt += (sender, e) =>
        {
            Debug.Log($"{DateTime.Now} Reconnecting with server: attempt = {e}");
        };

        Debug.Log("Connecting...");
        socket.Connect();

        socket.On(Constants.ENVIRONMENT_OJBECTS_UPDATE, (response) =>
        {

            UnityThread.executeInUpdate(() =>
            {
                string message = response.GetValue().GetRawText();
                EventManager.TriggerEvent(Constants.ENVIRONMENT_OJBECTS_UPDATE, message);
                Debug.Log(LOG + ": " + message);
                JSONNode jsonResponse = JSONArray.Parse(message);
            });

        });

        socket.On(Constants.INITIATE_LESSON_REQUEST, (response) =>
        {
            UnityThread.executeInUpdate(() =>
            {
                string message = response.GetValue().GetRawText();
                EventManager.TriggerEvent(Constants.ENVIRONMENT_OJBECTS_UPDATE, message);
                JSONNode jsonResponse = JSONArray.Parse(message);
                Debug.Log(LOG + ": " + jsonResponse);

            });

        });





        // socket.OnUnityThread("spin", (data) =>
        // {
        //     rotateAngle = 0;
        // });

        // ReceivedText.text = "";
        // socket.OnAnyInUnityThread((name, response) =>
        // {
        //     ReceivedText.text += "Received On " + name + " : " + response.GetValue().GetRawText() + "\n";
        // });
    }

    void OnEnable()
    {
        //markers[0] = (Instantiate(labelType, Camera.main.transform.position, Camera.main.transform.rotation) as GameObject);
        EventManager.StartListening(Constants.SPEECH_SENTENCE_SPOKEN, OnSentenceSpoken);
    }

    void OnDisable()
    {
        EventManager.StopListening(Constants.SPEECH_SENTENCE_SPOKEN, OnSentenceSpoken);
    }

    private async void OnSentenceSpoken(string message)
    {
        Debug.Log(LOG + " Sending  " + message + "to server");
        await socket.EmitAsync(Constants.SPEECH_SENTENCE_SPOKEN, message);
    }

    private void OnApplicationQuit()
    {
        socket.Disconnect();
    }

    // Update is called once per frame
    void Update()
    {
    }
}
