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
using System.Linq;
using UnityEngine.Windows.WebCam;
using TMPro;
using System.Security.Cryptography.X509Certificates;
using System.Security.Cryptography;
using System.Runtime.InteropServices;
using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.UX;
using Microsoft.MixedReality.Toolkit.Subsystems;
using Microsoft.MixedReality.Toolkit.SpatialManipulation;
using Microsoft.MixedReality.Toolkit.Input;
using UnityEngine.Windows.Speech;
using UnityEngine.UI;
using NativeWebSocket;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine.XR.Interaction.Toolkit;
using SimpleJSON;

public class ExploreState : MonoBehaviour
{
    public float delta_x = 0, delta_y = 0, delta_z = 0;
    public GameObject labelType;

    public PressableButton button;
    public GameObject[] markers = new GameObject[20];
    void Start()
    {
        for (int i = 0; i < 20; i++)
        {
            markers[i] = (Instantiate(labelType, Camera.main.transform.position, Camera.main.transform.rotation) as GameObject);
            markers[i].AddComponent<PressableButton>();
            markers[i].transform.parent = gameObject.transform;
            markers[i].GetComponentInChildren<PressableButton>().selectEntered.AddListener(OnButtonEnabled);
        }
        InvokeRepeating("GetEnvironmentUpdates", 0.0f, 5f);
    }

    private void OnButtonEnabled(SelectEnterEventArgs arg0)
    {
        Debug.Log("Button Clicked" + arg0.ToString());
        EventManager.TriggerEvent(Constants.BUTTON_PRESSED, arg0.ToString());
        EventManager.TriggerEvent(Constants.INITIATE_LESSON_REQUEST, "cup");
    }

    void GetEnvironmentUpdates()
    {
        EventManager.TriggerEvent(Constants.REQUEST_ENV_INFO_UPDATE, "Requesting env information");
    }
    void OnEnable()
    {
        EventManager.StartListening(Constants.ENVIRONMENT_OJBECTS_UPDATE, OnEnvironmentUpdate);

    }

    void OnDisable()
    {
        EventManager.StopListening(Constants.ENVIRONMENT_OJBECTS_UPDATE, OnEnvironmentUpdate);
    }
    // Update is called once per frame
    void Update()
    {
        // int i = 0;
        // while (i < 20)
        // {
        //     markers[i].transform.rotation = Camera.main.transform.rotation;
        // }
        // i++;
    }
    void OnEnvironmentUpdate(String msg)
    {
        JSONNode message = JSONArray.Parse(msg);
        Debug.Log(Constants.DATA_TYPE + message[Constants.DATA_TYPE]);
        Debug.Log(Constants.DATA_VALUE + message[Constants.DATA_VALUE]["Items"][0]["name"]);
        int i = 0;
        while (i < 20)
        {
            JSONNode item = message[Constants.DATA_VALUE]["Items"][i];
            Vector3 finalPosition = new Vector3(0, 0, 0);
            Vector3 deltaVector = new Vector3(delta_x, delta_y, delta_z);
            finalPosition = new Vector3((float.Parse(item["x"])), (float.Parse(item["y"])), (float.Parse(item["z"]))) + deltaVector;
            markers[i].transform.position = finalPosition;
            markers[i].transform.rotation = Camera.main.transform.rotation;
            markers[i].GetComponentInChildren<TMP_Text>().text = item["name"];
            i++;

        }

    }

}