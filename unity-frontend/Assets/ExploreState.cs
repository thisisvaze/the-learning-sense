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
using UnityEngine.UI;
using UnityEngine.XR.Interaction.Toolkit;
using SimpleJSON;
public class ExploreState : MonoBehaviour
{
    public float delta_x = 0, delta_y = 0, delta_z = 0;
    Vector3 zed_reference_position = new Vector3(0, 0, 0);
    public GameObject labelType;

    public float UpdateEnvironmentRate;
    public PressableButton button;
    public GameObject[] markers = new GameObject[40];

    GameObject empty;
    void Start()
    {

        empty = new GameObject();
        GLTFast.GltfAsset gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = Application.dataPath + "/Resources/moon.glb";
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        empty.transform.localScale = new Vector3(Constants.scaleMap["moon"], Constants.scaleMap["moon"], Constants.scaleMap["moon"]);
        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        Vector3 position = Camera.main.transform.position + 0.8f * forwardPosition;
        empty.transform.position = position;
        empty.AddComponent<BoxCollider>();
        empty.AddComponent<BoundsControl>();
        empty.AddComponent<ObjectManipulator>();
        empty.AddComponent<ConstraintManager>();
        for (int i = 0; i < 30; i++)
        {
            markers[i] = (Instantiate(labelType, Camera.main.transform.position - 30f * forwardPosition, Camera.main.transform.rotation) as GameObject);
            markers[i].AddComponent<PressableButton>();
            markers[i].transform.parent = gameObject.transform;
            PressableButton b = markers[i].GetComponentInChildren<PressableButton>();
            b.selectEntered.AddListener(delegate { DoThis(b); });

        }
        InvokeRepeating("GetEnvironmentUpdates", 0.0f, UpdateEnvironmentRate);
        GameObject boundstemp = Instantiate(BoundsControlPrefab, new Vector3(-2.12f, 0.24f, -1.57f), Camera.main.transform.rotation);
        boundstemp.GetComponentInChildren<GLTFast.GltfAsset>().url = Application.dataPath + "/Resources/" + "mars" + ".glb";
        boundstemp.GetComponentInChildren<GLTFast.GltfAsset>().gameObject.transform.localScale = new Vector3(2f, 2f, 2f);
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
        zed_reference_position = empty.transform.position;
        JSONNode message = JSONArray.Parse(msg);
        Debug.Log(Constants.DATA_TYPE + message[Constants.DATA_TYPE]);
        Debug.Log(Constants.DATA_VALUE + message[Constants.DATA_VALUE]["Items"][0]["name"]);
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