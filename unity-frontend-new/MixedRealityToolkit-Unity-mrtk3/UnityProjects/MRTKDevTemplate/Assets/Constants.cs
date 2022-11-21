using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Constants : MonoBehaviour
{

    public static string WEB_SOCKET_URL = "ws://localhost:8000/ws";
    public static string ENVIRONMENT_OJBECTS_UPDATE = "ENVIRONMENT_OJBECTS_UPDATE";
    public static string SESSION_STATE_LAUNCH = "SESSION_STATE_LAUNCH";
    public static string SESSION_STATE_EXPLORE = "SESSION_STATE_EXPLORE";
    public static string SESSION_STATE_INITIATING_LESSON = "SESSION_STATE_INITIATING_LESSON";
    public static string SESSION_STATE_LESSON_INITIATED = "SESSION_STATE_LESSON_INITIATED";
    public static string SESSION_STATE_DISCONNECTED = "SESSION_STATE_DISCONNECTED";
    public static string SOCKET_IO_URL = "http://192.168.0.117:8000";

    //CLIENT_SERVER PROTOCOL
    public static string REQUEST_ENV_INFO_UPDATE = "REQUEST_ENV_INFO_UPDATE";
    public static string INITIATE_LESSON_REQUEST = "INITIATE_LESSON_REQUEST";
    public static string LESSON_INIT_INFO = "LESSON_INIT_INFO";
    public static string SPEECH_SENTENCE_SPOKEN = "SPEECH_SENTENCE_SPOKEN";
    public static string SHOW_3D_MODEL = "SHOW_3D_MODEL";
    public static string DATA_TYPE = "DATA_TYPE";


    public static string DATA_VALUE = "DATA_VALUE";
    public static string BUTTON_PRESSED = "BUTTON_PRESSED";


    public static Dictionary<string, float> scaleMap = new Dictionary<string, float>(){
        {"cylinder",   0.1f},
        {"plant_cell",   0.1f},
        {"moon",   0.0005f},
        {"earth", 0.1f},
        {"mars",   0.2f},
        {"saturn",  0.0001f}
        };

}
