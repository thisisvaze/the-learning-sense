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

public class LessonState : MonoBehaviour
{
    public GameObject BoundsControlPrefab;

    public GameObject LessonTemplate1Prefab;
    public Texture2D texture = null;

    GameObject lessonItem;

    // Start is called before the first frame update
    void Start()
    {




    }

    // private void OnButtonEnabled(SelectEnterEventArgs arg0)
    // {
    //     Debug.Log("Button Clicked" + arg0.ToString());
    //     EventManager.TriggerEvent(Constants.BUTTON_PRESSED, arg0.ToString());
    //     EventManager.TriggerEvent(Constants.INITIATE_LESSON_REQUEST, "cup");
    // }

    // void GetEnvironmentUpdates()
    // {
    //     EventManager.TriggerEvent(Constants.REQUEST_ENV_INFO_UPDATE, "None");
    // }
    void OnEnable()
    {
        //markers[0] = (Instantiate(labelType, Camera.main.transform.position, Camera.main.transform.rotation) as GameObject);
        EventManager.StartListening(Constants.LESSON_INIT_INFO, OnLessonInfoRecieved);
        EventManager.StartListening(Constants.SHOW_3D_MODEL, Load3DModel);
    }

    void OnDisable()
    {
        EventManager.StopListening(Constants.LESSON_INIT_INFO, OnLessonInfoRecieved);
        EventManager.StartListening(Constants.SHOW_3D_MODEL, Load3DModel);
    }
    // Update is called once per frame
    void Update()
    {

        //gameObject.transform.position = new Vector3(delta_x, delta_y, delta_z);

        //Debug.Log("Object seen: "+envInfo.name);
        // Debug.Log("here: "+ finalPosition);
        //Debug.Log("Text:"+gameObject.transform.position);
        //Debug.Log("Text:"+gameObject.GetComponentInChildren<TMP_Text>().text);
        //gameObject.transform.position = finalPosition;
        //
        //gameObject.GetComponentInChildren<TMP_Text>().text = envInfo.name;
    }

    void Load3DModel(string msg)
    {

        JSONNode message = JSONArray.Parse(msg);

        var empty = new GameObject();
        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        Vector3 finalPosition = Camera.main.transform.position + 0.8f * forwardPosition;
        Debug.Log("Model name recieved here" + Constants.DATA_TYPE + message[Constants.DATA_TYPE]);
        var bounds = Instantiate(BoundsControlPrefab, finalPosition, Camera.main.transform.rotation);
        bounds.GetComponentInChildren<GLTFast.GltfAsset>().url = Application.dataPath + "/Resources/" + message[Constants.DATA_VALUE] + ".glb";
        Debug.Log("Model name recieved here" + message[Constants.DATA_VALUE]);
    }

    void OnLessonInfoRecieved(String msg)
    {
        JSONNode message = JSONString.Parse(msg);

        String title = message[Constants.DATA_VALUE]["text"];
        String image = message[Constants.DATA_VALUE]["image_url"];
        String model = message[Constants.DATA_VALUE]["3d_model"];


        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        Vector3 finalPosition = Camera.main.transform.position + 1.2f * forwardPosition;
        finalPosition = finalPosition + new Vector3(-0.1f, 0.1f, 0);
        lessonItem = Instantiate(LessonTemplate1Prefab, finalPosition, Camera.main.transform.rotation);

        //text
        lessonItem.GetComponentInChildren<TMP_Text>().text = title;

        //image
        StartCoroutine(RetrieveImageandSetContent(image));

        //3d model
        forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        finalPosition = Camera.main.transform.position + 0.8f * forwardPosition + new Vector3(0f, 0.1f, 0); ;
        Debug.Log("Model name recieved here" + Constants.DATA_TYPE + message[Constants.DATA_TYPE]);
        var bounds = Instantiate(BoundsControlPrefab, finalPosition, Camera.main.transform.rotation);
        bounds.GetComponentInChildren<GLTFast.GltfAsset>().url = Application.dataPath + "/Resources/" + model + ".glb";
        Debug.Log("Model name recieved here" + message[Constants.DATA_VALUE]);
    }

    IEnumerator RetrieveImageandSetContent(string url)
    {
        UnityWebRequest req = UnityWebRequestTexture.GetTexture(url);
        yield return req.SendWebRequest();
        if (req.result != UnityWebRequest.Result.Success)
        {
            if (req.isNetworkError || req.isHttpError || req.isNetworkError)
                print("Error: " + req.error);
            Debug.Log(req.downloadHandler.text);
        }
        else
        {
            Debug.Log("Image downloaded");
            texture = DownloadHandlerTexture.GetContent(req);
            lessonItem.GetComponentInChildren<RawImage>().texture = texture;
        }
    }
}