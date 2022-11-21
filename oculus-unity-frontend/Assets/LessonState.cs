using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NativeWebSocket;
using System.Threading;
using System.Threading.Tasks;
using System;
using System.Net;
using UnityEngine.Networking;
using System.Collections;
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
using NativeWebSocket;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine.XR.Interaction.Toolkit;
using SimpleJSON;

public class LessonState : MonoBehaviour
{
    public Texture2D texture = null;
    Dictionary<string, float> scaleMap = null;

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
        //gameObject.transform.rotation =  Camera.main.transform.rotation;
        //gameObject.GetComponentInChildren<TMP_Text>().text = envInfo.name;
    }


    void Load3DModel(string msg)
    {
        JSONNode message = JSONArray.Parse(msg);
        Debug.Log("Model name recieved here" + Constants.DATA_TYPE + message[Constants.DATA_TYPE]);
        var empty = new GameObject();
        Debug.Log("Model name recieved here" + message[Constants.DATA_VALUE]);
        GLTFast.GltfAsset gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = Application.dataPath + "/Resources/" + message[Constants.DATA_VALUE] + ".glb";
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        empty.transform.localScale = new Vector3(scaleMap[message[Constants.DATA_VALUE]], scaleMap[message[Constants.DATA_VALUE]], scaleMap[message[Constants.DATA_VALUE]]);
        empty.AddComponent<BoxCollider>();
        empty.AddComponent<BoundsControl>();
        empty.AddComponent<ObjectManipulator>();
        empty.AddComponent<ConstraintManager>();
        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        Vector3 finalPosition = Camera.main.transform.position + 0.8f * forwardPosition;
        empty.transform.position = finalPosition;

    }


    void OnLessonInfoRecieved(String msg)
    {
        JSONNode message = JSONString.Parse(msg);
        Debug.Log(Constants.DATA_TYPE + message[Constants.DATA_TYPE]);
        Debug.Log("text" + message[Constants.DATA_VALUE]["text"]);
        Debug.Log("image" + message[Constants.DATA_VALUE]["image_url"]);
        JSONNode lesson_object = message[Constants.DATA_VALUE];
        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        Vector3 finalPosition = Camera.main.transform.position + 0.8f * forwardPosition;
        GetComponentInChildren<TMP_Text>().text = lesson_object["text"];
        StartCoroutine(RetrieveImageandSetContent(lesson_object["image_url"]));
        gameObject.transform.position = finalPosition;
        gameObject.transform.rotation = Camera.main.transform.rotation;
        // foreach (lesson_objects lesson_object in info[0].lesson_objects)
        // {
        //     if (lesson_object.type == "text")
        //     {
        //         ;
        //         //i++;
        //     }
        //     if (lesson_object.type == "media")
        //     {
        //         Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        //         Vector3 finalPosition = Camera.main.transform.position + new Vector3(float.Parse(lesson_object.info.position.x), float.Parse(lesson_object.info.position.y), float.Parse(lesson_object.info.position.z));

        //     }


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
            GetComponentInChildren<RawImage>().texture = texture;


            //quadRenderer.material.SetTexture("_MainTex", texture);
        }
    }

}