using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Constants : MonoBehaviour
{
    public static string SOCKET_URL = "http://192.168.0.117:8000";
    public static string ENVIRONMENT_OJBECTS_UPDATE = "ENVIRONMENT_OJBECTS_UPDATE";
    public static string SESSION_STATE_LAUNCH = "SESSION_STATE_LAUNCH";
    public static string SESSION_STATE_EXPLORE = "SESSION_STATE_EXPLORE";
    public static string SESSION_STATE_INITIATING_LESSON = "SESSION_STATE_INITIATING_LESSON";
    public static string SESSION_STATE_LESSON_INITIATED = "SESSION_STATE_LESSON_INITIATED";
    public static string SESSION_STATE_DISCONNECTED = "SESSION_STATE_DISCONNECTED";

    //CLIENT_SERVER PROTOCOL
    public static string INITIATE_LESSON_REQUEST = "INITIATE_LESSON_REQUEST";
    public static string LESSON_INIT_INFO = "LESSON_INIT_INFO";
    public static string SPEECH_SENTENCE_SPOKEN = "SPEECH_SENTENCE_SPOKEN";
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }
}
