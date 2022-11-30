using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NativeWebSocket;
using System.Threading;
using System.Threading.Tasks;
using System;
using System.Net;
using UnityEngine.Networking;
using System.Linq;
using TMPro;
using System.Security.Cryptography.X509Certificates;
using System.Security.Cryptography;
using System.Runtime.InteropServices;
using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.UX;
using Microsoft.MixedReality.Toolkit.Subsystems;
using Microsoft.MixedReality.Toolkit.SpatialManipulation;
using Microsoft.MixedReality.Toolkit.Input;
using UnityEngine.UI;
using UnityEngine.XR.Interaction.Toolkit;
using SimpleJSON;
using GLTFast;
using Newtonsoft.Json;
public class ExploreState : MonoBehaviour
{
    public float delta_x = 0, delta_y = 0, delta_z = 0;
    Vector3 zed_reference_position = new Vector3(0, 0, 0);
    public GameObject labelType;
    GameObject mug;

    public float UpdateEnvironmentRate = 2;
    public PressableButton button;
    public GameObject BoundsControlPrefab;
    public GameObject[] markers = new GameObject[40];
    TMP_Text loggerText;
    GameObject bounds;
    GameObject mars;
    void Start()
    {


        //loggerText = GameObject.Find("Logger").GetComponentInChildren<TMP_Text>();
        //Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        //Vector3 finalPosition = Camera.main.transform.position + 0.8f * forwardPosition;
        // bounds = Instantiate(BoundsControlPrefab, new Vector3(-1.7f, 0.8f, 1.3f), Camera.main.transform.rotation);
        // bounds.GetComponentInChildren<GLTFast.GltfAsset>().url = Application.dataPath + "/Resources/" + "moon" + ".glb";
        // bounds.GetComponentInChildren<GLTFast.GltfAsset>().gameObject.transform.localScale = new Vector3(0.01f, 0.01f, 0.01f);

        mug = GameObject.Find("Mug");
        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        Vector3 finalPosition = Camera.main.transform.position + 0.8f * forwardPosition;
        for (int i = 0; i < 30; i++)
        {
            markers[i] = (Instantiate(labelType, Camera.main.transform.position - 30f * forwardPosition, Camera.main.transform.rotation) as GameObject);
            markers[i].AddComponent<PressableButton>();
            markers[i].transform.parent = gameObject.transform;
            PressableButton b = markers[i].GetComponentInChildren<PressableButton>();
            b.selectEntered.AddListener(delegate { DoThis(b); });

        }
        InvokeRepeating("GetEnvironmentUpdates", 0.0f, UpdateEnvironmentRate);
        mars = GameObject.Find("PottedPlants");
        //mars.gameObject.transform.localScale = new Vector3(2f, 2f, 2f);

    }

    void Load3DModel(string msg)
    {
        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        Vector3 finalPosition = Camera.main.transform.position + 0.8f * forwardPosition;
        GameObject boundstemp = Instantiate(BoundsControlPrefab, finalPosition, Camera.main.transform.rotation);
        boundstemp.GetComponentInChildren<GLTFast.GltfAsset>().url = Application.persistentDataPath + "/Resources/" + msg + ".glb";
        boundstemp.GetComponentInChildren<GLTFast.GltfAsset>().gameObject.transform.localScale = new Vector3(0.01f, 0.01f, 0.01f);
    }


    private void DoThis(PressableButton b)
    {

        Debug.Log("Button Clicked" + b.GetComponentInChildren<TMP_Text>().text);

        EventManager.TriggerEvent(Constants.BUTTON_PRESSED, b.GetComponentInChildren<TMP_Text>().text);
        EventManager.TriggerEvent(Constants.INITIATE_LESSON_REQUEST, b.GetComponentInChildren<TMP_Text>().text);
    }

    void GetEnvironmentUpdates()
    {
        EventManager.TriggerEvent(Constants.REQUEST_ENV_INFO_UPDATE, "Requesting env information");
    }
    void OnEnable()
    {
        EventManager.StartListening(Constants.ENVIRONMENT_OJBECTS_UPDATE, OnEnvironmentUpdate);
        EventManager.StartListening(Constants.MARS_MOVED_LISTENER, OnMarsMovedByOtherClient);


    }

    void OnDisable()
    {
        EventManager.StopListening(Constants.ENVIRONMENT_OJBECTS_UPDATE, OnEnvironmentUpdate);
        EventManager.StopListening(Constants.MARS_MOVED_LISTENER, OnMarsMovedByOtherClient);
    }
    // Update is called once per frame
    void Update()
    {
        Camera.main.backgroundColor = new Color(0f, 0f, 0f, 0f);
        // int i = 0;
        // while (i < 20)
        // {
        //     markers[i].transform.rotation = Camera.main.transform.rotation;
        // }
        // i++;
    }
    void OnMarsMovedByOtherClient(string msg)
    {
        JSONNode message = JSONArray.Parse(msg);
        mars.transform.position = new Vector3(float.Parse(message[Constants.DATA_VALUE]["x"]), float.Parse(message[Constants.DATA_VALUE]["y"]), float.Parse(message[Constants.DATA_VALUE]["z"]))
         + mug.transform.position;
    }
    void OnEnvironmentUpdate(String msg)
    {

        mars.transform.position = new Vector3(-2.12f, -1.8f, -1.8f) + mug.transform.position;

        Dictionary<string, float> position = new Dictionary<string, float>();
        position.Add("x", mars.transform.position.x - zed_reference_position.x);
        position.Add("y", mars.transform.position.y - zed_reference_position.y);
        position.Add("z", mars.transform.position.z - zed_reference_position.z);
        string position_json = JsonConvert.SerializeObject(position);
        Dictionary<string, string> dict = new Dictionary<string, string>();
        dict.Add(Constants.DATA_TYPE, Constants.MARS_MOVED_LISTENER);
        dict.Add(Constants.DATA_VALUE, position_json);
        string send_this = JsonConvert.SerializeObject(dict);
        EventManager.TriggerEvent(Constants.MARS_MOVED_UPDATE_POSITION, send_this);



        zed_reference_position = mug.transform.position;
        JSONNode message = JSONArray.Parse(msg);
        Debug.Log(Constants.DATA_TYPE + message[Constants.DATA_TYPE]);
        Debug.Log(Constants.DATA_VALUE + message[Constants.DATA_VALUE]["Items"][0]["name"]);
        //loggerText.text += (Constants.DATA_TYPE + message[Constants.DATA_TYPE]);
        //loggerText.text += Constants.DATA_VALUE + message[Constants.DATA_VALUE]["Items"][0]["name"];
        int i = 0;
        while (i < 30)
        {
            JSONNode item = message[Constants.DATA_VALUE]["Items"][i];
            Vector3 finalPosition = new Vector3(0, 0, 0);
            finalPosition = new Vector3((float.Parse(item["x"])), (float.Parse(item["y"])), (float.Parse(item["z"]))) + zed_reference_position;

            markers[i].transform.position = finalPosition;
            markers[i].transform.rotation = Camera.main.transform.rotation;
            markers[i].GetComponentInChildren<TMP_Text>().text = item["name"];
            i++;

        }



    }

}